import PySide6
from PySide6.QtWidgets import (
        QApplication,
        QStyleOptionViewItem,
        QWidget,
        QStyledItemDelegate,
        QComboBox,
        QLineEdit,
        QDateEdit,
        QColorDialog,
        QStyle,
        QStyleOptionViewItem,
    )

from PySide6.QtCore import (QAbstractItemModel, Qt,QEvent,QRect,QDate,QModelIndex,QPersistentModelIndex,QRect)

from PySide6.QtGui import (
        QColor,
        QPainter,
        QPen,
        QFontMetrics,
        QPixmap,
        QIcon
    )

from enum import Enum,auto
from typing import Optional, Dict, Any,cast

class DelegateType(Enum):
    """Delegate类型枚举"""
    DATE     = auto()
    COLOR    = auto()
    COMBOBOX = auto()
    CHECKBOX = auto()
    LINEEDIT = auto()
    

class RComboBoxDelegate(QStyledItemDelegate):
    """下拉框代理"""
    
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.options = options  # 下拉选项列表
        self._editor_count = 0
        self._last_click_pos = None  # 记录最后一次点击位置
    
    def editorEvent(self, event:QEvent, model:QAbstractItemModel, option:QStyleOptionViewItem, index: QModelIndex):
        """单击触发编辑，并记录点击位置"""
        if event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                # 记录点击位置（相对于单元格）
                self._last_click_pos = event.pos()
                view = option.widget
                if view:
                    view.edit(index)
                return True
        return super().editorEvent(event, model, option, index)
    
    def createEditor(self, parent:QWidget, option:QStyleOptionViewItem, index:QModelIndex) -> QWidget:
        """创建下拉框编辑器，如果点击三角区域则立即展开"""
        self._editor_count += 1
        editor_id = self._editor_count
        
        print(f"[BookDelegate] 创建编辑器 #{editor_id} - {self.options[:3]}...")
        
        editor = QComboBox(parent)
        editor.setEditable(False)
        editor.setProperty("_model_index",index)
        
        # 添加选项
        for opt in self.options:
            editor.addItem(opt)
        
        # 连接activated信号：选择项后立即提交并关闭编辑器
        editor.activated.connect(lambda: self._commit_and_close(editor))
        
        # 自定义showPopup：滚动到顶部 + 显示在正下方
        original_show_popup = editor.showPopup
        def custom_show_popup():
            original_show_popup()
            
            list_view = editor.view()
            if list_view:
                list_view.scrollToTop()
                
                popup = list_view.parent()
                if popup:
                    combo_pos = editor.mapToGlobal(editor.rect().bottomLeft())
                    popup.move(combo_pos)
        
        editor.showPopup = custom_show_popup
        editor.destroyed.connect(lambda: print(f"[BookDelegate] 编辑器 #{editor_id} 已销毁"))
        
        # 判断是否点击了三角区域，如果是则立即展开下拉列表
        if 0:#self._last_click_pos:
            arrow_width = 20
            arrow_rect = option.rect.adjusted(option.rect.width() - arrow_width, 0, -2, 0)
            if arrow_rect.contains(self._last_click_pos):
                # 使用QTimer延迟调用，确保编辑器完全初始化
                from PySide6.QtCore import QTimer
                QTimer.singleShot(0, editor.showPopup)
            # 清除点击位置
            self._last_click_pos = None
        
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, editor.showPopup)
        
        return editor
    
    def _commit_and_close(self, editor:QWidget):
        """提交数据并关闭编辑器"""
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QStyledItemDelegate.EndEditHint.NoHint)

    def paint(self, painter:QPainter, option:QStyleOptionViewItem, index:QModelIndex) -> None:   
        """自定义绘制ComboBox样式：边框 + 文本 + 下拉三角形"""
        painter.save()
        
        # 1. 绘制背景（使用模型返回的背景色）
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        else:
            # 从模型获取背景色
            bg_color = index.data(Qt.ItemDataRole.BackgroundRole)
            if bg_color:
                painter.fillRect(option.rect, bg_color)
            else:
                painter.fillRect(option.rect, option.palette.base())
        
        # 2. 绘制边框
        from PySide6.QtGui import QPen
        pen = QPen(QColor(180, 180, 180), 1)  # 灰色边框
        painter.setPen(pen)
        # 留出1像素边距，避免边框被截断
        border_rect = option.rect.adjusted(1, 1, -1, -1)
        painter.drawRect(border_rect)
        
        # 3. 计算区域
        arrow_width = 20  # 下拉箭头区域宽度
        text_rect = option.rect.adjusted(5, 0, -arrow_width - 5, 0)  # 文本区，左边距5px
        arrow_rect = option.rect.adjusted(option.rect.width() - arrow_width, 0, -2, 0)  # 箭头区
        
        # 4. 绘制文本
        text = index.data(Qt.ItemDataRole.DisplayRole) or index.data(Qt.ItemDataRole.EditRole) or ''
        if option.state & QStyle.StateFlag.State_Selected:
            painter.setPen(option.palette.highlightedText().color())
        else:
            painter.setPen(option.palette.text().color())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
        
        # 5. 绘制下拉三角形
        from PySide6.QtGui import QPolygon
        from PySide6.QtCore import QPoint
        
        # 三角形中心点
        center_x = arrow_rect.center().x()
        center_y = arrow_rect.center().y()
        
        # 三角形顶点（向下的三角形）
        triangle = QPolygon([
            QPoint(center_x - 4, center_y - 2),  # 左上
            QPoint(center_x + 4, center_y - 2),  # 右上
            QPoint(center_x, center_y + 3)       # 底部中心
        ])
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(100, 100, 100))  # 深灰色三角形
        painter.drawPolygon(triangle)
        
        painter.restore()
    
    def setEditorData(self, editor:QWidget, index):
        """设置编辑器当前值"""
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        comboBox:QComboBox = cast(QComboBox,editor)
        if value and value in self.options:
            idx = self.options.index(value)
            comboBox.setCurrentIndex(idx)
        else:
            comboBox.setCurrentIndex(0)
    
    def setModelData(self, editor:QWidget, model:QAbstractItemModel, index:QModelIndex)->None:
        """保存编辑器的值"""
        print("setModelData+++++++++++++++")
        comboBox:QComboBox = cast(QComboBox,editor)
        value:str = comboBox.currentText()
        model.setData(index, value, Qt.ItemDataRole.EditRole)
    
    def updateEditorGeometry(self, editor:QWidget, option:QStyleOptionViewItem, index:QModelIndex)->None:
        """更新编辑器位置"""
        editor.setGeometry(option.rect)

