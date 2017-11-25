'''
Database class
'''
import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database(object):
    session = None
    engine = None
    connection = None

    @classmethod
    def create_session(cls):
        if cls.session is not None:
            return
        # configure Session class with desired options
        Session = sessionmaker()
        # later, we create the engine
        cls.set_engine()
        # associate it with our custom Session class
        Session.configure(bind=cls.engine)
        # work with the session
        cls.session = Session()


    @classmethod
    def open_connection(cls):
        if cls.session is None and cls.engine is None:
            raise "Session and engine are not defined"
        if cls.connection != None:
            cls.connection.close()
        if cls.session:
            cls.connection = cls.session.connection()
        else:
            cls.connection = cls.engine.connect()
    
    @classmethod
    def close_connection(cls):
        if cls.connection is not None:
            cls.connection.close()
            cls.connection = None

    @classmethod
    def close_session(cls):
        if cls.session is not None:
            cls.session.close()
            cls.session = None
    
    @classmethod
    def set_engine(cls):
        if cls.engine is None:
            cls.engine = create_engine('mssql+pyodbc://%s:%s@%s/%s?driver=SQL+Server+Native+Client+11.0'\
                % (settings.SQLSERVER_USERNAME, settings.SQLSERVER_PASSWORD, settings.SQLSERVER_HOST, settings.SQLSERVER_DB))
