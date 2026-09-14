# Mobile-App Retention & Funnel Analysis

## Project overview

This project analyses a fictional mobile application's acquisition, activation, early engagement, and cohort retention. It demonstrates an end-to-end senior analytics workflow: metric definition, data validation, SQL analysis, Python visualisation, interpretation, and business recommendations.

The dataset is entirely synthetic and does not contain employer, customer, or production data.

## Business questions

1. What percentage of acquired users register and become activated?
2. How do D1, D3, D7, and D30 retention differ by acquisition channel?
3. Does first-session duration predict stronger retention?
4. Which channels attract valuable users rather than simply producing installs?
5. Where should Product and Growth teams focus to improve retention?

## Metrics

| Metric | Definition |
|---|---|
| Acquisition | First app open by a new user |
| Registration rate | Registered users ÷ acquired users |
| Activation rate | Users completing the activation event ÷ acquired users |
| D1 retention | Users active one day after acquisition ÷ eligible acquired users |
| D7 retention | Users active seven days after acquisition ÷ eligible acquired users |
| D30 retention | Users active 30 days after acquisition ÷ eligible acquired users |
| Qualified first session | First session lasting at least 30 seconds |

## Repository structure

```text
data/sample_users.csv             Synthetic example data
scripts/generate_data.py          Reproducible dataset generator
scripts/analyse_retention.py      Python analysis and charts
sql/retention_analysis.sql        BigQuery-compatible cohort SQL
outputs/                          Generated tables and visualisations
```

## How to run

```bash
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/analyse_retention.py
```

## Analytical approach

- Validate user identifiers, acquisition dates, event dates, and duplicate records.
- Build acquisition cohorts by date and channel.
- Calculate registration, activation, and qualified-session rates.
- Calculate retention only when a cohort has completed the required observation window.
- Compare retention across first-session duration bands.
- Rank channels using downstream retention, not acquisition volume alone.

## Example insights to evaluate

- Channels with the most users may not produce the strongest D7 retention.
- Very short first sessions can indicate weak onboarding or mismatched acquisition targeting.
- A clear retention uplift after a particular engagement threshold can guide onboarding design.
- Campaign decisions should combine acquisition cost with activation and retained-user quality.

## Recommended business actions

1. Optimise campaigns using cost per retained user alongside CPI.
2. Test onboarding changes that help new users reach meaningful content faster.
3. Monitor event-tracking completeness before interpreting funnel drops.
4. Segment experiments by channel and first-session engagement.
5. Maintain a governed KPI dictionary so Product and Marketing use consistent definitions.

## Skills demonstrated

`SQL` · `Python` · `Pandas` · `BigQuery` · `Cohort Analysis` · `Retention` · `Funnels` · `Data Validation` · `Product Analytics` · `Growth Analytics` · `Business Communication`

