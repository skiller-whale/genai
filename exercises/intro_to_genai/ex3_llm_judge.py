import numpy as np
import boto3
import tqdm
from utils import extract_output, bprint, get_attendance_id

session = boto3.Session(
    region_name='eu-central-1',
    aws_access_key_id=get_attendance_id(),
    aws_secret_access_key='<unused>',
)

client = session.client(
    service_name='bedrock-runtime', region_name='eu-central-1',
    endpoint_url='https://bedrock-runtime.aws-proxy.skillerwhale.com/'
)

# An example company policy document
company_policy = """
- Security: We enforce multi-layered protection including encryption at rest and in transit, regular vulnerability assessments, and strict access controls.
- Availability: Our platform guarantees 99.9% uptime via redundant systems, automated failover, and real-time monitoring.
- Data Privacy: Customer data is isolated per account, backed up daily, and only accessed by authorized personnel under strict audit trails.
- Compliance: We maintain certifications for ISO 27001, SOC 2 Type II, and GDPR; regular third-party audits ensure ongoing adherence.
- Support: 24/7 support via email and chat with a maximum initial response time of 1 hour; priority handling for critical incidents.
- Incident Response: Documented response plans with predefined escalation paths; customers are notified within 30 minutes of any major outage.
- Acceptable Use: Prohibit abusive, illegal, or insecure content; resources may be suspended after warning if policy violations occur.
"""

# Example questions and answers based on the company policy
# The questions are designed to test the LLM's understanding of the policy document.
# The answers are the expected responses based on the policy document.
example_questions = [
    {'question': 'What security measures does the platform enforce?',
     'answer': 'We enforce multi-layered protection including encryption at rest and in transit, regular vulnerability assessments, and strict access controls.'},
    {'question': 'What uptime guarantee does the platform provide?',
     'answer': 'We guarantee 99.9% uptime via redundant systems, automated failover, and real-time monitoring.'},
    {'question': 'How often is customer data backed up?',
     'answer': 'Customer data is backed up daily.'},
    {'question': 'Who is authorized to access customer data?',
     'answer': 'Only authorized personnel under strict audit trails may access customer data.'},
    {'question': 'Which compliance certifications does the company maintain?',
     'answer': 'We maintain certifications for ISO 27001, SOC 2 Type II, and GDPR.'},
    {'question': 'How are compliance standards ensured?',
     'answer': 'Through regular third-party audits to ensure ongoing adherence.'},
    {'question': 'What support options are available and what is the response time?',
     'answer': 'We offer 24/7 support via email and chat with a maximum initial response time of 1 hour, with priority handling for critical incidents.'},
    {'question': 'What does the incident response plan include?',
     'answer': 'Documented response plans with predefined escalation paths.'},
    {'question': 'How quickly will customers be notified of a major outage?',
     'answer': 'Customers are notified within 30 minutes of any major outage.'},
    {'question': 'What content is prohibited under the acceptable use policy?',
     'answer': 'Abusive, illegal, or insecure content is prohibited, and resources may be suspended after warning if policy violations occur.'}
]

# TODO: Comment out to judge all questions.
example_questions = example_questions[:3]

# A judge system prompt for the LLM
# The judge system prompt is used to evaluate the responses of the LLM to the questions above.
JUDGE_SYSPROMPT = """\
OUTPUT ONLY A NUMBER ON A SCALE OF 1 TO 10.
You are comparing a submitted answer to an expert answer on a given question.

Compare the factual content of the submitted answer with the expert answer.
Ignore any differences in style, grammar, or punctuation.

Be extremely harsh about any factual errors or made-up data.
"""

# A template for the judge message prompt
# The judge message prompt is used to format the input data for the LLM.
# This is needed to delimit the different sections of the input data.
# The input data includes the question, the expected answer, and the submitted answer.
JUDGE_MSG_PROMPT = """
Here is the data:
[BEGIN DATA]
************
[Question]: {input}
************
[Expert]: {expected}
************
[Submission]: {output}
************
[END DATA]
"""

# A system prompt for the LLM that answers questions without any context.
# It should receive quite a poor score from the judge!
# It has no access to the company policy document and is expected to make up answers.
no_context_llm_sysprompt = """
Answer the following question in 1 sentence. If you don't know the answer, then make up some details.

Make sure to always answer it confidently, even if you don't know the answer. Do not use words
like "perhaps", "likely", "maybe", etc. or punctuation like "...".
Do not admit that you cannot or do not know the answer.
"""

# Generate answers to the example questions using the LLM without any context.
bprint('Generating answers without context...')
resp = []
for data in tqdm.tqdm(example_questions):
    resp.append(
        client.converse(
            modelId='eu.amazon.nova-micro-v1:0',
            # The LLM does not have access to the company policy document.
            system=[{ "text": no_context_llm_sysprompt }],
            messages=[{"role": "user", "content": [{"text": data['question']}]}]
        )
    )

resp_text = [extract_output(r) for r in resp]

bprint('No context LLM responses:')
print('=' * 50)
print()

scores = []

# Judge the responses from the LLM without any context.
for i, r in enumerate(resp_text):
    judge_resp = client.converse(
        modelId='eu.amazon.nova-lite-v1:0',
        system=[{ "text": JUDGE_SYSPROMPT }],
        messages=[{
            "role": "user",
            "content": [{
                "text": JUDGE_MSG_PROMPT.format(
                    input=example_questions[i]['question'],
                    expected=example_questions[i]['answer'],
                    output=r
                )
            }]
        }]
    )

    try:
        resp = extract_output(judge_resp).split('\n')[0].strip()
        scores.append(int(resp))
    except ValueError:
        pass

    judge_resp_text = extract_output(judge_resp)
    bprint(f'Question: {example_questions[i]["question"]}')
    bprint('Answer: ', end='')
    print(r)

    bprint('Expert answer: ', end='')
    print(example_questions[i]["answer"])

    bprint('Judge response: ', end='')
    print(judge_resp_text)

    print()
    print('-' * 50)
    print()

std_err = np.std(scores) / np.sqrt(len(scores))
bprint(f'Average score: {np.mean(scores):.3f} +- {std_err:.3f}')
