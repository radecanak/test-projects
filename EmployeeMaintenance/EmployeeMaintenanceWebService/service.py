'''
EmployeeMaintenanceWebService
'''
from urllib.request import urlopen
from hashlib import md5
import json
from datetime import datetime
from flask import Flask, jsonify, request
from models.employee_model import EmployeeModel
from models.person_model import PersonModel
from sqlalchemy.exc import IntegrityError
from database import Database
from logger import Log

app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        Log.exception(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        items = dict(self.payload or ())
        items['message'] = self.message
        return items

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

class Service(object):
    @app.route("/api/person", methods=['POST', 'PUT'])
    def update_person():
        if request.method == 'POST' or request.method == 'PUT':
            last_name = request.form.get('last_name')
            first_name = request.form.get('first_name')
            birth_date = datetime.strptime(request.form.get('birth_date'), "%Y-%m-%d")
            person_id = int(request.form.get('person_id')) if 'person_id' in request.form.keys() else 0
            return Service.add_person(last_name, first_name, birth_date, person_id) 

    @app.route("/api/person/<person_id>", methods=['GET', 'DELETE'])
    def person_by_id(person_id):
        if request.method == 'GET':
            return Service.get_person(person_id)
        elif request.method == 'DELETE':
            return Service.delete_person(person_id)

    @app.route("/api/employee", methods=['POST', 'PUT'])
    def update_employee():
        if request.method == 'POST' or request.method == 'PUT':
            employee_id = int(request.form.get('employee_id')) if 'employee_id' in request.form.keys() else 0
            person_id = request.form.get('person_id')
            employee_num = request.form.get('employee_num')
            employed_date = datetime.strptime(request.form.get('employed_date'), "%Y-%m-%d")
            terminated_date = datetime.strptime(request.form.get('terminated_date'), "%Y-%m-%d")
            return Service.add_employee(employee_id, person_id, employee_num, employed_date, terminated_date) 

    @app.route("/api/employee/<employee_id>", methods=['GET', 'DELETE'])
    def employee_by_id(employee_id):
        if request.method == 'GET':
            return Service.get_employee(employee_id)
        elif request.method == 'DELETE':
            return Service.delete_employee(employee_id)

    @staticmethod
    def add_person(last_name, first_name, birth_date, person_id):
        Database.create_session()
        person = None
        try:
            Database.open_connection()
            person = PersonModel(person_id, last_name, first_name, birth_date)
            person.save()
            Database.session.commit()
        except Exception as ex:
            Database.session.rollback()
            raise InvalidUsage(str(ex), status_code=500)
        finally:
            Database.close_connection()
            Database.close_session()
        return json.dumps({'status':'ok', 'person_id':person.person_id, \
            'last_name':person.last_name, 'first_name':person.first_name,\
            'birth_date':datetime.strftime(person.birth_date, "%Y-%m-%d")})

    @staticmethod
    def delete_person(person_id):
        Database.create_session()
        try:
            Database.open_connection()
            EmployeeModel.delete_by_personid(person_id)
            person = PersonModel(person_id, None, None, None)
            person.delete()
            Database.session.commit()
        except Exception as ex:
            Database.session.rollback()
            raise InvalidUsage(str(ex), status_code=500)
        finally:
            Database.close_connection()
            Database.close_session()
        return json.dumps({'status':'ok'})
        

    @staticmethod
    def get_person(person_id):
        Database.set_engine()
        person = PersonModel(person_id, None, None, None)
        try:
            Database.open_connection()
            person.getdata()
        except Exception as ex:
            raise InvalidUsage(str(ex), status_code=500)
        finally:
            Database.close_connection()
        return json.dumps({
            'person_id':person.person_id,
            'last_name':person.last_name,
            'first_name':person.first_name,
            'birth_date':datetime.strftime(person.birth_date, "%Y-%m-%d")})

    @staticmethod
    def add_employee(employee_id, person_id, employee_num, employed_date, terminated_date):
        Database.create_session()
        employee = None
        try:
            Database.open_connection()
            employee = EmployeeModel(employee_id, person_id, employee_num, employed_date, terminated_date)
            employee.save()
            Database.session.commit()
        except Exception as ex:
            Database.session.rollback()
            raise InvalidUsage(str(ex), status_code=500)
        finally:
            Database.close_connection()
            Database.close_session()
        return json.dumps({'status':'ok', 'employee_id':employee.employee_id, 
            'person_id':employee.person_id, 'employee_num':employee.employee_num,\
            'employed_date':datetime.strftime(employee.employed_date, "%Y-%m-%d"),\
            'terminated_date':datetime.strftime(employee.terminated_date, "%Y-%m-%d")
                           })

    @staticmethod
    def delete_employee(employee_id):
        Database.set_engine()
        try:
            Database.open_connection()
            employee = EmployeeModel(employee_id, None, None, None, None)
            employee.delete()
        except Exception as ex:
            raise InvalidUsage(str(ex), status_code=500)
        finally:
            Database.close_connection()
        return json.dumps({'status':'ok',})
        

    @staticmethod
    def get_employee(employee_id):
        Database.set_engine()
        employee = EmployeeModel(employee_id, None, None, None, None)
        try:
            Database.open_connection()
            employee.getdata()
        except Exception as ex:
            raise InvalidUsage(str(ex), status_code=500)
        finally:
            Database.close_connection()
        return json.dumps({
            'employee_id':employee.employee_id,
            'person_id':employee.person_id,
            'employee_num':employee.employee_num,
            'employed_date':datetime.strftime(employee.employed_date, "%Y-%m-%d"),
            'terminated_date':datetime.strftime(employee.terminated_date, "%Y-%m-%d")})


    

if __name__ == "__main__":
    app.run()
