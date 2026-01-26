import sys
from PySide6.QtCore import (Qt, QAbstractTableModel, QModelIndex,
                            QThread, Signal)
from PySide6.QtWidgets import (QApplication, QTableView, QMainWindow,
                               QHeaderView)

# ==========================================
# 1. 数据对象：聚合后的 BOM 行
# ==========================================
class BomItem:
    # 显式定义内存槽
    __slots__ = ('cpn', 'item_no', 'refs', 'pkg', 'qty_check')

    def __init__(self, cpn):
        self.cpn = cpn
        self.item_no = ""      # 存 ITEM 编号
        self.refs = set()      # 使用 set 自动去重，防止重复添加
        self.pkg = ""          # 封装
        self.qty_check = 0.0   # 存尾部读取到的 QNT，用于校验

    @property
    def qty(self):
        # 数量 = 位号列表的长度
        return len(self.refs)

    @property
    def ref_string(self):
        # 将集合转为有序字符串 "C1, C2, C3"
        if not self.refs: return ""
        try:
            # 尝试智能排序：先按字母，再按数字 (C2 < C10)
            # 这里做一个简单的处理，如果需要复杂的自然排序可以再优化
            sorted_list = sorted(list(self.refs))
        except:
            sorted_list = list(self.refs)
        return ", ".join(sorted_list)

# ==========================================
# 2. Model：表格显示逻辑
# ==========================================
class AggregatedBomModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 这是你要的理想列顺序
        self._headers = ["Item", "Part Number (CPN)", "Qty", "Reference Designator", "Package"]
        self._data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid(): return None
        item = self._data[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0: return item.item_no
            elif col == 1: return item.cpn
            elif col == 2: return str(item.qty)      # 计算出的数量
            elif col == 3: return item.ref_string    # 合并后的位号字符串
            elif col == 4: return item.pkg

        # 调试辅助：如果 REF 数量和文件尾部 QNT 不一致，标红显示
        elif role == Qt.ForegroundRole:
            if item.qty_check > 0 and item.qty != int(item.qty_check):
                return Qt.red # 数量对不上，标红警告

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

# ==========================================
# 3. 解析器：流式聚合逻辑 (关键修改)
# ==========================================
class BomLoader(QThread):
    loaded = Signal(list)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        # 核心字典：Key=CPN, Value=BomItem对象
        # 无论在文件哪里读到这个CPN，都指向同一个对象
        bom_map = {}

        # 状态变量
        pending_ref = None   # 暂存刚刚读到的 REF
        last_seen_cpn = None # 暂存刚刚读到的 CPN (用于后续读 ITEM/QNT)

        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): continue

                    # 简单的分词
                    parts = line.split(maxsplit=1)
                    key = parts[0]
                    value = parts[1] if len(parts) > 1 else ""

                    # --- 逻辑分支 ---

                    if key == "REF":
                        # 场景 A：头部区域，读到了 REF
                        pending_ref = value
                        # 注意：读到 REF 时我们还不知道它属于哪个 CPN，
                        # 所以先存到 pending_ref，等下一行读到 CPN 时再处理

                    elif key == "CPN":
                        # 场景 B：读到了 CPN (无论头部还是尾部)
                        cpn = value
                        last_seen_cpn = cpn # 记录下来，因为后面可能有 ITEM/QNT

                        # 1. 确保这个 CPN 在字典里存在
                        if cpn not in bom_map:
                            bom_map[cpn] = BomItem(cpn)

                        # 2. 检查是否有待归档的 REF (这就是头部聚合的关键！)
                        if pending_ref:
                            bom_map[cpn].refs.add(pending_ref)
                            pending_ref = None # 归档完毕，清空

                    elif key == "ITEM":
                        # 场景 C：尾部区域，读到了 ITEM
                        # 这属于最近一次见到的 CPN
                        if last_seen_cpn and last_seen_cpn in bom_map:
                            bom_map[last_seen_cpn].item_no = value

                    elif key == "QNT":
                        # 场景 D：尾部区域，读到了 QNT
                        if last_seen_cpn and last_seen_cpn in bom_map:
                            try:
                                bom_map[last_seen_cpn].qty_check = float(value)
                            except:
                                pass

                    elif key == "PKG":
                        if last_seen_cpn and last_seen_cpn in bom_map:
                            bom_map[last_seen_cpn].pkg = value

        except Exception as e:
            print(f"解析错误: {e}")

        # 将字典转为列表
        # 过滤掉那些没有 Item 号且没有 Ref 的空数据 (可选)
        final_list = [item for item in bom_map.values() if item.qty > 0 or item.item_no]

        # 排序：按 Item 号排序，如果没有 Item 号则按 CPN 排序
        final_list.sort(key=lambda x: (int(x.item_no) if x.item_no.isdigit() else 999999, x.cpn))

        self.loaded.emit(final_list)

# ==========================================
# 4. 主窗口
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 700)
        self.setWindowTitle("BOM Consolidated View")

        self.table = QTableView()
        self.setCentralWidget(self.table)

        # 样式与性能设置
        v_header = self.table.verticalHeader()
        v_header.setDefaultSectionSize(30)
        v_header.setSectionResizeMode(QHeaderView.Fixed)

        # 开启排序功能
        self.table.setSortingEnabled(True)

        self.model = AggregatedBomModel()
        self.table.setModel(self.model)

        # 设置列宽，让 Reference 那一列宽一点
        self.table.setColumnWidth(0, 50)  # Item
        self.table.setColumnWidth(1, 150) # CPN
        self.table.setColumnWidth(2, 50)  # Qty
        self.table.setColumnWidth(3, 500) # Refs (最重要的一列)

        # 加载文件 (请修改为您的真实路径)
        #
        file_path = r"C:\NPI\Bom\demo_cad+bom\steps\rev_a\boms\bom\bom"
        self.loader = BomLoader(file_path)
        self.loader.loaded.connect(self.model.update_data)
        self.loader.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

    data = {
        {},
        {},
        {}
    }