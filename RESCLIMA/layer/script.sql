ALTER TABLE "Layer_layer" ADD COLUMN textsearchable_index tsvector;

UPDATE "Layer_layer" SET textsearchable_index = to_tsvector('spanish',coalesce(title,'') || ' ' || coalesce(abstract,''));

CREATE INDEX textsearch_idx ON "Layer_layer" USING GIN (textsearchable_index);

SELECT title,id FROM "Layer_layer" WHERE textsearchable_index @@ plainto_tsquery('spanish','Playas');

SELECT title, id, abstract, ts_rank_cd(textsearchable_index, query) AS rank
FROM "Layer_layer", plainto_tsquery('spanish','Playas') query
WHERE query @@ textsearchable_index
ORDER BY rank DESC
LIMIT 10;


CREATE TRIGGER tsvector_update_layer BEFORE INSERT OR UPDATE
ON "Layer_layer" FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger("textsearchable_index", 'pg_catalog.spanish', title, abstract);


CREATE OR REPLACE FUNCTION InsertSky2Measurements
(idStation INTEGER, ts_in TIMESTAMP,readings JSON)
RETURNS void AS $$
BEGIN
	IF NOT(EXISTS(SELECT * FROM "TimeSeries_measurement"
		WHERE "idStation_id"=idStation and "ts"=ts_in))
	THEN
		INSERT INTO "TimeSeries_measurement"("idStation_id","ts","readings")
		VALUES(idStation,ts_in,readings);
	END IF;
END;
$$ LANGUAGE plpgsql;
