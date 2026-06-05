import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid


# =====================================================================================
# UTILITY FUNCTIONS
# =====================================================================================

# -----------------------------------------------------------------------------
# Generate a unique thread ID for every new conversation
# This thread_id is used by LangGraph to uniquely identify a chat session
# -----------------------------------------------------------------------------
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


# -----------------------------------------------------------------------------
# Reset the current chat
# 1. Create a new thread ID
# 2. Add it to the conversation list
# 3. Clear current chat history from UI
# -----------------------------------------------------------------------------
def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []


# -----------------------------------------------------------------------------
# Add a new thread to sidebar conversation list
# Prevents duplicate thread entries
# -----------------------------------------------------------------------------
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


# -----------------------------------------------------------------------------
# Load conversation history from LangGraph persistence layer
# Uses thread_id to fetch saved state/messages
# -----------------------------------------------------------------------------
def load_conversation(thread_id):
    state = chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    )

    # Return messages if available, otherwise return empty list
    return state.values.get('messages', [])


# =====================================================================================
# SESSION STATE INITIALIZATION
# =====================================================================================

# -----------------------------------------------------------------------------
# Stores messages displayed in the current UI session
# Format:
# [
#   {"role": "user", "content": "..."},
#   {"role": "assistant", "content": "..."}
# ]
# -----------------------------------------------------------------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# -----------------------------------------------------------------------------
# Stores the currently active LangGraph thread ID
# -----------------------------------------------------------------------------
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


# -----------------------------------------------------------------------------
# Stores all conversation thread IDs for sidebar navigation
# -----------------------------------------------------------------------------
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []


# -----------------------------------------------------------------------------
# Ensure current thread appears in sidebar conversation list
# -----------------------------------------------------------------------------
add_thread(st.session_state['thread_id'])


# =====================================================================================
# SIDEBAR UI
# =====================================================================================

# -----------------------------------------------------------------------------
# Sidebar title
# -----------------------------------------------------------------------------
st.sidebar.title('LangGraph Chatbot')


# -----------------------------------------------------------------------------
# New Chat Button
# Creates a fresh thread and clears current conversation
# -----------------------------------------------------------------------------
if st.sidebar.button('New Chat'):
    reset_chat()


# -----------------------------------------------------------------------------
# Sidebar section showing all previous conversations
# -----------------------------------------------------------------------------
st.sidebar.header('My Conversations')


# -----------------------------------------------------------------------------
# Display all conversation threads in reverse order
# Latest conversation appears first
# -----------------------------------------------------------------------------
for thread_id in st.session_state['chat_threads'][::-1]:

    # Clicking a thread loads that conversation
    if st.sidebar.button(str(thread_id)):

        # Set selected thread as active thread
        st.session_state['thread_id'] = thread_id

        # Fetch stored conversation from LangGraph
        messages = load_conversation(thread_id)

        temp_messages = []

        # Convert LangChain message objects into UI-friendly format
        for msg in messages:

            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            temp_messages.append({
                'role': role,
                'content': msg.content
            })

        # Load conversation into Streamlit session state
        st.session_state['message_history'] = temp_messages


# =====================================================================================
# MAIN CHAT UI
# =====================================================================================

# -----------------------------------------------------------------------------
# Display all messages stored in current session history
# This recreates the chat interface on page refresh/reload
# -----------------------------------------------------------------------------
for message in st.session_state['message_history']:

    with st.chat_message(message['role']):
        st.text(message['content'])


# -----------------------------------------------------------------------------
# Chat input box for user queries
# -----------------------------------------------------------------------------
user_input = st.chat_input('Type here')


# =====================================================================================
# USER MESSAGE PROCESSING
# =====================================================================================

# -----------------------------------------------------------------------------
# Runs when user submits a message
# -----------------------------------------------------------------------------
if user_input:

    # -------------------------------------------------------------------------
    # Store user message in session history
    # -------------------------------------------------------------------------
    st.session_state['message_history'].append({
        'role': 'user',
        'content': user_input
    })

    # Display user message immediately
    with st.chat_message('user'):
        st.text(user_input)

    # -------------------------------------------------------------------------
    # LangGraph configuration
    # thread_id ensures persistence/memory separation between chats
    # -------------------------------------------------------------------------
    CONFIG = {
        'configurable': {
            'thread_id': st.session_state['thread_id']
        }
    }

    # -------------------------------------------------------------------------
    # Generate and stream AI response
    # -------------------------------------------------------------------------
    with st.chat_message("assistant"):

        # ---------------------------------------------------------------------
        # Stream only AI-generated tokens
        # Ignore HumanMessage chunks if any appear
        # ---------------------------------------------------------------------
        def ai_only_stream():

            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):

                # Stream only assistant responses
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        # Stream tokens live in UI
        ai_message = st.write_stream(ai_only_stream())

    # -------------------------------------------------------------------------
    # Save final assistant response into session history
    # This ensures response remains visible after reruns
    # -------------------------------------------------------------------------
    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_message
    })