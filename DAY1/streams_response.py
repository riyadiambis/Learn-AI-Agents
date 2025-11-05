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
    ],
    stream=True, #default --> False

)

full_response = '' #Menyimpan full respons

# chunk.choices[0].delta.content
for kata in respons:
    if kata.choices[0].delta.content is not None:
        content = kata.choices[0].delta.content
        print(content, end='', flush=True) #flush ini menghindari output perparagraf
        full_response += content

