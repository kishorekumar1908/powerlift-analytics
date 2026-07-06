-- ============================================================================
-- File        : 007_date_analysis.sql
-- Project     : PowerLift Analytics
-- Description : Date-based analytics using the PowerLiftDW star schema.
-- Author      : Kishore Kumar
-- ============================================================================

USE PowerLiftDW;

-- ============================================================================
-- Query 1: Competitions by Year
-- Purpose:
--     Displays the number of competitions held each year.
-- ============================================================================

SELECT

    d.Year,

    COUNT(DISTINCT fr.MeetKey) AS Competitions

FROM fact_results fr

JOIN dim_date d
    ON fr.DateKey = d.DateKey

GROUP BY
    d.Year

ORDER BY
    d.Year;


-- ============================================================================
-- Query 2: Athlete Participation by Year
-- Purpose:
--     Displays the number of unique athletes who competed each year.
-- ============================================================================

SELECT

    d.Year,

    COUNT(DISTINCT fr.AthleteKey) AS Athletes

FROM fact_results fr

JOIN dim_date d
    ON fr.DateKey = d.DateKey

GROUP BY
    d.Year

ORDER BY
    d.Year;


-- ============================================================================
-- Query 3: Yearly Performance Trends
-- Purpose:
--     Shows yearly average performance metrics.
-- ============================================================================

SELECT

    d.Year,

    ROUND(AVG(fr.Best3SquatKg), 2) AS AvgSquatKg,

    ROUND(AVG(fr.Best3BenchKg), 2) AS AvgBenchKg,

    ROUND(AVG(fr.Best3DeadliftKg), 2) AS AvgDeadliftKg,

    ROUND(AVG(fr.TotalKg), 2) AS AvgTotalKg,

    ROUND(AVG(fr.DOTS), 2) AS AvgDOTS

FROM fact_results fr

JOIN dim_date d
    ON fr.DateKey = d.DateKey

GROUP BY
    d.Year

ORDER BY
    d.Year;


-- ============================================================================
-- Query 4: Monthly Competition Distribution
-- Purpose:
--     Displays the number of competitions conducted in each month.
-- ============================================================================

SELECT

    d.Month,

    d.MonthName,

    COUNT(DISTINCT fr.MeetKey) AS Competitions

FROM fact_results fr

JOIN dim_date d
    ON fr.DateKey = d.DateKey

GROUP BY
    d.Month,
    d.MonthName

ORDER BY
    d.Month;