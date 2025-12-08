"""
图书库管理系统主窗口
基于data.csv的图书数据展示和编辑
使用PySide6实现
"""

import sys
import csv
import time
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QScrollBar, QVBoxLayout, QWidget,
    QPushButton, QFileDialog, QHBoxLayout, QLabel, QMessageBox,
    QDockWidget, QTextEdit
)
from PySide6.QtCore import Qt, QTimer

from r_model import RTableModel, RTreeModel
from r_view import RTableView, RTreeView
from r_delegate import DelegateFactory, DelegateType


class RBookTableMainWindow(QMainWindow):
    """图书库管理表格视图主窗口"""
    
    def __init__(self):
        super().__init__()
        self.model = RTableModel()
        self.stats_dock = None
        self.stats_timer = None
        self.csv_file_path = None
        self.load_rows = 10000
        self.is_loading = False
        
        # 下拉选项列表
        self.categories = [
            '文学', '历史', '哲学', '艺术', '社会科学', '自然科学',
            '工业技术', '计算机', '经济', '管理', '教育', '语言',
            '小说', '诗歌', '散文', '传记'
        ]
        
        self.authors = [
            '鲁迅', '老舍', '巴金', '茅盾', '钱钟书', '沈从文', '张爱玲', '冰心',
            '曹雪芹', '吴承恩', '施耐庵', '罗贯中', '金庸', '古龙', '梁羽生',
            '莫言', '余华', '王小波', '刘慈欣', '韩寒', '郭敬明', '安妮宝贝'
        ]
        
        self.publishers = [
            '人民文学出版社', '作家出版社', '中华书局', '商务印书馆', '三联书店',
            '上海译文出版社', '北京大学出版社', '清华大学出版社', '机械工业出版社',
            '电子工业出版社', '科学出版社', '高等教育出版社'
        ]
        
        self.statuses = ['在架', '借出', '维修', '下架']
        self.notes_options = ['', '热门', '新书', '推荐', '畅销', '经典', '珍藏版']
        
        # 使用工厂类创建delegates
        factory = DelegateFactory()
        delegates = factory.create_batch({
            'category': (DelegateType.COMBOBOX, {'options': self.categories}),
            'author': (DelegateType.COMBOBOX, {'options': self.authors}),
            'publisher': (DelegateType.COMBOBOX, {'options': self.publishers}),
            'status': (DelegateType.COMBOBOX, {'options': self.statuses}),
            'notes': (DelegateType.COMBOBOX, {'options': self.notes_options}),
            'borrowed': (DelegateType.CHECKBOX, {}),
            'title': (DelegateType.LINEEDIT, {}),
            'publish_date': (DelegateType.DATE, {}),
            'color': (DelegateType.COLOR, {})
        })
        
        # 保存delegates
        self.delegates = delegates
        
        self.init_ui()
        
        # 自动加载data.csv
        import os
        csv_path = os.path.join(os.path.dirname(__file__), 'data.csv')
        if os.path.exists(csv_path):
            self.load_csv_file(csv_path, self.load_rows)
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('图书库管理系统 - 表格视图')
        self.setGeometry(100, 100, 1400, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        self.load_btn = QPushButton('加载CSV文件')
        self.load_btn.clicked.connect(self.load_csv)
        toolbar_layout.addWidget(self.load_btn)
        
        self.save_btn = QPushButton('保存CSV文件')
        self.save_btn.clicked.connect(self.save_csv)
        toolbar_layout.addWidget(self.save_btn)
        
        self.row_count_label = QLabel('行数: 0')
        toolbar_layout.addWidget(self.row_count_label)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        # 使用自定义表格视图
        self.table_view = RTableView()
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)
        
        # 创建统计DockWidget
        self.create_stats_dock()
        
        # 启动定时器
        self.start_stats_timer()
        
        # 状态栏
        self.statusBar().showMessage('就绪')
    
    def on_scrollbar_valueChanged(self, value: int) -> None:
        """滚动条变化时检查是否需要自动加载更多数据"""
        scrollbar: QScrollBar = self.table_view.verticalScrollBar()
        total: int = scrollbar.maximum()
        if total > 0 and value >= total * 0.8:
            current_rows = self.model.rowCount()
            if not self.is_loading and self.csv_file_path and current_rows < self.model._total_count:
                self.auto_load_more_data()

    def auto_load_more_data(self):
        """自动加载更多数据"""
        self.is_loading = True
        current_rows: int = self.model.rowCount()
        remaining: int = self.model._total_count - 2 - current_rows
        batch_size = min(self.load_rows, remaining)
        batch_start_time = time.time()
        
        if batch_size > 0:
            self.statusBar().showMessage(f'正在加载更多数据... ({current_rows} -> {current_rows + batch_size})')
            QApplication.processEvents()

        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                totals = next(reader)
                headers = next(reader)
                for _ in range(current_rows):
                    next(reader)

                new_rows = []
                for i, row in enumerate(reader):
                    if i >= batch_size:
                        break
                    new_rows.append(row)
                    
                if new_rows:
                    added_count = self.model.append_rows(new_rows)
                    batch_elapsed = time.time() - batch_start_time
                    
                    total = int(totals[0]) - 2
                    loaded_rows = self.model.rowCount()
                    
                    if loaded_rows < total:
                        self.row_count_label.setText(f'行数: {loaded_rows} / {total} (滚动自动加载)')
                        status_msg = f'已加载 {loaded_rows} / {total} 行 | 此批耗时: {batch_elapsed:.3f}秒'
                        self.statusBar().showMessage(status_msg)
                        print(f"[Performance] 懒加载批次 | 加载 {added_count} 行 | 耗时: {batch_elapsed:.3f}秒")
                    else:
                        self.row_count_label.setText(f'行数: {loaded_rows} (全部加载完成)')
                        self.statusBar().showMessage('所有数据已加载完成！')
                        print(f"[Performance] 懒加载完成 | 总行数: {loaded_rows}")
        except Exception as e:
            error_msg = f'加载更多数据失败: {str(e)}'
            self.statusBar().showMessage(error_msg)
            print(error_msg)
        finally:
            self.is_loading = False
    
    def load_csv(self):
        """打开文件对话框加载CSV"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, '选择CSV文件', '', 'CSV文件 (*.csv);;所有文件 (*.*)'
        )
        if filepath:
            self.load_csv_file(filepath)
    
    def load_csv_file(self, filepath, load_rows=None):
        """加载CSV文件"""
        success, message = self.model.load_csv(filepath, load_rows)
        
        if success:
            headers = self.model.get_headers()
            self.csv_file_path = filepath
            
            # 设置各列的代理
            column_mapping = {
                'category': 'category',
                'author': 'author',
                'publisher': 'publisher',
                'title': 'title',
                'notes': 'notes',
                'borrowed': 'borrowed',
                'publish_date': 'publish_date',
                'color': 'color'
            }
            
            for col_name, delegate_key in column_mapping.items():
                if col_name in headers and delegate_key in self.delegates:
                    col = headers.index(col_name)
                    self.table_view.setItemDelegateForColumn(col, self.delegates[delegate_key])
            
            # 更新行数显示
            loaded_rows = self.model.rowCount()
            total_rows = self.model._total_count - 2
            self.row_count_label.setText(f'行数: {loaded_rows} / {total_rows}')
            self.statusBar().showMessage(message)
            
            # 连接滚动条事件（用于懒加载）
            scrollbar = self.table_view.verticalScrollBar()
            scrollbar.valueChanged.connect(self.on_scrollbar_valueChanged)
            
            # 自适应列宽
            self.table_view.resizeColumnsToContents()
        else:
            self.statusBar().showMessage(message)
            QMessageBox.warning(self, '加载错误', message)
    
    def save_csv(self):
        """保存CSV文件"""
        filepath, _ = QFileDialog.getSaveFileName(
            self, '保存CSV文件', '', 'CSV文件 (*.csv);;所有文件 (*.*)'
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    total = len(self.model.get_data()) + 2
                    writer.writerow([total])
                    writer.writerow(self.model.get_headers())
                    writer.writerows(self.model.get_data())
                
                self.statusBar().showMessage(f'成功保存到: {filepath}')
                QMessageBox.information(self, '保存成功', f'数据已保存到:\n{filepath}')
            except Exception as e:
                error_msg = f'保存失败: {str(e)}'
                self.statusBar().showMessage(error_msg)
                QMessageBox.critical(self, '保存错误', error_msg)
    
    def create_stats_dock(self):
        """创建渲染统计DockWidget"""
        self.stats_dock = QDockWidget('渲染统计 (虚拟化验证)', self)
        self.stats_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        
        title_label = QLabel('实时渲染统计')
        title_label.setStyleSheet('font-weight: bold; font-size: 14px; padding: 5px;')
        stats_layout.addWidget(title_label)
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #00ff00;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                border: 1px solid #555;
                padding: 5px;
            }
        """)
        stats_layout.addWidget(self.stats_text, 1)
        
        btn_layout = QHBoxLayout()
        
        reset_btn = QPushButton('重置统计')
        reset_btn.clicked.connect(self.reset_stats)
        btn_layout.addWidget(reset_btn)
        
        refresh_btn = QPushButton('立即刷新')
        refresh_btn.clicked.connect(self.update_stats_display)
        btn_layout.addWidget(refresh_btn)
        
        stats_layout.addLayout(btn_layout, 0)
        
        self.stats_dock.setWidget(stats_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.stats_dock)
    
    def start_stats_timer(self):
        """启动定时器"""
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats_display)
        self.stats_timer.start(1000)
    
    def update_stats_display(self):
        """更新统计显示"""
        stats = self.model.get_render_stats()
        total = stats['total_rows']
        rendered = stats['unique_rows_rendered']
        calls = stats['total_data_calls']
        
        stats_text = f"""
总数据行数:     {total:,}
已渲染行数:     {rendered:,}
data()调用次数: {calls:,}
• 单击可编辑列即可修改
"""
        self.stats_text.setPlainText(stats_text)
    
    def reset_stats(self):
        """重置统计"""
        self.model.reset_render_stats()
        self.update_stats_display()
        self.statusBar().showMessage('统计已重置', 2000)


