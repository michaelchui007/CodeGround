import json
import difflib
import tkinter as tk
from tkinter import font, messagebox
import itertools
import ast

class DiffGUI:
    """
    交互式差异对比工具：支持粘贴 JSON/Python 数据进行左右对比，带行号显示
    """
    def __init__(self, window_size="1200x800"):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("JSON/List 差异对比工具 (带行号)")
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
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 1. 垂直滚动条 (控制所有文本框的垂直滚动)
        self.v_scrollbar = tk.Scrollbar(main_container, orient=tk.VERTICAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 2. PanedWindow (左右拖动调节分割线)
        self.paned_window = tk.PanedWindow(main_container, orient=tk.HORIZONTAL, sashwidth=5, bg="#dddddd")
        self.paned_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # === 创建左右两侧面板 ===
        # 左侧
        self.left_text, self.left_linenum = self.create_text_panel(self.paned_window, "原数据 (Left)")
        # 右侧
        self.right_text, self.right_linenum = self.create_text_panel(self.paned_window, "新数据 (Right)")

        # === 滚动联动配置 ===
        # 垂直滚动条控制 4 个组件
        self.v_scrollbar.config(command=self._scroll_all)

        # 只有左侧主文本框驱动滚动条滑块位置 (避免冲突)
        self.left_text.config(yscrollcommand=self.v_scrollbar.set)

        # 鼠标滚轮绑定到所有组件
        for widget in [self.left_text, self.left_linenum, self.right_text, self.right_linenum]:
            self._bind_mousewheel(widget)

        # === 编辑模式下的行号自动更新绑定 ===
        self.left_text.bind('<<Modified>>', lambda e: self._on_text_modified(self.left_text, self.left_linenum))
        self.right_text.bind('<<Modified>>', lambda e: self._on_text_modified(self.right_text, self.right_linenum))
        # 同时也绑定 KeyRelease 以获得更即时的响应
        self.left_text.bind('<KeyRelease>', lambda e: self.update_line_numbers(self.left_text, self.left_linenum))
        self.right_text.bind('<KeyRelease>', lambda e: self.update_line_numbers(self.right_text, self.right_linenum))

        # === 颜色标签配置 ===
        for widget in [self.left_text, self.right_text]:
            widget.tag_config('del', background='#ffe0e0', foreground='#b30000')
            widget.tag_config('add', background='#e0ffe0', foreground='#006600')
            widget.tag_config('header', font=(self.custom_font.cget("family"), 10, 'bold'), background='#f8f8f8', foreground='#555555')

    def create_text_panel(self, parent, title):
        """辅助函数：创建包含 标题+行号+文本框+横向滚动条 的面板"""
        frame = tk.Frame(parent)
        parent.add(frame, minsize=100) # 添加到 PanedWindow

        # 标题
        tk.Label(frame, text=title, font=('Arial', 10, 'bold'), bg="#f0f0f0").pack(fill=tk.X)

        # 内容容器 (行号 + 文本)
        content_frame = tk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 横向滚动条
        h_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # 行号栏 (宽度固定, 背景略灰, 禁用编辑)
        line_num = tk.Text(
            content_frame,
            width=4,
            font=self.custom_font,
            bg="#f0f0f0",
            fg="#888888",
            bd=0,
            state=tk.DISABLED,
            wrap=tk.NONE,
            cursor="arrow"
        )
        line_num.pack(side=tk.LEFT, fill=tk.Y)

        # 主文本框
        text_area = tk.Text(
            content_frame,
            font=self.custom_font,
            wrap=tk.NONE,
            xscrollcommand=h_scroll.set,
            # yscrollcommand 由外部统一配置
            undo=True,
            bd=0
        )
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 连接横向滚动条
        h_scroll.config(command=text_area.xview)

        return text_area, line_num

    def _bind_mousewheel(self, widget):
        """绑定鼠标滚轮事件"""
        # Windows
        widget.bind("<MouseWheel>", self._on_mousewheel)
        # Linux
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)

    def _scroll_all(self, *args):
        """垂直滚动条回调：同时移动所有 4 个文本区域"""
        self.left_text.yview(*args)
        self.left_linenum.yview(*args)
        self.right_text.yview(*args)
        self.right_linenum.yview(*args)

    def _on_mousewheel(self, event):
        """鼠标滚轮回调"""
        if event.num == 5 or event.delta < 0:
            delta = 1
        else:
            delta = -1

        # 同时滚动所有组件
        for widget in [self.left_text, self.left_linenum, self.right_text, self.right_linenum]:
            widget.yview_scroll(delta, "units")
        return "break"

    def _on_text_modified(self, text_widget, line_widget):
        """处理文本修改事件"""
        # 重置修改标志，否则下次不会触发
        if text_widget.edit_modified():
            self.update_line_numbers(text_widget, line_widget)
            text_widget.edit_modified(False)

    def update_line_numbers(self, text_widget, line_widget):
        """重新计算并绘制行号"""
        line_widget.config(state=tk.NORMAL)
        line_widget.delete(1.0, tk.END)

        # 获取总行数
        # end-1c 避免获取末尾自动添加的换行符
        row_count = int(text_widget.index('end-1c').split('.')[0])

        # 生成行号文本 "1\n2\n3..."
        line_content = "\n".join(str(i) for i in range(1, row_count + 1))
        line_widget.insert(1.0, line_content)

        # 保持位置同步（防止更新行号后位置跳变）
        first_visible = text_widget.yview()[0]
        line_widget.yview_moveto(first_visible)

        line_widget.config(state=tk.DISABLED)

    def parse_content(self, text):
        text = text.strip()
        if not text:
            return []
        try:
            obj = json.loads(text)
            formatted = json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)
            return formatted.splitlines()
        except json.JSONDecodeError:
            pass
        try:
            obj = ast.literal_eval(text)
            formatted = json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)
            return formatted.splitlines()
        except (ValueError, SyntaxError):
            pass
        return text.splitlines()

    def run_compare(self):
        """执行对比逻辑"""
        raw_left = self.left_text.get(1.0, tk.END)
        raw_right = self.right_text.get(1.0, tk.END)

        lines_left = self.parse_content(raw_left)
        lines_right = self.parse_content(raw_right)

        d = difflib.Differ()
        diff = list(d.compare(lines_left, lines_right))

        # 清空
        self.reset_ui_for_result()

        # 渲染差异
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

        # 更新行号
        self.update_line_numbers(self.left_text, self.left_linenum)
        self.update_line_numbers(self.right_text, self.right_linenum)

        # 锁定编辑
        self.left_text.config(state=tk.DISABLED)
        self.right_text.config(state=tk.DISABLED)

    def reset_inputs(self):
        """重置为输入模式"""
        self.left_text.config(state=tk.NORMAL)
        self.right_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)
        self.right_text.delete(1.0, tk.END)
        self.update_line_numbers(self.left_text, self.left_linenum)
        self.update_line_numbers(self.right_text, self.right_linenum)

    def reset_ui_for_result(self):
        """清空文本框用于显示结果"""
        self.left_text.config(state=tk.NORMAL)
        self.right_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)
        self.right_text.delete(1.0, tk.END)
        # 行号稍后统一更新

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