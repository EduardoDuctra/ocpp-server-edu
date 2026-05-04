import logging
import json
import requests

headers={
    'Content-type':'application/json'
}

def functoJson(data):
    var = "".join(map(str,data))
    payload = var.replace("\'", "\"")
    payload=json.dumps(json.JSONDecoder().decode(payload))
    return payload

def sendDataToServer(url: str, func: str, charger_id: str, sendData):
    try:
        response = requests.post(url, headers=headers, data = functoJson(sendData), timeout=5)
        return response.json()
    except requests.exceptions.HTTPError as errh:
        logging.error('ERROR: %s -> no envio da funcao %s do carregador id = %s', errh, func, charger_id)
    except requests.exceptions.ConnectionError as errc:
        logging.error('ERROR: %s -> no envio da funcao %s do carregador id = %s', errc, func, charger_id)
    except requests.exceptions.Timeout as errt:
        logging.error('ERROR: %s -> no envio da funcao %s do carregador id = %s', errt, func, charger_id)
    except requests.exceptions.RequestException as err:
        logging.error('ERROR: %s -> no envio da funcao %s do carregador id = %s', err, func, charger_id)