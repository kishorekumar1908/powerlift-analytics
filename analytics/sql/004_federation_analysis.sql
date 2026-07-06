-- ============================================================================
-- File        : 004_federation_analysis.sql
-- Project     : PowerLift Analytics
-- Description : Federation-level analytics using the PowerLiftDW star schema.
-- ============================================================================

USE PowerLiftDW;

-- ============================================================================
-- Query 1: Federation Overview
-- Purpose:
--     Displays participation and performance summary for each federation.
-- ============================================================================

SELECT

    fed.FederationName,

    COUNT(DISTINCT fr.AthleteKey) AS Athletes,

    COUNT(DISTINCT fr.MeetKey) AS Competitions,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,

    ROUND(AVG(fr.DOTS),2) AS AvgDOTS

FROM fact_results fr

JOIN dim_federation fed
    ON fr.FederationKey = fed.FederationKey

GROUP BY
    fed.FederationKey,
    fed.FederationName

ORDER BY Athletes DESC;

-- ============================================================================
-- Query 2: Federation Meet Distribution
-- Purpose:
--     Shows how many competitions each federation has conducted
--     and the average number of athletes per competition.
-- ============================================================================

SELECT

    fed.FederationName,

    COUNT(DISTINCT fr.MeetKey) AS Competitions,

    COUNT(DISTINCT fr.AthleteKey) AS Athletes,

    ROUND(
        COUNT(DISTINCT fr.AthleteKey) /
        COUNT(DISTINCT fr.MeetKey),
        2
    ) AS AvgAthletesPerCompetition

FROM fact_results fr

JOIN dim_federation fed
    ON fr.FederationKey = fed.FederationKey

GROUP BY
    fed.FederationKey,
    fed.FederationName

ORDER BY Competitions DESC;

-- ============================================================================
-- Query 3: Federation Performance Summary
-- Purpose:
--     Displays average lift performance for each federation.
-- ============================================================================

SELECT

    fed.FederationName,

    ROUND(AVG(fr.Best3SquatKg),2)    AS AvgSquatKg,

    ROUND(AVG(fr.Best3BenchKg),2)    AS AvgBenchKg,

    ROUND(AVG(fr.Best3DeadliftKg),2) AS AvgDeadliftKg,

    ROUND(AVG(fr.TotalKg),2)         AS AvgTotalKg,

    ROUND(AVG(fr.DOTS),2)            AS AvgDOTS

FROM fact_results fr

JOIN dim_federation fed
    ON fr.FederationKey = fed.FederationKey

GROUP BY
    fed.FederationKey,
    fed.FederationName

ORDER BY AvgDOTS DESC;

-- ============================================================================
-- Query 4: Top Federations by Performance
-- Purpose:
--     Ranks federations by Average Total and DOTS.
-- ============================================================================

SELECT

    fed.FederationName,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,

    ROUND(AVG(fr.DOTS),2) AS AvgDOTS

FROM fact_results fr

JOIN dim_federation fed
    ON fr.FederationKey = fed.FederationKey

GROUP BY
    fed.FederationKey,
    fed.FederationName

HAVING COUNT(DISTINCT fr.AthleteKey) >= 10

ORDER BY
    AvgDOTS DESC,
    AvgTotalKg DESC

LIMIT 10;

-- ============================================================================
-- Query 5: Tested vs Untested Analysis
-- Purpose:
--     Compares athlete performance in tested and untested federations.
-- ============================================================================

SELECT

    fed.FederationName,

    CASE
        WHEN fr.Tested = 1 THEN 'Tested'
        ELSE 'Untested'
    END AS TestingStatus,

    COUNT(*) AS Results,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,

    ROUND(AVG(fr.DOTS),2) AS AvgDOTS

FROM fact_results fr

JOIN dim_federation fed
    ON fr.FederationKey = fed.FederationKey

GROUP BY
    fed.FederationName,
    TestingStatus

ORDER BY
    fed.FederationName,
    TestingStatus;