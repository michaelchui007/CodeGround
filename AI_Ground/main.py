import os

from google import genai
from dotenv import load_dotenv


load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)

def test(aaa: str) -> None:
    """
    测试方法
    Args:
        aaa: 传入参数

    Returns:
        无

    """
    print(aaa)

if __name__ == '__main__':

    print(response.text)