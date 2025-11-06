from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

image_url = input('Masukkan URL gambar : ')
bahasan = input('Masukkan apa yang ingin anda tanyakan soal gambar ini : ')

respons = client.chat.completions.create (
    model='gpt-4'
    messages=[
        {'role' : 'user', 'content' : [
            {'type' : 'text', 'text' : bahasan },
            {'type' : 'image_url', 'image_url' : {'url' : image_url}}
        ]}
    ]
)


