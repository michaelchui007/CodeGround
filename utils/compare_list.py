import json
import difflib
import tkinter as tk
from tkinter import scrolledtext, font
import itertools

class DiffGUI:
    """
    使用 Tkinter 创建弹窗显示左右对比差异
    """
    def __init__(self, width=60, window_size="1200x800"):
        self.width = width  # 单侧文本的字符宽度

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("列表/字典 差异对比查看器")
        self.root.geometry(window_size)

        # 设置字体 (使用等宽字体以保证对齐)
        # Windows/Linux 常用 Consolas 或 Courier New，Mac 常用 Menlo
        try:
            self.custom_font = font.Font(family="Consolas", size=10)
        except:
            self.custom_font = font.Font(family="Courier New", size=10)

        # 创建带滚动条的文本框
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            font=self.custom_font,
            wrap=tk.NONE,  # 不自动换行，保持左右结构
            state=tk.NORMAL
        )
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)

        # === 配置颜色标签 ===
        # 删除/旧值 (红色背景)
        self.text_area.tag_config('del', background='#ffe0e0', foreground='#b30000')
        # 新增/新值 (绿色背景)
        self.text_area.tag_config('add', background='#e0ffe0', foreground='#006600')
        # 分隔符 (灰色)
        self.text_area.tag_config('sep', foreground='#999999')
        # 标题 (加粗背景)
        self.text_area.tag_config('title', font=(self.custom_font.cget("family"), 12, 'bold'), background='#eeeeee', spacing1=10, spacing3=5)
        self.text_area.tag_config('header', font=(self.custom_font.cget("family"), 10, 'bold'))

    def _format_json(self, data):
        """将数据转换为格式化的 JSON 字符串列表"""
        json_str = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
        return json_str.splitlines()

    def add_diff(self, title, data1, data2):
        """
        添加一组对比数据到窗口中
        """
        lines1 = self._format_json(data1)
        lines2 = self._format_json(data2)

        d = difflib.Differ()
        diff = list(d.compare(lines1, lines2))

        # --- 打印标题 ---
        self.text_area.insert(tk.END, f"=== {title} ===\n", 'title')

        # --- 打印表头 ---
        header = f"{'List A (Left)':^{self.width}} | {'List B (Right)':^{self.width}}\n"
        self.text_area.insert(tk.END, header, 'header')
        self.text_area.insert(tk.END, "-" * (self.width * 2 + 3) + "\n", 'sep')

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

        # 添加一个空行分隔不同案例
        self.text_area.insert(tk.END, "\n" + "="* (self.width * 2 + 3) + "\n\n")

    def _flush_buffer(self, left_buf, right_buf):
        """将缓冲区的差异行成对写入"""
        for l_line, r_line in itertools.zip_longest(left_buf, right_buf, fillvalue=None):
            self._insert_row(l_line, r_line, mode='diff')
        left_buf.clear()
        right_buf.clear()

    def _insert_row(self, left_text, right_text, mode):
        """
        插入一行左右对比文本
        mode: 'common' | 'diff'
        """
        # 左侧处理
        if left_text is not None:
            display = left_text[:self.width].ljust(self.width)
            tag = 'del' if mode == 'diff' else ''
            self.text_area.insert(tk.END, display, tag)
        else:
            self.text_area.insert(tk.END, " " * self.width)

        # 中间分隔线
        self.text_area.insert(tk.END, " | ", 'sep')

        # 右侧处理
        if right_text is not None:
            display = right_text[:self.width].ljust(self.width)
            tag = 'add' if mode == 'diff' else ''
            self.text_area.insert(tk.END, display, tag)
        else:
            self.text_area.insert(tk.END, " " * self.width)

        self.text_area.insert(tk.END, "\n")

    def show(self):
        """显示窗口并禁止编辑"""
        self.text_area.config(state=tk.DISABLED) # 禁止用户手动修改内容
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
    # 初始化 GUI 查看器
    viewer = DiffGUI(width=50) # 可以调整列宽

    # 添加第一个对比案例
    viewer.add_diff("案例 1: 简单的值修改和新增项", list_a, list_b)

    # 添加第二个对比案例
    viewer.add_diff("案例 2: 嵌套列表差异", list_c, list_d)

    # 启动弹窗显示
    print("正在打开差异对比窗口...")
    viewer.show()