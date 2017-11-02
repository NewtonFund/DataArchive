CREATE FUNCTION vincenty (lat1 NUMERIC, long1 NUMERIC, lat2 DOUBLE PRECISION, long2 DOUBLE PRECISION) RETURNS DOUBLE PRECISION
  AS $$
  BEGIN
  return
    DEGREES(
      ATAN2(
        SQRT(
          POW(
            COS(RADIANS(lat1)) * SIN(RADIANS(long1 - long2)),
            2
          ) +
          POW(
            COS(RADIANS(lat2))*SIN(RADIANS(lat1)) - (
              SIN(RADIANS(lat2))*COS(RADIANS(lat1)) * COS(RADIANS(long1 - long2))
            ),
            2
          )
        ),
        SIN(RADIANS(lat2))*SIN(RADIANS(lat1)) +
        COS(RADIANS(lat2)) * COS(RADIANS(lat1)) * COS(RADIANS(long1 - long2))
      )
    ) as dist;
    END;
  $$ LANGUAGE plpgsql;

CREATE EXTENSION btree_gin;

CREATE TABLE allkeys_q3c AS SELECT * FROM allkeys;
CREATE INDEX ON allkeys_q3c (q3c_ang2ipix(ra_degree, dec_degree));
CLUSTER allkeys_q3c_q3c_ang2ipix_idx ON allkeys_q3c;
ANALYZE allkeys_q3c;

CREATE TABLE allkeys_pgsphere AS SELECT * FROM allkeys;
ALTER TABLE allkeys_pgsphere ADD COLUMN coords spoint;
UPDATE allkeys_pgsphere set coords = spoint(radians(ra_degree),radians(dec_degree));
CREATE INDEX allkeys_pgspheres_coords ON tgas USING GIST(coords);
CLUSTER allkeys_pgspheres_coords ON allkeys_pgspheres;

CREATE TABLE allkeys_pgsphere_testing AS SELECT * FROM allkeys;
ALTER TABLE allkeys_pgsphere_testing ADD COLUMN coords spoint;
UPDATE allkeys_pgsphere_testing set coords = spoint(radians(ra_degree),radians(dec_degree));
CREATE INDEX allkeys_pgspheres_testing_coords ON tgas USING GIST(coords);
CLUSTER allkeys_pgspheres_testing_coords ON allkeys_pgspheres_testing;
CREATE INDEX allkeys_pgsphere_testing_object_idx ON allkeys_pgsphere_testing USING BTREE("OBJECT");
CREATE INDEX allkeys_pgsphere_testing_tagid_idx ON allkeys_pgsphere_testing USING BTREE("TAGID");
CREATE INDEX allkeys_pgsphere_testing_userid_idx ON allkeys_pgsphere_testing USING BTREE("USERID");
CREATE INDEX allkeys_pgsphere_testing_propid_idx ON allkeys_pgsphere_testing USING BTREE("PROPID");
CREATE INDEX allkeys_pgsphere_testing_groupid_idx ON allkeys_pgsphere_testing USING BTREE("GROUPID");
CREATE INDEX allkeys_pgsphere_testing_obsid_idx ON allkeys_pgsphere_testing USING BTREE("OBSID");
CREATE INDEX allkeys_pgsphere_testing_instrume_idx ON allkeys_pgsphere_testing USING BTREE("INSTRUME");

CREATE TABLE allkeys_testing AS SELECT * FROM allkeys;
CREATE INDEX allkeys_testing_instrume_btree_idx ON allkeys_testing USING BTREE("INSTRUME");
CREATE INDEX allkeys_testing_tagid_btree_idx ON allkeys_testing USING BTREE("TAGID");
CREATE INDEX allkeys_testing_userid_btree_idx ON allkeys_testing USING BTREE("USERID");
CREATE INDEX allkeys_testing_propid_btree_idx ON allkeys_testing USING BTREE("PROPID");
CREATE INDEX allkeys_testing_obsid_btree_idx ON allkeys_testing USING BTREE("OBSID");
CREATE INDEX allkeys_testing_groupid_btree_idx ON allkeys_testing USING BTREE("GROUPID");

