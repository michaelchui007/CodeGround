import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QApplication, QAbstractItemView, QListWidget, QListWidgetItem, \
    QFileDialog, QMessageBox
from PySide6.QtCore import Qt

from templetes.export_report_dialog.export_dialog import Ui_ExportDialog


class ExportReportView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ExportDialog()
        self.ui.setupUi(self)
        self.all_columns = [f"选项{i}" for i in range(1, 20)]

        # 2. 定义默认已经在右边的列
        self.default_selected = []

        self.init_ui_setup()
        self.init_data()
        self.init_connections()


    # ... (init_ui_setup 代码保持不变，此处省略) ...
    def init_ui_setup(self):
        # 1. 获取 GroupBox 内部的网格布局
        grid_layout = self.ui.groupBox_columns.layout()

        # 2. 【关键】设置列拉伸权重
        # 参数: setColumnStretch(列索引, 权重)
        # 权重 0 表示：只占用控件的最小尺寸，不参与瓜分多余空间
        # 权重 >0 表示：按比例瓜分多余空间
        grid_layout.setColumnStretch(0, 10)  # 左侧列表：占大头
        grid_layout.setColumnStretch(1, 0)   # 中间按钮：权重0 (尽可能窄)
        grid_layout.setColumnStretch(2, 10)  # 右侧列表：占大头
        grid_layout.setColumnStretch(3, 0)   # 右侧按钮：权重0 (尽可能窄)

        # 3. 【优化】去掉中间按钮布局的边距 (这一步能让它更窄)
        # 默认布局四周有空隙，设为 0 可以紧贴列表
        self.ui.verticalLayout_mid_btns.setContentsMargins(0, 0, 0, 0)
        self.ui.verticalLayout_right_btns.setContentsMargins(0, 0, 0, 0)

        # 4. 设置按钮固定大小 (防止被拉伸)
        min_btn_width = 40
        buttons = [self.ui.btn_move_left, self.ui.btn_move_right,
                   self.ui.btn_top, self.ui.btn_up, self.ui.btn_down, self.ui.btn_bottom]
        for btn in buttons:
            # 既设置最小宽度，又设置最大宽度，这就锁死了宽度
            btn.setFixedWidth(min_btn_width)
            # 如果想限制高度也可以 setFixedSize(40, 30)

        # 5. 调整整个界面的左右比例 (3:2 或 1:1)
        # 这是调整 Template 那一栏和 Output Columns 那一栏的比例
        self.ui.horizontalLayout_content.setStretch(0, 1) # 左边大区域
        self.ui.horizontalLayout_content.setStretch(1, 1) # 右边 Output Columns

        # 6. 其他设置
        self.ui.btn_ok.setFixedSize(80, 30)
        self.ui.btn_cancel.setFixedSize(80, 30)

        self.ui.le_template.setPlaceholderText("模板存放路径")
        self.ui.le_save_path.setPlaceholderText("保存文件路径")
        self.ui.le_project_name.setText("job name")
        self.ui.le_prepared_by.setText("支持用户手动输入作业人员名字信息")
        self.ui.te_description.setText("支持用户手动输入项目描述信息")

        # 设置多选模式
        self.ui.list_available.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.list_output.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def init_data(self):
        """
        初始化数据：核心在于'同步'左侧的隐藏状态
        """
        self.ui.combo_format.addItems(["Html", "PDF", "Excel"])

        # 1. 定义全量的列名 (按照初始顺序)


        # 3. 填充左侧列表 (全部填充)
        for col_name in self.all_columns:
            item = QListWidgetItem(col_name)
            self.ui.list_available.addItem(item)

            # 【关键逻辑】如果这个项默认在右边，左边就得隐藏它
            if col_name in self.default_selected:
                item.setHidden(True)

        # 4. 填充右侧列表
        self.ui.list_output.addItems(self.default_selected)

    def init_connections(self):
        self.ui.btn_move_right.clicked.connect(self.on_move_right)
        self.ui.btn_move_left.clicked.connect(self.on_move_left)

        # 排序逻辑复用之前的
        self.ui.btn_top.clicked.connect(lambda: self.on_reorder("top"))
        self.ui.btn_up.clicked.connect(lambda: self.on_reorder("up"))
        self.ui.btn_down.clicked.connect(lambda: self.on_reorder("down"))
        self.ui.btn_bottom.clicked.connect(lambda: self.on_reorder("bottom"))

        self.ui.btn_ok.clicked.connect(self.on_ok_clicked)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.ui.btn_template_browse.clicked.connect(self.on_browse_template)
        self.ui.btn_save_path_browse.clicked.connect(self.on_browse_save_path)

        # ... (其他的 move_right, btn_ok 等逻辑保持不变) ...

    # ==========================
    #       文件选择逻辑
    # ==========================

    def on_browse_template(self):
        """
        方式变更：从静态方法 getOpenFileName -> 实例化 QFileDialog
        """
        # 1. 实例化对象
        file_dialog = QFileDialog(self, "选择模板文件", os.getcwd())

        # 2. 【核心】设置图标 (使用 QRC 路径)
        # 这一步在静态方法里是做不到的
        file_dialog.setWindowIcon(QIcon(":/assets/logo.png"))

        # 3. 设置过滤器
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls);;Word Files (*.docx);;All Files (*)")

        # 4. 设置模式 (比如只选文件，不选文件夹)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        # 5. 显示并判断返回值
        # exec() 返回 1 表示用户点了打开，0 表示取消
        if file_dialog.exec():
            # 获取选中的文件列表 (哪怕只选了一个，返回的也是 list)
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.ui.le_template.setText(file_path)

    def on_browse_save_path(self):
        """
        场景 B: 保存路径
        新增功能：默认预填自定义文件名
        """
        # 1. 获取格式配置 (保持之前的 Strategy Pattern)
        current_fmt = self.ui.combo_format.currentText()
        fmt_config = {
            "Html":  ("Html Files (*.html)", "html"),
            "PDF":   ("PDF Files (*.pdf)",   "pdf"),
            "Excel": ("Excel Files (*.xlsx)", "xlsx"),
            "CSV":   ("CSV Files (*.csv)",    "csv")
        }
        target_filter, default_ext = fmt_config.get(current_fmt, ("All Files (*)", ""))

        # ==========================================
        # 2. 【新增】定义您的自定义文件名
        # ==========================================
        # 这里您可以写死，也可以从界面上的 Project Name 输入框获取
        base_name = "Analysis_Report_v1"

        input_name = self.ui.le_save_path.text() or base_name

        # 拼接后缀 (e.g., "Analysis_Report_v1.html")
        default_filename = f"{input_name}.{default_ext}" if default_ext else input_name

        # 3. 实例化 Dialog
        file_dialog = QFileDialog(self, "保存分析报告", os.getcwd())
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setWindowIcon(QIcon(":/assets/logo.png"))

        # 4. 应用配置
        file_dialog.setNameFilters([target_filter, "All Files (*)"])
        file_dialog.selectNameFilter(target_filter)

        if default_ext:
            file_dialog.setDefaultSuffix(default_ext)

        # 5. 【关键一步】设置默认文件名
        # selectFile 会把字符串填入对话框底部的 "文件名" 输入框中
        file_dialog.selectFile(default_filename)

        # 6. 显示并处理
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.ui.le_save_path.setText(file_path)
    # ==========================
    #       修改后的移动逻辑
    # ==========================

    def on_move_right(self):
        """ 左 -> 右：复制 + 隐藏左侧 """
        source_list = self.ui.list_available
        target_list = self.ui.list_output

        selected_items = source_list.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            # 1. 在右侧创建一个新的 item (副本)
            new_item = QListWidgetItem(item.text())
            target_list.addItem(new_item)

            # 2. 在左侧隐藏该 item，并取消选中状态
            item.setHidden(True)
            item.setSelected(False)

    def on_move_left(self):
        """ 右 -> 左：删除右侧 + 显示左侧 """
        source_list = self.ui.list_output  # 右边
        target_list = self.ui.list_available # 左边

        selected_items = source_list.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            text = item.text()

            # 1. 在左侧找到对应的 item 并“复活” (Show)
            # findItems 返回的是列表，Qt.MatchExactly 确保全字匹配
            found_items = target_list.findItems(text, Qt.MatchExactly)
            if found_items:
                original_item = found_items[0]
                original_item.setHidden(False)
                # 可选：移回去后自动选中左侧的该项，方便用户知道它回哪儿了
                original_item.setSelected(True)

            # 2. 从右侧彻底删除
            row = source_list.row(item)
            source_list.takeItem(row)

    # ==========================
    #       排序逻辑 (保持不变)
    # ==========================
    def on_reorder(self, direction: str):
        """右侧列表内部排序，代码逻辑不需要变"""
        list_widget = self.ui.list_output
        selected_items = list_widget.selectedItems()
        if not selected_items: return

        rows = sorted([list_widget.row(item) for item in selected_items])
        items_to_move = [list_widget.item(r) for r in rows]

        if direction == "top":
            for row in reversed(rows): list_widget.takeItem(row)
            for i, item in enumerate(items_to_move):
                list_widget.insertItem(i, item)
                item.setSelected(True)

        elif direction == "bottom":
            for row in reversed(rows): list_widget.takeItem(row)
            for item in items_to_move:
                list_widget.addItem(item)
                item.setSelected(True)

        elif direction == "up":
            if rows[0] == 0: return
            for item in items_to_move:
                row = list_widget.row(item)
                list_widget.takeItem(row)
                list_widget.insertItem(row - 1, item)
                item.setSelected(True)

        elif direction == "down":
            if rows[-1] == list_widget.count() - 1: return
            for item in reversed(items_to_move):
                row = list_widget.row(item)
                list_widget.takeItem(row)
                list_widget.insertItem(row + 1, item)
                item.setSelected(True)

    def on_ok_clicked(self):
        """
        点击 OK 按钮后的自定义逻辑
        """


        # 1. --- 获取 UI 数据 ---
        # 既然您现在用的是 setText 填默认值，获取时就直接取 text()
        template_path = self.ui.le_template.text().strip()
        save_path = self.ui.le_save_path.text().strip()
        project_name = self.ui.le_project_name.text().strip()
        prepared_by = self.ui.le_prepared_by.text().strip()
        des_text = self.ui.te_description.toPlainText().strip()

        # 2. --- 数据校验 (非常重要) ---
        # 如果校验不通过，直接 return，窗口就不会关闭
        if not template_path:
            QMessageBox.warning(self, "校验失败", "请选择模板文件路径！")
            return
        if not save_path:
            QMessageBox.warning(self, "校验失败", "请选择保存路径！")
            return

        current_output_columns = [self.ui.list_output.item(i).text() for i in range(self.ui.list_output.count())]
        output_format = self.ui.combo_format.currentText()


        # 3. --- 调用后端接口 ---
        # 组装数据参数
        params = {
            "template": template_path,
            "output": save_path,
            "project": project_name,
            "user": prepared_by,
            "columns": current_output_columns,
            "output_format": output_format,
            "description": des_text
        }
        print(f"\n正在调用后端接口，参数: {params}")

        try:
            # ===============================================
            # 这里调用您的 C++ / Python 业务函数
            # result = my_backend_api.generate_report(params)
            # ===============================================

            # 模拟业务执行成功
            success = True

            if success:
                # 4. --- 业务成功，手动关闭窗口 ---
                # 这一步等同于之前的 self.accept()，它会    关闭弹窗并让 exec() 返回 1
                self.accept()
            else:
                # 如果业务失败（比如文件被占用），弹窗提示，且不关闭窗口
                QMessageBox.critical(self, "错误", "导出失败：目标文件被占用")

        except Exception as e:
            QMessageBox.critical(self, "异常", f"发生未知错误: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExportReportView()
    window.show()
    sys.exit(app.exec())