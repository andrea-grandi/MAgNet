"""
Utility script to show configuration options and profiles.
"""

import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from magnet.nets.coding_net.config.loader import load_config


def print_config_info():
    """Print information about available configurations."""
    
    print("="*80)
    print("⚙️  CODING_NET CONFIGURATION GUIDE")
    print("="*80)
    
    # Load default config
    config = load_config()
    
    print("\n📋 DEFAULT CONFIGURATION:")
    print("-"*80)
    print(f"  Agents: {config.num_agents}")
    print(f"  Model: {config.model}")
    print(f"  Max Concurrent: {config.max_concurrent}")
    print(f"  Parallel Execution: {config.parallel_execution}")
    print(f"  Temperature Range: {config.temperature_range}")
    print(f"  Aggregation Method: {config.aggregation_method}")
    print(f"  Min Consensus: {config.min_consensus}%")
    print(f"  Similarity Threshold: {config.similarity_threshold}")
    print(f"  Timeout: {config.timeout_seconds}s")
    
    # Show profiles
    print("\n🎯 AVAILABLE PROFILES:")
    print("-"*80)
    
    profiles = config.config.get('profiles', {})
    
    for profile_name, profile_config in profiles.items():
        print(f"\n  📌 {profile_name}")
        for key, value in profile_config.items():
            print(f"     {key}: {value}")
    
    print("\n💡 USAGE EXAMPLES:")
    print("-"*80)
    print("  # Use a profile:")
    print("  python -m magnet.nets.coding_net.app --profile quick_test")
    print("")
    print("  # Override specific values:")
    print("  python -m magnet.nets.coding_net.app --num-agents 50")
    print("")
    print("  # Combine profile + overrides:")
    print("  python -m magnet.nets.coding_net.app --profile production --num-agents 150")
    print("")
    print("  # Use custom config file:")
    print("  python -m magnet.nets.coding_net.app --config my_config.yaml")
    
    print("\n🔧 CONFIGURATION FILE LOCATION:")
    print("-"*80)
    print(f"  {config.config_path}")
    
    print("\n📊 SCALABILITY EXAMPLES:")
    print("-"*80)
    
    scenarios = [
        ("Quick Test", 10, 10, "~5s", "Basso"),
        ("Development", 50, 15, "~10s", "Medio"),
        ("Production", 100, 20, "~15s", "Medio-Alto"),
        ("High Accuracy", 200, 30, "~20s", "Alto"),
        ("Massive Scale", 500, 50, "~30s", "Molto Alto"),
    ]
    
    print(f"\n  {'Scenario':<20} {'Agenti':<10} {'Concurrent':<12} {'Tempo':<10} {'Costo'}")
    print("  " + "-"*72)
    for name, agents, concurrent, time, cost in scenarios:
        print(f"  {name:<20} {agents:<10} {concurrent:<12} {time:<10} {cost}")
    
    print("\n" + "="*80)
    print("💡 TIP: Start with 'quick_test' profile and scale up as needed!")
    print("="*80)
    print()


if __name__ == "__main__":
    print_config_info()
