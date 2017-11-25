'''
EmployeeModel define all operations on model and Employee table in the database.
'''
from sqlalchemy import Table, Column, Integer, String, MetaData, Date
from database import Database

class EmployeeModel(object):
    '''
    EmployeeModel
    '''
    __table = None

    def __init__(self, employee_id, person_id, employee_num, employed_date, terminated_date):
        """
        Init
        """
        self.employee_id = employee_id
        self.person_id = person_id
        self.employee_num = employee_num
        self.employed_date = employed_date
        self.terminated_date = terminated_date

    @classmethod
    def get_table(cls):
        '''
        Get model of Employee table in the database.
        :result: Model of the table
        '''
        if cls.__table is None:
            cls.__table = Table('Employee', MetaData(), \
            Column('EmployeeId', Integer, primary_key=True), \
            Column('PersonId', Integer), \
            Column('EmployeeNum', String), \
            Column('EmployedDate', Date), \
            Column('TerminatedDate', Date), \
            )
        return cls.__table

    def save(self):
        '''
        Save Employee
        '''
        if not Database.connection:
            return
        Database.connection.execute(EmployeeModel.get_table().update(EmployeeModel.get_table().c.EmployeeId == self.employee_id)\
            if self.employee_id != 0 else EmployeeModel.get_table().insert(None),  \
           PersonId=self.person_id, EmployeeNum=self.employee_num, EmployedDate=self.employed_date, TerminatedDate=self.terminated_date)
        if self.employee_id == 0:
            self.employee_id =  Database.connection.execute("SELECT MAX(EmployeeId) FROM Employee").fetchone()[0]
        return self.employee_id

    def delete(self):
        '''
        Delete employee
        '''
        if not Database.connection:
            return
        Database.connection.execute(EmployeeModel.get_table().delete(EmployeeModel.get_table().c.EmployeeId == self.employee_id))
    
    @classmethod
    def delete_by_personid(cls, person_id):
        '''
        Delete employees
        '''
        if not Database.connection:
            return
        Database.connection.execute(cls.get_table().delete(cls.get_table().c.PersonId == person_id))

    def getdata(self):
        '''
        Get employee
        '''
        if not Database.connection:
            return
        item = Database.connection.execute(EmployeeModel.get_table().select(EmployeeModel.get_table().c.EmployeeId == self.employee_id)).fetchone()
        self.person_id = item["PersonId"] if item and "PersonId" in item else ""
        self.employee_num = item["EmployeeNum"] if item and "EmployeeNum" in item else ""
        self.employed_date = item["EmployedDate"] if item and "EmployedDate" in item else ""
        self.terminated_date = item["TerminatedDate"] if item and "TerminatedDate" in item else ""
    

