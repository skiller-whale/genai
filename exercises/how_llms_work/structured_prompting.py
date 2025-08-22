from utils import extract_output, get_bedrock_client


with open('recipes.xml', 'r') as f:
    recipes = f.read()


sysprompt = """
    You will answer user queries about recipes.

    Here is the data:

    {recipes}
""".format(recipes=recipes)


usermsg = "Extract <name> and <prepTime> for each recipe."


client = get_bedrock_client()
response = client.converse(
    modelId='eu.amazon.nova-pro-v1:0',
    system=[{ "text": sysprompt }],
    messages=[{"role": "user", "content": [{"text": usermsg}]}],
)

print(extract_output(response))
