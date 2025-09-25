import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from trl.models.utils import setup_chat_format
from time import perf_counter

device = "cpu"
checkpoint = "traiko-skillerwhale/smollm-email-funetine"

orig_tokenizer = AutoTokenizer.from_pretrained(checkpoint)
orig_model = AutoModelForCausalLM.from_pretrained(checkpoint, dtype=torch.float16).to(device)

orig_tokenizer.chat_template = None
model, tokenizer = setup_chat_format(model=orig_model, tokenizer=orig_tokenizer)

def converse(message):
    messages = [{"role": "user", "content": message}]
    input_text = tokenizer.apply_chat_template(messages, tokenize=False)
    inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
    
    outputs = model.generate(inputs, max_new_tokens=50, temperature=0.2, top_p=0.9, do_sample=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response


emails = [
    'How are you?',
    'Can I download and run the platform code?'
]

for email in emails:
    st = perf_counter()
    print(converse(f"<email>{email}</email>"))
    et = perf_counter()
    print('-' * 50)
    print(f'Total time {et - st:.3f}s')

