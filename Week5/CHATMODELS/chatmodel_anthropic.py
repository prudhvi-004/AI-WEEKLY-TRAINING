from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(model = '')

result = model.invoke("what is the capitol of India?")

print(result)