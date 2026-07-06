-- ============================================================================
-- File        : 001_athlete_analysis.sql
-- Project     : PowerLift Analytics
-- Description : Athlete-level analytics using the PowerLiftDW star schema.
-- ============================================================================

USE PowerLiftDW;

-- ============================================================================
-- Query 1: Athlete Career Overview
-- Purpose:
--     Displays each athlete's career duration and number of competitions.
-- ============================================================================

SELECT
    a.AthleteID,
    a.AthleteName,
    COUNT(*) AS Competitions,
    MIN(d.FullDate) AS FirstCompetition,
    MAX(d.FullDate) AS LatestCompetition,
    TIMESTAMPDIFF(
        YEAR,
        MIN(d.FullDate),
        MAX(d.FullDate)
    ) AS CareerYears
FROM fact_results fr
JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey
JOIN dim_date d
    ON fr.DateKey = d.DateKey
GROUP BY
    a.AthleteID,
    a.AthleteName
ORDER BY Competitions DESC;

-- ============================================================================
-- Query 2: Athlete Best Performance Summary
-- Purpose:
--     Shows the best lifts and best overall performance of each athlete.
-- ============================================================================

SELECT
    a.AthleteID,
    a.AthleteName,

    MAX(fr.Best3SquatKg)    AS BestSquatKg,
    MAX(fr.Best3BenchKg)    AS BestBenchKg,
    MAX(fr.Best3DeadliftKg) AS BestDeadliftKg,

    MAX(fr.TotalKg) AS BestTotalKg,
    MAX(fr.DOTS)    AS BestDOTS

FROM fact_results fr
JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

GROUP BY
    a.AthleteID,
    a.AthleteName

ORDER BY BestTotalKg DESC;

-- ============================================================================
-- Query 3: Athlete Average Performance
-- Purpose:
--     Calculates average competition performance for each athlete.
-- ============================================================================

SELECT

    a.AthleteID,
    a.AthleteName,

    ROUND(AVG(fr.Best3SquatKg),2)    AS AvgSquatKg,
    ROUND(AVG(fr.Best3BenchKg),2)    AS AvgBenchKg,
    ROUND(AVG(fr.Best3DeadliftKg),2) AS AvgDeadliftKg,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,
    ROUND(AVG(fr.DOTS),2)    AS AvgDOTS

FROM fact_results fr

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

GROUP BY
    a.AthleteID,
    a.AthleteName

ORDER BY AvgDOTS DESC;

-- ============================================================================
-- Query 4: Complete Athlete Career Summary
-- Purpose:
--     Generates a comprehensive athlete profile by combining career,
--     performance, and average statistics.
-- ============================================================================

SELECT

    a.AthleteID,
    a.AthleteName,

    COUNT(*) AS Competitions,

    MIN(d.FullDate) AS FirstCompetition,
    MAX(d.FullDate) AS LatestCompetition,

    TIMESTAMPDIFF(
        YEAR,
        MIN(d.FullDate),
        MAX(d.FullDate)
    ) AS CareerYears,

    MAX(fr.Best3SquatKg)    AS BestSquatKg,
    MAX(fr.Best3BenchKg)    AS BestBenchKg,
    MAX(fr.Best3DeadliftKg) AS BestDeadliftKg,

    MAX(fr.TotalKg) AS BestTotalKg,
    MAX(fr.DOTS)    AS BestDOTS,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,
    ROUND(AVG(fr.DOTS),2)    AS AvgDOTS

FROM fact_results fr

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

JOIN dim_date d
    ON fr.DateKey = d.DateKey

GROUP BY
    a.AthleteID,
    a.AthleteName

ORDER BY BestTotalKg DESC;

-- ============================================================================
-- Query 5: Top 10 Strongest Athletes
-- Purpose:
--     Ranks athletes by their best Total and DOTS score.
-- ============================================================================

SELECT

    a.AthleteID,
    a.AthleteName,

    MAX(fr.TotalKg) AS BestTotalKg,
    MAX(fr.DOTS)    AS BestDOTS

FROM fact_results fr

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

GROUP BY
    a.AthleteID,
    a.AthleteName

ORDER BY
    BestTotalKg DESC,
    BestDOTS DESC

LIMIT 10;