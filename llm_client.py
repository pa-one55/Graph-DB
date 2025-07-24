import os
import requests
 
# Groq setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")
 
def extract_triples(note):
    prompt = f"""
    Extract relationships from the following note as (Node1)-[RELATION]->(Node2) triples:
 
    "{note}"
 
    Output:
    (A)-[REL]->(B)
    ...
    """
 
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
 
    payload = {
        "model": GROQ_MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
 
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    output = response.json()["choices"][0]["message"]["content"]
    return parse_triples(output)
 
 
def parse_triples(output):
    triples = []
    for line in output.strip().split('\n'):
        if line.startswith("(") and ")-[" in line:
            try:
                src = line.split("(")[1].split(")")[0].strip()
                rel = line.split("[")[1].split("]")[0].strip()
                tgt = line.split("->(")[1].split(")")[0].strip()
                triples.append((src, rel, tgt))
            except:
                continue
    return triples
 