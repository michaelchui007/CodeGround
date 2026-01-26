import struct

def analyze_bom_head(filepath):
    print(f"正在分析文件: {filepath}")
    with open(filepath, 'rb') as f:
        # 读取前 128 字节
        header_bytes = f.read(128)

    print("-" * 60)
    print("【Hex Dump (前128字节)】")
    # 打印十六进制，方便看有没有规律的 00 00 分隔符
    hex_str = " ".join(f"{b:02X}" for b in header_bytes)
    print(hex_str)

    print("\n【ASCII 预览】")
    # 尝试转成文本，不可见字符显示为 .
    text_preview = "".join(chr(b) if 32 <= b <= 126 else '.' for b in header_bytes)
    print(text_preview)
    print("-" * 60)

if __name__ == '__main__':

    # 请把文件名换成您真实的文件路径
    analyze_bom_head("C:\\NPI\\Bom\\demo_cad+bom\\steps\\rev_a\\boms\\bom\\bom")
    file_path = r"C:\NPI\Bom\demo_cad+bom\steps\rev_a\boms\bom\bom"