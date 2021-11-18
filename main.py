import requests
import json

def save_file(data):
    with open('complete_purchase.json', 'w') as outfile:
        outfile.write(str(data))


if __name__ == '__main__':
    get_purchase = requests.get("http://127.0.0.1:5000/purchases").json()
    # requisicoes realizada e status
    complete_purchase = [] 
    for p in get_purchase["purchases"]:
        if not "WithoutError" in p:
            response_API = requests.post("https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback", 
                        data = {'document': p["customer"]["document"],'cashback':p["cashback"]})
            print(response_API.status_code)
            print(response_API.text)
            complete_purchase.append(response_API.text)
    save_file(complete_purchase)