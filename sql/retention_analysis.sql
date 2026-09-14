-- BigQuery Standard SQL
-- Replace `portfolio.events` with the table containing the synthetic event data.

WITH first_open AS (
  SELECT
    user_id,
    DATE(MIN(event_timestamp)) AS acquisition_date,
    ARRAY_AGG(acquisition_channel ORDER BY event_timestamp LIMIT 1)[OFFSET(0)] AS channel
  FROM `portfolio.events`
  WHERE event_name = 'first_open'
  GROUP BY user_id
),

daily_activity AS (
  SELECT DISTINCT
    user_id,
    DATE(event_timestamp) AS activity_date
  FROM `portfolio.events`
  WHERE event_name IN ('session_start', 'screen_view')
),

retention_flags AS (
  SELECT
    f.user_id,
    f.acquisition_date,
    f.channel,
    MAX(IF(DATE_DIFF(a.activity_date, f.acquisition_date, DAY) = 1, 1, 0)) AS retained_d1,
    MAX(IF(DATE_DIFF(a.activity_date, f.acquisition_date, DAY) = 3, 1, 0)) AS retained_d3,
    MAX(IF(DATE_DIFF(a.activity_date, f.acquisition_date, DAY) = 7, 1, 0)) AS retained_d7,
    MAX(IF(DATE_DIFF(a.activity_date, f.acquisition_date, DAY) = 30, 1, 0)) AS retained_d30
  FROM first_open f
  LEFT JOIN daily_activity a USING (user_id)
  GROUP BY 1, 2, 3
)

SELECT
  acquisition_date,
  channel,
  COUNT(*) AS acquired_users,
  AVG(retained_d1) AS d1_retention,
  AVG(retained_d3) AS d3_retention,
  AVG(retained_d7) AS d7_retention,
  AVG(retained_d30) AS d30_retention
FROM retention_flags
GROUP BY 1, 2
ORDER BY 1, 2;

