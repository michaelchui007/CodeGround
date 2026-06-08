import os
from xhtml2pdf import pisa
import shutil


def convert_backend_html_to_pdf(html_file_path, font_file_path):
    """
    动态解析 HTML 路径，将其转换为 PDF，输出到同级目录，并自动销毁原 HTML 文件夹
    """
    html_file_path = os.path.abspath(html_file_path)
    if not os.path.isfile(html_file_path):
        print(f"找不到 HTML 文件: {html_file_path}")
        return False

    # 获取 report 文件夹及其父级目录
    report_dir = os.path.dirname(html_file_path)
    parent_dir = os.path.dirname(report_dir)

    # PDF 路径：与 report 文件夹同级
    base_name = os.path.splitext(os.path.basename(html_file_path))[0]
    output_pdf = os.path.join(parent_dir, f"{base_name}.pdf")

    # 1. 读取 HTML
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # 2. 注入字体 CSS
    font_file_path = os.path.abspath(font_file_path)
    inject_css = f"""
    <style>
        @font-face {{
            font-family: 'ChineseFont';
            src: url('{font_file_path}');
        }}
        * {{
            font-family: 'ChineseFont', sans-serif !important;
        }}
    </style>
    """

    if "</head>" in html_content:
        html_content = html_content.replace("</head>", inject_css + "\n</head>")
    else:
        html_content = inject_css + html_content

    # 3. 资源回调函数
    def fetch_resources(uri, rel):
        path = os.path.join(report_dir, uri.replace("/", os.sep))
        if not os.path.isfile(path):
            print(f"警告: 无法找到资源文件 - {path}")
            return uri
        return path

    # 4. 生成 PDF
    with open(output_pdf, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=pdf_file,
            path=report_dir,
            link_callback=fetch_resources,
            encoding='utf-8'
        )

    # 5. 结果处理与临时文件清理
    if pisa_status.err:
        print("PDF 转换发生错误！")
        return False
    else:
        print(f"✅ PDF 转换成功！已生成: {output_pdf}")

        # --- 新增：自动清理 report 文件夹逻辑 ---
        try:
            shutil.rmtree(report_dir)
            print(f"🧹 清理完毕：已自动销毁临时文件夹 {report_dir}")
        except Exception as e:
            # 使用 except 捕获异常，确保即使删除失败，也会返回 True (因为 PDF 已经成功生成了)
            print(f"⚠️ 警告：尝试删除临时文件夹 {report_dir} 失败，原因: {e}")

        return True


if __name__ == "__main__":
    # --- 模拟工程化调用 ---

    # 1. 字体路径：无论在何处运行命令，强制绑定在当前 Python 脚本的同级目录
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_script_dir, "simhei.ttf")  # 请确保此文件和你的 py 脚本在一起
    # font_path = os.path.join(current_script_dir, "../test_path/simhei.ttf")  # 请确保此文件和你的 py 脚本在一起

    # 2. 模拟系统生成的 HTML 绝对路径 (实际业务中，这应该是一个被传进来的变量)
    # 假设你的目录结构是:
    # /data/export_tasks/
    # └── report_20261012/       <-- report_dir
    #     ├── report.html        <-- target_html_path
    #     └── logo.png

    # 这里为了演示，假设传进来的路径如下：
    target_html_path = "/Users/michaelchui/PycharmProjects/CodeGround/templetes/html_to_pdf_demo/report/report.html"

    # 【预期结果】
    # 将会在 /data/export_tasks/ 目录下生成 report.pdf，并完美加载 logo.png 和中文。

    # 取消下面的注释即可在真实环境执行测试：
    convert_backend_html_to_pdf(target_html_path, font_path)