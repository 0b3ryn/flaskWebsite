from sqlalchemy import schema, types
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import update
from sqlalchemy import delete,join
from passlib.hash import pbkdf2_sha256
from sqlalchemy import *

metadata = schema.MetaData()


engine = create_engine('sqlite:///data.db', echo=True)
metadata.bind = engine
hash = pbkdf2_sha256.encrypt("dummy_pass", rounds=20000, salt_size=16)
connection=engine.connect()


customer = schema.Table('customer', metadata,
    schema.Column('customerid', types.Integer, primary_key=True),
    schema.Column('username', types.Text, default=u''),
    schema.Column('firstname', types.Unicode(255), default=u''),
    schema.Column('lastname', types.Unicode(255), default=u''),
    schema.Column('password', types.Text(), default=hash),
    schema.Column('number', types.Integer(), default=u''),
    schema.Column('programid', types.Integer(), default=u'')
    )

seller = schema.Table('seller', metadata,
    schema.Column('sellerid', types.Integer, primary_key=True),
    schema.Column('username', types.Text, default=u''),
    schema.Column('firstname', types.Unicode(255), default=u''),
    schema.Column('lastname', types.Unicode(255), default=u''),
    schema.Column('password', types.Text(),default=hash)
)


admin = schema.Table('admin', metadata,
    schema.Column('adminid', types.Integer, primary_key=True),
    schema.Column('username', types.Text, default=u''),
    schema.Column('firstname', types.Unicode(255), default=u''),
    schema.Column('lastname', types.Unicode(255), default=u''),
    schema.Column('password', types.Text(),default=hash)
)


program = schema.Table('program', metadata,
    schema.Column('programid', types.Integer, primary_key=True),
    schema.Column('programname', types.Text(), default=u''),
    schema.Column('costpercall', types.Integer(), default=u'')
)


calls = schema.Table('calls', metadata,
    schema.Column('callid', types.Integer, primary_key=True),
    schema.Column('customerid', types.Integer(), default=u''),
    schema.Column('duration', types.Integer(), default=u'')
)





metadata.create_all(checkfirst=True)
