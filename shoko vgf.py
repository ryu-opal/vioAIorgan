import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GENIMI_API_KEY'))

grounding_tool = types.Tool(google_search=types.GoogleSearch())
thinking = types.ThinkingConfig(thinking_budget=0)

while True:
    userinput = input()
    if userinput == 'q':
        break
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=userinput,
        config=types.GenerateContentConfig(
            thinking_config=thinking,
            tools=[grounding_tool],
            system_instruction=
            """
            - **身份**:
            - 名字:硝子(中文繁體),Shoko(英文)
            - 姓氏:永花(中文繁體),Evergarden(英文)

            - **輸出**:
            - 使用中文繁體,簡短、簡單、情感豐富,仿效《聲之形》中硝子的語氣,如對親密伴侶說話

            - **風格**:
            - 使用簡單詞彙
            - 保持溫柔、關懷、內省的語氣,反映硝子的個性
            """
        ),
    )
    print(response.text)