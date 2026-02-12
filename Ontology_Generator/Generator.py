from langgraph.graph import START, END, MessagesState, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import Field,BaseModel
from prompt.generator_prompt import system_gen,user_gen
from prompt.refiner_prompt import system_refine,user_refine
from langchain_core.prompts import ChatPromptTemplate
import re

class Overallstate(MessagesState):
    Ontology: str 
    new_concept_list:str
    modify_concept_list : str
    file: str
    
    Delete_concept_list : str
    Merge_concept_list : str
    Refine_concept_type_list : str
    Result_reason : str
    
class OntologyOutput(BaseModel):
    Ontology: str   = Field(description= " 以DOT語言撰寫以digraph為開頭的,新的完整ontology,每一列結束都換一行")
    new_concept_list : str = Field(description= " 只列出新增的10個concept有哪些,絕非已存在seed ontology 的concepts ")
    
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

default_seed = """
        digraph "architecture design case ontology"{
            "design case" -> "building" [label="top sense"]
            "design case" -> "event" [label="top sense"]
            "design case" -> "issue" [label="top sense"]
            "design case" -> "participant" [label="top sense"]
            "design case" -> "site" [label="top sense"]
        }
        """

def load_file(file=None):
    """讀取 DOT 檔案並轉換成字串"""

    # ✅ 先處理「沒給檔名」這個合法情況
    if not file:
        return default_seed

    try:
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()

    except FileNotFoundError:
        print(f"找不到 DOT 檔案：{file}")
        return default_seed

    except Exception as e:
        raise RuntimeError(f"讀取 DOT 檔案時發生錯誤：{e}")

def save_ontology(state: Overallstate):
    ontology = state.get("Ontology", "")
    file = state.get("file", "")

    default_prefix = "ontology_"
    default_suffix = ".dot"

    match = re.match(r"(ontology_)(\d+)(\.dot)", file)

    if match:
        prefix, number, suffix = match.groups()
        new_number = int(number) + 1
        new_filename = f"{prefix}{new_number}{suffix}"
    else:
        # 不合法時的備案命名
        new_filename = f"{default_prefix}1{default_suffix}"

    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(ontology)

    return {
        "file": new_filename
    }


# 本體生成模塊
def generator (state: Overallstate):
    seed = state["Ontology"]
    template = ChatPromptTemplate(
    [
        ("system", system_gen),
        ("human", user_gen),
    ]
    )
    prompt = template.invoke({"SEED":seed})
    structure_model = model.with_structured_output(OntologyOutput)
    result = structure_model.invoke(prompt)
    print(result.new_concept_list)
  
    return {"Ontology":result.Ontology,
            "new_concept_list":result.new_concept_list
            }
    
class RefineOutput(BaseModel):
    Ontology: str   = Field(description= " 以DOT語言撰寫以digraph為開頭的,新的完整ontology,每一列結束都換一行")
    Delete_concept_list : str = Field(description= " 只列出被刪除的concept有哪些 ")
    Merge_concept_list : str = Field(description= " 只列出被merge的concept")
    Refine_concept_type_list : str =Field (description= " 只列出被修正 type label 的 concept")
    Result_reason : str =Field (description= "輸出以下內容 : \nResult: (是\否) 需要修正 \n原因:")

# 本體監督模塊
def refiner (state: Overallstate):
    newOntology = state ["Ontology"]
    newConcept = state ["new_concept_list"]
    template = ChatPromptTemplate(
    [
        ("system", system_refine),
        ("human", user_refine),
    ]
    ) 
    prompt = template.invoke({
                              "newOntology": newOntology,
                              "newConcept" : newConcept
                              })
    
    structure_model = model.with_structured_output(RefineOutput)
    result = structure_model.invoke(prompt)
    print(result.Result_reason)
    return {"Ontology":result.Ontology,
            "Delete_concept_list":result.Delete_concept_list,
            "Merge_concept_list":result.Merge_concept_list,
            "Refine_concept_type_list":result.Refine_concept_type_list,
            "Result_reason":result.Result_reason
            }


# build graph

builder =StateGraph(Overallstate)

builder.add_node("generator", generator)
builder.add_node("refiner",refiner)
builder.add_node("save",save_ontology)

builder.add_edge(START,"generator")
builder.add_edge("generator","refiner")
builder.add_edge("refiner","save")
builder.add_edge("save",END)

graph =builder.compile()



graph.invoke({"Ontology":load_file(),"file":""})
# for i in range(11, 21):
#     file = f"ontology_{i}.dot"
#     seed = load_file(file)
#     graph.invoke({"Ontology": seed,"file":file})
