# Tarefa realizada por:
# Thiago Macedo - 21104690
# Vitor Pires - 21101680
# Erik Mondin - 

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)

df = pd.read_csv('constituents-financials.csv')
df['Market Cap'] = df['Market Cap'].astype('float64')

def abort_if_company_doesnt_exist(company_id):
    if company_id not in df.index:
        abort(404, message=f'Company {company_id} doesn\'t exist')

parser = reqparse.RequestParser()
parser.add_argument('Symbol')
parser.add_argument('Name')
parser.add_argument('Sector')
parser.add_argument('Price')
parser.add_argument('Price/Earnings')
parser.add_argument('Dividend Yield')
parser.add_argument('Earnings/Share') 
parser.add_argument('52 Week Low') 
parser.add_argument('52 Week High') 
parser.add_argument('Market Cap') 
parser.add_argument('EBITDA')
parser.add_argument('Price/Sales') 
parser.add_argument('Price/Book') 
parser.add_argument('SEC Filings')

class Company(Resource):
    def get(self, company_id):
        abort_if_company_doesnt_exist(company_id)
        return dict(df.loc[company_id])

    def delete(self, company_id):
        abort_if_company_doesnt_exist(company_id)
        df.drop(company_id, inplace=True)
        return 'deleted', 201

    def put(self, company_id):
        args = parser.parse_args()
        content = {'Symbol': args['Symbol'], 
                   'Name': args['Name'], 
                   'Sector': args['Sector'],
                   'Price': args['Price'], 
                   'Price/Earnings': args['Price/Earnings'], 
                   'Dividend Yield':args['Dividend Yield'],
                   'Earnings/Share': args['Earnings/Share'], 
                   '52 Week Low': args['52 Week Low'], 
                   '52 Week high': args['52 Week High'], 
                   'Market Cap': args['Market Cap'], 
                   'EBITDA': args['EBITDA'],
                   'Price/Sales': args['Price/Sales'], 
                   'Price/Book': args['Price/Book'], 
                   'SEC Filings': args['SEC Filings']}
        df.loc[company_id] = content
        abort_if_company_doesnt_exist(company_id)
        return content, 201

class CompanyList(Resource):
    def get(self):
        companies = {}
        for index in df.index:
            company = dict(df.loc[index])
            companies[index] = company
        return companies

    def post(self):
        args = parser.parse_args()
        company_id = max(df.index) + 1
        content = {'Symbol': args['Symbol'], 
                   'Name': args['Name'], 
                   'Sector': args['Sector'],
                   'Price': args['Price'], 
                   'Price/Earnings': args['Price/Earnings'], 
                   'Dividend Yield':args['Dividend Yield'],
                   'Earnings/Share': args['Earnings/Share'], 
                   '52 Week Low': args['52 Week Low'], 
                   '52 Week high': args['52 Week High'], 
                   'Market Cap': args['Market Cap'], 
                   'EBITDA': args['EBITDA'],
                   'Price/Sales': args['Price/Sales'], 
                   'Price/Book': args['Price/Book'], 
                   'SEC Filings': args['SEC Filings']}
        df.loc[company_id] = content
        return str(company_id)+' inserido como sucesso'


api.add_resource(Company, '/company/<int:company_id>')
api.add_resource(CompanyList, '/companies')

app.run(debug=True)