from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

chat_history = []

while True:

    question = input("You : ")

    if question.lower() in ["exit", "quit"]:
        break

    messages = prompt.invoke({
        "chat_history": chat_history,
        "question": question
    })

    response = llm.invoke(messages)

    print("\nAI :", response.content)

    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response.content))