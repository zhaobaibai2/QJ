from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_ijmlc_diagnostics import apply_action_filter


class FakeWrapper:
    def __init__(self, *, min_ttc: float, speed_kmh: float):
        self.env = SimpleNamespace(agent=SimpleNamespace(speed_km_h=speed_kmh))
        self._min_ttc = min_ttc

    def _ttc_risk(self):
        return 0.0, self._min_ttc


def args(action_filter: str) -> Namespace:
    return Namespace(
        action_filter=action_filter,
        rss_hard_ttc=3.5,
        rss_soft_ttc=6.0,
        rss_target_speed_kmh=20.0,
        runtime_ttc_threshold=12.0,
        runtime_hard_ttc=7.2,
        runtime_target_speed_kmh=18.0,
    )


def run_filter(action_filter: str, *, min_ttc: float, speed_kmh: float, accel: float = 0.8):
    env = SimpleNamespace(env=FakeWrapper(min_ttc=min_ttc, speed_kmh=speed_kmh))
    return apply_action_filter(env, np.asarray([0.0, accel], dtype=np.float32), args(action_filter))


def test_runtime_ttc_filter_only_counts_ttc_intervention():
    action, intervention, soft, hard, overspeed = run_filter("runtime_ttc", min_ttc=5.0, speed_kmh=10.0)

    assert action[1] == -1.0
    assert (intervention, soft, hard, overspeed) == (1, 0, 1, 0)


def test_runtime_speed_filter_only_counts_overspeed_intervention():
    action, intervention, soft, hard, overspeed = run_filter("runtime_speed", min_ttc=20.0, speed_kmh=25.0)

    assert action[1] == -0.35
    assert (intervention, soft, hard, overspeed) == (1, 0, 0, 1)


def test_runtime_ttc_speed_filter_combines_ttc_and_speed_guards():
    action, intervention, soft, hard, overspeed = run_filter("runtime_ttc_speed", min_ttc=10.0, speed_kmh=19.0)

    assert action[1] == -0.6
    assert (intervention, soft, hard, overspeed) == (1, 1, 0, 0)
