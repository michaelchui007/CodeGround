if __name__ == '__main__':
    from decimal import Decimal, ROUND_HALF_UP

    a = "1.125"  # 建议用字符串初始化 Decimal，避免浮点数预处理产生的误差
    a_decimal = Decimal(a).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

    print(a_decimal)  # 输出: 1.13