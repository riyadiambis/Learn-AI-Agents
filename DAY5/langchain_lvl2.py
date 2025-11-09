from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # biar bisa diganti oleh history
from langchain_core.chat_history import InMemoryChatMessageHistory # menyimpan percakapan saat ini
from langchain_core.runnables.history import RunnableWithMessageHistory


SYSTEM_PROMPT = 'kamun adalah chatbot yandg ditugaskan membantuku...'

prompt = ChatPromptTemplate([
    ('system', SYSTEM_PROMPT),
    MessagesPlaceholder('chat_history'),
    ('human', '{input}')
])

llm = ChatOpenAI(
    model='gpt-4o-mini',   
)

chain = prompt | llm # prompt --> llm

session_store = {}
def get_history(session_id):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

agent = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key='input',
    history_messages_key='chat_history'
)

#looping chat
session_id = 'demo-level-2'

while True:
    user_text = input("\nYou : ").strip()

    ai_message = agent.invoke({'input' : user_text}, config=
                                {'configurable': {'session_id' : session_id}})
    print(f'AI : {ai_message.content}')
