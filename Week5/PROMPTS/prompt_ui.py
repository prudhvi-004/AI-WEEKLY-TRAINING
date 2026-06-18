from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate

load_dotenv()

# LLM
llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Pro",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

# UI
st.header("Research Tool")

paper_input = st.selectbox(
    "Select Research Paper Name",
    [
        "Select...",
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis"
    ]
)

style_input = st.selectbox(
    "Select Explanation Style",
    [
        "Beginner-Friendly",
        "Technical",
        "Code-Oriented",
        "Mathematical"
    ]
)

length_input = st.selectbox(
    "Select Explanation Length",
    [
        "Short (1-2 paragraphs)",
        "Medium (3-5 paragraphs)",
        "Long (detailed explanation)"
    ]
)

# Prompt Template
template = PromptTemplate(
    template="""
Please summarize the research paper titled "{paper_input}" with the following specifications:

Explanation Style: {style_input}

Explanation Length: {length_input}

1. Mathematical Details:
Include relevant mathematical equations if present in the paper.

2. Code Examples:
Explain mathematical concepts using simple, intuitive code snippets where applicable.

3. Analogies:
Use relatable analogies to simplify complex ideas.

If certain information is not available in the paper, respond with:
"Insufficient information available"

instead of guessing.

Ensure the summary is clear, accurate, and aligned with the provided style and length.
""",
    input_variables=[
        'paper_input',
        'style_input',
        'length_input'
    ]
)

# --- REDUNDANT PLACEHOLDER BLOCK DELETED FROM HERE ---

# Button
if st.button('Summarize'):
    # Early escape if user didn't pick a paper
    if paper_input == "Select...":
        st.warning("Please select a valid research paper first!")
    else:
        # Define the chain
        chain = template | model

        # Passing the raw inputs directly here is all you need.
        # LangChain pipelines it: template fills -> model executes.
        result = chain.invoke({
            'paper_input': paper_input,
            'style_input': style_input,
            'length_input': length_input
        })

        st.write(result.content)