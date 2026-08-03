import os
import pandas as pd
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq


# --------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PragyanAI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 PragyanAI Intelligent Assistant")
st.caption("AI Powered Admission & Career Counselor")


# --------------------------------------------------
# Create Default FAQ Excel (Only Once)
# --------------------------------------------------

if not os.path.exists("pragyan_faq_prices.xlsx"):

    faq_data = {
        "Category":[
            "Program Overview",
            "Program Structure",
            "Program Structure",
            "Pricing & Fees",
            "Pricing & Fees",
            "Curriculum & Skills",
            "Curriculum & Skills",
            "Evaluation & Projects",
            "Career & Placement",
            "Leadership & Contact"
        ],

        "Question":[
            "What is the total duration and structure of the PragyanAI program?",
            "What happens in Phase 1 (First 6 Months)?",
            "What happens in Phase 2 (12 Months)?",
            "What is the fee structure?",
            "What salary can students expect?",
            "Months 1-3 modules?",
            "Months 4-6 modules?",
            "How are students evaluated?",
            "Career pathways?",
            "Who leads PragyanAI?"
        ],

        "Answer":[
            "18 Months consisting of 6 Months Offline Training followed by 12 Month Internship & Placement Drive.",
            "Half-day classroom, half-day labs, projects, hackathons and seminars.",
            "Internship, placement, resume building, startup exposure.",
            "Founding Batch ₹50,000 Training Fee + ₹50,000 Success Fee.",
            "AI Engineer ₹6-15 LPA, GenAI ₹8-18 LPA, Agentic AI ₹10-25 LPA.",
            "Python Full Stack, Data Science, Machine Learning.",
            "Deep Learning, Computer Vision, NLP, Generative AI, Agentic AI.",
            "Technical seminars and 48-hour Hackathons.",
            "AI Engineer, GenAI Engineer, Agentic AI Engineer, Data Scientist and more.",
            "Sateesh Ambesange (NITK Alumni)."
        ]
    }

    pd.DataFrame(faq_data).to_excel(
        "pragyan_faq_prices.xlsx",
        index=False
    )


# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = None
# --------------------------------------------------
# Persona Prompts
# --------------------------------------------------

SALES_PROMPTS = {

    "PragyanAI Student Counselor": """
You are Aarav, an Academic & Career Advisor for PragyanAI.

Goal:
Guide students to enroll in PragyanAI's 18-Month AI Program.

Always answer ONLY using the retrieved context.

Context:
{context}

Behavior:
- Friendly
- Motivating
- Practical
- Never hallucinate.
""",

    "PragyanAI Institutional Advisor": """
You are Dr. Kavita.

Help colleges understand PragyanAI's curriculum.

Always use only the retrieved context.

Context:
{context}
""",

    "PragyanAI Enterprise Lead": """
You are Rohan.

Help hiring partners recruit PragyanAI students.

Always answer only from context.

Context:
{context}
"""
}


import tempfile

# --------------------------------------------------
# Build Vector Store
# --------------------------------------------------

def load_documents_into_vectorstore(uploaded_files=None):

    global vectorstore

    docs = []

    # -------------------------
    # Load Uploaded Files
    # -------------------------
    if uploaded_files:

        for file in uploaded_files:

            suffix = os.path.splitext(file.name)[1].lower()

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            if suffix == ".pdf":

                loader = PyPDFLoader(tmp_path)
                docs.extend(loader.load())

            elif suffix in [".xlsx", ".xls"]:

                df = pd.read_excel(tmp_path)

                for _, row in df.iterrows():

                    content = " | ".join(
                        f"{col}: {val}" for col, val in row.items()
                    )

                    docs.append(
                        Document(
                            page_content=content,
                            metadata={"source": file.name}
                        )
                    )

    # -------------------------
    # Load Default FAQ
    # -------------------------
    if os.path.exists("pragyan_faq_prices.xlsx"):

        df = pd.read_excel("pragyan_faq_prices.xlsx")

        for _, row in df.iterrows():

            content = " | ".join(
                f"{col}: {val}" for col, val in row.items()
            )

            docs.append(
                Document(
                    page_content=content,
                    metadata={"source": "Default FAQ"}
                )
            )

    # -------------------------
    # Fallback Knowledge
    # -------------------------
    if not docs:

        docs = [
            Document(
                page_content="PragyanAI offers 6 Months Offline Training followed by 12 Months Internship & Placement."
            ),
            Document(
                page_content="Founding Batch Fee: ₹50,000 Training Fee + ₹50,000 Success Fee."
            )
        ]

    vectorstore = FAISS.from_documents(docs, embeddings)

    return f"✅ Knowledge Base Loaded ({len(docs)} documents)"


    # Load default FAQ

    if os.path.exists("pragyan_faq_prices.xlsx"):

        df = pd.read_excel("pragyan_faq_prices.xlsx")

        for _, row in df.iterrows():

            content = " | ".join(
                [f"{col}: {value}" for col, value in row.items()]
            )

            docs.append(
                Document(
                    page_content=content,
                    metadata={"source": "Default FAQ"}
                )
            )


    # Fallback knowledge

    if not docs:

        docs = [

            Document(
                page_content="""
PragyanAI offers
6 Months Offline Training
+
12 Months Internship & Placement.
"""
            ),

            Document(
                page_content="""
Founding Batch Fee:
₹50,000 Training
₹50,000 Success Fee
"""
            )

        ]


    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    return f"Knowledge Base Loaded ({len(docs)} documents)"


