from urllib import response
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import *
import ocpp.v16.enums as enums
from ocpp.v16 import call_result, call
import json
from typing import Optional
from datetime import datetime
import random
from utils import dataOut
import os
from dotenv import load_dotenv

load_dotenv()

SEND_DATA_TO_FW = bool(int(os.getenv('SEND_DATA_TO_FW')))
URL_SERVER = os.getenv('URL_SERVER')

class ChargePoint(cp):
    @on(Action.Authorize)
    def on_authorize(
            self,
            id_tag
    ):
        return call_result.AuthorizePayload(
            id_tag_info={
                "status": 'Accepted'
            }
        )

    @on(Action.BootNotification)
    def on_boot_notification(
            self,
            charge_point_vendor: str,
            charge_point_model: str,
            charge_box_serial_number: Optional[str] = "None",
            charge_point_serial_number: Optional[str] = "None",
            firmware_version: Optional[str] = "None",
            iccid: Optional[str] = "None",
            **kwargs
    ):

        sendData = [{
                "charger_id": self.id,
                "charge_point_vendor": charge_point_vendor,
                "charge_point_model": charge_point_model,
                "charge_box_serial_number": charge_box_serial_number,
                "charge_point_serial_number": charge_point_serial_number,
                "firmware_version": firmware_version,
                "iccid": iccid
            }]
        
        if(SEND_DATA_TO_FW):
            response = dataOut.sendDataToServer(URL_SERVER + "bootNotification", "BootNotification", self.id, sendData)
        
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            interval=300,
            status=RegistrationStatus.accepted
        )
        
        
 
    @on(Action.DataTransfer)
    def on_data_transfer(
            self,
            vendor_id: str,
            message_id: Optional[str] = "None",
            data: Optional[str] = "None",
            **kwargs
    ):
        return call_result.DataTransferPayload(
            status='Accepted'
        )

    @on(Action.DiagnosticsStatusNotification)
    def on_diagnostics_status_notification(
            self,
            status: str,
            **kwargs
    ):
        return call_result.DiagnosticsStatusNotificationPayload()

    @on(Action.FirmwareStatusNotification)
    def on_firmware_status_notification(
            self,
            status: str,
            **kwargs
    ):
        return call_result.FirmwareStatusNotificationPayload()

    @on(Action.Heartbeat)
    def on_heartbeat(
            self,
            **kwargs
    ):
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        sendData = [{
                "charger_id": self.id,
                "heartbeat": now
            }]

        if(SEND_DATA_TO_FW):
            response = dataOut.sendDataToServer(URL_SERVER + "heartbeat", "Heartbeat", self.id, sendData)

        return call_result.HeartbeatPayload(
            current_time= now
        )

    @on(Action.MeterValues)
    def on_meter_value(
            self,
            connector_id: int,
            meter_value: list,
            transaction_id: Optional[int] = -1,
            **kwargs
    ):
        sendData = [{
                "charger_id": self.id,
                "connector_id": connector_id,
                "transaction_id": transaction_id,
                "meter_value": meter_value
            }]

        if(SEND_DATA_TO_FW):
            response = dataOut.sendDataToServer(URL_SERVER + "meterValues", "MeterValues", self.id, sendData)

        return call_result.MeterValuesPayload()

    @on(Action.StartTransaction)
    def on_start_transaction(
            self,
            connector_id: int,
            id_tag: str,
            meter_start: int,
            timestamp: str,
            reservation_id: Optional[int] = -1,
            **kwargs
    ):
        
        sendData = [{
                "charger_id": self.id,
                "connector_id": connector_id,
                "tag_id": id_tag,
                "meter_start": meter_start,
                "timestamp": timestamp,
                "reservation_id": reservation_id,
            }]

        if(SEND_DATA_TO_FW):
            response = dataOut.sendDataToServer(URL_SERVER + "startTransaction", "StartTransaction", self.id, sendData)

        try:
            rStatus = response['status']
            rTransaction_id = response['idTransaction']
            if(rStatus == 'charge_allowed'):
                status = "Accepted"
            if(rStatus == 'charge_not_allowed'):
                status = "Invalid"

        except:
            rTransaction_id = random.randint(1000000,9999999)
            status = "Accepted"
        transaction_id = int(rTransaction_id)

        return call_result.StartTransactionPayload(
            id_tag_info={
                "status": status
            },
            transaction_id=int(transaction_id)
        )

    @on(Action.StatusNotification, skip_schema_validation=True)
    def on_status_notification(
            self,
            connector_id: int,
            error_code: str,
            status: str,
            timestamp: Optional[str] = "None",
            info: Optional[str] = "None",
            vendor_id: Optional[str] = "None",
            vendor_error_code: Optional[str] = "None",
            **kwargs
    ):
        sendData = [{
                "charger_id": self.id,
                "connector_id": connector_id,
                "error_code": error_code,
                "status": status,
                "timestamp": timestamp,
                "info": info,
                "vendor_id":vendor_id,
                "vendor_error_code": vendor_error_code
            }]

        if(SEND_DATA_TO_FW):
            response = dataOut.sendDataToServer(URL_SERVER + "statusNotification", "StatusNotification", self.id, sendData)

        return call_result.StatusNotificationPayload()

    @on(Action.StopTransaction)
    def on_stop_transaction(
            self,
            meter_stop: int,
            timestamp: str,
            transaction_id: int,
            reason: Optional[str] = "None",
            id_tag: Optional[str] = "None",
            transaction_data: Optional[list] = "None",
            **kwargs
    ):

        sendData = [{
                "charger_id": self.id,
                "meter_stop": meter_stop,
                "timestamp": timestamp,
                "transaction_id": transaction_id,
                "reason": reason,
                "tag_id": id_tag,
                "transaction_data": transaction_data
            }]
        

        if(SEND_DATA_TO_FW):
            response = dataOut.sendDataToServer(URL_SERVER + "stopTransaction", "StopTransaction", self.id, sendData)

        return call_result.StopTransactionPayload()

    """------------------- Funções chamadas pelo CSMS -------------------"""

    async def change_configuration(self, key: str, value: str):
        request = call.ChangeConfigurationPayload(
            key=key, 
            value=value
        )
        response = await self.call(request)
        return response.status

    async def reset(self, value: str):
        request = call.ResetPayload(
            type=value
        )
        response = await self.call(request)
        return response.status


    async def get_configuration(self): 
        request = call.GetConfigurationPayload()
        response = await self.call(request)
        return json.dumps(response.configuration_key)


    async def remote_start_transaction(self, charger_id: str, connector_id: int):
        request = call.RemoteStartTransactionPayload(
            id_tag=charger_id,
            connector_id = connector_id
        )
        response = await self.call(request)
        return response.status


    async def remote_stop_transaction(self, transaction_id: int):
        request = call.RemoteStopTransactionPayload(
            transaction_id = transaction_id
        )
        response = await self.call(request)
        return response.status


    async def unlock_connector(self, connector_id: int):
        request = call.UnlockConnectorPayload(
            connector_id=connector_id
        )
        response = await self.call(request)
        return response.status


    async def availability_type(self, connector_id: int, type: str):
        request = call.ChangeAvailabilityPayload(
            connector_id=connector_id,
            type=type
        )
        response = await self.call(request)
        return response.status

    async def clear_cache(self):
        request = call.ClearCachePayload()
        response = await self.call(request)
        return response.status

    async def set_charge_max_prof(self, connector_id, startSchedule, limit):
        cs_charging_profiles = {
            "chargingProfileId": 1,   
            "stackLevel": 0,
            "chargingProfilePurpose": "TxDefaultProfile",
            "chargingProfileKind": "Absolute",
            "chargingSchedule": {
                "startSchedule": startSchedule,    
                "chargingRateUnit": "A",
                "chargingSchedulePeriod": [{
                    "startPeriod": 0,
                    "limit": limit
                }]
            }
        }

        request = call.SetChargingProfilePayload(
            connector_id=connector_id,
            cs_charging_profiles=cs_charging_profiles
        )

        response = await self.call(request)
        return response.status


    async def set_charge_max_prof_rec(self, connector_id, chargingSchedulePeriod):
        cs_charging_profiles = {
            "chargingProfileId":1,
            "stackLevel":1,
            "chargingProfilePurpose":"TxDefaultProfile",
            "chargingProfileKind":"Recurring",
            "recurrencyKind": "Daily",
            "chargingSchedule":{
                "duration": 86400,
                "chargingRateUnit":"A",
                "chargingSchedulePeriod": chargingSchedulePeriod
            }
        }
        

        request = call.SetChargingProfilePayload(
            connector_id=connector_id,
            cs_charging_profiles=cs_charging_profiles
        )

        response = await self.call(request)
        return response.status
        

    async def clear_configuration_profile(self):
        request = call.ClearChargingProfilePayload()
        response = await self.call(request)
        return response.status
