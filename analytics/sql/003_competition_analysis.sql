-- ============================================================================
-- File        : 003_competition_analysis.sql
-- Project     : PowerLift Analytics
-- Description : Competition-level analytics using the PowerLiftDW star schema.
-- ============================================================================

USE PowerLiftDW;

-- ============================================================================
-- Query 1: Competition Overview
-- Purpose:
--     Displays summary statistics for each competition.
-- ============================================================================

SELECT

    m.MeetName,
    m.MeetTown,
    m.MeetDate,

    COUNT(DISTINCT fr.AthleteKey) AS Participants,

    ROUND(AVG(fr.TotalKg),2) AS AverageTotalKg,
    ROUND(AVG(fr.DOTS),2) AS AverageDOTS

FROM fact_results fr

JOIN dim_meet m
    ON fr.MeetKey = m.MeetKey

GROUP BY
    m.MeetKey,
    m.MeetName,
    m.MeetTown,
    m.MeetDate

ORDER BY
    m.MeetDate DESC;

-- ============================================================================
-- Query 2: Largest Competitions
-- Purpose:
--     Shows the Top 10 competitions with the highest participation.
-- ============================================================================

SELECT

    m.MeetName,
    m.MeetTown,
    m.MeetDate,

    COUNT(DISTINCT fr.AthleteKey) AS Participants

FROM fact_results fr

JOIN dim_meet m
    ON fr.MeetKey = m.MeetKey

GROUP BY
    m.MeetKey,
    m.MeetName,
    m.MeetTown,
    m.MeetDate

ORDER BY Participants DESC

LIMIT 10;

-- ============================================================================
-- Query 3: Competition Performance Summary
-- Purpose:
--     Displays average lift performance for each competition.
-- ============================================================================

SELECT

    m.MeetName,

    ROUND(AVG(fr.Best3SquatKg),2)    AS AvgSquatKg,
    ROUND(AVG(fr.Best3BenchKg),2)    AS AvgBenchKg,
    ROUND(AVG(fr.Best3DeadliftKg),2) AS AvgDeadliftKg,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,
    ROUND(AVG(fr.DOTS),2)    AS AvgDOTS

FROM fact_results fr

JOIN dim_meet m
    ON fr.MeetKey = m.MeetKey

GROUP BY
    m.MeetKey,
    m.MeetName

ORDER BY AvgTotalKg DESC;

-- ============================================================================
-- Query 4: Top 10 Strongest Competitions
-- Purpose:
--     Ranks competitions by average Total and DOTS.
-- ============================================================================

SELECT

    m.MeetName,
    m.MeetTown,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,
    ROUND(AVG(fr.DOTS),2)    AS AvgDOTS

FROM fact_results fr

JOIN dim_meet m
    ON fr.MeetKey = m.MeetKey

GROUP BY
    m.MeetKey,
    m.MeetName,
    m.MeetTown

ORDER BY
    AvgTotalKg DESC,
    AvgDOTS DESC

LIMIT 10;

-- ============================================================================
-- Query 5: Meet Lookup
-- Purpose:
--     Displays all athlete results for a selected competition.
--     Replace the Meet Name as required.
-- ============================================================================

SELECT

    m.MeetName,
    m.MeetDate,

    a.AthleteID,
    a.AthleteName,

    fr.Best3SquatKg,
    fr.Best3BenchKg,
    fr.Best3DeadliftKg,

    fr.TotalKg,
    fr.DOTS

FROM fact_results fr

JOIN dim_meet m
    ON fr.MeetKey = m.MeetKey

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

WHERE m.MeetName = 'Indian Classic Powerlifting Championships'

ORDER BY fr.TotalKg DESC;