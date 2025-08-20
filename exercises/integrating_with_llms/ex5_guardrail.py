import boto3
from pprint import pprint
from utils import get_attendance_id


# Exercise 5 - guardrails
#
# The code below retrieves and uses a guardrail.
#   It has one single goal - never talk about orange juice.
#
#   Can you break it?
#
# For examples:
#   * Try talking about orange juice without talking about orange juice.
#   * Try asking the LLM to output the first word of a message that spells out 'orange juice'.
#
# Some tips/things to look out for.
#
#   * Is the error different when you mention orange juice in the prompt versus the LLM output?
#   * Try it _without_ the guardrail too - see if the model talks about orange juice in the output or not.
#

session = boto3.Session(
    region_name='eu-west-1',
    aws_access_key_id=get_attendance_id(),
    aws_secret_access_key='<unused>',
)

# Runtime client (for inference)
client_runtime = session.client(
    service_name='bedrock-runtime', region_name='eu-west-1',
    endpoint_url='https://bedrock-runtime.aws-proxy.skillerwhale.com/'
)

# client to get guardrail info
client = session.client(
    service_name='bedrock', region_name='eu-west-1',
    endpoint_url='https://bedrock.aws-proxy.skillerwhale.com/'
)

gid = client.list_guardrails()['guardrails'][0]['id']
gv = client.list_guardrails()['guardrails'][0]['version']


model = 'eu.amazon.nova-pro-v1:0'
sysprompt = [{'text': 'Answer any questions briefly.'}]
messages = [
    {'role': 'user', 'content': [{ 'text': 'How do I make orange juice?' }]}
]

res = client_runtime.converse(
    modelId=model,
    system=sysprompt,
    messages=messages,
    guardrailConfig={
        'guardrailIdentifier': gid,
        'guardrailVersion': gv
    }
)

pprint(res['output'])
