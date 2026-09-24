"""Experiment configuration and paper variants."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class RewardWeights:
    base_scale: float = 0.5
    ttc: float = 2.0
    lane: float = 0.5
    smooth: float = 0.02
    accel: float = 0.01
    cost: float = 20.0
    overspeed: float = 2.0
    target_speed_kmh: float = 20.0
    progress: float = 30.0
    idle_penalty: float = 0.15
    min_speed_kmh: float = 2.0
    success_bonus: float = 40.0
    crash_penalty: float = 80.0
    out_of_road_penalty: float = 80.0
    ttc_threshold: float = 5.0


@dataclass(frozen=True)
class CurriculumStage:
    name: str
    traffic_density: float
    map_blocks: int | str
    accident_prob: float
    horizon: int = 1000


DEFAULT_STAGES = (
    CurriculumStage("warmup", traffic_density=0.00, map_blocks="S", accident_prob=0.0, horizon=600),
    CurriculumStage("easy", traffic_density=0.03, map_blocks=3, accident_prob=0.0, horizon=800),
    CurriculumStage("medium", traffic_density=0.08, map_blocks=5, accident_prob=0.0, horizon=1000),
    CurriculumStage("prehard", traffic_density=0.12, map_blocks=6, accident_prob=0.0, horizon=1100),
    CurriculumStage("hard", traffic_density=0.15, map_blocks=7, accident_prob=0.0, horizon=1200),
)


@dataclass
class ExperimentConfig:
    variant: str = "proposed"
    algo: str = "ppo"
    seed: int = 0
    train_scenarios: int = 200
    test_scenarios: int = 100
    train_start_seed: int = 0
    test_start_seed: int = 10000
    horizon: int = 1000
    timesteps: int = 1_000_000
    n_envs: int = 16
    risk_reward: bool = True
    use_risk_reward: bool = True
    use_action_guard: bool = True
    use_gated_risk_reward: bool = False
    curriculum: bool = True
    fixed_traffic_density: float = 0.10
    fixed_map_blocks: int | str = 5
    reward_weights: RewardWeights = field(default_factory=RewardWeights)
    risk_gate_min_speed_kmh: float = 3.0
    risk_gate_min_route_progress: float = 1e-4
    risk_gate_lane_deviation: float = 0.25
    risk_gate_min_ttc_risk: float = 0.01
    stages: tuple[CurriculumStage, ...] = DEFAULT_STAGES
    curriculum_window: int = 30
    stage0_route_completion: float = 0.60
    stage0_cost: float = 0.25
    stage1_success: float = 0.30
    stage1_route_completion: float = 0.75
    stage1_cost: float = 0.35
    stage2_success: float = 0.25
    stage2_cost: float = 0.45
    demote_success: float = 0.05
    demote_route_completion: float = 0.65
    demote_cost: float = 0.45
    demote_grace_episodes: int = 40
    allow_demote: bool = True
    eval_episodes: int = 50
    eval_freq: int = 20_000
    policy_layers: tuple[int, ...] = (256, 256)
    ent_coef: float = 0.0
    learning_rate: float = 3e-4
    rcpo_lagrangian: bool = False
    rcpo_cost_limit: float = 0.25
    rcpo_lambda_init: float = 20.0
    rcpo_lambda_lr: float = 5.0
    rcpo_lambda_max: float = 200.0
    rcpo_update_window: int = 20

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def get_variant_config(variant: str, algo: str, seed: int, timesteps: int | None = None) -> ExperimentConfig:
    flags = {
        "baseline": (False, False, False),
        "risk": (True, True, False),
        "curriculum": (False, False, True),
        "proposed": (True, True, True),
        "proposed_wo_ttc": (True, True, True),
        "proposed_wo_lane": (True, True, True),
        "proposed_wo_smooth": (True, True, True),
        "proposed_gated_risk": (True, True, True),
        "reward_only": (True, True, True),
        "guard_only": (True, False, True),
        "no_action_guard": (True, True, True),
        "shield_only": (True, False, False),
        "rcpo_lagrangian": (True, True, True),
    }
    if variant not in flags:
        raise ValueError(f"Unknown variant {variant!r}; use one of {sorted(flags)}.")
    risk_reward, use_risk_reward, curriculum = flags[variant]
    use_action_guard = bool(risk_reward)
    if variant in {"reward_only", "no_action_guard", "rcpo_lagrangian"}:
        use_action_guard = False
    config = ExperimentConfig(
        variant=variant,
        algo=algo.lower(),
        seed=seed,
        risk_reward=risk_reward,
        use_risk_reward=use_risk_reward,
        use_action_guard=use_action_guard,
        use_gated_risk_reward=variant == "proposed_gated_risk",
        curriculum=curriculum,
    )
    if variant == "proposed_wo_ttc":
        config.reward_weights = RewardWeights(ttc=0.0)
    elif variant == "proposed_wo_lane":
        config.reward_weights = RewardWeights(lane=0.0)
    elif variant == "proposed_wo_smooth":
        config.reward_weights = RewardWeights(smooth=0.0, accel=0.0)
    elif variant == "proposed_gated_risk":
        config.reward_weights = RewardWeights(
            ttc=4.0,
            lane=1.0,
            cost=10.0,
            overspeed=3.0,
            target_speed_kmh=18.0,
            progress=40.0,
            success_bonus=55.0,
            crash_penalty=100.0,
            out_of_road_penalty=150.0,
            ttc_threshold=12.0,
        )
        config.ent_coef = 0.01
    elif variant == "rcpo_lagrangian":
        config.reward_weights = RewardWeights(
            ttc=0.0,
            lane=0.0,
            smooth=0.0,
            accel=0.0,
            cost=0.0,
            overspeed=0.0,
            target_speed_kmh=20.0,
            progress=30.0,
            idle_penalty=0.05,
            success_bonus=40.0,
            crash_penalty=0.0,
            out_of_road_penalty=0.0,
            ttc_threshold=5.0,
        )
        config.rcpo_lagrangian = True
        config.ent_coef = 0.01
    if timesteps is not None:
        config.timesteps = timesteps
    return config
