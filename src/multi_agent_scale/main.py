import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from net import StockAnalysisNet

def run():
    inputs = {
        'query': 'What is the company you want to analyze?',
        'company_stock': 'AMZN',
    }
    return StockAnalysisNet().net().kickoff(inputs=inputs)

def train():
    """
    Train the network for a given number of iterations.
    """
    inputs = {
        'query': 'What is last years revenue',
        'company_stock': 'AMZN',
    }
    try:
        StockAnalysisNet().net().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the network: {e}")
    

if __name__ == "__main__":
    print("## Welcome to Stock Analysis Net")
    print('-------------------------------')
    result = run()
    print("\n\n########################")
    print("## Here is the Report")
    print("########################\n")
    print(result)
