
import os
import re
from openai import OpenAI

client = OpenAI()

# Step 1: Our knowledge base
documents = [
    "Full-time employees receive 2 floating holidays.",
    "Floating holidays can be used from December 21 to 31, 2026.",
    "December 25 is a paid company holiday.",
    "Part-time employees are not eligible for floating holidays.",
]

# Step 2: Simple keyword retrieval
def retrieve(question: str, top_k: int = 2):
    query_words = set(
        re.findall(r"\b\w+\b", question.lower())
    )

    scored = []

    for doc in documents:
        doc_words = set(
            re.findall(r"\b\w+\b", doc.lower())
        )
        score = len(query_words & doc_words)
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        doc for score, doc in scored[:top_k]
        if score > 0
    ]


# Step 3: Augment and generate
def answer_question(question: str):
    relevant_docs = retrieve(question)

    if not relevant_docs:
        return "No relevant information found."

    context = "\n".join(relevant_docs)

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "Answer using only the supplied context. "
            "If the answer is not in the context, "
            "say you do not know."
        ),
        input=(
            f"Context:\n{context}\n\n"
            f"Question: {question}"
        ),
    )

    return response.output_text


question = "How many floating holidays do full-time employees receive?"

print("Retrieved documents:")
for doc in retrieve(question):
    print("-", doc)

print("\nAnswer:")
print(answer_question(question))
