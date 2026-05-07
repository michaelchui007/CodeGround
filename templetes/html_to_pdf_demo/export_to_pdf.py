import os
from xhtml2pdf import pisa

def convert_html_to_pdf(source_html, output_pdf):
    # 确保文件存在
    if not os.path.isfile(source_html):
        print(f"找不到 HTML 文件: {source_html}")
        return False
        
    # 读取 HTML 内容
    with open(source_html, "r", encoding="utf-8") as file:
        html_content = file.read()

    # 打开要写入的 PDF 文件
    with open(output_pdf, "wb") as pdf_file:
        # dest 是目标文件对象
        # path 参数非常关键！它告诉 xhtml2pdf 当前 HTML 的基础路径，
        # 这样它才能正确找到相对路径引用的图片(如 src="logo.png")
        base_dir = os.path.dirname(os.path.abspath(source_html))
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=pdf_file,
            path=base_dir,
            encoding='utf-8'
        )

    # pisa_status.err 返回 1 代表有错误，0 代表成功
    if pisa_status.err:
        print("PDF 转换失败！")
        return False
    else:
        print(f"PDF 转换成功！保存在: {output_pdf}")
        return True

if __name__ == "__main__":
    html_file = os.path.join("report", "report.html")
    pdf_file = os.path.join("report", "report_exported.pdf")
    convert_html_to_pdf(html_file, pdf_file)
