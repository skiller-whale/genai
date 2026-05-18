"""
Utility functions for the GenAI exercises.
"""

import boto3
import os


def get_bedrock_client():
    session = boto3.Session(
        region_name='eu-west-1',
        aws_access_key_id=get_attendance_id(),
        aws_secret_access_key='<unused>',
    )
    return session.client(
        service_name='bedrock-runtime', region_name='eu-west-1',
        endpoint_url='https://bedrock-runtime.aws-proxy.skillerwhale.com/'
    )


def get_attendance_id(env_var='SW_ATTENDANCE_ID'):
    """
    Get the attendance ID from an environment variable.

    Args:
        env_var (str): The environment variable name.
    Returns:
        str: The attendance ID."""

    attendance_id = os.getenv(env_var)

    if not attendance_id:
        raise ValueError(f"Attendance ID not found in environment variable '{env_var}'.")

    return attendance_id


def accuracy_score(y_true, y_pred):
    """
    Calculate the accuracy score.
    Args:
        y_true (list): True labels.
        y_pred (list): Predicted labels.
    Returns:
        float: Accuracy score."""
    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return correct / len(y_true) if y_true else 0.0


def extract_output(resp):
    """
    Extracts the output from the response of a GenAI model.
    Args:
        resp (dict): The response from the GenAI model.
    Returns:
        str: The extracted output text."""
    msg = resp['output']['message']['content']

    if len(msg) > 1:
        raise ValueError

    return msg[0]['text']


bprint = lambda x, end='\n': print(f'\033[1m{x}\033[0m', end=end)
