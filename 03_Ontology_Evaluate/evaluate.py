import json
import numpy as np
import pandas as pd

def load_embedding_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    keys = list(data.keys())
    vectors = np.array(list(data.values()))

    return keys, vectors

def batch_cosine_similarity(A, B):
    """
    A: (num_A, dim)
    B: (num_B, dim)
    Return: (num_A, num_B)
    """
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    B = B / np.linalg.norm(B, axis=1, keepdims=True)
    return np.dot(A, B.T)


def shared_concepts(ontology,corpus):
    
    a_keys, a_vectors = load_embedding_json(ontology)  #Ontology
    b_keys, b_vectors = load_embedding_json(corpus)  # Corpus
    similarity_matrix = batch_cosine_similarity(a_vectors, b_vectors)
    (len(a_keys), len(b_keys))

    threshold = 0.75
    rows = []
    for j, b_key in enumerate(b_keys):
        scores = similarity_matrix[:, j]
        best_i = np.argmax(scores)

        rows.append({
            "Domain Concepts": b_key,
            "Ontology Concepts ": a_keys[best_i],
            "Similarity": float(scores[best_i])
            })
        
    top1_llm_df = pd.DataFrame(rows)
    shared_df = (
        top1_llm_df[top1_llm_df["Similarity"] >= threshold]
        .reset_index(drop=True)
    )

    return len(a_keys),len(b_keys),len(shared_df)


def main(ontology,corpus):
    ontology_concept,domain_concept,shared_concept = shared_concepts(ontology, corpus)
   
    print(ontology_concept,domain_concept,shared_concept)
    
    Domain_coverage = shared_concept / domain_concept
    Ontology_relevance = shared_concept / ontology_concept

    print("EVALUATE RESULT:")
    print(f"Domain_coverage: {Domain_coverage}")
    print(f"Ontology_relevance: {Ontology_relevance}")




ontology_path = "Ontology/LLM10.json"
corpus_path = "DomainConcepts/ArchdailyConcepts.json"
    
main(ontology_path, corpus_path)