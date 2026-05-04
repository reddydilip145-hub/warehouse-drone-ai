from __future__ import annotations


DATASET_SCALE_TIERS = {
    "demo": 250,
    "mvp": 10_000,
    "mvp_100k": 100_000,
    "production": 200_000,
    "enterprise": 500_000,
}

DEFAULT_DATASET_TIER = "mvp_100k"
TARGET_ACCURACY = 0.98
