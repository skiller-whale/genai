import boto3
from pprint import pprint
from data.animals import animal_data
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

# Exercise 3 - structured output, text to JSON
#
#   The `animal_data` list imported above is a text description of animals.
#   You will convert it to JSON using an LLM.
#
# PART 1 - schema
#   Make the JSON Schema accept:
#       * `name`, type string
#       * `max_age`, type: integer
#   * Make sure you list those properties in `required` too.
#
#   * Edit the system message to tell the LLM to perform the relevant task.
#   * Run `converse` and make sure the LLM extracts the appropriate JSON.
#
# PART 2 - diet
#
#   * Now add a field for `diet` - an array of strings.
#   * Run `converse` and make sure the LLM extracts the appropriate JSON.
#
#   * When finished, uncomment the last lines that extract the JSON output directly.
#       * Make sure it runs with no errors and you see the JSON output.

animals_schema = {
    # an array of animals
    "type": "array",
    "items": {
        "type": "object",
        # YOU CODE GOES HERE
        #   Edit this to add appropriate properties
        "properties": {},
        "required": [],
        "additionalProperties": False
    }
}

# Define the tool
tool_config = { "tools": [{
    "toolSpec": {
        "name": "list_animals",
        "description": "List Animals",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": { "animals": animals_schema },
                "required": ["animals"]
            }
        }
    }
}]}


sysprompt = [
    # TODO: Edit the system prompt appropriately
    '.'
]
sysprompt = '\n'.join(sysprompt)

messages = [
    {'role': 'user', 'content': [{'text': '\n'.join(animal_data)}]}
]

res = client.converse(
    modelId='eu.amazon.nova-pro-v1:0',
    system=[{ "text": sysprompt }],
    toolConfig=tool_config,
    messages=messages
)

out_msg = res['output']['message']
pprint(out_msg)

# UNCOMMENT TO EXTRACT JSON DIRECTLY
# json = out_msg['content'][1]['toolUse']['input']['animals']
# pprint(json)