class RBookTreeMainWindow(QMainWindow):
    """图书树形视图主窗口 - 支持分类→作者→书名三级折叠"""
    
    def __init__(self):
        super().__init__()
        self.is_loading = False
        self.setWindowTitle('图书库管理系统 - 树形视图')
        self.setGeometry(100, 100, 1400, 800)
        self.csv_file_path = ''
        
        # 下拉选项
        self.categories = ['文学', '历史', '哲学', '艺术', '计算机', '经济', '科学', '教育', '社会', '医学', '法律', '心理', '传记', '小说', '诗歌', '其他']
        self.authors = ['鲁迅', '老舍', '巴金', '茅盾', '沈从文', '钱锺书', '史铁生', '林语堂', '沈石溪', '张爱玲', '梁启超', '胡适', '费孝通', '季羡林', '赵树理', '严复', '黄仁宇', '楊绠', '柳青', '张恒', '李明', '高建群']
        self.publishers = ['人民文学出版社', '三联书店', '中华书局', '商务印书馆', '机械工业出版社', '北京大学出版社', '清华大学出版社', '中国科学技术出版社', '中国社会科学出版社', '上海译文出版社', '广西师范大学出版社', '电子工业出版社']
        self.statuses = ['在架', '借出', '维修', '下架']
        self.notes_options = ['无', '新书', '热门', '经典', '珍本', '限量', '即将到货']
        
        # 创建模型
        self.tree_model = RTreeModel()
        
        # 使用工厂类创建delegates
        factory = DelegateFactory()
        delegates = factory.create_batch({
            'category': (DelegateType.COMBOBOX, {'options': self.categories}),
            'author': (DelegateType.COMBOBOX, {'options': self.authors}),
            'publisher': (DelegateType.COMBOBOX, {'options': self.publishers}),
            'status': (DelegateType.COMBOBOX, {'options': self.statuses}),
            'notes': (DelegateType.COMBOBOX, {'options': self.notes_options}),
            'borrowed': (DelegateType.CHECKBOX, {}),
            'title': (DelegateType.LINEEDIT, {}),
            'publish_date': (DelegateType.DATE, {}),
            'color': (DelegateType.COLOR, {})
        })
        
        self.delegates = delegates
        
        self.init_ui()
        
        # 自动加载数据
        import os
        csv_path = os.path.join(os.path.dirname(__file__), 'data.csv')
        if os.path.exists(csv_path):
            self.load_csv_file(csv_path, max_rows=1000)
    
    def init_ui(self):
        """初始化UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        load_btn = QPushButton('加载CSV文件')
        load_btn.clicked.connect(self.load_csv_dialog)
        toolbar_layout.addWidget(load_btn)
        
        expand_all_btn = QPushButton('展开所有')
        expand_all_btn.clicked.connect(self.expand_all)
        toolbar_layout.addWidget(expand_all_btn)
        
        collapse_all_btn = QPushButton('折叠所有')
        collapse_all_btn.clicked.connect(self.collapse_all)
        toolbar_layout.addWidget(collapse_all_btn)
        
        expand_level1_btn = QPushButton('展开至分类')
        expand_level1_btn.clicked.connect(lambda: self.tree_view.expandToDepth(0))
        toolbar_layout.addWidget(expand_level1_btn)
        
        expand_level2_btn = QPushButton('展开至作者')
        expand_level2_btn.clicked.connect(lambda: self.tree_view.expandToDepth(1))
        toolbar_layout.addWidget(expand_level2_btn)
        
        toolbar_layout.addStretch()
        
        # 添加"加载更多"按钮
        self.load_more_btn = QPushButton('加载更多数据')
        self.load_more_btn.clicked.connect(self.load_more_data)
        self.load_more_btn.setEnabled(False)
        toolbar_layout.addWidget(self.load_more_btn)
        
        self.row_count_label = QLabel('行数: 0')
        toolbar_layout.addWidget(self.row_count_label)
        
        layout.addLayout(toolbar_layout)
        
        # 使用自定义树形视图
        self.tree_view = RTreeView()
        self.tree_view.setModel(self.tree_model)
        
        # 监听滚动事件
        scrollbar: QScrollBar = self.tree_view.verticalScrollBar()
        scrollbar.valueChanged.connect(self.on_scrollbar_valueChanged)
        
        layout.addWidget(self.tree_view)
        
        # 状态栏
        self.statusBar().showMessage('就绪')
    
    def on_scrollbar_valueChanged(self, value: int) -> None:
        """滚动条变化时检查是否需要自动加载更多数据"""
        scrollbar: QScrollBar = self.tree_view.verticalScrollBar()
        total: int = scrollbar.maximum()
        
        if total > 0 and value >= total * 0.8:
            progress = self.tree_model.get_load_progress()
            if not self.is_loading and progress['remaining'] > 0:
                self.auto_load_more_data()

    def auto_load_more_data(self):
        """自动加载更多数据（懒加载）"""
        if self.is_loading:
            return
        
        self.is_loading = True
        progress = self.tree_model.get_load_progress()
        
        if progress['remaining'] > 0:
            self.statusBar().showMessage(f'正在加载更多数据... ({progress["loaded"]} -> {progress["loaded"] + 1000})')
            QApplication.processEvents()
            
            count, message = self.tree_model.append_more_data(self.csv_file_path, batch_size=1000)
            
            if count > 0:
                progress = self.tree_model.get_load_progress()
                self.row_count_label.setText(f'图书数: {progress["loaded"]} / {progress["total"]}')
                self.statusBar().showMessage(message)
                
                if progress['remaining'] > 0:
                    self.load_more_btn.setEnabled(True)
                    self.load_more_btn.setText(f'加载更多 (剩余 {progress["remaining"]} 行)')
                else:
                    self.load_more_btn.setEnabled(False)
                    self.load_more_btn.setText('全部已加载')
            else:
                self.statusBar().showMessage(message)
        
        self.is_loading = False
    
    def load_more_data(self):
        """手动点击按钮加载更多数据"""
        self.auto_load_more_data()

    def load_csv_dialog(self):
        """打开文件对话框"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, '选择CSV文件', '', 'CSV Files (*.csv);;All Files (*)'
        )
        if filepath:
            self.load_csv_file(filepath)
    
    def load_csv_file(self, filepath, max_rows=None):
        """加载CSV文件"""
        self.statusBar().showMessage(f'正在加载: {filepath}...')
        QApplication.processEvents()
        
        success, message = self.tree_model.load_csv_to_tree(filepath, max_rows)
        
        if success:
            headers = self.tree_model.get_headers()
            self.csv_file_path = filepath
            
            # 更新进度显示
            progress = self.tree_model.get_load_progress()
            self.row_count_label.setText(f'图书数: {progress["loaded"]} / {progress["total"]}')
            
            # 更新"加载更多"按钮
            if progress['remaining'] > 0:
                self.load_more_btn.setEnabled(True)
                self.load_more_btn.setText(f'加载更多 (剩余 {progress["remaining"]} 行)')
            else:
                self.load_more_btn.setEnabled(False)
                self.load_more_btn.setText('全部已加载')
            
            # 设置delegates
            delegate_mapping = {
                'status': 'status',
                'notes': 'notes',
                'borrowed': 'borrowed',
                'title': 'title',
                'publish_date': 'publish_date',
                'color': 'color'
            }
            
            for col_name, delegate_key in delegate_mapping.items():
                if col_name in headers and delegate_key in self.delegates:
                    col = headers.index(col_name)
                    self.tree_view.setItemDelegateForColumn(col, self.delegates[delegate_key])
            
            # 默认展开至分类级别
            self.tree_view.expandToDepth(0)
            
            self.statusBar().showMessage(message)
        else:
            self.statusBar().showMessage(message)
            QMessageBox.critical(self, '加载错误', message)
    
    def expand_all(self):
        """展开所有节点"""
        self.tree_view.expandAll()
        self.statusBar().showMessage('已展开所有节点', 2000)
    
    def collapse_all(self):
        """折叠所有节点"""
        self.tree_view.collapseAll()
        self.statusBar().showMessage('已折叠所有节点', 2000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 选择视图类型
    choice = QMessageBox.question(
        None,
        '选择视图类型',
        '请选择要使用的视图：\n\n'
        '• Yes - 树形视图（分类→作者→书名 折叠）\n'
        '• No - 表格视图（传统平面表格）',
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.Yes
    )
    
    if choice == QMessageBox.StandardButton.Yes:
        window = RBookTreeMainWindow()  # 树形视图
    else:
        window = RBookTableMainWindow()  # 表格视图
    
    window.show()
    sys.exit(app.exec())
