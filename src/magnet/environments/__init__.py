"""Adapted from τ-bench https://arxiv.org/abs/2406.12045"""

from typing import Optional, Union
from magnet.environments.base import Env, EnvProtocol
from magnet.environments.user import UserStrategy


def get_env(
    env_name: str,
    user_strategy: Union[str, UserStrategy],
    user_model: str,
    task_split: str,
    user_provider: Optional[str] = None,
    task_index: Optional[int] = None,
    n_distractors: Optional[int] = None,
    wrap_index: bool = False,
) -> Env:
    if env_name == "retail":
        from magnet.environments.retail import MockRetailDomainEnv

        return MockRetailDomainEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "airline":
        from magnet.environments.airline import MockAirlineDomainEnv

        return MockAirlineDomainEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "combined":
        from magnet.environments.combined import CombinedEnv

        return CombinedEnv(
            n_distractors=n_distractors,
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "spotify":
        from magnet.environments.noisy.spotify import MockSpotifyDomainEnv

        return MockSpotifyDomainEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "techsupport":
        from magnet.environments.noisy.techsupport import MockTechSupportEnv

        return MockTechSupportEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "financialadvisor":
        from magnet.environments.noisy.financialadvisor import MockFinancialAdvisorEnv

        return MockFinancialAdvisorEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "automotive":
        from magnet.environments.noisy.automotive import MockAutomotiveDomainEnv

        return MockAutomotiveDomainEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "homeimprovement":
        from magnet.environments.noisy.homeimprovement import MockHomeImprovementEnv

        return MockHomeImprovementEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "pharmacy":
        from magnet.environments.noisy.pharmacy import MockPharmacyEnv

        return MockPharmacyEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    elif env_name == "restaurant":
        from magnet.environments.noisy.restaurant import MockRestaurantEnv

        return MockRestaurantEnv(
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_provider,
            task_index=task_index,
            wrap_index=wrap_index,
        )
    else:
        raise ValueError(f"Unknown environment: {env_name}")


__all__ = [
    "Env",
    "EnvProtocol",
    "get_env",
]
