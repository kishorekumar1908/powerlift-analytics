-- ============================================================================
-- File        : 008_equipment_analysis.sql
-- Project     : PowerLift Analytics
-- Description : Equipment-level analytics using the PowerLiftDW star schema.
-- ============================================================================

USE PowerLiftDW;

-- ============================================================================
-- Query 1: Equipment Overview
-- Purpose:
--     Displays participation and competition summary for each equipment type.
-- ============================================================================

SELECT

    e.EquipmentName,

    COUNT(DISTINCT fr.AthleteKey) AS Athletes,

    COUNT(DISTINCT fr.MeetKey) AS Competitions,

    COUNT(*) AS Results

FROM fact_results fr

JOIN dim_equipment e
    ON fr.EquipmentKey = e.EquipmentKey

GROUP BY
    e.EquipmentKey,
    e.EquipmentName

ORDER BY
    Athletes DESC;


-- ============================================================================
-- Query 2: Performance Comparison by Equipment
-- Purpose:
--     Compares average lifting performance across equipment types.
-- ============================================================================

SELECT

    e.EquipmentName,

    ROUND(AVG(fr.Best3SquatKg),2) AS AvgSquatKg,

    ROUND(AVG(fr.Best3BenchKg),2) AS AvgBenchKg,

    ROUND(AVG(fr.Best3DeadliftKg),2) AS AvgDeadliftKg,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,

    ROUND(AVG(fr.DOTS),2) AS AvgDOTS

FROM fact_results fr

JOIN dim_equipment e
    ON fr.EquipmentKey = e.EquipmentKey

GROUP BY
    e.EquipmentKey,
    e.EquipmentName

ORDER BY
    AvgDOTS DESC;


-- ============================================================================
-- Query 3: Athlete Distribution by Equipment
-- Purpose:
--     Displays the number of unique athletes using each equipment type.
-- ============================================================================

SELECT

    e.EquipmentName,

    COUNT(DISTINCT fr.AthleteKey) AS AthleteCount

FROM fact_results fr

JOIN dim_equipment e
    ON fr.EquipmentKey = e.EquipmentKey

GROUP BY
    e.EquipmentKey,
    e.EquipmentName

ORDER BY
    AthleteCount DESC;


-- ============================================================================
-- Query 4: Equipment Performance Rankings
-- Purpose:
--     Ranks equipment categories by average Total and DOTS.
-- ============================================================================

SELECT

    e.EquipmentName,

    ROUND(AVG(fr.TotalKg),2) AS AvgTotalKg,

    ROUND(AVG(fr.DOTS),2) AS AvgDOTS

FROM fact_results fr

JOIN dim_equipment e
    ON fr.EquipmentKey = e.EquipmentKey

GROUP BY
    e.EquipmentKey,
    e.EquipmentName

ORDER BY
    AvgDOTS DESC,
    AvgTotalKg DESC;


-- ============================================================================
-- Query 5: Best Athlete by Equipment Type
-- Purpose:
--     Identifies the highest Total achieved within each equipment category.
-- ============================================================================

WITH RankedAthletes AS
(
    SELECT

        e.EquipmentName,

        a.AthleteID,

        a.AthleteName,

        fr.TotalKg,

        fr.DOTS,

        ROW_NUMBER() OVER(
            PARTITION BY e.EquipmentName
            ORDER BY fr.TotalKg DESC
        ) AS RankInEquipment

    FROM fact_results fr

    JOIN dim_equipment e
        ON fr.EquipmentKey = e.EquipmentKey

    JOIN dim_athlete a
        ON fr.AthleteKey = a.AthleteKey
)

SELECT

    EquipmentName,

    AthleteID,

    AthleteName,

    TotalKg,

    DOTS

FROM RankedAthletes

WHERE RankInEquipment = 1

ORDER BY
    EquipmentName;