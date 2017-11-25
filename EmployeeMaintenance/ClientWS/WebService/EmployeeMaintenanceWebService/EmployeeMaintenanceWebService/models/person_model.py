'''
PersonModel defines all operations on the model and Person table in the database.
'''
from sqlalchemy import Table, Column, String, MetaData, Date, Integer
from database import Database

class PersonModel(object):
    '''
    PersonModel class
    '''
    __table = None

    def __init__(self, person_id, last_name, first_name, birth_date):
        """
        Init
        """
        self.person_id = person_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date

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
            Column('BirthDate', Date), \
            )
        return cls.__table

   
    def save(self):
        '''
        Save person
        '''
        if not Database.connection:
            return
        Database.connection.execute(PersonModel.get_table().update(PersonModel.get_table().c.PersonId == self.person_id)\
            if self.person_id != 0 else PersonModel.get_table().insert(None), \
           LastName=self.last_name, FirstName=self.first_name, BirthDate=self.birth_date)
        if not self.person_id:
            self.person_id =  Database.connection.execute("SELECT MAX(PersonId) FROM Person").fetchone()[0]
        return self.person_id

    def delete(self):
        '''
        Delete person
        '''
        if not Database.connection:
            return
        Database.connection.execute(PersonModel.get_table().delete(PersonModel.get_table().c.PersonId == self.person_id))

    def getdata(self):
        '''
        Get person
        '''
        if not Database.connection:
            return
        item = Database.connection.execute(PersonModel.get_table().select(PersonModel.get_table().c.PersonId == self.person_id)).fetchone()
        self.last_name = item["LastName"] if item and "LastName" in item else ""
        self.first_name = item["FirstName"] if item and "FirstName" in item else ""
        self.birth_date = item["BirthDate"] if item and "BirthDate" in item else ""
        
