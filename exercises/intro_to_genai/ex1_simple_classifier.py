# =========================================================
# (FAKE) TEXT MESSAGE DATA
#
# The two lists contain fake spam/non-spam text messages.
# =========================================================

spam_texts = [
    "Congratulations! You've been selected for a $1,000 Walmart gift card. Click here to claim: http://bit.ly/FreeGift2025",
    "Alert: Your bank account has unusual activity. Verify your identity now at http://secure-bank-login.example.com to avoid suspension.",
    "Get a low-interest personal loan with no credit check! Apply today at http://easyloan.example.com and get approved in minutes.",
    "URGENT: Your parcel delivery could not be completed. Confirm your address here to reschedule: http://delivery-update.example.com",
    "You have an unpaid parking ticket. Pay now to avoid fines: http://pay-parking-fine.example.com/payment"
]

not_spam_texts = [
    "Hey Sarah, it's Tom. Just wanted to see if you're free for coffee tomorrow around 2 PM?",
    "Your prescription from Maple Pharmacy is ready for pickup. Please show this message at the counter. Thank you!",
    "Reminder: Dental appointment with Dr. Lee on May 10 at 3:30 PM at Smile Bright Clinic.",
    "Your Amazon order #123-4567890-1234567 has shipped and will arrive on May 5. Track here: https://amazon.com/track/1234567",
    "Your 2FA code for GitHub is 789012. It will expire in 10 minutes."
]

example_text = 'free gift claim a free gift http://bit.ly/gift4u'

# =========================================================
# Utility functions - extract bag of words from a text.
# =========================================================

bprint = lambda x, end='\n': print(f'\033[1m{x}\033[0m', end=end)

def extract_bag_of_words(text):
    """Extract a bag of words model from a text."""
    words = {}
    for word in text.split(' '):
        word = word.lower().strip()
        words[word] = words.get(word, 0) + 1
    return words


bow_spam_texts = [extract_bag_of_words(text) for text in spam_texts]
bow_not_spam_texts = [extract_bag_of_words(text) for text in not_spam_texts]

print('=' * 100)
bprint('Extracting bag of words')
print('')

bprint(f'{"When text is":<15}\t', end='')
print(example_text)

bprint(f'{"Bag of words is":<15}\t', end='')
print(extract_bag_of_words(example_text))
print('=' * 100)


# =========================================================
# Simple classifier based on word counts in a text message.
# =========================================================

def spam_model(word_counts):
    """
    Predict whether a text message is spam.

    A VERY BAD MODEL.
    """
    spam_score = \
        10.5 * word_counts.get('gift', 0) + \
        5.25 * word_counts.get('fine', 0) + \
        20.0 * word_counts.get('loan', 0) + \
        7.0 * word_counts.get('amazon', 0) - \
        3.0  * word_counts.get('coffee', 0)

    if spam_score > 5:
        return 'spam'
    else:
        return 'not spam'


# =========================================================
# Print accuracy
# =========================================================

n_correct = 0
for bow in bow_spam_texts:
    if spam_model(bow) == 'spam':
        n_correct += 1

for bow in bow_not_spam_texts:
    if spam_model(bow) == 'not spam':
        n_correct += 1

accuracy = n_correct / (len(spam_texts) + len(not_spam_texts))

print('')
bprint(f'Accuracy (# of correct/# of examples): {accuracy}')
print('')


# =========================================================
# Print predictions
# =========================================================

bprint('Model Predictions')
bprint('Should be spam:\n')
for text, bow in zip(spam_texts, bow_spam_texts):
    pred = spam_model(bow)

    bprint(f'{pred:<10} \t', end='')
    print(text)

bprint('\nShould be NOT spam:\n')
for text, bow in zip(not_spam_texts, bow_not_spam_texts):
    pred = spam_model(bow)

    bprint(f'{pred:<10} \t', end='')
    print(text)


print('=' * 100)
