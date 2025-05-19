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


# A synthetic dataset of emails with different classes
# The dataset contains business, personal, and spam emails
# The emails are labeled with their respective classes
email_data = [
    # Business emails (including some borderline/promotional tones)
    {'text': "Hello Team,\n\nOur vendor meeting is moved to May 7th, 2 PM. Agenda: contract renewal, pricing tiers, SLAs. Dial-in details in calendar invite.\n\n- Procurement", 'class': 'Business'},
    {'text': "Hi Jenna,\n\nThanks for your feedback on the draft. I've incorporated your edits on sections 2-4. Please review when you have a moment.\n\nBest,\nMark", 'class': 'Business'},
    {'text': "Reminder: Q3 budget submissions are due Friday. Use the template in SharePoint and cc finance@corp.com with any questions.", 'class': 'Business'},
    {'text': "Good morning,\n\nYour trial for our analytics dashboard ends tomorrow. To keep access, please upgrade to Pro by clicking here: https://app.example.com/upgrade\n\nRegards,\nSales", 'class': 'Business'},
    {'text': "Dear Ms. Li,\n\nAttached is the NDA for your review. Once signed, we can schedule the product demo.\n\nSincerely,\nLegal Dept.", 'class': 'Business'},
    {'text': "Hi all,\n\nFYI: Server maintenance planned this weekend. Expect 2-hour downtime starting Saturday 1 AM UTC. Apologies for inconvenience.\n\n- IT Ops", 'class': 'Business'},
    {'text': "Team,\n\nPlease submit your weekly timesheets by EOD Monday. Late entries will affect payroll processing.\n\nThanks,\nHR", 'class': 'Business'},
    {'text': "Hello,\n\nWe've noticed unusual activity on your account. Reply with confirmation code to secure it or contact support.\n\n- Account Security", 'class': 'Business'},
    {'text': "Hi Raj,\n\nCould you send me the latest customer survey results? I need them for the presentation next Wednesday.\n\nCheers,\nAna", 'class': 'Business'},

    # Personal emails (including some formal or ambiguous tones)
    {'text': "Hey Sophie,\n\nLoved catching up yesterday. Let's plan that weekend getaway soon—any ideas on where to go?\n\nLove,\nJess", 'class': 'Personal'},
    {'text': "Hi Dad,\n\nJust booked my tickets to visit over the bank holiday. Arriving May 24th morning. Can't wait!\n\n- Your son", 'class': 'Personal'},
    {'text': "Dear Kate,\n\nThanks for the recommendation. I started reading that novel and it's brilliant! Let's chat about it over coffee.\n\nXO,\nTina", 'class': 'Personal'},
    {'text': "Morning,\n\nI'll be out of office next week for vacation. For urgent matters, reach out to Sam or check the shared drive.\n\n- Alex", 'class': 'Personal'},
    {'text': "Hey,\n\nForgot to tell you: the cookies you dropped off were amazing. Mind sending me the recipe? \n\nCheers!", 'class': 'Personal'},
    {'text': "Hi Mom,\n\nJust planted the herbs you sent. Basil is thriving already! Thanks for thinking of me.\n\nLove you.", 'class': 'Personal'},
    {'text': "Yo Mike,\n\nGame night at my place Friday? BYOB and bring your A-game. Let me know if you're in.\n\n- Sam", 'class': 'Personal'},
    {'text': "Dear John,\n\nThanks for the help moving last weekend. Lunch is on me when you're free!\n\nBest,\nCarlos", 'class': 'Personal'},

    # Spam emails (including some that mimic legitimate notices)
    {'text': "Congratulations! Your invoice #12345 has an overpayment of £50. Click to claim your refund: http://refund.example.com", 'class': 'Spam'},
    {'text': "Alert: Unusual sign-in attempt detected. Verify your identity at secure-login.example.net to avoid account suspension.", 'class': 'Spam'},
    {'text': "You've been pre-approved for a low-interest loan up to £10,000. No credit check! Apply now: fastcash.ltd/apply", 'class': 'Spam'},
    {'text': "Final notice: Your subscription expires today. Renew immediately to continue enjoying premium features.", 'class': 'Spam'},
    {'text': "Earn £300/day working from home. Flexible hours, zero experience. Sign up here: homejobs.example.org", 'class': 'Spam'},
    {'text': "Exclusive offer! Buy 1 perfume, get 2 free. Limited stock. Visit deals.example.com before midnight.", 'class': 'Spam'},
    {'text': "Re: Payment\n\nPlease open the attached ZIP to review your overdue invoice. Invoice2025.zip", 'class': 'Spam'},
    {'text': "Hi,\n\nI'm a representative of a foreign embassy. Need your details to transfer $5M. Send account info ASAP.\n\nRegards,\nAmbassador", 'class': 'Spam'},
]

# YOUR CODE GOES HERE
# Modify the system prompt to classify emails appropriately.
sysprompt = [
    'You are a text classifier.',
    'Classify the following text into the following 3 classes: Business, Personal, Spam',
]
sysprompt = '\n'.join(sysprompt)

# Limit the number of examples for testing,
# TODO: Once you are happy with the system prompt, you can comment this line.
email_data = email_data[:1]


# <<< DO NOT CHANGE THE LINES BELOW HERE >>>
print('Classifying emails...')
y_pred = []
for email in tqdm.tqdm(email_data):
    # Call model to classify emails
    res = client.converse(
        modelId='eu.amazon.nova-lite-v1:0',
        # The system prompt contains the instructions for the model
        system=[{ "text": sysprompt }],
        # The user prompt contains the text to classify
        messages=[{
            "role": "user",
            "content": [{
                "text": email['text']
            }]
        }]
    )
    y_pred.append(res)


# Extract the predicted labels from the model's response
y_pred_labels = [extract_output(y) for y in y_pred]

# Print the predicted labels
y_true = [d['class'] for d in email_data]

print('Predicted labels:')
print('-' * 50)
print('True label -> Predicted label')
for i, (true, pred) in enumerate(zip(y_true, y_pred_labels)):
    print(f'{i+1}: {true} -> {pred}')

print('-' * 50)
print(f'Accuracy: {accuracy_score(y_true, y_pred_labels):.2}')

