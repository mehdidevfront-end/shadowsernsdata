from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import requests

try:
    from opensearchpy import OpenSearch, RequestsHttpConnection
except Exception:
    OpenSearch = None

router = APIRouter(prefix='/qa', tags=['qa'])


class QARequest(BaseModel):
    question: str
    top_k: Optional[int] = 5


def get_opensearch_client():
    url = os.getenv('OPENSEARCH_URL', 'http://localhost:9200')
    if OpenSearch is None:
        raise RuntimeError('opensearch-py not installed')
    return OpenSearch([url], connection_class=RequestsHttpConnection)


def retrieve_contexts(question: str, index: str = 'llm_contexts', top_k: int = 5):
    client = get_opensearch_client()
    body = {
        'size': top_k,
        'query': {
            'multi_match': {
                'query': question,
                'fields': ['title^2', 'content']
            }
        }
    }
    res = client.search(index=index, body=body)
    hits = [h['_source'] for h in res.get('hits', {}).get('hits', [])]
    return hits


def call_llm(prompt: str) -> str:
    # prefer OpenAI if API key set
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        payload = {
            'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 512,
        }
        r = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        j = r.json()
        return j['choices'][0]['message']['content']
    # fallback: simple echo/resume
    return 'RESPONSE: ' + (prompt[:1000])


@router.post('/', tags=['qa'])
def ask(req: QARequest):
    try:
        contexts = []
        try:
            contexts = retrieve_contexts(req.question, top_k=req.top_k)
        except Exception:
            # return minimal retrieval failure info but continue
            contexts = []

        # build prompt with contexts
        prompt_parts = ['You are an assistant. Use the following contexts to answer the question.\n']
        for i, c in enumerate(contexts):
            prompt_parts.append(f"Context {i+1}: {c.get('title', '')}\n{c.get('content', '')}\n---\n")
        prompt_parts.append(f"Question: {req.question}\nAnswer in JSON with keys: answer, sources\n")
        prompt = '\n'.join(prompt_parts)

        answer = call_llm(prompt)
        return {'answer': answer, 'contexts': contexts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
