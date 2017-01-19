import ckan.model as model

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from ckan.model.meta import metadata,  mapper, Session


slider_table = Table(
    'slider',
    metadata,
    Column('id_slider', types.INTEGER, primary_key=True),
    Column('image', types.String(300)),
    Column('h1', types.String(300), nullable=True),
    Column('p', types.String(3000), nullable=True),
    Column('button_left_link', types.String(300), nullable=True),
    Column('button_left_name', types.String(50), nullable=True),
    Column('button_left_enabled', types.Boolean, default=False),
    Column('button_right_link', types.String(300), nullable=True),
    Column('button_right_name', types.String(50), nullable=True),
    Column('button_right_enabled', types.Boolean, default=False),
    Column('is_text_left', types.Boolean, default=True),
    Column('ordering', types.SmallInteger, default=0, index=True),
    Column('is_active', types.Boolean, index=True, default=True)
)


class Slider(model.DomainObject):

    @classmethod
    def get(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).first()

    @classmethod
    def find(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw)

    def get_slider_items(self):
        pass


model.meta.mapper(Slider, slider_table)
