from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-large",dimension=32)

docs = [
    'Delhi is the capital of India',
    'Hello Everyone',
    'Happy to here '
]

result = embedding.embed_documnets(docs)

print(str(result))