CREATE TABLE allkeys_testing_hash AS SELECT * FROM allkeys;
CREATE INDEX allkeys_testing_instrume_hash_idx ON allkeys_testing_hash USING HASH("INSTRUME");
CREATE INDEX allkeys_testing_tagid_hash_idx ON allkeys_testing_hash USING HASH("TAGID");
CREATE INDEX allkeys_testing_userid_hash_idx ON allkeys_testing_hash USING HASH("USERID");
CREATE INDEX allkeys_testing_propid_hash_idx ON allkeys_testing_hash USING HASH("PROPID");
CREATE INDEX allkeys_testing_obsid_hash_idx ON allkeys_testing_hash USING HASH("OBSID");
CREATE INDEX allkeys_testing_groupid_hash_idx ON allkeys_testing_hash USING HASH("GROUPID");


CREATE TABLE allkeys_testing_gin AS SELECT * FROM allkeys;

ALTER TABLE allkeys_testing_gin ADD COLUMN "INSTRUME_tsvector" TSVECTOR;
UPDATE allkeys_testing_gin SET "INSTRUME_tsvector" = to_tsvector("INSTRUME");
CREATE INDEX allkeys_testing_instrume_gin_idx ON allkeys_testing_gin USING GIN("INSTRUME_tsvector");
CREATE INDEX allkeys_testing_instrume_btree_gin_idx ON allkeys_testing_gin USING GIN("INSTRUME");

ALTER TABLE allkeys_testing_gin ADD COLUMN "TAGID_tsvector" TSVECTOR;
UPDATE allkeys_testing_gin SET "TAGID_tsvector" = to_tsvector("TAGID");
CREATE INDEX allkeys_testing_tagid_gin_idx ON allkeys_testing_gin USING GIN("TAGID_tsvector");
CREATE INDEX allkeys_testing_tagid_btree_gin_idx ON allkeys_testing_gin USING GIN("TAGID");

ALTER TABLE allkeys_testing_gin ADD COLUMN "USERID_tsvector" TSVECTOR;
UPDATE allkeys_testing_gin SET "USERID_tsvector" = to_tsvector("USERID");
CREATE INDEX allkeys_testing_userid_gin_idx ON allkeys_testing_gin USING GIN("USERID_tsvector");
CREATE INDEX allkeys_testing_userid_btree_gin_idx ON allkeys_testing_gin USING GIN("USERID");

ALTER TABLE allkeys_testing_gin ADD COLUMN "PROPID_tsvector" TSVECTOR;
UPDATE allkeys_testing_gin SET "PROPID_tsvector" = to_tsvector("PROPID");
CREATE INDEX allkeys_testing_propid_gin_idx ON allkeys_testing_gin USING GIN("PROPID_tsvector");
CREATE INDEX allkeys_testing_propid_btree_gin_idx ON allkeys_testing_gin USING GIN("PROPID");

ALTER TABLE allkeys_testing_gin ADD COLUMN "OBSID_tsvector" TSVECTOR;
UPDATE allkeys_testing_gin SET "OBSID_tsvector" = to_tsvector("OBSID");
CREATE INDEX allkeys_testing_obsid_gin_idx ON allkeys_testing_gin USING GIN("OBSID_tsvector");
CREATE INDEX allkeys_testing_obsid_btree_gin_idx ON allkeys_testing_gin USING GIN("OBSID");

ALTER TABLE allkeys_testing_gin ADD COLUMN "GROUPID_tsvector" TSVECTOR;
UPDATE allkeys_testing_gin SET "GROUPID_tsvector" = to_tsvector("GROUPID");
CREATE INDEX allkeys_testing_groupid_gin_idx ON allkeys_testing_gin USING GIN("GROUPID_tsvector");
CREATE INDEX allkeys_testing_groupid_btree_gin_idx ON allkeys_testing_gin USING GIN("GROUPID");


SELECT         
   relname AS objectname,
   relkind AS objecttype,
   reltuples AS "#entries", pg_size_pretty(relpages::bigint*8*1024) AS size
   FROM pg_class
   WHERE relpages >= 8
   ORDER BY relpages DESC;


/* List all indexes and other stuff. */
SELECT i.relname as indname,
       i.relowner as indowner,
       idx.indrelid::regclass,
       am.amname as indam,
       idx.indkey,
       ARRAY(
       SELECT pg_get_indexdef(idx.indexrelid, k + 1, true)
       FROM generate_subscripts(idx.indkey, 1) as k
       ORDER BY k
       ) as indkey_names,
       idx.indexprs IS NOT NULL as indexprs,
       idx.indpred IS NOT NULL as indpred
FROM   pg_index as idx
JOIN   pg_class as i
ON     i.oid = idx.indexrelid
JOIN   pg_am as am
ON     i.relam = am.oid;