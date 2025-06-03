import boto3
import tqdm
from utils import accuracy_score, extract_output, get_attendance_id
import re

session = boto3.Session(
    region_name='eu-west-1',
    aws_access_key_id=get_attendance_id(),
    aws_secret_access_key='<unused>',
)

client = session.client(
    service_name='bedrock-runtime', region_name='eu-west-1',
    endpoint_url='https://bedrock-runtime.aws-proxy.skillerwhale.com/'
)



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

res = client.converse(
    modelId='eu.amazon.nova-pro-v1:0',
    system=[{ "text": sysprompt }],
    messages=[{
        "role": "user",
        "content": [{
            "text": chat
        }]
    }],
    inferenceConfig={
        'temperature': 1.0,
        'topP': 1.0,
    },
)

out = extract_output(res)
print(out)
