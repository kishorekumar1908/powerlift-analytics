-- ============================================================================
-- File        : 005_weightclass_analysis.sql
-- Project     : PowerLift Analytics
-- Description : Weight class analytics using the PowerLiftDW star schema.
-- Author      : Kishore Kumar
-- ============================================================================

USE PowerLiftDW;

-- ============================================================================
-- Query 1: Weight Class Overview
-- Purpose:
--     Displays athlete participation and competition count
--     for each weight class.
-- ============================================================================

SELECT

    wc.WeightClassKg,

    COUNT(DISTINCT fr.AthleteKey) AS Athletes,

    COUNT(*) AS Results,

    COUNT(DISTINCT fr.MeetKey) AS Competitions

FROM fact_results fr

JOIN dim_weight_class wc
    ON fr.WeightClassKey = wc.WeightClassKey

GROUP BY
    wc.WeightClassKey,
    wc.WeightClassKg

ORDER BY
    wc.WeightClassKg;

-- ============================================================================
-- Query 2: Performance Summary by Weight Class
-- Purpose:
--     Displays average performance metrics for each weight class.
-- ============================================================================

SELECT

    wc.WeightClassKg,

    ROUND(AVG(fr.BodyweightKg),2)      AS AvgBodyweightKg,

    ROUND(AVG(fr.Best3SquatKg),2)      AS AvgSquatKg,

    ROUND(AVG(fr.Best3BenchKg),2)      AS AvgBenchKg,

    ROUND(AVG(fr.Best3DeadliftKg),2)   AS AvgDeadliftKg,

    ROUND(AVG(fr.TotalKg),2)           AS AvgTotalKg,

    ROUND(AVG(fr.DOTS),2)              AS AvgDOTS

FROM fact_results fr

JOIN dim_weight_class wc
    ON fr.WeightClassKey = wc.WeightClassKey

GROUP BY
    wc.WeightClassKey,
    wc.WeightClassKg

ORDER BY
    wc.WeightClassKg;

-- ============================================================================
-- Query 3: Strongest Weight Classes
-- Purpose:
--     Ranks weight classes by average Total and DOTS.
-- ============================================================================

SELECT

    wc.WeightClassKg,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,

    ROUND(AVG(fr.DOTS),2) AS AvgDOTS

FROM fact_results fr

JOIN dim_weight_class wc
    ON fr.WeightClassKey = wc.WeightClassKey

GROUP BY
    wc.WeightClassKey,
    wc.WeightClassKg

HAVING COUNT(DISTINCT fr.AthleteKey) >= 10

ORDER BY
    AvgDOTS DESC,
    AvgTotalKg DESC;

-- ============================================================================
-- Query 4: Weight Class Participation Ranking
-- Purpose:
--     Ranks weight classes by athlete participation.
-- ============================================================================

SELECT

    wc.WeightClassKg,

    COUNT(DISTINCT fr.AthleteKey) AS Athletes

FROM fact_results fr

JOIN dim_weight_class wc
    ON fr.WeightClassKey = wc.WeightClassKey

GROUP BY
    wc.WeightClassKey,
    wc.WeightClassKg

ORDER BY
    Athletes DESC;

-- ============================================================================
-- Query 5: Top Athletes in Each Weight Class
-- Purpose:
--     Displays the strongest athlete in every weight class
--     based on TotalKg.
-- ============================================================================

WITH RankedAthletes AS
(
    SELECT

        wc.WeightClassKg,

        a.AthleteID,

        a.AthleteName,

        fr.TotalKg,

        fr.DOTS,

        ROW_NUMBER() OVER(
            PARTITION BY wc.WeightClassKg
            ORDER BY fr.TotalKg DESC
        ) AS RankInClass

    FROM fact_results fr

    JOIN dim_weight_class wc
        ON fr.WeightClassKey = wc.WeightClassKey

    JOIN dim_athlete a
        ON fr.AthleteKey = a.AthleteKey
)

SELECT

    WeightClassKg,

    AthleteID,

    AthleteName,

    TotalKg,

    DOTS

FROM RankedAthletes

WHERE RankInClass = 1

ORDER BY WeightClassKg;