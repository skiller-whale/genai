from utils import bprint, extract_output_and_reasoning, get_bedrock_client
import re
import tqdm
from time import perf_counter


sysprompt = """

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
    Query: I'm not sure if I need to renew, upgrade, or fix something on my subscription.
"""


client = get_bedrock_client()

N_TRIALS = 5
classes = []
times = []

print('=' * 50)
for i in tqdm.tqdm(range(N_TRIALS)):
    start_time = perf_counter()
    res = client.converse(
        modelId='eu.anthropic.claude-haiku-4-5-20251001-v1:0',
        system=[{ "text": sysprompt }],
        messages=[{"role": "user", "content": [{"text": chat}]}],
        inferenceConfig={
            'temperature': 0.0
        },
        additionalModelRequestFields={
            "reasoning_config": {
                "type": "disabled",
                # "budget_tokens": 1024
            }
        }
    )
    times.append(perf_counter() - start_time)

    reasoning, out = extract_output_and_reasoning(res)

    print('\n')
    bprint('Reasoning:')
    print('-' * 20)
    print(reasoning)
    print('-' * 20)
    bprint('Assistant:')
    print('-' * 20)
    print(out)
    print('\n')
    print('=' * 50)

    if match_ := re.search(r"Department:\s*([A-Za-z ]+)", out):
        class_ = match_.group(1).strip()
        classes.append(class_)

print('--------------------------------------------------')
print('Samples:', classes)
print('Classes:', set(classes))
print('Ratio of each class:', [
    f'{classes.count(c) / len(classes):.3f}' for c in set(classes)
])
print('Average inference time:', sum(times) / len(times))
print('Total time:', sum(times))
print()
