import boto3
import time
from botocore.exceptions import ClientError
from utils import get_attendance_id


# Exercise 4 - Streaming/Blocking
#
# PART 1
#   * Run this script and make note of how long it takes to get a response from the LLM.
#
# PART 2
#   * Uncomment the rest of `user_messages` and run the for-loop.
#       * Is there a noticeable difference in time-to-first token for each message?
#

model_id = "eu.amazon.nova-pro-v1:0"

session = boto3.Session(
    region_name='eu-west-1',
    aws_access_key_id=get_attendance_id(),
    aws_secret_access_key='<unused>',
)

client = session.client(
    service_name='bedrock-runtime', region_name='eu-west-1',
    endpoint_url='https://bedrock-runtime.aws-proxy.skillerwhale.com/'
)


# PART 2 - Uncomment the rest of `user_messages`.
user_messages = [
    "Explain the major limitations of LLMs.",
    # "Write Clojure code to find the shortest route between two points in a network. Be concise.",
    # "What is the smallest species of whale?"
]


for user_message in user_messages:
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    times_per_chunk = []

    # STREAMING
    try:
        # Send the message to the model, using a basic inference configuration.
        streaming_response = client.converse_stream(
            modelId=model_id,
            messages=conversation
        )

        start_time = time.perf_counter()

        if len(user_messages) == 1:
            print('LLM Response, streamed:')
            print('-' * 50)

        # Extract and print the streamed response text in real-time.
        for chunk in streaming_response["stream"]:
            if "contentBlockDelta" in chunk:
                text = chunk["contentBlockDelta"]["delta"]["text"]

                if len(user_messages) == 1:
                    # only print if we're testing a single message
                    print(text, end="", flush=True)

                times_per_chunk.append(time.perf_counter() - start_time)
                start_time = time.perf_counter()

        if len(user_messages) == 1:
            print()
            print('-' * 50)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)


    # BLOCKING
    if len(user_messages) == 1:
        print('LLM Response, blocking:')
        print('-' * 50)

    start_time_block = time.perf_counter()
    blocking_response = client.converse(
        modelId=model_id,
        messages=conversation,
    )
    total_time_block = time.perf_counter() - start_time_block

    if len(user_messages) == 1:
        print(blocking_response['output']['message']['content'][0]['text'])
        print('-' * 50)

    print()
    print()
    print('Message: ', user_message)
    print(f'Time to first chunk (streamed): {times_per_chunk[0]:.4f}')
    print(f'Time to full output (blocking): {total_time_block:.4f}')
    print('-' * 50)

