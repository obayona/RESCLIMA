
/*Index for ts_index field*/
CREATE INDEX textsearch_idx ON "layer_layer" USING GIN (ts_index);

/*Trigger that fills the ts_index column before any insert or update in the Layer table*/
CREATE TRIGGER tsvector_update_layer BEFORE INSERT OR UPDATE
ON "layer_layer" FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger("ts_index", 'pg_catalog.spanish', title, abstract, categories_string);

/*Trigger that fills the ts_index column before any insert or update in the Variable table*/
CREATE TRIGGER tsvector_update_variable BEFORE INSERT OR UPDATE
ON "timeSeries_variable" FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger("ts_index", 'pg_catalog.spanish', name, categories_string);

/*Function to insert a measurement that comes from a
meteorologycal station of type Sky2*/
CREATE OR REPLACE FUNCTION InsertSky2Measurements
(idStation INTEGER, ts_in TIMESTAMP,readings JSON)
RETURNS void AS $$
BEGIN
	IF NOT(EXISTS(SELECT * FROM "timeSeries_measurement"
		WHERE "idStation_id"=idStation and "ts"=ts_in))
	THEN
		INSERT INTO "timeSeries_measurement"("idStation_id","ts","readings")
		VALUES(idStation,ts_in,readings);
	END IF;
END;
$$ LANGUAGE plpgsql;


/*Example of a query of fts over the variable table*/
/*
SELECT id,name FROM "timeSeries_variable" WHERE ts_index @@ plainto_tsquery('spanish','velocida');

SELECT title, id, abstract, ts_rank_cd(textsearchable_index, query) AS rank
FROM "Layer_layer", plainto_tsquery('spanish','Playas') query
WHERE query @@ textsearchable_index
ORDER BY rank DESC
LIMIT 10;*/
