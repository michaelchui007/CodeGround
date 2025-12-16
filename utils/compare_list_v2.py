import json
import difflib
import tkinter as tk
from tkinter import font, messagebox
import itertools
import ast

class DiffGUI:
    """
    交互式差异对比工具：支持粘贴 JSON/Python 数据进行左右对比
    """
    def __init__(self, window_size="1200x800"):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("JSON/List 差异对比工具 (粘贴 -> 对比)")
        self.root.geometry(window_size)

        # 设置字体 (使用等宽字体以保证对齐)
        try:
            self.custom_font = font.Font(family="Consolas", size=10)
        except:
            self.custom_font = font.Font(family="Courier New", size=10)

        # === 顶部工具栏 ===
        toolbar = tk.Frame(self.root, pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # 按钮样式
        btn_config = {'padx': 15, 'pady': 5, 'font': ('Arial', 10, 'bold')}

        self.btn_compare = tk.Button(toolbar, text="开始对比 (Compare)", command=self.run_compare, bg="#e1f5fe", **btn_config)
        self.btn_compare.pack(side=tk.LEFT, padx=10)

        self.btn_clear = tk.Button(toolbar, text="清空/重置 (Reset)", command=self.reset_inputs, bg="#ffebee", **btn_config)
        self.btn_clear.pack(side=tk.LEFT, padx=10)

        lbl_tip = tk.Label(toolbar, text="支持格式: JSON 或 Python List/Dict", fg="gray")
        lbl_tip.pack(side=tk.LEFT, padx=20)

        # === 主容器 ===
        # 使用 Frame 容纳 PanedWindow 和 垂直滚动条
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 1. 垂直滚动条 (控制两个文本框的垂直滚动)
        self.v_scrollbar = tk.Scrollbar(main_container, orient=tk.VERTICAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 2. PanedWindow (左右拖动调节分割线)
        self.paned_window = tk.PanedWindow(main_container, orient=tk.HORIZONTAL, sashwidth=5, bg="#dddddd")
        self.paned_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # === 左侧区域 ===
        self.left_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, minsize=100)

        tk.Label(self.left_frame, text="原数据 (Left)", font=('Arial', 10, 'bold'), bg="#f0f0f0").pack(fill=tk.X)

        self.left_h_scroll = tk.Scrollbar(self.left_frame, orient=tk.HORIZONTAL)
        self.left_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.left_text = tk.Text(
            self.left_frame,
            font=self.custom_font,
            wrap=tk.NONE,
            xscrollcommand=self.left_h_scroll.set,
            yscrollcommand=self.v_scrollbar.set,
            undo=True, # 允许 Ctrl+Z
            bd=0
        )
        self.left_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_h_scroll.config(command=self.left_text.xview)

        # === 右侧区域 ===
        self.right_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, minsize=100)

        tk.Label(self.right_frame, text="新数据 (Right)", font=('Arial', 10, 'bold'), bg="#f0f0f0").pack(fill=tk.X)

        self.right_h_scroll = tk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL)
        self.right_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.right_text = tk.Text(
            self.right_frame,
            font=self.custom_font,
            wrap=tk.NONE,
            xscrollcommand=self.right_h_scroll.set,
            undo=True,
            bd=0
        )
        self.right_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.right_h_scroll.config(command=self.right_text.xview)

        # === 联动配置 ===
        self.v_scrollbar.config(command=self._scroll_both)
        self._bind_mousewheel(self.left_text)
        self._bind_mousewheel(self.right_text)

        # === 颜色标签配置 ===
        for widget in [self.left_text, self.right_text]:
            widget.tag_config('del', background='#ffe0e0', foreground='#b30000')
            widget.tag_config('add', background='#e0ffe0', foreground='#006600')
            # 差异行背景稍微加深一点以便区分
            widget.tag_config('header', font=(self.custom_font.cget("family"), 10, 'bold'), background='#f8f8f8', foreground='#555555')

    def _bind_mousewheel(self, widget):
        """绑定鼠标滚轮事件以实现同步滚动"""
        # Windows
        widget.bind("<MouseWheel>", self._on_mousewheel)
        # Linux
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)

    def _scroll_both(self, *args):
        self.left_text.yview(*args)
        self.right_text.yview(*args)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            delta = 1
        else:
            delta = -1
        self.left_text.yview_scroll(delta, "units")
        self.right_text.yview_scroll(delta, "units")
        return "break"

    def parse_content(self, text):
        """
        尝试解析文本内容：
        1. 尝试 JSON
        2. 尝试 Python literal (例如 {'a':1} 单引号写法)
        3. 失败则返回原始行列表
        """
        text = text.strip()
        if not text:
            return []

        # 尝试 JSON
        try:
            obj = json.loads(text)
            # 重新格式化为漂亮的 JSON 字符串以便对比
            formatted = json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)
            return formatted.splitlines()
        except json.JSONDecodeError:
            pass

        # 尝试 Python 字面量 (兼容单引号)
        try:
            obj = ast.literal_eval(text)
            formatted = json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)
            return formatted.splitlines()
        except (ValueError, SyntaxError):
            pass

        # 如果都不是，直接按行分割原始文本进行对比
        return text.splitlines()

    def run_compare(self):
        """执行对比逻辑"""
        # 1. 获取输入内容
        raw_left = self.left_text.get(1.0, tk.END)
        raw_right = self.right_text.get(1.0, tk.END)

        # 2. 解析并格式化
        lines_left = self.parse_content(raw_left)
        lines_right = self.parse_content(raw_right)

        # 3. 计算差异
        d = difflib.Differ()
        diff = list(d.compare(lines_left, lines_right))

        # 4. 清空界面准备显示结果
        self.reset_ui_for_result()

        # 5. 渲染差异
        buffer_left = []
        buffer_right = []

        for line in diff:
            code = line[:2]
            text = line[2:]

            if code == '  ':
                self._flush_buffer(buffer_left, buffer_right)
                self._insert_row(text, text, mode='common')
            elif code == '- ':
                buffer_left.append(text)
            elif code == '+ ':
                buffer_right.append(text)
            elif code == '? ':
                continue

        self._flush_buffer(buffer_left, buffer_right)

        # 6. 设置为只读，防止误改结果
        self.left_text.config(state=tk.DISABLED)
        self.right_text.config(state=tk.DISABLED)

    def reset_inputs(self):
        """重置为输入模式 (清空内容)"""
        self.left_text.config(state=tk.NORMAL)
        self.right_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)
        self.right_text.delete(1.0, tk.END)

    def reset_ui_for_result(self):
        """清空文本框用于显示结果"""
        self.left_text.config(state=tk.NORMAL)
        self.right_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)
        self.right_text.delete(1.0, tk.END)

    def _flush_buffer(self, left_buf, right_buf):
        for l_line, r_line in itertools.zip_longest(left_buf, right_buf, fillvalue=None):
            self._insert_row(l_line, r_line, mode='diff')
        left_buf.clear()
        right_buf.clear()

    def _insert_row(self, left_text, right_text, mode):
        # 左侧
        if left_text is not None:
            tag = 'del' if mode == 'diff' else ''
            self.left_text.insert(tk.END, left_text + "\n", tag)
        else:
            self.left_text.insert(tk.END, "\n") # 空行占位

        # 右侧
        if right_text is not None:
            tag = 'add' if mode == 'diff' else ''
            self.right_text.insert(tk.END, right_text + "\n", tag)
        else:
            self.right_text.insert(tk.END, "\n")

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DiffGUI()
    app.show()