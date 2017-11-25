'''
ClientModel define all operations on model and Clients table in database.
'''
from sqlalchemy import Table, Column, Integer, String, MetaData
from database import Database

class ClientModel(object):
    '''
    ClientModel
    '''
    __table = None

    def __init__(self):
        self.name = None
        self.dashboard_name = None
        self.client_id = None
        self.account_skybox = None
        self.api_key_stubhub = None
        self.api_token_vivid_seats = None
        self.api_token_skybox = None
        self.api_token_ticket_evolution = None
        self.api_secret_stubhub = None
        self.api_secret_ticket_evolution = None
        self.username_stubhub = None
        self.password_stubhub = None
        self.user_guid_stubhub = None

    def get_data(self, client_id):
        '''
        Get data of the client.
        :param client_id: Client Id
        :result: Client model
        '''
        res = Database.connection.execute(ClientModel.get_table().select(\
        ClientModel.get_table().c.Id == client_id))
        row = res.fetchone()
        if not row:
            return
        self.client_id = row['Id']
        self.account_skybox = row['AccountSkybox']
        self.dashboard_name = row['DashboardName']
        self.api_key_stubhub = row['APIKeyStubhub']
        self.api_token_vivid_seats = row['APITokenVividSeats']
        self.api_token_skybox = row['APITokenSkybox']
        self.api_token_ticket_evolution = row['APITokenTicketEvolution']
        self.api_secret_stubhub = row['APISecretStubhub']
        self.api_secret_ticket_evolution = row['APISecretTicketEvolution']
        self.username_stubhub = row['UsernameStubhub']
        self.password_stubhub = row['PasswordStubhub']
        self.user_guid_stubhub = row['UserGuidStubhub']

    def get_by_dashboard_companyname(self, companyname):
        '''
        Get data of the client.
        :param companyname: dashboard companyname
        :result: Client model
        '''
        res = Database.connection.execute(ClientModel.get_table().select(\
        ClientModel.get_table().c.DashboardName == companyname))
        row = res.fetchone()
        if not row:
            return
        self.client_id = row['Id']
        self.account_skybox = row['AccountSkybox']
        self.dashboard_name = row['DashboardName']
        self.api_key_stubhub = row['APIKeyStubhub']
        self.api_token_vivid_seats = row['APITokenVividSeats']
        self.api_token_skybox = row['APITokenSkybox']
        self.api_token_ticket_evolution = row['APITokenTicketEvolution']
        self.api_secret_stubhub = row['APISecretStubhub']
        self.api_secret_ticket_evolution = row['APISecretTicketEvolution']
        self.username_stubhub = row['UsernameStubhub']
        self.password_stubhub = row['PasswordStubhub']
        self.user_guid_stubhub = row['UserGuidStubhub']

    @classmethod
    def get_table(cls):
        '''
        Get model of Clients table in the database.
        :result: Model of the table
        '''
        if cls.__table is None:
            cls.__table = Table('Clients', MetaData(), \
            Column('Id', Integer, primary_key=True), \
            Column('Name', String), \
            Column('DashboardName', String), \
            Column('AccountSkybox', String), \
            Column('APIKeyStubhub', String), \
            Column('APITokenVividSeats', String), \
            Column('APITokenSkybox', String), \
            Column('APITokenTicketEvolution', String), \
            Column('APISecretStubhub', String), \
            Column('APISecretTicketEvolution', String), \
            Column('UsernameStubhub', String), \
            Column('PasswordStubhub', String), \
            Column('UserGuidStubhub', String), \
            )
        return cls.__table

    @classmethod
    def add_client(cls, name, dashboard_name, account_skybox, api_key_stubhub, 
       api_token_vivid_seats, api_token_skybox, api_token_ticket_evolution, api_secret_stubhub,
       api_secret_ticket_evolution, username_stubhub, password_stubhub, user_guid_stubhub):
        '''
        Add client to the database.
        :param name: Name
        :param dashboard_name: DashboardName
        :param account_skybox: AccountSkybox
        :param api_key_stubhub: API Key Stubhub
        :param api_token_vivid_seats: API Token Vivid Seats
        :param api_token_skybox: API Token Vivid Invoices
        :param api_token_ticket_evolution: API Token Ticket Evolution
        :param api_secret_stubhub: API Secret Stubhub
        :param api_secret_ticket_evolution: API Secret Ticket Evolution
        :param username_stubhub: Username Stubhub
        :param password_stubhub: Password Stubhub
        :param user_guid_stubhub: User GUID Stubhub
        '''
        if not Database.connection:
            return
        Database.connection.execute(cls.get_table().insert(None), \
            Name=name, DashboardName=dashboard_name, AccountSkybox=account_skybox, APIKeyStubhub=api_key_stubhub, \
                           APITokenVividSeats=api_token_vivid_seats, APITokenSkybox=api_token_skybox,\
                           APITokenTicketEvolution=api_token_ticket_evolution, APISecretStubhub=api_secret_stubhub,\
                           APISecretTicketEvolution=api_secret_ticket_evolution,\
                           UsernameStubhub=username_stubhub, PasswordStubhub=password_stubhub, UserGuidStubhub=user_guid_stubhub)

    @classmethod
    def get_ids(cls):
        '''
        Get ids of clients.
        :result: Model Ids
        '''
        if not Database.connection:
            return
        result = []
        for res in Database.connection.execute(ClientModel.get_table().select()):
            result.append(res['Id'])
        return result

    def determine_vendors_and_pos(self):
        '''
        Get client vendors and pos.
        :result: vendors and pos
        '''
        results = {"vendors":[], "pos":[]}
        if self.api_token_vivid_seats:
            results["vendors"].append("VividPayments")
        if self.api_token_ticket_evolution:
            results["vendors"].append("TicketEvolutionPayments")
        if self.user_guid_stubhub:
            results["vendors"].append("StubhubPayment")
        if self.api_token_skybox:
            results["pos"].append("Skybox")
        return results

