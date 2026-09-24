#!/usr/bin/env python
"""Validate hardware, imports and a short MetaDrive rollout."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from racrl.bootstrap import assert_metadrive_version, resolve_device  # noqa: E402
from racrl.config import get_variant_config  # noqa: E402
from racrl.envs import build_env  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-gpu", action="store_true")
    args = parser.parse_args()
    import torch

    version = assert_metadrive_version()
    device = resolve_device("cuda" if args.require_gpu else ("cuda" if torch.cuda.is_available() else "cpu"), args.require_gpu)
    print(f"MetaDrive={version} torch={torch.__version__} device={device} cuda={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU={torch.cuda.get_device_name(0)}")
    config = get_variant_config("proposed", "ppo", seed=0, timesteps=32)
    config.horizon = 20
    env = build_env(config, training=True)
    try:
        obs, _ = env.reset(seed=0)
        print(f"observation_shape={obs.shape} action_space={env.action_space}")
        info = {}
        for _ in range(5):
            obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
            if terminated or truncated:
                break
        print(f"step_reward={reward:.4f} risk_penalty={info.get('risk_penalty', 0):.4f}")
    finally:
        env.close()


if __name__ == "__main__":
    main()

