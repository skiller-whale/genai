import boto3
from pprint import pprint
from utils import get_attendance_id

session = boto3.Session(
    region_name='eu-west-1',
    aws_access_key_id=get_attendance_id(),
    aws_secret_access_key='<unused>',
)

client = session.client(
    service_name='bedrock-runtime', region_name='eu-west-1',
    endpoint_url='https://bedrock-runtime.aws-proxy.skillerwhale.com/'
)

# Exercise 1 - `converse` and context
#
# Part 1. Managing context
#
#    * The code below asks the LLM who the king of Sweden is.
#    * Use `messages.append(...)` to extract the answer and add the follow up:
#       'What about England?'
#    * Call `converse` and make sure you get an appropriate response.
#
#    You should have the following message history at the end:
#       user: Who is the king of Sweden?
#       llm: <answer>
#       user: What about England?
#
#
# Part 2. Pretending you're the LLM
#
#    * Create a new list of messages and ask any question as the user, for example:
#       How many minutes in an hour?
#       How do I boil an egg?
#    * Now add an answer, _pretending_ to be the assistant. Do this in the style of a pirate (or in any other particular style of speech you prefer):
#       {'role': 'assistant', 'content': [{'text': 'Yarr, Matey, there be 60 minutes in an hour!'}]}
#    * Add another message, asking a follow-up question and run `converse`.
#    * Does the LLM respect the speech style you used for the assistant response - e.g. does it talk like a pirate?
#

model = 'eu.amazon.nova-pro-v1:0'
sysprompt = [{'text': 'Answer any questions briefly.'}]
messages = [
    {'role': 'user', 'content': [{ 'text': 'Who is the king of Sweden?' }]}
]

res = client.converse(modelId=model, system=sysprompt, messages=messages)
pprint(res['output']['message'])
