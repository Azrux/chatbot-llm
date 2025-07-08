import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.schema import Document


class KavakRAG:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.qa_chain = None

    def scrape_kavak_content(self):
        """Scrapea el contenido de la página de Kavak"""
        url = "https://www.kavak.com/mx/blog/sedes-de-kavak-en-mexico"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraer el contenido principal (ajusta según la estructura del sitio)
            main_content = soup.find('main') or soup.find('article') or soup

            # Limpiar el texto
            for script in main_content(["script", "style"]):
                script.decompose()

            text = main_content.get_text(separator='\n', strip=True)
            return text

        except Exception as e:
            print(f"Error al scrapear: {e}")
            return None

    def setup_vectorstore(self):
        """Configura el vectorstore con el contenido scrapeado"""
        print("Scrapeando contenido de Kavak...")
        content = self.scrape_kavak_content()

        if not content:
            print("No se pudo obtener el contenido")
            return False

        print("Dividiendo texto en chunks...")
        # Dividir el texto en chunks más pequeños
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Tamaño de cada fragmento
            chunk_overlap=200,  # Overlap entre fragmentos
            length_function=len,
        )

        # Crear documentos
        documents = [Document(page_content=content, metadata={
                              "source": "kavak_sedes"})]
        texts = text_splitter.split_documents(documents)

        print(f"Creados {len(texts)} fragmentos de texto")

        # Crear vectorstore
        print("Creando vectorstore...")
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)

        # Crear cadena de QA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                # Recuperar los 3 fragmentos más relevantes
                search_kwargs={"k": 3}
            ),
            return_source_documents=True
        )

        print("✅ RAG configurado correctamente")
        return True

    def answer_question(self, question: str):
        """Responde una pregunta usando RAG"""
        if not self.qa_chain:
            return "Error: RAG no está configurado"

        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        except Exception as e:
            return f"Error al procesar la pregunta: {e}"


kavak_rag = KavakRAG()
kavak_rag.setup_vectorstore()
