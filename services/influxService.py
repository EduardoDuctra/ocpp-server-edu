import asyncio
import datetime
import logging
import time, json
import pandas as pd
from influxdb import InfluxDBClient
from typing import Optional
from pytz import timezone, utc
from datetime import datetime



def customTime(*args):
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("America/Sao_Paulo")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()

'''
Connection with InfluxDB (Global)
'''
INFLUXDB_HOST = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_USER = "ocppUFSM"
INFLUXDB_PASS = "OcppUfsm2021"
INFLUXDB_DB = "ocpp"
INFLUXDB_MEASUREMENT_METER = "OCPP_CEESP_METERVALUES"
INFLUXDB_MEASUREMENT_STATUS = "OCPP_CEESP_STATUS"
INFLUXDB_MEASUREMENT_ENERGY = "OCPP_CEESP_ENERGY"



def buildMeterValuesInflux(charger_id: str, connector_id: int, transaction_id: int, Corrente: float, EnergiaAtual: float, EnergiaTotal: float, Potencia: float, Soc: float, Tensao: float):
   METERVALUES_BODY = [
       {
         "measurement": INFLUXDB_MEASUREMENT_METER,
         "tags":{
           "charger_id": charger_id,
           "connector_id": connector_id
         },
         "fields": {
           "transaction_id": transaction_id,
           "Corrente": Corrente,
           "EnergiaAtual": EnergiaAtual,
           "EnergiaTotal": EnergiaTotal,
           "Potencia": Potencia,
           "Soc": Soc,
           "Tensao": Tensao
         }
       }
   ]
   logging.info('Envio de dados: MeterValues')
   write_points_to_influxdb(METERVALUES_BODY)


def buildStatusInflux(charger_id: str, connector_id: int, error_code: str, status: str):
   STATUS_BODY = [
       {
         "measurement": INFLUXDB_MEASUREMENT_STATUS,
         "tags":{
           "charger_id": charger_id,
           "connector_id": connector_id
         },
         "fields": {
           "status": status,
           "error_code": error_code
         }
       }
   ]
   logging.info('Envio de dados: Status')
   write_points_to_influxdb(STATUS_BODY)


def buildEnergiaInflux(charger_id: str, connector_id: int, EnergiaIouF: float):
   ENERGY_BODY= [
       {
         "measurement": INFLUXDB_MEASUREMENT_ENERGY,
         "tags":{
           "charger_id": charger_id,
           "connector_id": connector_id
         },
         "fields": {
           "EnergiaIouF": EnergiaIouF
         }
       }
   ]
   logging.info('Envio de dados: Energia')
   write_points_to_influxdb(ENERGY_BODY)



def write_points_to_influxdb(points):
  client = InfluxDBClient(
    host=INFLUXDB_HOST, port=INFLUXDB_PORT,
    username=INFLUXDB_USER, password=INFLUXDB_PASS,
    database=INFLUXDB_DB, timeout=10)
  try:
    client.write_points(points=points, time_precision='s')
  except Exception:
    logging.error("Erro ao adicionar os dados no influx.")


def read_points_to_influxdb(charger_id: str, connector_id: int, func_query: str):
  client = InfluxDBClient(
    host=INFLUXDB_HOST, port=INFLUXDB_PORT,
    username=INFLUXDB_USER, password=INFLUXDB_PASS,
    database=INFLUXDB_DB, timeout=10)
  if(func_query == 'status'):
    query = 'SELECT last("status") FROM "OCPP_CEESP_STATUS" WHERE ("charger_id" = ' + '\'' +  str(charger_id) + '\'' +' AND "connector_id" =' +'\'' + str(connector_id) + '\'' + ')'
  elif(func_query == 'energy'):
    query = 'SELECT last("EnergiaIouF") FROM "OCPP_CEESP_ENERGY" WHERE ("charger_id" = ' + '\'' +  str(charger_id) + '\'' +' AND "connector_id" =' +'\'' + str(connector_id) + '\'' + ')'
  else:
    return
  try:
    result =  client.query(query)
    for point in result.get_points():
        return point['last']
  except Exception:
    logging.error("Erro ao ler os dados no influx.")


class myInfluxDB:
    def clearMeterValues(data):
        charger_id = data['charger_id']
        connector_id = data['connector_id']
        transaction_id = data['transaction_id']

        metervalues = data['meter_value']
        metervalues = pd.json_normalize(metervalues)
        try:
          metervalues = metervalues['sampled_value']
        except:
          metervalues = metervalues['sampledValue']
        metervalues = metervalues[0]
        df = pd.json_normalize(metervalues)


        if(connector_id == 1):
            getEnergy = df.value.loc[(df["measurand"] == "Energy.Active.Import.Register")]
            getStop = df.context.loc[(df["measurand"] == "Energy.Active.Import.Register")]

            index = getEnergy.index[0]
            EnergiaTotal = float(getEnergy[index])
            Corrente = float(0)
            Potencia = float(0)
            Soc = float(0)
            Tensao = float(0)

            index = getStop.index[0]
            print(getStop[index])
            if(getStop[index] == ('Transaction.Begin' or 'Transaction.End')):
                EnergiaIouF = EnergiaTotal
                buildEnergiaInflux(charger_id, connector_id, EnergiaIouF)   

        elif(connector_id != 1):
            getCurrent = df.value.loc[(df["measurand"] == "Current.Import")]
            getEnergy = df.value.loc[(df["measurand"] == "Energy.Active.Import.Register")]
            getPower = df.value.loc[(df["measurand"] == "Power.Active.Import")]
            getSoc = df.value.loc[(df["measurand"] == "SoC")]
            getVoltage = df.value.loc[(df["measurand"] == "Voltage")]
            getStop = df.context.loc[(df["measurand"] == "Current.Import")]

            index = getCurrent.index[0]
            Corrente = float(getCurrent[index])
            index = getEnergy.index[0]
            EnergiaTotal = float(getEnergy[index])
            index = getPower.index[0]
            Potencia = float(getPower[index])
            index = getSoc.index[0]
            Soc = float(getSoc[index])
            index = getVoltage.index[0]
            Tensao = float(getVoltage[index])

            index = getStop.index[0]
            if(getStop[index] == 'Transaction.Begin'):
                EnergiaIouF = EnergiaTotal
                buildEnergiaInflux(charger_id, connector_id, EnergiaIouF)

            if(getStop[index] == 'Transaction.End'):
                Soc = float(0)
                Tensao = float(0)
                EnergiaIouF = EnergiaTotal
                Corrente = float(0)
                Potencia = float(0)
                buildEnergiaInflux(charger_id, connector_id, EnergiaIouF)

        EnergiaHistorica = read_points_to_influxdb(charger_id, connector_id, 'energy')
        EnergiaAtual = EnergiaTotal - float(EnergiaHistorica)
      
        buildMeterValuesInflux(charger_id, connector_id, transaction_id, Corrente, EnergiaAtual, EnergiaTotal, Potencia, Soc, Tensao)
        return


    def clearStatus(data):
        charger_id = (data["charger_id"])
        connector_id = (data["connector_id"])
        error_code = (data["error_code"])
        status = (data["status"])

        buildStatusInflux(charger_id, connector_id, error_code, status)
        return

  