class RCheckBoxDelegate(QStyledItemDelegate):
    """CheckBox代理 - 用于borrowed列等布尔值或数字切换"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def paint(self, painter:QPainter, option:QStyleOptionViewItem, index:QModelIndex)->None:
        """绘制CheckBox + 数值文本"""
        # 获取数据值
        value = index.data(Qt.ItemDataRole.DisplayRole)
        
        # 判断是否选中（borrowed > 0 为选中）
        try:
            num_value = int(value) if value else 0
            checked = num_value > 0
        except (ValueError, TypeError):
            num_value = 0
            checked = False
        
        # 绘制背景（使用模型返回的背景色）
        painter.save()
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        else:
            # 从模型获取背景色
            bg_color = index.data(Qt.ItemDataRole.BackgroundRole)
            if bg_color:
                painter.fillRect(option.rect, bg_color)
            else:
                painter.fillRect(option.rect, option.palette.base())
        
        # 使用系统样式绘制CheckBox
        from PySide6.QtWidgets import QStyleOptionButton
        checkbox_option = QStyleOptionButton()
        
        # 计算CheckBox位置（左侧）
        checkbox_size = 18
        checkbox_x = option.rect.x() + 5  # 左边距5px
        checkbox_y = option.rect.y() + (option.rect.height() - checkbox_size) // 2
        checkbox_option.rect = QRect(checkbox_x, checkbox_y, checkbox_size, checkbox_size)
        
        # 设置状态
        checkbox_option.state = QStyle.StateFlag.State_Enabled
        if checked:
            checkbox_option.state |= QStyle.StateFlag.State_On
        else:
            checkbox_option.state |= QStyle.StateFlag.State_Off
        
        # 绘制CheckBox
        QApplication.style().drawControl(QStyle.ControlElement.CE_CheckBox, checkbox_option, painter)
        
        # 绘制数值文本（CheckBox右侧）
        text_rect = option.rect.adjusted(checkbox_size + 10, 0, -5, 0)  # CheckBox后面留10px间距
        if option.state & QStyle.StateFlag.State_Selected:
            painter.setPen(option.palette.highlightedText().color())
        else:
            painter.setPen(option.palette.text().color())
        if num_value > 0 :
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, str("借出"))
        else:
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, str("未借出"))
        
        painter.restore()
    
    def editorEvent(self, event:QEvent, model:QAbstractItemModel, option:QStyleOptionViewItem, index:QModelIndex)->bool:
        """处理点击事件切换CheckBox状态"""
        if event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                # 获取当前值
                current_value = index.data(role = Qt.ItemDataRole.EditRole)
                try:
                    current_num = int(current_value) if current_value else 0
                except (ValueError, TypeError):
                    current_num = 0
                
                # 点击切换：如果是0则变为1，如果>0则变为0
                if current_num == 0:
                    new_value = 1  
                else:
                    new_value = 0  
                
                # 保存到模型
                model.setData(index, str(new_value), role = Qt.ItemDataRole.EditRole)
                return True
        
        return super().editorEvent(event, model, option, index)

class RDateDelegate(QStyledItemDelegate):
    """日期列的代理"""
    _editor_count = 0  # 统计编辑器创建次数
    def createEditor(self, parent:QWidget, option:QStyleOptionViewItem, index:QModelIndex)->QWidget:
        """创建日期编辑器"""
        editor = QDateEdit(parent)
        RDateDelegate._editor_count += 1
        editor_id = RDateDelegate._editor_count
        print(f"[Delegate] 创建编辑器 #{editor_id} - parent: {parent.__class__.__name__}")
        editor.setCalendarPopup(True) 
        editor.setDisplayFormat('yyyy-MM-dd')  
        editor.destroyed.connect(lambda: print(f"[Delegate] 编辑器 #{editor_id} 已销毁"))
        return editor
    
    def setEditorData(self, editor:QWidget, index):
        """设置编辑器的当前值"""
        value:Any = index.model().data(index, Qt.EditRole)
        dateEdit:QDateEdit = cast(QDateEdit,editor)
        if value:
            try:
                date:QDate = QDate.fromString(str(value), 'yyyy-MM-dd')
                if date.isValid():
                    dateEdit.setDate(date)
                else:
                    dateEdit.setDate(QDate.currentDate())
            except:
                dateEdit.setDate(QDate.currentDate())
        else:
            dateEdit.setDate(QDate.currentDate())
    
    def setModelData(self, editor, model, index):
        """将编辑器的值保存到模型"""
        date = editor.date()
        value = date.toString('yyyy-MM-dd')
        model.setData(index, value, Qt.EditRole)

class RLineEditDelegate(QStyledItemDelegate):
    """LineEdit代理（用于price和discount）"""
    _editor_count = 0  # 统计编辑器创建次数
    def __init__(self, parent=None)->None:
        super().__init__(parent)
    
    def createEditor(self, parent:QWidget, option:QStyleOptionViewItem, index)->QWidget:
        """创建输入编辑器"""
        editor: QLineEdit = QLineEdit(parent)
        RLineEditDelegate._editor_count += 1
        editor_id = RLineEditDelegate._editor_count
        print(f"[Delegate] 创建编辑器 #{editor_id} - parent: {parent.__class__.__name__}")
        editor.destroyed.connect(lambda: print(f"[Delegate] 编辑器 #{editor_id} 已销毁"))
        return editor
    
    def setEditorData(self, editor, index)->None:
        """设置编辑器的当前值"""
        value:Any = index.model().data(index, Qt.EditRole)
        if value:
            editor.setText(str(value))
        else:
            editor.setText('0.0')
    
    def setModelData(self, editor, model, index)->None:
        """将编辑器的值保存到模型"""
        text = editor.text()
        try:
            model.setData(index, text, Qt.EditRole)
        except ValueError:
            pass

class RColorDelegate(QStyledItemDelegate):
    """颜色块代理 - 显示和选择颜色"""
    _editor_count = 0
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def paint(self, painter, option, index):
        """绘制颜色块"""
        painter.save()
        
        # 获取颜色值（支持多种格式）
        value:Any = index.data(Qt.ItemDataRole.DisplayRole)
        color:QColor = self._parse_color(value)
        
        # 绘制选中背景
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        else:
            # 从模型获取背景色
            bg_color = index.data(Qt.ItemDataRole.BackgroundRole)
            if bg_color:
                painter.fillRect(option.rect, bg_color)
            else:
                painter.fillRect(option.rect, option.palette.base())
        
        # 计算颜色块区域（左侧）
        color_block_size = min(option.rect.height() - 6, 30)  # 颜色块大小
        color_block_x = option.rect.x() + 5
        color_block_y = option.rect.y() + (option.rect.height() - color_block_size) // 2
        color_block_rect = QRect(color_block_x, color_block_y, color_block_size, color_block_size)
        
        # 绘制颜色块
        painter.fillRect(color_block_rect, color)
        
        # 绘制颜色块边框
        from PySide6.QtGui import QPen
        pen = QPen(QColor(120, 120, 120), 1)
        painter.setPen(pen)
        painter.drawRect(color_block_rect)
        
        # 绘制颜色值文本（颜色块右侧）
        text_rect = option.rect.adjusted(color_block_size + 10, 0, -5, 0)
        if option.state & QStyle.StateFlag.State_Selected:
            painter.setPen(option.palette.highlightedText().color())
        else:
            painter.setPen(option.palette.text().color())
        
        # 显示颜色值（RGB或十六进制）
        if value:
            display_text = str(value)
        else:
            display_text = color.name()  # 显示十六进制值
        
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, display_text)
        
        painter.restore()
    
    def _parse_color(self, value)->QColor:
        """解析颜色值，支持多种格式"""
        if not value:
            return QColor(255, 255, 255)  # 默认白色
        
        value_str = str(value).strip()
        
        # 尝试解析 #RRGGBB 格式
        if value_str.startswith('#'):
            color = QColor(value_str)
            if color.isValid():
                return color
        
        # 尝试解析 R,G,B 格式
        if ',' in value_str:
            try:
                parts = [int(p.strip()) for p in value_str.split(',')]
                if len(parts) == 3:
                    return QColor(parts[0], parts[1], parts[2])
            except ValueError:
                pass
        
        # 尝试解析颜色名称
        color = QColor(value_str)
        if color.isValid():
            return color
        
        return QColor(255, 255, 255)  # 默认白色
    
    def editorEvent(self, event:QEvent, model:QAbstractItemModel, option:QStyleOptionViewItem, index:QModelIndex)->bool:
        """处理点击事件，打开颜色选择器"""
        if event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                # 获取当前颜色
                value = index.data(Qt.ItemDataRole.EditRole)
                current_color = self._parse_color(value)
                
                # 打开颜色选择对话框
                color = QColorDialog.getColor(current_color, option.widget, "选择颜色")
                
                if color.isValid():
                    # 保存为 #RRGGBB 格式
                    color_value = color.name()
                    model.setData(index, color_value, Qt.ItemDataRole.EditRole)
                
                return True
        
        return super().editorEvent(event, model, option, index)


class DelegateFactory:
    """
    Delegate工厂类 - 用于创建和管理各种类型的Delegate
    
    使用示例:
        factory = DelegateFactory()
        
        # 创建单个delegate
        category_delegate = factory.create(DelegateType.COMBOBOX, options=['文学', '历史', '哲学'])
        date_delegate = factory.create(DelegateType.DATE)
        
        # 批量创建delegates
        delegates = factory.create_batch({
            'category': (DelegateType.COMBOBOX, {'options': ['文学', '历史']}),
            'date': (DelegateType.DATE, {}),
            'borrowed': (DelegateType.CHECKBOX, {})
        })
    """
    
    def __init__(self):
        """初始化工厂，注册所有Delegate类型"""
        self._delegate_registry: Dict[DelegateType, type] = {
            DelegateType.DATE: RDateDelegate,
            DelegateType.COLOR: RColorDelegate,
            DelegateType.COMBOBOX: RComboBoxDelegate,
            DelegateType.CHECKBOX: RCheckBoxDelegate,
            DelegateType.LINEEDIT: RLineEditDelegate,
        }
    
    def create(self, 
               delegate_type: DelegateType, 
               parent: Optional[Any] = None,
               **kwargs) -> QStyledItemDelegate:
        """
        创建指定类型的Delegate实例
        
        参数:
            delegate_type: Delegate类型（DelegateType枚举）
            parent: 父对象（可选）
            **kwargs: 传递给Delegate构造函数的额外参数
                - COMBOBOX需要: options (list)
                - 其他类型: 无需额外参数
        
        返回:
            创建的Delegate实例
        
        异常:
            ValueError: 如果delegate_type未注册或参数不正确
        
        示例:
            factory.create(DelegateType.COMBOBOX, options=['选项1', '选项2'])
            factory.create(DelegateType.DATE, parent=self)
        """
        if delegate_type not in self._delegate_registry:
            raise ValueError(f"未注册的Delegate类型: {delegate_type}")
        
        delegate_class = self._delegate_registry[delegate_type]
        
        # 根据不同类型创建delegate，传递相应参数
        try:
            if delegate_type == DelegateType.COMBOBOX:
                # ComboBox需要options参数
                if 'options' not in kwargs:
                    raise ValueError("RComboBoxDelegate需要'options'参数")
                return delegate_class(options=kwargs['options'], parent=parent)
            
            else:
                # 其他类型只需要parent
                return delegate_class(parent=parent)
        
        except TypeError as e:
            raise ValueError(f"创建{delegate_type}失败: {str(e)}")
    
    def create_batch(self, 
                     config: Dict[str, tuple],
                     parent: Optional[Any] = None) -> Dict[str, QStyledItemDelegate]:
        """
        批量创建多个Delegate
        
        参数:
            config: 配置字典，格式:
                {
                    'column_name': (DelegateType, kwargs_dict),
                    ...
                }
            parent: 所有delegate的父对象
        
        返回:
            Dict[str, QStyledItemDelegate]: 列名到delegate的映射
        
        示例:
            delegates = factory.create_batch({
                'category': (DelegateType.COMBOBOX, {'options': ['文学', '历史']}),
                'publish_date': (DelegateType.DATE, {}),
                'borrowed': (DelegateType.CHECKBOX, {}),
                'color': (DelegateType.COLOR, {})
            })
        """
        result = {}
        
        for column_name, (delegate_type, kwargs) in config.items():
            result[column_name] = self.create(delegate_type, parent=parent, **kwargs)
        
        return result