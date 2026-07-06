-- ============================================================================
-- File        : 002_progress_analysis.sql
-- Project     : PowerLift Analytics
-- Description : Analyze athlete performance progression over time.
-- ============================================================================

USE PowerLiftDW;

-- ============================================================================
-- Query 1: Competition Timeline
-- Purpose:
--     Displays an athlete's competition history in chronological order.
--     Replace 'ATH00001' with the required AthleteID.
-- ============================================================================

SELECT
    a.AthleteID,
    a.AthleteName,
    d.FullDate,
    m.MeetName,
    fr.TotalKg,
    fr.DOTS

FROM fact_results fr

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

JOIN dim_date d
    ON fr.DateKey = d.DateKey

JOIN dim_meet m
    ON fr.MeetKey = m.MeetKey

WHERE a.AthleteID = 'ATH00020'

ORDER BY d.FullDate;

-- ============================================================================
-- Query 2: Lift Progression
-- Purpose:
--     Shows the progression of all lifts across competitions.
-- ============================================================================

SELECT

    d.FullDate,

    fr.Best3SquatKg,
    fr.Best3BenchKg,
    fr.Best3DeadliftKg,
    fr.TotalKg,
    fr.DOTS

FROM fact_results fr

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

JOIN dim_date d
    ON fr.DateKey = d.DateKey

WHERE a.AthleteID = 'ATH00020'

ORDER BY d.FullDate;

-- ============================================================================
-- Query 3: Competition-to-Competition Improvement
-- Purpose:
--     Calculates improvement in Total compared to the previous competition.
-- ============================================================================

SELECT

    a.AthleteID,
    a.AthleteName,
    d.FullDate,

    fr.TotalKg,

    LAG(fr.TotalKg) OVER (
        PARTITION BY a.AthleteID
        ORDER BY d.FullDate
    ) AS PreviousTotal,

    fr.TotalKg -
    LAG(fr.TotalKg) OVER (
        PARTITION BY a.AthleteID
        ORDER BY d.FullDate
    ) AS ImprovementKg

FROM fact_results fr

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

JOIN dim_date d
    ON fr.DateKey = d.DateKey

WHERE a.AthleteID = 'ATH00020'

ORDER BY d.FullDate;

-- ============================================================================
-- Query 4: Career Improvement Summary
-- Purpose:
--     Compares an athlete's first and latest competition totals.
-- ============================================================================

WITH CareerTotals AS
(
    SELECT

        a.AthleteID,
        a.AthleteName,
        d.FullDate,
        fr.TotalKg,

        ROW_NUMBER() OVER(
            PARTITION BY a.AthleteID
            ORDER BY d.FullDate
        ) AS FirstCompetition,

        ROW_NUMBER() OVER(
            PARTITION BY a.AthleteID
            ORDER BY d.FullDate DESC
        ) AS LastCompetition

    FROM fact_results fr

    JOIN dim_athlete a
        ON fr.AthleteKey = a.AthleteKey

    JOIN dim_date d
        ON fr.DateKey = d.DateKey
)

SELECT

    AthleteID,
    AthleteName,

    MAX(CASE WHEN FirstCompetition = 1 THEN TotalKg END) AS FirstTotal,

    MAX(CASE WHEN LastCompetition = 1 THEN TotalKg END) AS LatestTotal,

    MAX(CASE WHEN LastCompetition = 1 THEN TotalKg END)
    -
    MAX(CASE WHEN FirstCompetition = 1 THEN TotalKg END)
    AS TotalImprovement

FROM CareerTotals

GROUP BY
    AthleteID,
    AthleteName;

-- ============================================================================
-- Query 5: Plateau Detection
-- Purpose:
--     Determines whether the athlete is improving, declining or plateauing
--     based on the latest competition.
-- ============================================================================

WITH Progress AS
(
    SELECT

        a.AthleteID,

        d.FullDate,

        fr.TotalKg,

        LAG(fr.TotalKg) OVER(
            PARTITION BY a.AthleteID
            ORDER BY d.FullDate
        ) AS PreviousTotal

    FROM fact_results fr

    JOIN dim_athlete a
        ON fr.AthleteKey = a.AthleteKey

    JOIN dim_date d
        ON fr.DateKey = d.DateKey
)

SELECT *

FROM
(
    SELECT

        AthleteID,
        FullDate,
        TotalKg,
        PreviousTotal,

        CASE

            WHEN PreviousTotal IS NULL THEN 'First Competition'
            WHEN TotalKg > PreviousTotal THEN 'Improving'
            WHEN TotalKg < PreviousTotal THEN 'Declining'
            ELSE 'Plateau'

        END AS PerformanceTrend,

        ROW_NUMBER() OVER(
            PARTITION BY AthleteID
            ORDER BY FullDate DESC
        ) AS rn

    FROM Progress

) AS LatestCompetition

WHERE rn = 1;