'''
PersonModel defines all operations on the model and Person table in the database.
'''
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, and_
from database import Database

class PersonModel(object):
    '''
    UserModel
    '''
    __table = None

    @classmethod
    def get_table(cls):
        '''
        Get model of UserModel table in the database
        '''
        if cls.__table is None:
            cls.__table = Table('Person', MetaData(), \
            Column('PersonId', Integer, primary_key=True), \
            Column('LastName', String), \
            Column('FirstName', String), \
            Column('BirthDate', String), \
            )
        return cls.__table

    @classmethod
    def exists(cls, username, password):
        '''
        Does exist an user with credentials
        :param username: Username
        :param password: Password
        :result: User exists or not
        '''
        res = Database.connection.execute(cls.get_table().select(and_(cls.get_table().c.Username == \
        username, cls.get_table().c.Password == password))).fetchone()
        return True if res else False