# --------------------------------------------------
# Build Knowledge Base on Startup
# --------------------------------------------------

load_documents_into_vectorstore()
# --------------------------------------------------
# Groq API Key
# --------------------------------------------------

# For Streamlit Cloud
groq_api_key = st.secrets.get("GROQ_API")

# Optional: Local fallback
if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API")

if not groq_api_key:
    st.error("❌ GROQ_API not found.")
    st.stop()


# --------------------------------------------------
# Initialize LLM
# --------------------------------------------------

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
)


# --------------------------------------------------
# Chat Memory Store
# --------------------------------------------------

store = {}


def get_session_history(session_id: str):

    if session_id not in store:

        store[session_id] = ChatMessageHistory()

    return store[session_id]


# --------------------------------------------------
# Create RAG Chain
# --------------------------------------------------

def create_rag_chain(persona_name, context):

    system_prompt = SALES_PROMPTS.get(
        persona_name,
        SALES_PROMPTS["PragyanAI Student Counselor"]
    ).format(
        context=context
    )

    prompt = ChatPromptTemplate.from_messages(

        [
            ("system", system_prompt),

            MessagesPlaceholder(
                variable_name="history"
            ),

            ("human", "{input}")
        ]

    )

    chain = (

        prompt
        | llm
        | StrOutputParser()

    )

    return chain


# --------------------------------------------------
# Response Function
# --------------------------------------------------

def respond(question, persona):

    retriever = vectorstore.as_retriever(

        search_kwargs={
            "k": 4
        }

    )

    docs = retriever.invoke(question)

    context = "\n\n".join(

        [

            doc.page_content

            for doc in docs

        ]

    )

    session_id = f"session_{persona}"

    rag_chain = create_rag_chain(

        persona,

        context

    )

    conversational_chain = RunnableWithMessageHistory(

        rag_chain,

        get_session_history,

        input_messages_key="input",

        history_messages_key="history",

    )

    answer = conversational_chain.invoke(

        {

            "input": question

        },

        config={

            "configurable": {

                "session_id": session_id

            }

        }

    )

    return answer


# --------------------------------------------------
# Clear Memory
# --------------------------------------------------

def clear_memory(persona):

    session_id = f"session_{persona}"

    if session_id in store:

        store[session_id].clear()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    persona = st.selectbox(
        "Choose Persona",
        list(SALES_PROMPTS.keys())
    )

    uploaded_files = st.file_uploader(
        "Upload PDFs / Excel",
        type=["pdf", "xlsx", "xls"],
        accept_multiple_files=True
    )

    if uploaded_files:

        with st.spinner("Updating Knowledge Base..."):

            status = load_documents_into_vectorstore(uploaded_files)

        st.success(status)

    if st.button("🗑 Clear Conversation"):

        clear_memory(persona)

        st.session_state.messages = []

        st.success("Conversation Cleared")


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask anything about PragyanAI..."
)


# --------------------------------------------------
# Generate Response
# --------------------------------------------------

if question:

    # Show user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # Generate AI response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = respond(
                question,
                persona
            )

            st.markdown(answer)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
