"""
Configuration loader for ensemble setup.
Loads and validates YAML configuration files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import os


class EnsembleConfig:
    """Load and manage ensemble configuration from YAML files."""
    
    def __init__(self, config_path: Optional[str] = None, profile: Optional[str] = None):
        """
        Initialize configuration loader.
        
        Args:
            config_path: Path to YAML config file. If None, uses default.
            profile: Profile name to use (quick_test, development, production, etc.)
        """
        if config_path is None:
            # Default config path
            config_dir = Path(__file__).parent
            self.config_path = config_dir / "ensemble_config.yaml"
        else:
            self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # Apply profile if specified
        if profile:
            self._apply_profile(profile)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _apply_profile(self, profile_name: str):
        """Apply a predefined profile to override settings."""
        profiles = self.config.get('profiles', {})
        
        if profile_name not in profiles:
            available = ', '.join(profiles.keys())
            raise ValueError(f"Profile '{profile_name}' not found. Available: {available}")
        
        profile = profiles[profile_name]
        
        # Override ensemble settings with profile values
        for key, value in profile.items():
            if key in self.config['ensemble']:
                self.config['ensemble'][key] = value
            elif key == 'temperature_range' and 'diversification' in self.config:
                self.config['diversification']['temperature_range'] = value
            elif key == 'min_consensus' and 'aggregation' in self.config:
                self.config['aggregation']['majority_vote']['min_consensus'] = value
    
    @property
    def num_agents(self) -> int:
        """Get number of agents to create."""
        return self.config['ensemble']['num_agents']
    
    @property
    def model(self) -> str:
        """Get model name."""
        return self.config['ensemble']['model']
    
    @property
    def max_concurrent(self) -> int:
        """Get max concurrent executions."""
        return self.config['ensemble']['max_concurrent']
    
    @property
    def parallel_execution(self) -> bool:
        """Check if parallel execution is enabled."""
        return self.config['ensemble']['parallel_execution']
    
    @property
    def temperature_range(self) -> tuple:
        """Get temperature range for diversification."""
        temp_range = self.config['diversification']['temperature_range']
        return tuple(temp_range)
    
    @property
    def vary_temperature(self) -> bool:
        """Check if temperature should vary."""
        return self.config['diversification']['vary_temperature']
    
    @property
    def aggregation_method(self) -> str:
        """Get aggregation method."""
        return self.config['aggregation']['method']
    
    @property
    def min_consensus(self) -> int:
        """Get minimum consensus percentage."""
        return self.config['aggregation']['majority_vote']['min_consensus']
    
    @property
    def similarity_threshold(self) -> float:
        """Get similarity threshold for comparing responses."""
        return self.config['aggregation']['majority_vote']['similarity_threshold']
    
    @property
    def timeout_seconds(self) -> int:
        """Get timeout in seconds."""
        return self.config['ensemble']['timeout_seconds']
    
    @property
    def min_successful_responses(self) -> int:
        """Get minimum successful responses required."""
        return self.config['ensemble']['min_successful_responses']
    
    @property
    def early_stopping(self) -> bool:
        """Check if early stopping is enabled."""
        return self.config['performance'].get('early_stopping', False)
    
    @property
    def early_stop_threshold(self) -> float:
        """Get early stopping threshold."""
        return self.config['performance'].get('early_stop_threshold', 0.9)
    
    @property
    def include_metadata(self) -> bool:
        """Check if metadata should be included in output."""
        return self.config['output']['include_metadata']
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def override(self, **kwargs):
        """
        Override configuration values at runtime.
        
        Example:
            config.override(num_agents=50, max_concurrent=10)
        """
        for key, value in kwargs.items():
            # Try to find and update the key in nested structure
            if key in self.config.get('ensemble', {}):
                self.config['ensemble'][key] = value
            elif key in self.config.get('diversification', {}):
                self.config['diversification'][key] = value
            elif key in self.config.get('aggregation', {}).get('majority_vote', {}):
                self.config['aggregation']['majority_vote'][key] = value
    
    def __repr__(self) -> str:
        """String representation."""
        return f"EnsembleConfig(agents={self.num_agents}, model={self.model}, method={self.aggregation_method})"


def load_config(config_path: Optional[str] = None, profile: Optional[str] = None) -> EnsembleConfig:
    """
    Load ensemble configuration.
    
    Args:
        config_path: Path to config file (optional)
        profile: Profile to use (optional)
    
    Returns:
        EnsembleConfig instance
    """
    return EnsembleConfig(config_path, profile)
