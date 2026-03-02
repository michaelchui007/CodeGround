from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Optional, Any


class CoordConverter:
    # 定义全局显示精度，例如 PCB 常用的 6 位小数
    PRECISION = "0.000000"

    @staticmethod
    def to_decimal(str_val, default=Decimal("0.000000")):
        """将字符串安全转换为 Decimal"""
        try:
            # 去除空格并转换
            return Decimal(str(str_val).strip())
        except (InvalidOperation, ValueError, TypeError):
            return default

    @staticmethod
    def format_display(decimal_val: Optional[Decimal, str]) -> Any:
        """将 Decimal 格式化为指定位数的字符串（用于 UI 显示）"""
        if not isinstance(decimal_val, Decimal):
            decimal_val = CoordConverter.to_decimal(decimal_val)
        # QUANTIZE 用于执行四舍五入并固定小数位
        return decimal_val.quantize(Decimal(CoordConverter.PRECISION), rounding=ROUND_HALF_UP)

    @staticmethod
    def to_ui_string(x, y):
        """生成符合你 UI 按钮样式的字符串"""
        val_x = CoordConverter.format_display(x)
        val_y = CoordConverter.format_display(y)
        return f"Anchor :  X = {val_x}, Y = {val_y}"