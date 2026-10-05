from fastapi import APIRouter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

router = APIRouter(
    prefix="/query",
    tags=["Query"]
)
openai_client = OpenAI("your_api_key")

# Embedding the chunks using OpenAI Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key="your_api_key"
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333"
)

@router.post("/")
async def query(question: str):
   search_result = vector_db.similarity_search(query=question)
   print (f"search results for question '{question}':{search_result}")

   context = " ".join(
      [
         f"[Page {result.metadata.get("page","unknown")}]{result.page_content}"
         for result in search_result
      ]
      
      )


   SYSTEM_PROMPT = """You are a helpful assistant that answers question based on the provided context." 
   "if the context does not contain the answer, respons with I' don't know"
   {context}
   """
   response = openai_client.chat.completions.create(
      model="gpt-5",
      messages=[
         {"role":"system", "content": SYSTEM_PROMPT},
         {"role":"user", "content": question}
      ]
   )
   return {"question":question, "answer": response.choice[0].message.content }