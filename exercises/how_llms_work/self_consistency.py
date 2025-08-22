from utils import extract_output, get_bedrock_client
import re


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


client = get_bedrock_client()

N_TRIALS = 10

classes = []
for i in range(N_TRIALS):
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
    if i == 0:
        print('Example output:')
        print('--------------------------------------------------')
        print(out)
        print('--------------------------------------------------')
        print('Classifying queries...')

    if match_ := re.search(r"Department:\s*([A-Za-z ]+)", out):
        class_ = match_.group(1).strip()
        classes.append(class_)
        print(class_)


print('--------------------------------------------------')
print('Samples:', classes)
print('Classes:', set(classes))
print('Probabilities:', [
    f'{classes.count(c) / len(classes):.3f}' for c in set(classes)
])
print()
