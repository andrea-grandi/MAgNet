#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from {{folder_name}}.net import {{crew_name}}

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# net locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the net.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        {{crew_name}}().net().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the net: {e}")


def train():
    """
    Train the net for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        {{crew_name}}().net().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the net: {e}")

def replay():
    """
    Replay the net execution from a specific task.
    """
    try:
        {{crew_name}}().net().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the net: {e}")

def test():
    """
    Test the net execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        {{crew_name}}().net().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the net: {e}")
