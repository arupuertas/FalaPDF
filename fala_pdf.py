import streamlit as st
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import speech_recognition as sr

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    #embeddings = HuggingFaceInstructEmbeddings(model_name="bigscience/bloom-560m")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    #lidando com a resposta do usuario
    response = st.session_state.conversation({'question':user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Fala PDF", page_icon='🗣️')
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header('Fala PDF')
    st.subheader('A :blue[IA] que faz você falar com seu PDF', divider='blue')
    st.subheader('Converse agora com seu arquivo e tire suas dúvidas :speaking_head_in_silhouette:')

    # Criando uma coluna com largura de 2/3 para o input e 1/3 para o botão
    input_column, button_column = st.columns([3, 1])

    # Adicionando o botão com margem superior
    st.markdown(
        """
        <style>
        .stButton>button {
            margin-top: 29px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Inicializa o recognizer
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        # st.write("Pressione o botão abaixo para perguntar por voz.")
        audio_button = button_column.button("Pergunte :studio_microphone:")
        if audio_button:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            try:
                audio = recognizer.listen(mic)
                # Reconhece o áudio capturado
                text = recognizer.recognize_google(audio, language="pt-BR")
                text = text.lower()
                st.session_state.user_question = text
            except sr.UnknownValueError:
                st.write("Não foi possível reconhecer a pergunta.")
            except KeyboardInterrupt:
                st.write("Gravação interrompida.")

    user_question = input_column.text_input("Pergunte sobre os documentos abaixo ou clique em 'Pergunte' para usar áudio.", st.session_state.get("user_question", ""))
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        #Logo
        logo = 'src/img/logo_pdf.png'
        st.image(logo, width=220, use_column_width=False)
        st.subheader("Faça o upload dos seus arquivos abaixo:")
        pdf_docs = st.file_uploader("Faça o upload dos seus PDF's aqui e clique em 'Processar'", accept_multiple_files=True)
        if st.button("Processar"):
            with st.spinner("Processando"):
                #pegando o texto do pdf
                raw_text = get_pdf_text(pdf_docs)
                # pegando os chunks
                text_chunks = get_text_chunks(raw_text)
                # vetorizando
                vectorstore = get_vectorstore(text_chunks)
                # criando a conversa
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()
