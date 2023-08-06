import tables as tb


class HitInfoTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    frame = tb.UInt8Col(pos=1)
    column = tb.UInt16Col(pos=2)
    row = tb.UInt16Col(pos=3)
    charge = tb.UInt16Col(pos=4)


class MetaInfoEventTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    time_stamp = tb.Float64Col(pos=1)
    error_code = tb.UInt32Col(pos=2)


class ClusterHitInfoTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    frame = tb.UInt8Col(pos=1)
    column = tb.UInt16Col(pos=2)
    row = tb.UInt16Col(pos=3)
    charge = tb.UInt16Col(pos=4)
    cluster_id = tb.UInt16Col(pos=5)
    is_seed = tb.UInt8Col(pos=6)
    cluster_size = tb.UInt16Col(pos=7)
    n_cluster = tb.UInt16Col(pos=8)


class ClusterInfoTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    id = tb.UInt16Col(pos=1)
    n_hits = tb.UInt16Col(pos=2)
    charge = tb.Float32Col(pos=3)
    seed_column = tb.UInt16Col(pos=4)
    seed_row = tb.UInt16Col(pos=5)
    mean_column = tb.Float32Col(pos=6)
    mean_row = tb.Float32Col(pos=7)
