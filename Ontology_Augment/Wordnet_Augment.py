from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt.Wordnet_prompt import Wordnet_prompt,Wordnet_system
from langchain.tools import tool
from nltk.corpus import wordnet as wn
from langchain_core.prompts import ChatPromptTemplate
from typing import List

wn.ensure_loaded() 

# Wordnet 查詢工具
@tool 
def Wordnet_Search(inputs: List[str]) -> str:
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


seed = """
digraph building ontology{
"building" -> "wall" [label="meronymy"]
}
"""

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
Wordnet_model = create_agent(model,tools = [Wordnet_Search], system_prompt = Wordnet_system)
prompt_template = ChatPromptTemplate.from_messages([
        ("human", Wordnet_prompt)
    ])


for event in Wordnet_model.stream(
    {"messages": prompt_template.format_messages(Seed_Ontology = seed) },
    stream_mode="values",
):
    event["messages"][-1].pretty_print()