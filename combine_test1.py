import requests
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
    ai_output = response.text
    print(response.text)

    url = "http://127.0.0.1:9880"
    data = {
        "text": ai_output, 
        "text_language": "zh",                  
        "gpt_model_path": "C:\\Users\\ryu21\\Downloads\\GPT-SoVITS-v3lora-20250228\\GPT_weights_v3\\violetvoice-e15.ckpt",
        "sovits_model_path": "C:\\Users\\ryu21\\Downloads\\GPT-SoVITS-v3lora-20250228\\SoVITS_weights_v3\\violetvoice_e2_s192_l32.pth",
        "refer_wav_path": "C:\\Users\\ryu21\\Downloads\\LANDrop\\3output_denoise\\vocal_qy3t56.mp3.reformatted.wav_10.wav_0001156480_0001335680.wav",
        "prompt_text": "我只是灵魂的抄写员，将他们的故事编织进时间的永恒之舞。",
        "prompt_language": "zh",
        "voice_style": "emotional"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        with open("output.wav", "wb") as f:
            f.write(response.content)
        print("save as output.wav")
    else:
        print("API fail status code:", response.status_code, "error message:", response.json())