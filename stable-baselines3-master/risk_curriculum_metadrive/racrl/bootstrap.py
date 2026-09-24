"""Local import and hardware checks used by every executable script."""

from __future__ import annotations

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent
LOCAL_METADRIVE_ROOT = REPO_ROOT / "metadrive"


def configure_runtime() -> None:
    """Prefer the supplied MetaDrive 0.4.3 source tree and stable cache paths."""
    if LOCAL_METADRIVE_ROOT.exists():
        path = str(LOCAL_METADRIVE_ROOT)
        if path not in sys.path:
            sys.path.insert(0, path)
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl-racrl")
    os.environ.setdefault("PYTHONHASHSEED", "0")


def assert_metadrive_version() -> str:
    configure_runtime()
    from metadrive.version import VERSION

    if VERSION != "0.4.3":
        raise RuntimeError(f"This project is validated for MetaDrive 0.4.3, found {VERSION}.")
    return VERSION


def resolve_device(device: str, require_gpu: bool = True) -> str:
    import torch

    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA was requested but PyTorch cannot access the GPU. "
            "Install a CUDA build compatible with the NVIDIA driver before training."
        )
    if require_gpu and not device.startswith("cuda"):
        raise RuntimeError("GPU execution is required for this experiment; pass --device cuda.")
    return device

