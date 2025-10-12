"""
Main application - Interactive coding assistant with ensemble of agents.
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from magnet.nets.coding_net.config.loader import load_config
from magnet.nets.coding_net.agent.ensemble import run_ensemble
from magnet.nets.coding_net.agent.prompts import CODING_AGENT_PROMPT


def print_result(result: dict, verbose: bool = False):
    """Print the ensemble result in a user-friendly format."""
    print("\n" + "="*80)
    
    if 'error' in result:
        print(f"❌ ERROR: {result['error']}")
        return
    
    # Check consensus
    if result.get('meets_consensus', True):
        print(f"✅ CONSENSUS REACHED: {result.get('consensus_percentage', 0):.1f}%")
    else:
        print(f"⚠️  LOW CONSENSUS: {result.get('consensus_percentage', 0):.1f}%")
    
    print("="*80)
    print("\n📝 FINAL ANSWER:\n")
    print(result.get('final_answer', 'No answer'))
    print("\n" + "="*80)
    
    # Print metadata
    if 'metadata' in result and verbose:
        print("\n📊 METADATA:")
        meta = result['metadata']
        print(f"  • Agents executed: {meta.get('num_agents_executed', 0)}")
        print(f"  • Successful responses: {meta.get('num_successful_responses', 0)}")
        print(f"  • Execution time: {meta.get('execution_time_seconds', 0):.2f}s")
        print(f"  • Avg response time: {meta.get('avg_response_time', 0):.2f}s")
        print(f"  • Temperature range: {meta.get('temperature_range', [])}")
        print(f"  • Aggregation method: {meta.get('aggregation_method', 'unknown')}")
    
    # Print response distribution
    if 'clusters' in result and verbose:
        print(f"\n📈 RESPONSE DISTRIBUTION:")
        for i, cluster in enumerate(result['clusters'][:3], 1):
            print(f"  {i}. {cluster['count']} agents ({cluster['percentage']:.1f}%)")
            if i == 1:
                print(f"     Preview: {cluster['response'][:100]}...")


async def interactive_mode(config):
    """Run interactive Q&A session."""
    print("="*80)
    print("🤖 Coding Assistant Ensemble")
    print("="*80)
    print(f"Configuration: {config.num_agents} agents, {config.aggregation_method} aggregation")
    print("Type 'exit' or 'quit' to end the session")
    print("="*80)
    
    while True:
        try:
            # Get user input
            question = input("\n💬 Your question: ").strip()
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not question:
                continue
            
            print(f"\n⏳ Running ensemble with {config.num_agents} agents...")
            
            # Run ensemble
            result = await run_ensemble(question, config, CODING_AGENT_PROMPT)
            
            # Print result
            print_result(result, verbose=True)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


async def single_question_mode(question: str, config):
    """Answer a single question and exit."""
    print(f"⏳ Running ensemble with {config.num_agents} agents...")
    
    result = await run_ensemble(question, config, CODING_AGENT_PROMPT)
    print_result(result, verbose=True)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Coding Assistant with Ensemble of Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with default config
  python -m magnet.nets.coding_net.app
  
  # Use a specific profile
  python -m magnet.nets.coding_net.app --profile quick_test
  
  # Override number of agents
  python -m magnet.nets.coding_net.app --num-agents 50
  
  # Single question mode
  python -m magnet.nets.coding_net.app --question "How to sort a list in Python?"
  
  # Custom config file
  python -m magnet.nets.coding_net.app --config my_config.yaml
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom config YAML file'
    )
    
    parser.add_argument(
        '--profile',
        type=str,
        choices=['quick_test', 'development', 'production', 'high_accuracy', 'high_diversity'],
        help='Use a predefined configuration profile'
    )
    
    parser.add_argument(
        '--num-agents',
        type=int,
        help='Override number of agents'
    )
    
    parser.add_argument(
        '--max-concurrent',
        type=int,
        help='Override max concurrent executions'
    )
    
    parser.add_argument(
        '--min-consensus',
        type=int,
        help='Override minimum consensus percentage (0-100)'
    )
    
    parser.add_argument(
        '--question',
        type=str,
        help='Ask a single question and exit (non-interactive mode)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config(config_path=args.config, profile=args.profile)
        
        # Apply overrides
        overrides = {}
        if args.num_agents:
            overrides['num_agents'] = args.num_agents
        if args.max_concurrent:
            overrides['max_concurrent'] = args.max_concurrent
        if args.min_consensus:
            overrides['min_consensus'] = args.min_consensus
        
        if overrides:
            config.override(**overrides)
        
    except Exception as e:
        print(f"❌ Error loading configuration: {str(e)}")
        sys.exit(1)
    
    # Run in appropriate mode
    try:
        if args.question:
            # Single question mode
            asyncio.run(single_question_mode(args.question, config))
        else:
            # Interactive mode
            asyncio.run(interactive_mode(config))
    
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
