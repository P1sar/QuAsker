from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('body', Text),
    Column('post_time', DateTime),
    Column('user_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=120)),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['question'].create()
    post_meta.tables['user'].columns['last_seen'].create()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['question'].drop()
    post_meta.tables['user'].columns['last_seen'].drop()
    post_meta.tables['user'].columns['password'].drop()
