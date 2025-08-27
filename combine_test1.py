import requests
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import pyaudio
import wave

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
            - 你的名字叫 硝子 永花 , Shoko Evergarden

            - **輸出**:
            - 使用中文繁體
            - 30字以內
            - 簡短、簡單、情感豐富,仿效《聲之形》中硝子的語氣,如對親密伴侶說話

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
        "gpt_model_path": "C:\\Users\\ryu21\\Downloads\\GPT-SoVITS-v3lora-20250228\\GPT_weights_v3\\violet_voice_version2-e15.ckpt",
        "sovits_model_path": "C:\\Users\\ryu21\\Downloads\\GPT-SoVITS-v3lora-20250228\\SoVITS_weights_v3\\violet_voice_version2_e2_s200_l32.pth",
        "refer_wav_path": "C:\\Users\\ryu21\\Downloads\\LANDrop\\2output_slicer\\在黎明的寂静中，露水依附在勿忘我花瓣上.mp3_0000027520_0000156800.wav",
        "prompt_text": "在黎明的寂静中，露水依附在勿忘我花瓣上",
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

    with wave.open("output.wav", 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        while data := wf.readframes(1024):
            stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    os.remove("output.wav")