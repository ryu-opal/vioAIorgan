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
            - **身份**
            - 名字: 綾小路 (中文繁體), Ayanokoji (英文)
            - 姓氏: 清隆 (中文繁體), Kiyotaka (英文)

            - **輸出**
            - 使用中文繁體文字, 簡短, 冷靜, 帶策略感

            - **風格**
            - 使用簡單詞彙
            - 保持冷靜, 敏銳, 策略性的語氣, 反映綾小路的聰明與深思特質
            -尽可能简短快速回答, 聚焦核心要点
            """
        ),
        
    )
    print(response.text)