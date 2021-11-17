from flask import Flask, request, jsonify
from flask_restful import Resource

class BuysList(Resource):
    
    #def __init__(self, buyList):
    #    self.buysList = buyList


    
    def get(self):
        
        return { 'buys' : [ self.geral_validation(buy) for buy in self.buysList  ] }, 200
    
    def geral_validation(self, buy):
        print(buy)
