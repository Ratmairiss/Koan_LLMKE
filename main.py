import json
import requests

API_URL = "https://api.intelligence.io.solutions/api/v1/chat/completions"
HEADERS = {
    "Authorization": "Bearer io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjIyMjZhNmEzLTFkNDktNDM3Yy05MmQyLWQyYmZhODE4ODJjYSIsImV4cCI6NDkxNjI5NTI3NH0.MKNz_PpRpKx5Gv0YyttIToOa9Q6W5MOoTLRMYBKrzTQWOb0Wnl2ypmhfbTJbnUEtTKarNZb9YRnx4cc3iM5OcQ",
    "Content-Type": "application/json"
}

text_to_process = """
Alice loves Bob. 
Bob works at OpenAI. 
Carol lives in Paris and likes croissants.
"""

questions = [
    "Who does Alice love?",
    "Where does Carol live?",
    "Where does Bob work?"
]

def extract_triplets(text):
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": f"Extract all meaningful triplets (subject, predicate, object) from the following text in strictly valid JSON:\n\n{text}"}],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "TripletsSchema",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "triplets": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "subject": {"type": "string"},
                                    "predicate": {"type": "string"},
                                    "object": {"type": "string"}
                                },
                                "required": ["subject", "predicate", "object"]
                            }
                        }
                    },
                    "required": ["triplets"]
                }
            }
        },
        "temperature": 0
    }
    return requests.post(API_URL, headers=HEADERS, json=payload).json()["choices"][0]["message"]["content"]

def answer_questions(triplets, questions):

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "user",
                "content": f"""
Given the following knowledge base (triplets):
{triplets}

Answer the following questions strictly in JSON format, including the question text and the answer as a single word or phrase:

{questions}
"""
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "AnswerWordsSchema",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "answers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "question": {"type": "string"},
                                    "answer": {"type": "string"}
                                },
                                "required": ["question", "answer"]
                            }
                        }
                    },
                    "required": ["answers"]
                }
            }
        },
        "temperature": 0
    }
    return requests.post(API_URL, headers=HEADERS, json=payload).json()["choices"][0]["message"]["content"]


triplets = extract_triplets(text_to_process)
print("Extracted Triplets:", triplets, sep = "\n")

answers = answer_questions(triplets, questions)
print("Result:", answers, sep = "\n")
