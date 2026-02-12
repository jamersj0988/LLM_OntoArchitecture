from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain.agents import create_agent
from langchain_community.vectorstores import FAISS
from langgraph.graph import START, END, MessagesState, StateGraph

from langchain_core.messages import HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field,BaseModel
from datetime import datetime
from typing import Annotated



from langchain.tools import tool
from nltk.corpus import wordnet as wn
from pydantic import BaseModel,Field

wn.ensure_loaded() 

@tool
def Wordnet_Search(inputs: list) -> str:
    """可以獲得 inputs 中所有單詞的 Synonyms 以及其 Meronyms
        查詢後會得到回覆:
        Vocabulary --> Vocabulary defintion 
    """
    
    results = []
    
    for x in inputs:
        synsets = wn.synsets(x, pos='n')
        results.append(f"\n=== {x} ===")

        if not synsets:
            results.append("未找到相關名詞。")
            continue

        # Synsets summary
        results.append("【Synonyms】")
        for syn in synsets:
            results.append(f" - {syn.name()} : {syn.definition()}")

        # Meronyms output
        meronym_found = False
        output_block = ["【Meronyms】"]

        for syn in synsets:
            part_meros = syn.part_meronyms()
            if not part_meros:
                continue

            meronym_found = True
            
            for m in part_meros:
                output_block.append(f"   - {m.name()} --> {m.definition()}")

        if meronym_found:
            results.extend(output_block)
        else:
            results.append("此單字沒有任何 meronym（part_meronyms）。")
        # Hyponyms output
        hyponym_found = False
        output_block = ["【Hyponyms】"]

        for syn in synsets:
            hypos = syn.hyponyms()
            if not hypos:
                continue

            hyponym_found = True

            for h in hypos:
                output_block.append(f"   - {h.name()} --> {h.definition()}")

        if hyponym_found:
            results.extend(output_block)
        else:
            results.append("此單字沒有任何 hyponym。")

    return "\n".join(results)

