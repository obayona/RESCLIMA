ALTER TABLE "Layer_layer" ADD COLUMN textsearchable_index tsvector;

UPDATE "Layer_layer" SET textsearchable_index = to_tsvector('spanish',coalesce(title,'') || ' ' || coalesce(abstract,''));

CREATE INDEX textsearch_idx ON "Layer_layer" USING GIN (textsearchable_index);

SELECT title,id FROM "Layer_layer" WHERE textsearchable_index @@ plainto_tsquery('spanish','Playas');

SELECT title, id, abstract, ts_rank_cd(textsearchable_index, query) AS rank
FROM "Layer_layer", plainto_tsquery('spanish','Playas') query
WHERE query @@ textsearchable_index
ORDER BY rank DESC
LIMIT 10;