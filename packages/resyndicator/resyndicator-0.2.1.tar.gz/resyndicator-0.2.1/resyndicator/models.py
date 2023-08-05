import importlib
from sqlalchemy import create_engine, Column, DateTime, Unicode
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from utilofies.stdlib import canonicalized
from . import settings


Base = declarative_base()


class EntryBase(object):
    __tablename__ = 'entry'

    id = Column(Unicode, primary_key=True)
    updated = Column(DateTime, index=True, nullable=False)
    published = Column(DateTime)
    fetched = Column(DateTime)
    title = Column(Unicode)
    author = Column(Unicode)
    link = Column(Unicode)
    summary = Column(Unicode)
    summary_type = Column(Unicode)
    content = Column(Unicode)
    content_type = Column(Unicode)
    source_id = Column(Unicode)
    source_title = Column(Unicode)
    source_link = Column(Unicode)

    def as_dict(self):
        return canonicalized({
            'id': self.id,
            'updated': self.updated,
            'published': self.published,
            'title': self.title,
            'author': self.author,
            'link': self.link,
            'description': self.summary,
            'content': self.content,
            'source': {'id': self.source_id,
                       'title': self.source_title,
                       'updated': self.updated,
                       'links': [{'href': self.source_link, 'rel': 'self'}]}})

    def __repr__(self):
        return '<Entry({id})>'.format(id=self.id)


if settings.ENTRY_CLASS:
    module_name, class_name = settings.ENTRY_CLASS.split(':')
    module = importlib.import_module(module_name)
    Entry = getattr(module, class_name)
else:
    class Entry(EntryBase, Base):
        pass


engine = create_engine(settings.DATABASE)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))
