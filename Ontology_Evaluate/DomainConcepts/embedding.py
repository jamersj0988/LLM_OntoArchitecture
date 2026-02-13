import json
from pathlib import Path
import re
import inflect
import spacy
import os
from collections import Counter
from langchain_openai import OpenAIEmbeddings
import json

file_path = '../Corpus/Archdaily'
save_path = 'ArchdailyConcepts.json'

p = inflect.engine()
nlp = spacy.load("en_core_web_sm")
        
def extract_entity_concepts(json_data):
    concepts = []
    for item in json_data:
        for node in item.get("nodes", []):
            if node.get("type") == "Entity":
                concepts.append(node.get("id"))
    return concepts


# 詞正規化

def normalize_concept_list(concept_list):
    normalized_list = []
    seen = set()

    for text in concept_list:
        # ---------- text-level normalization ----------
        text = re.sub(r"[^\w\s\-]", "", text)
        text = text.replace("-", " ")
        text = re.sub(r"\s+", " ", text).strip()

        doc = nlp(text)

        # ---------- term-level gate ----------
        has_noun_like = False
        for token in doc:
            if token.pos_ in {"NOUN", "PROPN"}:
                has_noun_like = True
                break
            if token.tag_ == "VBG" and token.dep_ in {"compound", "nsubj", "dobj", "pobj"}:
                has_noun_like = True
                break

        if not has_noun_like:
            continue

        # ---------- token-level normalization ----------
        tokens = []
        for token in doc:
            t = token.text.lower()
            if token.tag_ == "VBG" and token.dep_ in {"compound", "nsubj", "dobj", "pobj"}:
                t = token.lemma_

            singular = p.singular_noun(t)
            tokens.append(singular if singular else t)

        normalized = " ".join(tokens)
        normalized_list.append(normalized)
    return normalized_list


def filter_by_frequency(corpus_list, min_count=0):
    """
    回傳CorpusConcepts去重後的結果
    回傳出現次數大於 min_count 的元素列表
    """
    counter = Counter(corpus_list)
    result = [item for item, count in counter.items() if count > min_count]
    return result  


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


def main(input_path,output_path):
    result=[]
    corpus = (os.listdir(input_path))
    for i in corpus:
        with open(f"{input_path}/{i}", "r", encoding="utf-8") as f:
            data = json.load(f)
            concept_list = extract_entity_concepts(data)
            result.append(concept_list)

    Corpus_concepts = []

    for doc in list(result) :
        Corpus_concepts.extend(doc)
    print("原始 Corpus 詞彙共",len(Corpus_concepts),"個" )
    
    Corpus_concepts = normalize_concept_list(Corpus_concepts)
    print("完成詞正規化，剩餘:",len(Corpus_concepts),"個")
    
    Corpus_concepts = filter_by_frequency(Corpus_concepts)
    print("保留出現至少2次的concepts,共:",len(Corpus_concepts))
    
    Domain_Concepts = embed_concepts(Corpus_concepts)
    
    print("向量嵌入完成 !" )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(Domain_Concepts, f)
        
    print(f"成功匯出 {output_path} !")
    
main(file_path,save_path)