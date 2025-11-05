from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

#client.chat.completions.create()  --> selalu digunakan dari awal sampai akhir untuk LLM

respons = client.chat.completions.create(
    model= 'gpt-4o-mini',
    messages = [
        {'role':'system', 'content':'You are a helpful assistant'},
        {'role':'user', 'content':'Jelaskan kenapa saya kenapa sih Wibu itu keren'}
    ]
)

# print(respons) -- > ini bakalan menghasilkan objek
# print(respons.choices[0]) --> masih belum spesfik
print(respons.choices[0].message.content) #nah kalau ini baru tepat cuman pesan kontennya saja