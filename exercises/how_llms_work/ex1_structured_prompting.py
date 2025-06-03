import boto3
import tqdm
from utils import accuracy_score, extract_output, get_attendance_id

session = boto3.Session(
    region_name='eu-west-1',
    aws_access_key_id=get_attendance_id(),
    aws_secret_access_key='<unused>',
)

client = session.client(
    service_name='bedrock-runtime', region_name='eu-west-1',
    endpoint_url='https://bedrock-runtime.aws-proxy.skillerwhale.com/'
)


with open('recipes.xml', 'r') as f:
    recipes = f.read()

sysprompt = """
    You will answer user queries about recipes.
    Here is the data:

    {recipes}
""".format(recipes=recipes)


usermsg = """
    Extract <name> and <prepTime> for each recipe.
"""
\
# for _ in range(5):
res = client.converse(
    modelId='eu.amazon.nova-pro-v1:0',
    system=[{ "text": sysprompt }],
    messages=[{
        "role": "user",
        "content": [{
            "text": usermsg
        }]
    }],
)

print(extract_output(res))
