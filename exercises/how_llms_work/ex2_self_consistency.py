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
    Let's think step-by-step.
    You receive a user query sent over chat
    It should go to one of three departments:
        - Sales
        - Tech Support
        - Billing

    An example query:
        ```
        Query: I want to purchase a subscription.
        Department: Sales
        ```

    Use the above template. DO NOT OUTPUT ANYTHING AFTER `Department: <answer>`.
"""

chat = """
    Query: I need help with my account/subscription
    Department:
"""

for _ in range(10):
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

    if match_ := re.search(r"Department:\s*([A-Za-z ]+)", out):
        answer = match_.group(1).strip()
        print(answer)

print()
