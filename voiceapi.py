import requests

url = "http://127.0.0.1:9880"
data = {
    "text": input("hihi"), 
    "text_language": "zh",                  
    "gpt_model_path": "C:\\Users\\ryu21\\Downloads\\GPT-SoVITS-v3lora-20250228\\GPT_weights_v3\\violetvoice-e15.ckpt",
    "sovits_model_path": "C:\\Users\\ryu21\\Downloads\\GPT-SoVITS-v3lora-20250228\\SoVITS_weights_v3\\violetvoice_e2_s192_l32.pth",
    "refer_wav_path": "C:\\Users\\ryu21\\Downloads\\LANDrop\\3output_denoise\\vocal_qy3t56.mp3.reformatted.wav_10.wav_0001156480_0001335680.wav",
    "prompt_text": "我只是灵魂的抄写员，将他们的故事编织进时间的永恒之舞。",
    "prompt_language": "zh"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("save as output.wav")
else:
    print("API fail status code:", response.status_code, "error message:", response.json())