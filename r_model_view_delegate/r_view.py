"""
自定义TableView和TreeView视图组件
"""

from PySide6.QtWidgets import QTableView, QTreeView, QHeaderView
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QMouseEvent, QKeyEvent, QWheelEvent, QContextMenuEvent


class RTableView(QTableView):
    """自定义表格视图 - 优化性能和交互"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_view()
    
    def _setup_view(self):
        """配置视图基础设置"""
        # 交替行颜色
        self.setAlternatingRowColors(True)
        
        # 禁用排序（性能优化）
        self.setSortingEnabled(False)
        
        # 滚动模式 - 按项滚动（性能更好）
        self.setVerticalScrollMode(QTableView.ScrollMode.ScrollPerItem)
        self.setHorizontalScrollMode(QTableView.ScrollMode.ScrollPerItem)
        
        # 垂直表头设置
        self.verticalHeader().setDefaultSectionSize(24)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # 水平表头设置
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
    
    # ========== 鼠标事件 ==========
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """鼠标按下事件"""
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """鼠标释放事件"""
        super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """鼠标双击事件"""
        super().mouseDoubleClickEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """鼠标移动事件"""
        super().mouseMoveEvent(event)
    
    def wheelEvent(self, event: QWheelEvent) -> None:
        """鼠标滚轮事件"""
        super().wheelEvent(event)
    
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        """右键菜单事件"""
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        menu.addAction("复制")
        menu.addAction("粘贴")
        menu.addSeparator()
        menu.addAction("删除")
        menu.exec(event.globalPos())

        super().contextMenuEvent(event)
    
    # ========== 键盘事件 ==========
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        """键盘按下事件"""
        super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        """键盘释放事件"""
        super().keyReleaseEvent(event)
    
    # ========== 焦点事件 ==========
    
    def focusInEvent(self, event) -> None:
        """获得焦点事件"""
        super().focusInEvent(event)
    
    def focusOutEvent(self, event) -> None:
        """失去焦点事件"""
        super().focusOutEvent(event)


class RTreeView(QTreeView):
    """自定义树形视图 - 支持层级展示"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_view()
    
    def _setup_view(self):
        """配置视图基础设置"""
        # 交替行颜色
        self.setAlternatingRowColors(True)
        
        # 禁用排序
        self.setSortingEnabled(False)
        
        # 编辑触发方式 - 单击选中后再次单击编辑
        self.setEditTriggers(QTreeView.EditTrigger.SelectedClicked)
        
        # 表头设置
        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
    
    # ========== 鼠标事件 ==========
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """鼠标按下事件"""
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """鼠标释放事件"""
        super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """鼠标双击事件"""
        super().mouseDoubleClickEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """鼠标移动事件"""
        super().mouseMoveEvent(event)
    
    def wheelEvent(self, event: QWheelEvent) -> None:
        """鼠标滚轮事件"""
        super().wheelEvent(event)
    
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        """右键菜单事件"""

        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        menu.addAction("复制")
        menu.addAction("粘贴")
        menu.addSeparator()
        menu.addAction("删除")
        menu.exec(event.globalPos())
        
        super().contextMenuEvent(event)
    
    # ========== 键盘事件 ==========
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        """键盘按下事件"""
        super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        """键盘释放事件"""
        super().keyReleaseEvent(event)
    
    # ========== 焦点事件 ==========
    
    def focusInEvent(self, event) -> None:
        """获得焦点事件"""
        super().focusInEvent(event)
    
    def focusOutEvent(self, event) -> None:
        """失去焦点事件"""
        super().focusOutEvent(event)
