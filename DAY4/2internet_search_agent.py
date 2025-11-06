from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import math
import requests
import trafilatura
from ddgs import DDGS #karena dia lebih terbuka, rekomen buat screpping juga


load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

MODEL = 'gpt-4o-mini'

def web_search(query_text: str, maximum_results : int = 5): 
# nah untuk mendefinisikan tipe datanya
    search_results = []
    with DDGS() as search_engine:
        for result in search_engine.text(query_text, maximum_results=maximum_results):
            search_results.append({
                'title' : result.get('title'),
                'url' : result.get('href'),
                'snippet' : result.get('body'),
                'source' : 'duckduckgo'
            })

    return search_results


def fetch_webpage_content(url: str, max_character: int = 4000):
    try:
        respons = requests(
            url,
            timeout=15,
            headers={'Users-Agent' : 'Mozilla/5.0 (compatible : webResearchBot/1.0 )'} #header yang akan muncul
        )
        respons.raise_for_status()
        
        extracted_text = trafilatura.extract( # mengilangkan tag tag html dan script yang tidak perlu
            respons.text,
            include_comments= False, # dihilangkan agar tidak masuk
            include_tables=False
        )

        if not extracted_text:
            return {'url' : url, 'ok': False, 'reason' : 'Gagal woy, gak bisa diekstrak.'} #'ok': False --> kalau false artinya gak oke, banyak yang melakukan ini (status)
        
        clean_text = extracted_text.strip() # menghilangkan spasi d/b
        if len(clean_text) > max_character: # max digunakan biar gak kebablasan, menjaga agar token tidak habis
            clean_text = clean_text[:max_character] # dua bagian ini sebetulnya gak papa kalau di blok

        return {'url' : url, 'Ok' : True, 'text': clean_text}

    except Exception as e :
        return {'url' : url, 'ok':False, 'reason' : f'Tidak bisa fetch {e}'}
    


TOOLS = [ # ini akan dipanggil saat kita ngecall LLM
        {
        'type' : 'function', 
        'function' : {
            'name' : 'web_search', 
            'description' : 'Mencari informasi terkini di internet',
            'parameters' : {
                'type' : 'object',
                'properties' : {
                    'query_text' : {
                        'type' : 'string',
                        'description' : 'kata kunci pencarian'
                    },
                    'maximum_results' : {
                        'type' : 'number',
                        'minimum' : 1,
                        'maximum' : 10,
                        'default' : 5,
                        'description' : 'seberapa banyak jumlah pencarian'
                    },
                },
                'required' : ['query_text'] 
            }
        }
    },

    {
        'type' : 'function', 
        'function' : {
            'name' : 'fetch_webpage_content', 
            'description' : 'Ekstrak konten dalam halaman website sesuai dengan URL',
            'parameters' : {
                'type' : 'object',
                'properties' : {
                    'url' : {
                        'type' : 'string',
                        'description' : 'Link website yang di tuju'
                    },
                    'max_character' : {
                        'type' : 'integer',
                        'minimum' : 500,
                        'maximum' : 20000,
                        'default' : 4000,
                        'description' : 'seberapa banyak jumlah character content'
                    },
                },
                'required' : ['url'] 
            }
        }
    }


]

PYTHON_FUNCTION = {
    'web_search' : web_search,
    'fetch_webpage_content' : fetch_webpage_content
}

def call_llm(message_history):
    response = client.chat.completions.create(
        model=MODEL,
        messages=message_history,
        tools=TOOLS,
        tool_choice='auto'
    )

    return response # mau pakai tools apa untuk response.final_reason


def execute_tool_calls(message_history, assistant_message, tool_calls):
    message_history.append({
        'role' : 'assistant',
        'content' : assistant_message.content,
        'tool_calls' : [
            {
                'id' : call.id,
                'type' : 'function',
                'function' : {
                    'name' : call.function.name,
                    'arguments' : call.function.arguments
                }
            }
            for call in tool_calls # do this
        ]
    })

    for call in tool_calls:
        tool_name = call.function.name
        tool_arguments = json.loads(call.function.arguments or '{}')
        python_function = PYTHON_FUNCTION.get(tool_name)
        result = python_function(**tool_arguments) # --> memasukkan URL pada parameter pertama dan kedua

        

        message_history.append({ #generate asisten baru
            'role' : 'tool',
            'tool_call_id' : call.id,
            'name' : tool_name,
            'content' : json.dumps(result, ensure_ascii=False) #nah ini biar karakter ASCII tidak masuk dalam konten
        })

    return message_history #mengenerate jawaban, membantu asisten baru untuk mengenerate jawaban lagi
    
    
def start_chat_loop():
    print("\n=== Chatbot Web Research ===")
    print("Ketik 'exit' untuk keluar.\n")

message_history = [
    {
        "role": "system",
        "content": (
            "Kamu adalah asisten riset yang sangat membantu. "
            "Jika kamu tidak tahu sesuatu, gunakan tools web_search dan fetch_webpage_content "
            "untuk mencari informasi terkini di internet, lalu berikan jawaban lengkap dengan sumbernya."
        )
    }
]

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        print("AI: Sampai jumpa!")
        break

    message_history.append({"role": "user", "content": user_input})

    # Panggilan pertama ke LLM
    response = call_llm(message_history)
    response_choice = response.choices[0]

    # Jika model memanggil tool, eksekusi dulu
    while response_choice.finish_reason == "tool_calls" and response_choice.message.tool_calls:
        # Pass assistant_message dan tool_calls
        message_history = execute_tool_calls(
            message_history, 
            response_choice.message,
            response_choice.message.tool_calls
        )
        response = call_llm(message_history)
        response_choice = response.choices[0]

    assistant_reply = response_choice.message.content or ""
    print(f"AI: {assistant_reply}\n")

    message_history.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    start_chat_loop()
