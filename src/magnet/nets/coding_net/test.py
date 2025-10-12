"""
Test script for coding_net ensemble.
Quick test to verify the system works correctly.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from magnet.nets.coding_net.config.loader import load_config
from magnet.nets.coding_net.agent.ensemble import run_ensemble
from magnet.nets.coding_net.agent.prompts import CODING_AGENT_PROMPT


async def test_quick():
    """Quick test with 5 agents."""
    print("="*80)
    print("🧪 Testing Ensemble System - Quick Test (5 agents)")
    print("="*80)
    
    # Load config and override for quick test
    config = load_config(profile='quick_test')
    config.override(num_agents=5, max_concurrent=5)
    
    print(f"\nConfig: {config.num_agents} agents, {config.aggregation_method} aggregation")
    
    question = "What is a Python list comprehension? Give a simple example."
    
    print(f"\nQuestion: {question}")
    print(f"\n⏳ Running {config.num_agents} agents...")
    
    result = await run_ensemble(question, config, CODING_AGENT_PROMPT)
    
    print("\n" + "="*80)
    print("📊 RESULTS")
    print("="*80)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"\n✅ Consensus: {result.get('consensus_percentage', 0):.1f}%")
    print(f"Supporting agents: {result.get('num_supporting_agents', 0)}/{result.get('total_agents', 0)}")
    
    print(f"\n📝 Final Answer:")
    print("-"*80)
    print(result.get('final_answer', 'No answer'))
    print("-"*80)
    
    if 'metadata' in result:
        meta = result['metadata']
        print(f"\n⏱️  Execution time: {meta.get('execution_time_seconds', 0):.2f}s")
        print(f"✓  Successful responses: {meta.get('num_successful_responses', 0)}")
    
    print("\n" + "="*80)
    print("✅ Test completed successfully!")
    print("="*80)
    
    return True


async def test_config_loading():
    """Test configuration loading."""
    print("\n🧪 Testing Configuration Loading...")
    
    # Test default config
    config = load_config()
    print(f"  ✓ Default config: {config.num_agents} agents")
    
    # Test profiles
    for profile in ['quick_test', 'development', 'production']:
        config = load_config(profile=profile)
        print(f"  ✓ Profile '{profile}': {config.num_agents} agents")
    
    # Test overrides
    config = load_config()
    config.override(num_agents=42, max_concurrent=7)
    assert config.num_agents == 42
    assert config.max_concurrent == 7
    print(f"  ✓ Override works: {config.num_agents} agents")
    
    print("  ✅ All config tests passed!")
    return True


async def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🚀 CODING_NET ENSEMBLE - TEST SUITE")
    print("="*80 + "\n")
    
    try:
        # Test 1: Configuration
        if not await test_config_loading():
            print("❌ Configuration test failed")
            return
        
        # Test 2: Quick ensemble run
        if not await test_quick():
            print("❌ Ensemble test failed")
            return
        
        print("\n" + "="*80)
        print("🎉 ALL TESTS PASSED!")
        print("="*80)
        print("\nYou can now use the system:")
        print("  python -m magnet.nets.coding_net.app")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
