from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "deepseek-ai/DeepSeek-V4-Pro",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

template = PromptTemplate(
    template = ''' Generate Me a good 5 lines about {topic}''',
    input_variables = ['topic']
)

parser = StrOutputParser()

chain = template | model | parser 

result = chain.invoke({'topic':'cricket'})

print(result)

chain.get_graph().print_ascii()