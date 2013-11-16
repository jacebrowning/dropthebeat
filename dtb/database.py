#! /usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, eagerload


Base = declarative_base()

class Song(Base, object):
    __tablename__ = 'songs'

    id = Column('id', Integer, primary_key=True)
    artist = Column('artist', String)
    album = Column('album', String)
    title = Column('title', String)
    genre = Column('genre', String)
    bitrate = Column('bitrate', Integer)
    tracknum = Column('tracknum', Integer)
    year = Column('year', Integer)
    path = Column('path', String)


    def __init__(self, **kw):
        for attr, val in kw.items():
            setattr(self, attr, val)


    def __str__(self):
        return '%s - "%s"' % (self.artist.encode('utf-8'), self.title.encode('utf-8'))


    def to_dict(self):
        return {
            'artist': self.artist,
            'album': self.album,
            'title': self.title,
            'genre': self.genre,
            'bitrate': self.bitrate,
            'tracknum': self.tracknum,
            'year': self.year,
            'path': self.path,
        }


class Library(object):
    def __init__(self, uri, echo=False):
        # Create database engine
        self.engine = create_engine(uri, echo=echo)
        Song.metadata.create_all(self.engine)

        # Start database session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def search(self, query={}):
        q = self.session.query(Song).options(eagerload('*'))
        try:
            for col, value in query.items():
                # Apply filters to columns
                q = q.filter(getattr(Song, col).like(value))
        except AttributeError as e:
            print(e)

        q = q.order_by(Song.id)
        return q.all()


    def add(self, song):
        if self.search(song.to_dict()):
            print('add(): Duplicate:', song)
        else:
            print('add(): Added song:', s)
            self.session.add(song)
            self.session.commit()


if __name__ == '__main__':
    songs = [
        {
            'artist': 'Epica',
            'album': 'Design Your Universe',
            'title': 'Track1',
            'genre': 'Metal',
            'bitrate': 320,
            'tracknum': 1,
            'year': 2013,
            'path': '~/Music/Epica/Track1.mp3',
        },
        {
            'artist': 'Epica',
            'album': 'Design Your Universe',
            'title': 'Track2',
            'genre': 'Metal',
            'bitrate': 320,
            'tracknum': 1,
            'year': 2013,
            'path': '~/Music/Epica/Track2.mp3',
        },
        {
            'artist': 'Epica',
            'album': 'Design Your Universe',
            'title': 'Track3',
            'genre': 'Metal',
            'bitrate': 320,
            'tracknum': 1,
            'year': 2013,
            'path': '~/Music/Epica/Track3.mp3',
        },
        {
            'artist': 'Epica',
            'album': 'Design Your Universe',
            'title': 'Track4',
            'genre': 'Metal',
            'bitrate': 320,
            'tracknum': 1,
            'year': 2013,
            'path': '~/Music/Epica/Track4.mp3',
        }
    ]

    lib = Library('sqlite:///test.db', echo=False)

    for song in songs:
        s = Song(**song)
        lib.add(s)
