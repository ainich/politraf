from infi.clickhouse_orm import models, fields, engines
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import MergeTree
from infi.clickhouse_orm.engines import Memory
from infi.clickhouse_orm.engines import Buffer


class OPEN_PORTS(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    os = StringField()
    os_v = StringField()
    srv = StringField()
    addr = StringField()
    port = StringField()
    product = StringField()
    version = StringField()
    descr = StringField()
    vdesc = StringField()
    title = StringField()
    cvelist = StringField()
    score = Float32Field()

    
    engine = MergeTree('event_date', ('os', 'os_v', 'srv', 'addr', 'port', 'product', 'version', 'descr', 'vdesc', 'score'))
    #engine = Memory()

class IOC_OTX(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    indicator = StringField()
    name = StringField()
    references = StringField()
    #engine = MergeTree('event_date', ('timestamp', 'indicator', 'name', 'references'))
    engine = Memory()

class IOC_SELF(Model):

    event_date = DateField()
    timestamp = DateTimeField()
    indicator = StringField()
    name = StringField()
    references = StringField()
    #engine = MergeTree('event_date', ('timestamp', 'indicator', 'name', 'references'))
    engine = Memory()

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

    engine = MergeTree('event_date',
                       ('timestamp', 'protocol', 'src_addr', 'src_port', 'dst_addr', 'dst_port', 'qry_name'))


class CONNStats_buffer(Model):
    event_date = DateField()
    timestamp = DateTimeField()
    protocol = StringField()
    src_addr = StringField()
    src_port = Float32Field()
    dst_addr = StringField()
    dst_port = Float32Field()
    qry_name = StringField()

    engine = Buffer('connstats', 16, 10, 100, 10000, 1000000, 10000000, 100000000)