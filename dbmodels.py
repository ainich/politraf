from infi.clickhouse_orm import models, fields, engines
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import MergeTree

class IOC_OTX(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    indicator = StringField()
    name = StringField()
    references = StringField()
    
    engine = MergeTree('event_date', ('timestamp', 'indicator', 'name', 'references'))

class IOCStats(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    protocol = StringField()
    src_addr = StringField()
    src_port = Float32Field()
    dst_addr = StringField()
    dst_port = Float32Field()
    qry_name = StringField()
    indicator = StringField()
    name = StringField()
    references = StringField()

    engine = MergeTree('event_date', ('timestamp', 'protocol', 'src_addr', 'src_port', 'dst_addr', 'dst_port', 'qry_name', 'indicator', 'name', 'references'))

class CPUStats(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    cpu_id = UInt16Field()
    cpu_percent = Float32Field()

    engine = MergeTree('event_date', ('cpu_id', 'cpu_percent', 'timestamp'))

class MEMStats(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    total = Float32Field()
    used = Float32Field()

    engine = MergeTree('event_date', ('total', 'used', 'timestamp'))

class DISKStats(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    total = Float32Field()
    used = Float32Field()

    engine = MergeTree('event_date', ('total', 'used', 'timestamp'))

class CONNStats(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    protocol = StringField()
    src_addr = StringField()
    src_port = Float32Field()
    dst_addr = StringField()
    dst_port = Float32Field()
    qry_name = StringField()
    
    engine = MergeTree('event_date', ('timestamp', 'protocol', 'src_addr', 'src_port', 'dst_addr', 'dst_port', 'qry_name'))
