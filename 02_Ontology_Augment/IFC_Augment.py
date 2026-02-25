from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.retrievers import BM25Retriever
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from prompt.IFC_prompt import IFC_template



embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

faiss_store = FAISS.load_local(
    folder_path="IFC_CONCEPT",
    embeddings=embeddings,
    allow_dangerous_deserialization=True # 啟用此選項以載入在非當前環境中創建的資料庫
)

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    semantic_results = faiss_store.similarity_search(query, k=15)
    retrieved_docs = semantic_results 

    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

rag_agent = create_agent(model, tools=[retrieve_context])

phase1output="""
以下是從 `IfcRoot` 追溯的階層中，用於表示建築物理構建和空間構建的 IFC 實體(Entity)：

### 建築物理構建 (Physical Elements)
這些實體主要用於表示建築的物理組件：

- IfcElement
  - IfcBuildingElement
    - IfcBeam
    - IfcColumn
    - IfcCovering
    - IfcCurtainWall
    - IfcDoor
    - IfcFooting
    - IfcMember
    - IfcPile
    - IfcPlate
    - IfcRailing
    - IfcRamp
    - IfcRampFlight
    - IfcRoof
    - IfcSlab
    - IfcStair
    - IfcStairFlight
    - IfcWall
    - IfcWallStandardCase
    - IfcWindow
  - IfcDistributionElement
    - IfcDistributionFlowElement
      - IfcDuctSegment
      - IfcDuctFitting
      - IfcDuctSilencer
      - IfcPipeSegment
      - IfcPipeFitting
  - IfcFurnishingElement
    - IfcFurniture
    - IfcSystemFurnitureElement

### 建築空間構建 (Spatial Elements)
這些實體用於表示建築的空間和邊界：

- IfcSpatialElement
  - IfcSpatialStructureElement
    - IfcBuilding
    - IfcBuildingStorey
    - IfcSite
    - IfcSpace
    - IfcZone
  - IfcSpatialZone

這些實體涵蓋了從 `IfcRoot` 衍生出的關鍵實體，用於完整地表示建築物理構建和空間構建。每個類別下面的實體都代表在建築資訊建模(Building Information Modeling, BIM)中不同的物理元素或空間元素。
"""

def Ontology_Augment (target):
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是專業AGENT，可以透過工具[retrieve_context]獲得IFC相關知識或資訊，你會專業有條理的完成USER的指定的任務or問題，對於任務目標會做到盡自己所能做到最完整的程度，racking yours brains"),
        ("human", IFC_template)
    ])

    messages= prompt.invoke(
        {
            "phase1_output" : phase1output,
            "target_entity" : target #e.g :IfcRoof, IfcDoor
        }
    )

    for event in rag_agent.stream(
        messages,
        stream_mode="values",
    ):
        event["messages"][-1].pretty_print()
        
        
Ontology_Augment("IfcRoof")
