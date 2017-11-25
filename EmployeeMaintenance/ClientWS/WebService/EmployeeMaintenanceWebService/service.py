'''
Service
'''
from urllib.request import urlopen
from hashlib import md5
import json
from datetime import datetime
from flask import Flask, jsonify, request
from models.employee import Employee
from models.person import Person
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
    @app.route("/employee/<client_id>", methods=['GET'])
    def payments(client_id):
        client = ClientModel()
        Database.set_engine()
        try:
            Database.open_connection()
            client.get_data(client_id)
            Log.debug(str(client.client_id))
            if str(client.client_id) != client_id or client_id == '0':
                return json.dumps({})
            if client.api_token_vivid_seats:
                data = VividPaymentsRawModel.get_payments(client.client_id)
                return json.dumps(data)
            elif client.api_token_ticket_evolution:
                data = TicketEvolutionPaymentsRawModel.get_payments(client.client_id)
                return json.dumps(data)
            elif client.user_guid_stubhub:
                data = StubhubPaymentRawModel.get_payments(client.client_id)
                return json.dumps(data)
        except Exception as ex:
            raise InvalidUsage(str(ex), status_code=500)
        finally:
            Database.close_connection()
        return json.dumps({})


if __name__ == "__main__":
    app.run()
