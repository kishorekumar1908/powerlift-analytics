"""
queries.py
----------
Centralized SQL queries for Python analytics.
"""

# ==========================================================
# Athlete Report
# ==========================================================

ATHLETE_REPORT = """
SELECT
    da.AthleteID,
    da.AthleteName,
    dd.FullDate AS CompetitionDate,

    fs.BodyweightKg,

    fs.Best3SquatKg,
    fs.Best3BenchKg,
    fs.Best3DeadliftKg,
    fs.TotalKg,
    fs.Dots,

    LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS PreviousTotal,
    fs.TotalKg - LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS TotalImprovement,
    MAX(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS CareerBestTotal,
    CASE
        WHEN LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) IS NULL THEN 1
        WHEN fs.TotalKg > MAX(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) THEN 1
        ELSE 0
    END AS IsPR,
    ROW_NUMBER() OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS CompetitionNumber,
    DATEDIFF(dd.FullDate, LAG(dd.FullDate) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate)) AS DaysSinceLastCompetition

FROM fact_results fs

JOIN dim_athlete da
    ON fs.AthleteKey = da.AthleteKey

JOIN dim_date dd
    ON fs.DateKey = dd.DateKey

WHERE da.AthleteID = %(athlete_id)s

ORDER BY dd.FullDate;
"""


STATISTICAL_DATA = """
SELECT
    fs.BodyweightKg,
    fs.Best3SquatKg,
    fs.Best3BenchKg,
    fs.Best3DeadliftKg,
    fs.TotalKg,
    fs.Dots,
    ROUND(fs.TotalKg / fs.BodyweightKg, 2) AS StrengthRatio,
    fs.TotalKg - LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS TotalImprovement,
    ROW_NUMBER() OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS CompetitionNumber,
    DATEDIFF(dd.FullDate, LAG(dd.FullDate) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate)) AS DaysSinceLastCompetition

FROM fact_results fs

JOIN dim_date dd
    ON fs.DateKey = dd.DateKey;
"""
# ==========================================================
# Yearly Trend
# ==========================================================

YEARLY_TOTALS = """
SELECT
    dd.Year,
    AVG(fs.TotalKg) AS AverageTotal
FROM fact_results fs

JOIN dim_date dd
    ON fs.DateKey = dd.DateKey

GROUP BY dd.Year
ORDER BY dd.Year;
"""

# ==========================================================
# Complete Dataset
# ==========================================================

ALL_RESULTS = """
SELECT

    da.AthleteID,
    da.AthleteName,
    da.Sex,

    dm.MeetName,

    dd.FullDate,

    fs.BodyweightKg,
    fs.Best3SquatKg,
    fs.Best3BenchKg,
    fs.Best3DeadliftKg,
    fs.TotalKg,
    fs.Dots,

    ROUND(fs.TotalKg / fs.BodyweightKg, 2) AS StrengthRatio,
    LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS PreviousTotal,
    fs.TotalKg - LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS TotalImprovement,
    MAX(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS CareerBestTotal,
    CASE
        WHEN LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) IS NULL THEN 1
        WHEN fs.TotalKg > MAX(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) THEN 1
        ELSE 0
    END AS IsPR,
    ROW_NUMBER() OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS CompetitionNumber,
    DATEDIFF(dd.FullDate, LAG(dd.FullDate) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate)) AS DaysSinceLastCompetition

FROM fact_results fs

JOIN dim_athlete da
    ON fs.AthleteKey = da.AthleteKey

JOIN dim_date dd
    ON fs.DateKey = dd.DateKey

JOIN dim_meet dm
    ON fs.MeetKey = dm.MeetKey;
"""

# ==========================================================
# Statistical / Correlation Analysis
# ==========================================================

CORRELATION_DATA = """
SELECT

    da.Sex,

    fs.BodyweightKg,

    fs.Best3SquatKg,
    fs.Best3BenchKg,
    fs.Best3DeadliftKg,

    fs.TotalKg,
    fs.Dots,

    ROUND(fs.TotalKg / fs.BodyweightKg, 2) AS StrengthRatio,
    fs.TotalKg - LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS TotalImprovement,
    ROW_NUMBER() OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS CompetitionNumber,
    DATEDIFF(dd.FullDate, LAG(dd.FullDate) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate)) AS DaysSinceLastCompetition

FROM fact_results fs

JOIN dim_athlete da
    ON fs.AthleteKey = da.AthleteKey

JOIN dim_date dd
    ON fs.DateKey = dd.DateKey;
"""

# ==========================================================
# Distribution Analysis
# ==========================================================

DISTRIBUTION_DATA = """
SELECT

    TotalKg,
    Dots,
    BodyweightKg,
    ROUND(TotalKg / BodyweightKg, 2) AS StrengthRatio

FROM fact_results;
"""

# ==========================================================
# Comparative Analysis
# ==========================================================

COMPARATIVE_DATA = """
SELECT

    da.Sex,
    de.EquipmentName,

    fs.Tested,

    fs.TotalKg,
    fs.Dots,

    fs.BodyweightKg,

    fs.Best3SquatKg,
    fs.Best3BenchKg,
    fs.Best3DeadliftKg,
    ROUND(fs.TotalKg / fs.BodyweightKg, 2) AS StrengthRatio,

    fs.TotalKg - LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS TotalImprovement

FROM fact_results fs

JOIN dim_athlete da
    ON fs.AthleteKey = da.AthleteKey

JOIN dim_equipment de
    ON fs.EquipmentKey = de.EquipmentKey

JOIN dim_date dd
    ON fs.DateKey = dd.DateKey;
"""

# ==========================================================
# Outlier Detection
# ==========================================================

OUTLIER_DATA = """
SELECT

    da.AthleteID,
    da.AthleteName,

    ROW_NUMBER() OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS CompetitionNumber,
    fs.TotalKg,
    fs.Dots,
    fs.TotalKg - LAG(fs.TotalKg) OVER (PARTITION BY fs.AthleteKey ORDER BY dd.FullDate) AS TotalImprovement

FROM fact_results fs

JOIN dim_athlete da
    ON fs.AthleteKey = da.AthleteKey

JOIN dim_date dd
    ON fs.DateKey = dd.DateKey;
"""