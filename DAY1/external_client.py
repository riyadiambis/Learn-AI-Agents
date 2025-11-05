from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url= 'https://openrouter.ai/api/v1',
    api_key=os.getenv('OPENROUTER_API_KEY')
)#nah kedua bagian ini akan diganti sesuai dengan model yang mau kita gunakan

#client.chat.completions.create()  --> selalu digunakan dari awal sampai akhir untuk LLM

respons = client.chat.completions.create(
    model= 'x-ai/grok-4-fast',   # ini juga jangan lupa disesuaikan 
    messages = [
        {'role':'system', 'content':'You are a helpful assistant'},
        {'role':'user', 'content':'Jelaskan kenapa saya kenapa sih Wibu itu keren'}
    ]
)

print(respons.choices[0].message.content) 