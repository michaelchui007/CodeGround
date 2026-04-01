import uuid
import pyperclip

if __name__ == '__main__':
    new_uuid = str(uuid.uuid4())
    pyperclip.copy(new_uuid)  # 写入剪贴板
    # 可选：验证读取（确认是否写入成功）
    copied_uuid = pyperclip.paste()
    print(f"生成的 UUID：\n{new_uuid}")
    print(f"剪贴板内容：{copied_uuid}")
    print("✅ UUID 已成功写入剪贴板！")