import json
import difflib
import tkinter as tk
from tkinter import font
import itertools

class DiffGUI:
    """
    使用 Tkinter PanedWindow 创建左右可调节、带独立横向滚动的差异对比窗口
    """
    def __init__(self, window_size="1200x800"):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("列表/字典 差异对比查看器")
        self.root.geometry(window_size)

        # 设置字体 (使用等宽字体以保证对齐)
        try:
            self.custom_font = font.Font(family="Consolas", size=10)
        except:
            self.custom_font = font.Font(family="Courier New", size=10)

        # === 主容器 ===
        # 使用 Frame 容纳 PanedWindow 和 垂直滚动条
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 1. 垂直滚动条 (控制两个文本框的垂直滚动)
        self.v_scrollbar = tk.Scrollbar(main_container, orient=tk.VERTICAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 2. PanedWindow (左右拖动调节分割线)
        # sashwidth 设置分割线宽度，bg 设置分割线颜色使之可见
        self.paned_window = tk.PanedWindow(main_container, orient=tk.HORIZONTAL, sashwidth=5, bg="#dddddd")
        self.paned_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # === 左侧区域 ===
        self.left_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, minsize=100) # 添加到 PanedWindow

        # 左侧横向滚动条
        self.left_h_scroll = tk.Scrollbar(self.left_frame, orient=tk.HORIZONTAL)
        self.left_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # 左侧文本框 (wrap=tk.NONE 启用横向滚动)
        self.left_text = tk.Text(
            self.left_frame,
            font=self.custom_font,
            wrap=tk.NONE,
            xscrollcommand=self.left_h_scroll.set,
            yscrollcommand=self.v_scrollbar.set,
            state=tk.NORMAL,
            bd=0
        )
        self.left_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_h_scroll.config(command=self.left_text.xview)

        # === 右侧区域 ===
        self.right_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, minsize=100)

        # 右侧横向滚动条
        self.right_h_scroll = tk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL)
        self.right_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # 右侧文本框
        self.right_text = tk.Text(
            self.right_frame,
            font=self.custom_font,
            wrap=tk.NONE,
            xscrollcommand=self.right_h_scroll.set,
            # 注意：不在这里绑定 yscrollcommand，避免两个控件抢夺滚动条控制权，
            # 统一由垂直滚动条事件驱动，或者只由左侧驱动。
            # 这里我们采用手动联动的策略。
            state=tk.NORMAL,
            bd=0
        )
        self.right_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.right_h_scroll.config(command=self.right_text.xview)

        # === 联动配置 ===
        # 配置垂直滚动条同时控制两个文本框
        self.v_scrollbar.config(command=self._scroll_both)

        # 鼠标滚轮联动
        self._bind_mousewheel(self.left_text)
        self._bind_mousewheel(self.right_text)

        # === 颜色标签配置 ===
        # 需要为左右两个文本框都配置标签
        for widget in [self.left_text, self.right_text]:
            widget.tag_config('del', background='#ffe0e0', foreground='#b30000')
            widget.tag_config('add', background='#e0ffe0', foreground='#006600')
            widget.tag_config('title', font=(self.custom_font.cget("family"), 12, 'bold'), background='#eeeeee', spacing1=10, spacing3=5)
            widget.tag_config('header', font=(self.custom_font.cget("family"), 10, 'bold'), background='#f8f8f8', foreground='#555555')

    def _bind_mousewheel(self, widget):
        """绑定鼠标滚轮事件以实现同步滚动"""
        # Windows
        widget.bind("<MouseWheel>", self._on_mousewheel)
        # Linux
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)

    def _scroll_both(self, *args):
        """垂直滚动条回调：同时移动两个文本框"""
        self.left_text.yview(*args)
        self.right_text.yview(*args)

    def _on_mousewheel(self, event):
        """鼠标滚轮回调：同时滚动两个文本框"""
        # 判断滚动方向和距离
        if event.num == 5 or event.delta < 0:
            delta = 1
        else:
            delta = -1

        # 对两个文本框同时执行滚动
        self.left_text.yview_scroll(delta, "units")
        self.right_text.yview_scroll(delta, "units")
        return "break" # 阻止默认行为，防止重复滚动

    def _format_json(self, data):
        """将数据转换为格式化的 JSON 字符串列表"""
        json_str = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
        return json_str.splitlines()

    def add_diff(self, title, data1, data2):
        """
        添加一组对比数据
        """
        lines1 = self._format_json(data1)
        lines2 = self._format_json(data2)

        d = difflib.Differ()
        diff = list(d.compare(lines1, lines2))

        # --- 打印标题 (两边都打印以保持行数对齐) ---
        for widget in [self.left_text, self.right_text]:
            widget.insert(tk.END, f"=== {title} ===\n", 'title')

        # --- 打印表头 ---
        self.left_text.insert(tk.END, f"{'List A (Left)':^40}\n", 'header')
        self.right_text.insert(tk.END, f"{'List B (Right)':^40}\n", 'header')

        # 分割线
        for widget in [self.left_text, self.right_text]:
            widget.insert(tk.END, "-" * 40 + "\n", 'header')

        buffer_left = []
        buffer_right = []

        for line in diff:
            code = line[:2]
            text = line[2:]

            if code == '  ':
                # 遇到相同行，先输出之前缓存的差异块
                self._flush_buffer(buffer_left, buffer_right)
                # 输出当前相同行
                self._insert_row(text, text, mode='common')

            elif code == '- ':
                buffer_left.append(text)

            elif code == '+ ':
                buffer_right.append(text)

            elif code == '? ':
                continue

        # 输出剩余的差异块
        self._flush_buffer(buffer_left, buffer_right)

        # 添加底部空行
        for widget in [self.left_text, self.right_text]:
            widget.insert(tk.END, "\n\n")

    def _flush_buffer(self, left_buf, right_buf):
        """将缓冲区的差异行成对写入"""
        for l_line, r_line in itertools.zip_longest(left_buf, right_buf, fillvalue=None):
            self._insert_row(l_line, r_line, mode='diff')
        left_buf.clear()
        right_buf.clear()

    def _insert_row(self, left_text, right_text, mode):
        """
        分别向左右文本框插入一行，确保高度对齐
        """
        # 插入左侧
        if left_text is not None:
            tag = 'del' if mode == 'diff' else ''
            self.left_text.insert(tk.END, left_text + "\n", tag)
        else:
            self.left_text.insert(tk.END, "\n") # 插入空行保持对齐

        # 插入右侧
        if right_text is not None:
            tag = 'add' if mode == 'diff' else ''
            self.right_text.insert(tk.END, right_text + "\n", tag)
        else:
            self.right_text.insert(tk.END, "\n")

    def show(self):
        """显示窗口并禁止编辑"""
        # 设置为只读模式
        self.left_text.config(state=tk.DISABLED)
        self.right_text.config(state=tk.DISABLED)
        self.root.mainloop()

# ==========================================
# 测试数据
# ==========================================

list_a = [
    {'aaa': 'bbb', 'ccc': 'ddd'},
    {'eee': 'fff', 'ggg': 'hhh'}
]

list_b = [
    {'aaa': 'bbb', 'ccc': 'ddd'},
    {'eee': 'fff', 'ggg': 'CHANGED_VALUE'},
    {'new_key': 'new_value'}
]

list_c = [{'id': 1, 'tags': ['red', 'blue']}, {'id': 2}]
list_d = [{'id': 1, 'tags': ['red', 'green']}, {'id': 3}]

if __name__ == "__main__":
    # 初始化 GUI 查看器 (不需要 width 参数了，宽度由窗口和拖动决定)
    viewer = DiffGUI()

    # 添加第一个对比案例
    viewer.add_diff("案例 1: 简单的值修改和新增项", list_a, list_b)

    # 添加第二个对比案例
    viewer.add_diff("案例 2: 嵌套列表差异", list_c, list_d)

    # 启动弹窗显示
    print("正在打开差异对比窗口...")
    viewer.show()