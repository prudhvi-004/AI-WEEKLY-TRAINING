from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(model = 'gpt-4')

result = chat.invoke("what is the capital of india?")