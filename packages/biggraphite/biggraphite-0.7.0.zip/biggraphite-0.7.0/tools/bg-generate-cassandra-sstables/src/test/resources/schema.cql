CREATE TABLE IF NOT EXISTS "biggraphite"."datapoints" (
    metric uuid,
    time_start_ms bigint,
    offset smallint,
    shard smallint,
    value double,
    count smallint,
    PRIMARY KEY ((metric, time_start_ms), offset, shard))
    WITH CLUSTERING ORDER BY (offset DESC)
    AND default_time_to_live = 31536900
    AND compaction = {    'class': 'DateTieredCompactionStrategy',    'timestamp_resolution': 'MICROSECONDS',        'base_time_seconds': '87300',    'max_window_size_seconds': 172800000  };