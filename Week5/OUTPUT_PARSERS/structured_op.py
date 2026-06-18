from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint
)

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers import (
    StructuredOutputParser,
    ResponseSchema
)

load_dotenv()

# LLM
llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Pro",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)


schema = [
    ResponseSchema(
        name='fact_1',
        description='First fact about topic'
    ),

    ResponseSchema(
        name='fact_2',
        description='Second fact about topic'
    ),

    ResponseSchema(
        name='fact_3',
        description='Third fact about topic'
    ),
]

parser = StructuredOutputParser.from_response_schemas(
    schema
)

template = PromptTemplate(
    template="""
Give exactly 3 facts about {topic}.

Follow these instructions STRICTLY:

{format_instruction}
""",

    input_variables=['topic'],

    partial_variables={
        'format_instruction':
        parser.get_format_instructions()
    }
)

chain = template | model | parser

result = chain.invoke({
    'topic': 'black hole'
})

print(result)