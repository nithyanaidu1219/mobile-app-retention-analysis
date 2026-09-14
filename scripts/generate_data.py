from pathlib import Path

import numpy as np
import pandas as pd


SEED = 1219
N_USERS = 10000


def main() -> None:
    rng = np.random.default_rng(SEED)
    root = Path(__file__).resolve().parents[1]
    output = root / "data" / "sample_users.csv"
    output.parent.mkdir(parents=True, exist_ok=True)

    channels = rng.choice(
        ["Organic", "Paid Social", "Search", "Referral"],
        size=N_USERS,
        p=[0.35, 0.30, 0.20, 0.15],
    )
    acquisition_date = pd.Timestamp("2026-01-01") + pd.to_timedelta(
        rng.integers(0, 60, N_USERS), unit="D"
    )
    session_seconds = np.maximum(5, rng.lognormal(mean=4.5, sigma=1.0, size=N_USERS)).astype(int)

    channel_quality = pd.Series(channels).map(
        {"Organic": 0.08, "Paid Social": -0.03, "Search": 0.03, "Referral": 0.10}
    ).to_numpy()
    engagement = np.clip(np.log1p(session_seconds) / 10, 0, 0.65)

    registered = rng.random(N_USERS) < np.clip(0.42 + channel_quality + engagement * 0.35, 0.1, 0.95)
    activated = registered & (rng.random(N_USERS) < np.clip(0.50 + engagement * 0.45, 0.1, 0.95))

    p_d1 = np.clip(0.08 + channel_quality + engagement * 0.35 + activated * 0.10, 0.02, 0.75)
    p_d3 = np.clip(p_d1 * 0.78, 0.01, 0.60)
    p_d7 = np.clip(p_d1 * 0.60, 0.01, 0.50)
    p_d30 = np.clip(p_d1 * 0.34, 0.005, 0.30)

    data = pd.DataFrame(
        {
            "user_id": [f"U{i:06d}" for i in range(1, N_USERS + 1)],
            "acquisition_date": acquisition_date,
            "channel": channels,
            "first_session_seconds": session_seconds,
            "registered": registered.astype(int),
            "activated": activated.astype(int),
            "retained_d1": (rng.random(N_USERS) < p_d1).astype(int),
            "retained_d3": (rng.random(N_USERS) < p_d3).astype(int),
            "retained_d7": (rng.random(N_USERS) < p_d7).astype(int),
            "retained_d30": (rng.random(N_USERS) < p_d30).astype(int),
        }
    ).sort_values(["acquisition_date", "user_id"])

    data.to_csv(output, index=False)
    print(f"Created {len(data):,} synthetic users at {output}")


if __name__ == "__main__":
    main()

