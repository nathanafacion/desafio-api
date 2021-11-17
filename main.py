from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from json import dumps
import json
import requests
from flask_restful import Api, Resource
import datetime
import re

class PurchaseList(Resource):
    def get(self):
        return { 'purchases' : [ self.general_validation(purchase) for purchase in purchaseList  ] }, 200
    
    
    def general_validation(self, puchase):
        date_correct = self.date_validation(puchase["sold_at"])
        customer_correct = self.customer_validation(puchase["customer"])
        products_correct = self.products_validation(puchase["total"], puchase["products"])
        if (date_correct["WithoutError"] and products_correct["WithoutError"] and customer_correct["WithoutError"]):
            return puchase
        else: 
            return {"WithoutError": True,
                    "message": date_correct["message"] + customer_correct["message"] 
                              + products_correct["message"] }

    
    def date_validation(self, date):
        # Valida se eh data mesmo
        date_regex = re.compile('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')
        if(date_regex.match(date) != None):
            # Separa em Ano, Mes, Dia, Hora, Minutos
            date = date.replace(':',' ').replace('-',' ').split(" ")
            now = datetime.datetime.now()
            datetime_buy = datetime.datetime(int(date[0]), int(date[1]), int(date[2]),
                                            int(date[3]), int(date[4]))
            if datetime_buy < now:
                return {"WithoutError": True, "message":''}
        
        return {"WithoutError": False, "message": "Date invalid. "}
        
    
    def customer_validation(self, customer):
        if(self.validation_empty_and_type(customer["document"])
           and self.validation_empty_and_type(customer["name"])):
            # fazer validacao de numero de documento (se sao 11 numeros msm)
            document_regex = re.compile('(\d{11})')
            if(document_regex.match(customer["document"])!= None):
                return {"WithoutError": True, "message":''}
        
        return {"WithoutError": False, "message": "Consumer invalid"}
    
   
    def products_validation(self, total, products):
        sum_value = 0
        for p in products:
           if(self.validation_empty_and_type(p["type"]) and self.validation_empty_and_type(float(p["value"]),'float') 
              and self.validation_empty_and_type(p["qty"],'int')):
               sum_value = sum_value + float(p["value"])*int(p["qty"])
        if (float(total) == sum_value):
            return {"WithoutError": True, "message": ""}    
        return {"WithoutError": False, "message": "Products invalid"}
    
    
    def validation_empty_and_type(self, value, type='string'):
        type_correct = False
        if type == 'string':
            type_correct = isinstance(value, str)
        if type == 'int':
            type_correct = isinstance(value, int)
        if type == 'float':
            type_correct = isinstance(value, float)
        return value != " " and value != None and type_correct




if __name__ == '__main__':
    app = Flask(__name__)
    purchaseList = json.load(open('mock.json',))
    api = Api(app)
    api.add_resource(PurchaseList, '/purchases')
    app.run()
    
    #response_API = requests.get("https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback")
    #print(response_API.status_code)
    #print(response_API.text)