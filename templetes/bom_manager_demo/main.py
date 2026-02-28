import sys
from PySide6.QtWidgets import QApplication
from bom_model import BomManagerModel
from bom_view import BomManagerView
from bom_service import BomService

def main():
    # 你的原始测试数据
    raw_json = {
        '004-020-101': {
            'desc': None,
            'item': 1,
            'refd_quantity': 5,
            'mp': [
                {'mpn': 'TQC-216C-6R', 'vendor': 'TOYOCOM'},
                {'mpn': 'VM6S-20.0000-16PF', 'vendor': 'VALPEY-FISHER'}
            ],
            'package': '',
            'rd': ['XTAL1']
        },
        '006-111-222': {
            'item': 2,
            'mp': [{'mpn': 'CAP-0603-104', 'vendor': 'SAMSUNG'}],
            'rd': ['C1', 'C2', 'C3', 'C4']
        }
    }

    app = QApplication(sys.argv)

    # 1. 通过 Service 转换数据
    processed_data = BomService.parse_json_to_rows(raw_json)

    # 2. 创建 Model
    model = BomManagerModel(processed_data)

    # 3. 注入 Model 到 View
    view = BomManagerView(model)
    view.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()