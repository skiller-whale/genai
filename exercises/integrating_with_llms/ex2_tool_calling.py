import boto3
from data.projects import project_info
from pprint import pprint
from utils import get_attendance_id

session = boto3.Session(region_name='eu-west-1', aws_access_key_id=get_attendance_id(), aws_secret_access_key='<unused>')
client = session.client(service_name='bedrock-runtime', region_name='eu-west-1', endpoint_url='https://bedrock-runtime.aws-proxy.skillerwhale.com/')

# Exercise 2 - tool calling
#   In this exercise you will implement a tool with an LLM call.
#   The tool will return information about a project, given its code.
#   The user will ask the LLM to draft an email about a project.
#
#  The tool is already defined and implemented in the `get_project_info` function and `tool_config`.
#
#  * Run the code as it is, to see the LLM's response.
#
#  * Write code that calls the tool and adds the result into an LLM message.
#  * Append that message to the conversation.
#  * Add another call to `converse` to check whether the LLM generates an email with appropriate content.
#

def get_project_info(project_code):
    """
    Extract project info by project code.
    """
    if project_code not in project_info:
        return [{"json": {'error': 'Project not found'}}]
    else:
        return [{"json":project_info[project_code]}]


tool_config = { "tools": [{
    "toolSpec": {
        "name": "get_project_info",
        "description": "Get project information for a given project code.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": { "code": { "type": "string" } },
                "required": ["code"]
            }
        }
    }
}]}

# UNCOMMENT - to see how `get_project_info` works
# pprint(get_project_info('P5'))

sysprompt = 'You can use the tool get_project_info to retrieve project data.'
messages = [
    {'role': 'user', 'content': [{'text': 'Draft an email asking the contact about progress on Project P1.'}]},
]

res = client.converse(
    modelId='eu.amazon.nova-pro-v1:0',
    system=[{ "text": sysprompt }],
    toolConfig=tool_config,
    messages=messages
)

out_msg = res['output']['message']
pprint(out_msg)

# You can use these variables to extract tool call info.
tool_use = out_msg['content'][1]['toolUse']
project_code = tool_use['input']['code']

# UNCOMMENT - to see what `tool_use` and `project_code` are
# print('Tool use request:', tool_use)
# print('Project code:', project_code)

# YOUR CODE GOES HERE
