import csv
import time

from typing import Dict
from PySide6.QtCore import QAbstractTableModel,QModelIndex,Qt
from PySide6.QtGui import QStandardItemModel,QStandardItem,QColor

class RTreeModel(QStandardItemModel):
    """图书树形模型 - 支持分类→作者→书名三级折叠"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._raw_data = []  # 原始数据
        self._headers = []
        self._total_count = 0  # CSV文件总行数
        self._loaded_count = 0  # 已加载行数
        self._category_nodes = {}  # 缓存分类节点
        self._author_nodes = {}    # 缓存作者节点
        
    def load_csv_to_tree(self, filepath, max_rows=None):
        """加载CSV文件并构建树形结构"""
        start_time = time.time()
        
        try:
            # 读取CSV数据
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                total_line = next(reader)  # 第一行是总行数
                self._total_count = int(total_line[0])
                self._headers = next(reader)  # 第二行是表头
                
                # 读取数据
                if max_rows == -1:
                    self._raw_data = [row for row in reader]
                elif max_rows:
                    self._raw_data = []
                    for i, row in enumerate(reader):
                        if i >= max_rows:
                            break
                        self._raw_data.append(row)
                else:
                    self._raw_data = [row for row in reader]
            
            self._loaded_count = len(self._raw_data)
            
            # 设置表头
            self.setHorizontalHeaderLabels(self._headers)
            
            # 构建树形结构
            self._build_tree_structure()
            
            elapsed_time = time.time() - start_time
            load_type = f"分批加载({max_rows}行)" if max_rows else "全量加载"
            message = f"成功加载 {len(self._raw_data)} 行数据 | {load_type} | 耗时: {elapsed_time:.3f}秒"
            
            print(f"[TreePerformance] {message}")
            return True, message
        except Exception as e:
            elapsed_time = time.time() - start_time
            return False, f"加载失败: {str(e)} | 耗时: {elapsed_time:.3f}秒"
    
    def _build_tree_structure(self):
        """构建树形结构：分类→作者→书名"""
        self.clear()
        self.setHorizontalHeaderLabels(self._headers)
        
        # 重置节点缓存
        self._category_nodes = {}
        self._author_nodes = {}
        
        # 获取category, author, title的列索引
        category_idx = self._headers.index('category') if 'category' in self._headers else 0
        author_idx = self._headers.index('author') if 'author' in self._headers else 1
        title_idx = self._headers.index('title') if 'title' in self._headers else 2
        
        # 按分类、作者、书名排序
        sorted_data = sorted(self._raw_data, key=lambda x: (x[category_idx], x[author_idx], x[title_idx]))
        
        for row_data in sorted_data:
            self._add_book_to_tree(row_data, category_idx, author_idx, title_idx)
        
        print(f"[树结构] 分类: {len(self._category_nodes)}, 作者: {len(self._author_nodes)}, 图书: {len(sorted_data)}")
    
    def _add_book_to_tree(self, row_data, category_idx, author_idx, title_idx):
        """将单本书添加到树形结构（支持增量添加）"""
        category = row_data[category_idx]
        author = row_data[author_idx]
        title = row_data[title_idx]
        
        # 1. 创建或获取分类节点
        if category not in self._category_nodes:
            category_item = QStandardItem(f"📚 {category}")
            category_item.setEditable(False)
            self._category_nodes[category] = category_item
            self.appendRow(category_item)
        
        category_node = self._category_nodes[category]
        
        # 2. 创建或获取作者节点
        author_key = (category, author)
        if author_key not in self._author_nodes:
            author_item = QStandardItem(f"✍️ {author}")
            author_item.setEditable(False)
            self._author_nodes[author_key] = author_item
            category_node.appendRow(author_item)
        
        author_node = self._author_nodes[author_key]
        
        # 3. 创建书籍节点（完整数据行）
        book_items = []
        for col_idx, cell_value in enumerate(row_data):
            item = QStandardItem(str(cell_value))
            
            # 设置可编辑列
            editable_columns = ['category', 'author', 'title', 'publisher', 'status', 'notes']
            col_name = self._headers[col_idx] if col_idx < len(self._headers) else ''
            if col_name in editable_columns:
                item.setEditable(True)
            else:
                item.setEditable(False)
            
            # 设置背景色
            if col_name == 'status':
                if cell_value == '借出':
                    item.setBackground(QColor(255, 230, 230))
                elif cell_value == '在架':
                    item.setBackground(QColor(230, 255, 230))
                elif cell_value == '维修':
                    item.setBackground(QColor(255, 245, 200))
                elif cell_value == '下架':
                    item.setBackground(QColor(220, 220, 220))
            
            book_items.append(item)
        
        author_node.appendRow(book_items)
    
    def append_more_data(self, filepath, batch_size=1000):
        """追加加载更多数据（懒加载）"""
        if self._loaded_count >= self._total_count - 2:
            return 0, "所有数据已加载完成"
        
        start_time = time.time()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 跳过总行数
                next(reader)  # 跳过表头
                
                # 跳过已加载的数据
                for _ in range(self._loaded_count):
                    next(reader)
                
                # 获取列索引
                category_idx = self._headers.index('category') if 'category' in self._headers else 0
                author_idx = self._headers.index('author') if 'author' in self._headers else 1
                title_idx = self._headers.index('title') if 'title' in self._headers else 2
                
                # 读取新批次数据
                new_rows = []
                for i, row in enumerate(reader):
                    if i >= batch_size:
                        break
                    new_rows.append(row)
                    self._raw_data.append(row)
                
                # 按分类、作者排序后增量添加到树中
                sorted_new_rows = sorted(new_rows, key=lambda x: (x[category_idx], x[author_idx], x[title_idx]))
                
                for row_data in sorted_new_rows:
                    self._add_book_to_tree(row_data, category_idx, author_idx, title_idx)
                
                self._loaded_count += len(new_rows)
                
                elapsed_time = time.time() - start_time
                message = f"追加加载 {len(new_rows)} 行 | 总计: {self._loaded_count}/{self._total_count-2} | 耗时: {elapsed_time:.3f}秒"
                print(f"[TreePerformance] {message}")
                
                return len(new_rows), message
        except Exception as e:
            return 0, f"追加加载失败: {str(e)}"
    
    def get_headers(self):
        """获取表头"""
        return self._headers
    
    def get_raw_data(self):
        """获取原始数据"""
        return self._raw_data
    
    def get_load_progress(self):
        """获取加载进度"""
        total = self._total_count - 2 if self._total_count > 2 else 0
        return {
            'loaded': self._loaded_count,
            'total': total,
            'remaining': max(0, total - self._loaded_count)
        }


class RTableModel(QAbstractTableModel):
    """图书数据模型 - 支持大数据量和树形排序"""
    
    def __init__(self, data=None, headers=None, parent=None):
        super().__init__(parent)
        self._total_count : int = 0
        self._data = data or []
        self._headers = headers or []
        self._headers_col = Dict[str,int]
        self._filtered_indices = None
        self._use_filter = False
        self._render_count = 0
        self._rendered_rows = set()
    
    def _get_header(self, col):
        return self._headers[col] if col < len(self._headers) else ''
    
    def rowCount(self, parent=QModelIndex()):
        if self._use_filter and self._filtered_indices is not None:
            return len(self._filtered_indices)
        return len(self._data)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self._headers) if self._headers else 0
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        
        actual_row = self._get_actual_row(row)
        if actual_row >= len(self._data):
            return None
        
        # 渲染统计
        if col == 0:
            self._rendered_rows.add(actual_row)
            self._render_count += 1
        
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self._data[actual_row][col]
        
        if role == Qt.ItemDataRole.BackgroundRole: 
            if self._headers_col['color'] == col:
                return QColor(255, 255, 255)
            colors = self._data[actual_row][self._headers_col['color']]
            return QColor(colors)
            notes = self._data[actual_row][self._headers_col['notes']]
            colors = {
                ''    : QColor(255, 255, 255), 
                '热门': QColor(255, 10, 20), 
                '新书': QColor(240, 125, 20), 
                '推荐': QColor(240, 255, 20), 
                '畅销': QColor(255, 250, 120),  
                '经典': QColor(245, 245, 180),  
                '珍藏版': QColor(255, 150, 230)  
            }
            return colors.get(notes, QColor(255, 255, 255))
        
        
        return None
    
    def _get_actual_row(self, display_row):
        """获取实际行索引"""
        if self._use_filter and self._filtered_indices is not None:
            if display_row < len(self._filtered_indices):
                return self._filtered_indices[display_row]
            return len(self._data)
        return display_row
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """设置数据"""
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            col = index.column()
            actual_row = self._get_actual_row(row)
            if actual_row < len(self._data):
                self._data[actual_row][col] = value
                print("setData============")
                self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
                return True
        return False
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section] if section < len(self._headers) else ''
            else:
                return str(section + 1)
        return None
    
    def flags(self, index):
        """设置可编辑列"""
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        
        col = index.column()
        col_name = self._headers[col] if col < len(self._headers) else ''
        
        # 可编辑列：category, author, title, publisher, status, notes, borrowed, publish_date
        editable_columns = ['category', 'author', 'title', 'publisher', 'status', 'notes', 'borrowed', 'publish_date']
        #editable_columns = []
        if col_name in editable_columns:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable
        
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
    
    def load_csv(self, filepath, load_rows=None):
        """加载CSV文件"""
        start_time = time.time()
        
        try:
            self.beginResetModel()
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # 第一行是总行数
                total_line = next(reader)
                self._total_count = int(total_line[0])
                print(f"文件声明总行数: {total_line[0]}")
                
                # 第二行是表头
                self._headers = next(reader)
                self._headers_col = {h: i for i, h in enumerate(self._headers)}
                # 读取数据
                if load_rows:
                    self._data = []
                    for i, row in enumerate(reader):
                        if i >= load_rows:
                            break
                        self._data.append(row)
                else:
                    self._data = [row for row in reader]
            
            self._use_filter = False
            self._filtered_indices = None
            self.endResetModel()
            
            elapsed_time = time.time() - start_time
            load_type = f"分批加载({load_rows}行)" if load_rows else "全量加载"
            message = f"成功加载 {len(self._data)} 行数据 | {load_type} | 耗时: {elapsed_time:.3f}秒"
            
            print(f"[Performance] {message}")
            return True, message
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.endResetModel()
            return False, f"加载失败: {str(e)} | 耗时: {elapsed_time:.3f}秒"
    
    def filter_data(self, search_text):
        """搜索过滤"""
        if not search_text:
            self._use_filter = False
            self._filtered_indices = None
            self.layoutChanged.emit()
            return
        
        search_lower = search_text.lower()
        self._filtered_indices = []
        
        for i, row in enumerate(self._data):
            for cell in row:
                if search_lower in str(cell).lower():
                    self._filtered_indices.append(i)
                    break
        
        self._use_filter = True
        self.layoutChanged.emit()
    
    def get_headers(self):
        """获取表头"""
        return self._headers
    
    def get_data(self):
        """获取所有数据"""
        return self._data
    
    def get_filtered_row_count(self):
        """获取过滤后的行数"""
        if self._use_filter and self._filtered_indices:
            return len(self._filtered_indices)
        return len(self._data)
    
    def reset_render_stats(self):
        """重置渲染统计"""
        self._render_count = 0
        self._rendered_rows.clear()
    
    def get_render_stats(self):
        """获取渲染统计"""
        return {
            'total_rows': len(self._data),
            'unique_rows_rendered': len(self._rendered_rows),
            'total_data_calls': self._render_count
        }

    def append_rows(self, new_rows):
        """追加新行数据"""
        if not new_rows:
            return 0
        
        start_row = len(self._data)
        end_row = start_row + len(new_rows) - 1
        
        self.beginInsertRows(QModelIndex(), start_row, end_row)
        self._data.extend(new_rows)
        self.endInsertRows()  # 修复：添加括号
        
        return len(new_rows)