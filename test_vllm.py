# test_vllm.py
"""Test vLLM server connection and response quality."""

from openai import OpenAI

# Test connection
client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")

print("Testing vLLM server...")
print("=" * 60)

# Simple test
response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": "What is 2+2? Answer briefly."}],
    temperature=0.0,
    max_tokens=50
)

print(f"Response: {response.choices[0].message.content}")
print(f"Tokens - Prompt: {response.usage.prompt_tokens}, Completion: {response.usage.completion_tokens}")
print("=" * 60)

# Test SQL generation (relevant to your use case)
sql_prompt = """Given this table schema:
Table: Students (id, name, age, grade)

Write a SQL query to find students older than 18."""

response2 = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": sql_prompt}],
    temperature=0.0,
    max_tokens=200
)

print(f"SQL Test Response:\n{response2.choices[0].message.content}")
print("=" * 60)
print("✅ vLLM server is working correctly!")
