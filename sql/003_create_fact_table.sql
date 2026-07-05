CREATE TABLE fact_results (

    ResultKey BIGINT AUTO_INCREMENT PRIMARY KEY,

    AthleteKey INT NOT NULL,
    DateKey INT NOT NULL,
    MeetKey INT NOT NULL,
    FederationKey INT NOT NULL,
    WeightClassKey INT NOT NULL,
    EquipmentKey INT NOT NULL,
    EventKey INT NOT NULL,
    AgeClassKey INT NOT NULL,

    Age DECIMAL(5,2),
    BodyweightKg DECIMAL(6,2),

    Best3SquatKg DECIMAL(6,2),
    Best3BenchKg DECIMAL(6,2),
    Best3DeadliftKg DECIMAL(6,2),

    TotalKg DECIMAL(6,2),

    DOTS DECIMAL(7,2),

    Tested BOOLEAN,

    CONSTRAINT fk_fact_athlete
        FOREIGN KEY (AthleteKey)
        REFERENCES dim_athlete(AthleteKey),

    CONSTRAINT fk_fact_date
        FOREIGN KEY (DateKey)
        REFERENCES dim_date(DateKey),

    CONSTRAINT fk_fact_meet
        FOREIGN KEY (MeetKey)
        REFERENCES dim_meet(MeetKey),

    CONSTRAINT fk_fact_federation
        FOREIGN KEY (FederationKey)
        REFERENCES dim_federation(FederationKey),

    CONSTRAINT fk_fact_weight_class
        FOREIGN KEY (WeightClassKey)
        REFERENCES dim_weight_class(WeightClassKey),

    CONSTRAINT fk_fact_equipment
        FOREIGN KEY (EquipmentKey)
        REFERENCES dim_equipment(EquipmentKey),

    CONSTRAINT fk_fact_event
        FOREIGN KEY (EventKey)
        REFERENCES dim_event(EventKey),

    CONSTRAINT fk_fact_age_class
        FOREIGN KEY (AgeClassKey)
        REFERENCES dim_age_class(AgeClassKey)

);