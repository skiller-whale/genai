from utils import extract_output, get_bedrock_client


sysprompt = """
    You are a Python code assistant.
    You don't explain code, you just write it.
"""


chat = """
    Query:
        Write a function that divides two numbers.
    Answer:
        ```py
"""


client = get_bedrock_client()

res = client.converse(
    modelId='eu.amazon.nova-pro-v1:0',
    system=[{ "text": sysprompt }],
    messages=[{"role": "user", "content": [{"text": chat}]}],
    inferenceConfig={
        'temperature': 1.0,
        'topP': 1.0,
    },
)

out = extract_output(res)
print(out)
