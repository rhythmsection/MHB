from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text

from sqlalchemy.orm import sessionmaker
import fingerprinter

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here

class Song(Base):
	__tablename__ = "songs"

	id = Column(Integer, primary_key = True)
	title = Column(String(80), nullable = True)
	album = Column(String(80), nullable = True)
	artist = Column(String(80), nullable = True)
	fingerprint = Column(Text, nullable = True)

    #def compare_fingerprint(self, fingerprint):
        #if self.fingerprint <comparative quality> fingerprint:
            #return "Yay it is a match"

### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///fingerprints.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
