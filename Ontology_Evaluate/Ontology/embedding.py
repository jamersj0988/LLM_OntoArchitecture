import re
from langchain_openai import OpenAIEmbeddings
import json

def embed_concepts(
    concepts: list[str],
    model: str = "text-embedding-3-small"
) -> dict[str, list[float]]:
    """
    Input: list of concept strings
    Output: dict {concept: embedding_vector}
    """

    embeddings = OpenAIEmbeddings(model=model)

    vectors = embeddings.embed_documents(concepts)

    concept_embeddings = {
        concept: vector
        for concept, vector in zip(concepts, vectors)
    }

    return concept_embeddings

def extract_concepts_from_dot(dot_text: str) -> list[str]:
    """
    Extract unique concept names from a DOT graph.
    Concepts are node names appearing on both sides of '->'.
    """
    # 找出 "A" -> "B"
    pattern = r'"([^"]+)"\s*->\s*"([^"]+)"'
    matches = re.findall(pattern, dot_text)

    concepts = set()
    for src, tgt in matches:
        concepts.add(src)
        concepts.add(tgt)

    return sorted(concepts)

file = "LLM10.dot"
save = "LLM10.json" 

def main(input:str,output:str):

    with open(input, "r", encoding="utf-8") as f:
        dot_text = f.read()

    low_concepts = []
    concepts = extract_concepts_from_dot(dot_text)
    for i in concepts:
        low_concepts.append(i.lower().replace("_"," "))
        
    cleaned_concepts = []
    for i in low_concepts:
        if i.startswith("ifc"):
            cleaned_concepts.append(i[3:])
        else:
            cleaned_concepts.append(i)

    print(len(cleaned_concepts))
    
    embeddings = embed_concepts(cleaned_concepts)
    
    with open(output, "w", encoding="utf-8") as f:
        json.dump(embeddings, f)
        
main (file,save)