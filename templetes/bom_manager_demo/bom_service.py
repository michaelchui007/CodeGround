from bom_model import BomRow

class BomService:
    @staticmethod
    def parse_json_to_rows(json_data):
        """将原始嵌套JSON转换为扁平化的BomRow列表"""
        final_rows = []
        for cpn, info in json_data.items():
            item_no = info.get('item', '')
            rd_list = info.get('rd', [])
            qty = len(rd_list)
            rd_str = ", ".join(rd_list)
            mps = info.get('mp', [])

            if not mps:
                final_rows.append(BomRow(item_no, cpn, qty, rd_str, "", "", True))
                continue

            for i, mp in enumerate(mps):
                final_rows.append(BomRow(
                    item_no, cpn, qty, rd_str,
                    mp.get('vendor', ''), mp.get('mpn', ''),
                    is_first=(i == 0)
                ))
        return final_rows