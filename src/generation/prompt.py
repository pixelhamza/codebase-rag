def build_prompt(query, chunks):
    context = ""

    for i, chunk in enumerate(chunks, start=1):
        context += f"""=== Chunk {i} ===
File: {chunk["file_path"]}
Name: {chunk["qualified_name"]}
Docstring: {chunk.get("docstring") or "None"}

{chunk["source"]}

"""

    prompt = f"""You are an expert Python software engineer.

Answer the user's question using ONLY the provided repository context.

Instructions:
- Base your answer only on the provided code.
- If the answer is not present in the code, say that you don't have enough information.
- Do not invent functions, classes, or behavior.
- Explain your reasoning clearly.
- When referencing code, mention the function or class name.

Repository Context:

{context}

User Question:
{query}

Answer:
"""

    return prompt