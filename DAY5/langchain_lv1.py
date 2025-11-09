from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
# Perlu system prompt
from langchain_core.prompts import ChatPromptTemplate

# messages = []
# chain = history message(chatprompt)  --> llm(chatopenai) --> output


SYSTEM_PROMPT = 'kamun adalah chatbot yandg ditugaskan membantuku...'

prompt = ChatPromptTemplate([
    ('system', SYSTEM_PROMPT), # sebelumnya kita perlu role, content
    ('human', '{input}')
])

llm = ChatOpenAI(
    model='gpt-4o-mini',   
)

chain = prompt | llm # prompt --> llm, penghubung


#chat loop
while True:
    user_text = input("\nYou : ").strip()

    ai_message = chain.invoke({'input' : user_text})
    print(f'AI : {ai_message.content}')
