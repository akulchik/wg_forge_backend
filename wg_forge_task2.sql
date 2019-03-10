CREATE OR REPLACE FUNCTION _final_median(NUMERIC[])
    RETURNS NUMERIC AS
    $BODY$
    SELECT AVG(val)
    FROM (
        SELECT val
        FROM unnest($1) val
        ORDER BY 1
        LIMIT 2 - MOD(array_upper($1, 1), 2)
        OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
    ) sub;
    $BODY$
    LANGUAGE SQL IMMUTABLE;

CREATE AGGREGATE median(NUMERIC) (
    SFUNC=array_append,
    STYPE=NUMERIC[],
    FINALFUNC=_final_median,
    INITCOND='{}'
);

INSERT INTO cats_stat (tail_length_mean, tail_length_median, whiskers_length_mean, whiskers_length_median)
    SELECT AVG(tail_length),
        median(tail_length),
        AVG(whiskers_length),
        median(whiskers_length)
    FROM cats;
