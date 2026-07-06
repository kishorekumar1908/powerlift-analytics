-- ============================================================================
-- File        : 006_pr_analysis.sql
-- Project     : PowerLift Analytics
-- Description : Personal Record (PR) analytics using the PowerLiftDW star schema.
-- ============================================================================

USE PowerLiftDW;

-- ============================================================================
-- Query 1: Total PR Detection
-- Purpose:
--     Identifies competitions where an athlete achieved
--     a new Personal Record (Total).
-- ============================================================================

WITH TotalPR AS
(
    SELECT

        a.AthleteID,

        a.AthleteName,

        d.FullDate,

        fr.TotalKg,

        MAX(fr.TotalKg) OVER(

            PARTITION BY fr.AthleteKey

            ORDER BY d.FullDate

            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW

        ) AS CareerBestTotal

    FROM fact_results fr

    JOIN dim_athlete a
        ON fr.AthleteKey = a.AthleteKey

    JOIN dim_date d
        ON fr.DateKey = d.DateKey
)

SELECT *

FROM TotalPR

WHERE TotalKg = CareerBestTotal

ORDER BY
    AthleteID,
    FullDate;

-- ============================================================================
-- Query 2: Squat, Bench and Deadlift PR Detection
-- Purpose:
--     Detects new PRs for all three lifts.
-- ============================================================================

SELECT

    a.AthleteID,

    a.AthleteName,

    d.FullDate,

    fr.Best3SquatKg,

    MAX(fr.Best3SquatKg) OVER(
        PARTITION BY fr.AthleteKey
        ORDER BY d.FullDate
    ) AS CareerBestSquat,

    fr.Best3BenchKg,

    MAX(fr.Best3BenchKg) OVER(
        PARTITION BY fr.AthleteKey
        ORDER BY d.FullDate
    ) AS CareerBestBench,

    fr.Best3DeadliftKg,

    MAX(fr.Best3DeadliftKg) OVER(
        PARTITION BY fr.AthleteKey
        ORDER BY d.FullDate
    ) AS CareerBestDeadlift

FROM fact_results fr

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

JOIN dim_date d
    ON fr.DateKey = d.DateKey

ORDER BY
    AthleteID,
    FullDate;

-- ============================================================================
-- Query 3: PR Count by Athlete
-- Purpose:
--     Counts how many Total PRs each athlete has achieved.
-- ============================================================================

WITH PRHistory AS
(
    SELECT

        fr.AthleteKey,

        fr.TotalKg,

        MAX(fr.TotalKg) OVER(
            PARTITION BY fr.AthleteKey
            ORDER BY d.FullDate
        ) AS CareerBest

    FROM fact_results fr

    JOIN dim_date d
        ON fr.DateKey = d.DateKey
)

SELECT

    a.AthleteID,

    a.AthleteName,

    COUNT(*) AS TotalPRs

FROM PRHistory p

JOIN fact_results fr
    ON p.AthleteKey = fr.AthleteKey

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

WHERE p.TotalKg = p.CareerBest

GROUP BY
    a.AthleteID,
    a.AthleteName

ORDER BY TotalPRs DESC;

-- ============================================================================
-- Query 4: Latest PR by Athlete
-- Purpose:
--     Displays the most recent Personal Record for every athlete.
-- ============================================================================

WITH RankedPR AS
(
    SELECT

        a.AthleteID,

        a.AthleteName,

        d.FullDate,

        fr.TotalKg,

        ROW_NUMBER() OVER(

            PARTITION BY fr.AthleteKey

            ORDER BY d.FullDate DESC

        ) AS rn

    FROM fact_results fr

    JOIN dim_athlete a
        ON fr.AthleteKey = a.AthleteKey

    JOIN dim_date d
        ON fr.DateKey = d.DateKey
)

SELECT
    AthleteID,

    AthleteName,

    FullDate,

    TotalKg

FROM RankedPR

WHERE rn = 1;

-- ============================================================================
-- Query 5: PR Leaderboard
-- Purpose:
--     Displays athletes with the highest career Total.
-- ============================================================================

SELECT

    a.AthleteID,

    a.AthleteName,

    MAX(fr.TotalKg) AS CareerBestTotal,

    MAX(fr.DOTS) AS CareerBestDOTS

FROM fact_results fr

JOIN dim_athlete a
    ON fr.AthleteKey = a.AthleteKey

GROUP BY

    a.AthleteID,

    a.AthleteName

ORDER BY
    CareerBestTotal DESC

LIMIT 10;