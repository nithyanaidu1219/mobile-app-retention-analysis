from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "sample_users.csv"
    output_dir = root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path, parse_dates=["acquisition_date"])
    if df["user_id"].duplicated().any():
        raise ValueError("Duplicate user_id values detected")

    df["session_band"] = pd.cut(
        df["first_session_seconds"],
        bins=[0, 10, 30, 60, 180, 360, 600, float("inf")],
        labels=["<10s", "10–29s", "30–59s", "1–3m", "3–6m", "6–10m", ">10m"],
        right=False,
    )

    channel_summary = (
        df.groupby("channel", observed=True)
        .agg(
            acquired_users=("user_id", "nunique"),
            registration_rate=("registered", "mean"),
            activation_rate=("activated", "mean"),
            d1_retention=("retained_d1", "mean"),
            d7_retention=("retained_d7", "mean"),
            d30_retention=("retained_d30", "mean"),
        )
        .reset_index()
    )
    channel_summary.to_csv(output_dir / "channel_summary.csv", index=False)

    session_summary = (
        df.groupby("session_band", observed=True)
        .agg(users=("user_id", "nunique"), d1_retention=("retained_d1", "mean"), d7_retention=("retained_d7", "mean"))
        .reset_index()
    )
    session_summary.to_csv(output_dir / "session_engagement_summary.csv", index=False)

    sns.set_theme(style="whitegrid")
    chart = sns.barplot(data=session_summary, x="session_band", y="d1_retention", color="#246BFD")
    chart.set(title="D1 Retention by First-Session Duration", xlabel="First-session duration", ylabel="D1 retention")
    chart.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    plt.tight_layout()
    plt.savefig(output_dir / "d1_retention_by_session.png", dpi=160)
    plt.close()

    print(channel_summary.to_string(index=False))


if __name__ == "__main__":
    main()

