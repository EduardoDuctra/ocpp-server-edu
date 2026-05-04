import logging
from datetime import datetime, timedelta

class validData():
    def isValidChargerId(data):
        is_charger_id = isinstance(data, str)
        if not data:
            logging.error('validData | isValidChargerId | charger ID is NULL')
            return False
        if not is_charger_id:
            logging.error('validData | isValidChargerId | charger ID must be a string not a '+ str(type(data)))
            return False
        return True
    
    def isValidConnectorId(data):
        is_connector_id = isinstance(data, int)
        if not data >= 0:
            logging.error('validData | isValidConnectorId | Conector ID must be an integer >= 0, not ' + str(data))
            return False
        if not is_connector_id:
            logging.error('validData | isValidConnectorId | Conector ID must be an integer not a '+ str(type(data)))
            return False
        return True
    
    def isValidChargingProfile(data):
        is_charging_profiles = isinstance(data, dict)
        if not data:
            logging.error('validData | isValidChargingProfile | Charging Profile is NULL')
            return False
        if not is_charging_profiles:
            logging.error('validData | isValidChargingProfile | Charging Profile must be a dict not a '+ str(type(data)))
            return False
        return True
    
    def isValidTransactionId(data):
        is_transaction_id = isinstance(data, int)
        if not data >= 0:
            logging.error('validData | isValidTransactionId | Transaction ID must be an integer >= 0, not ' + str(data))
            return False
        if not is_transaction_id:
            logging.error('validData | isValidTransactionId | Transaction ID must be an integer not a '+ str(type(data)))
            return False
        return True
    
    def isValidValue(data):
        is_value = isinstance(data, str)
        if not data:
            logging.error('validData | isValidValue | Value is NULL')
            return False
        if not is_value:
            logging.error('validData | isValidValue | Value must be a string not a '+ str(type(data)))
            return False
        return True
    
    def isValidKey(data):
        is_key = isinstance(data, str)
        if not data:
            logging.error('validData | isValidKey | Key is NULL')
            return False
        if not is_key:
            logging.error('validData | isValidKey | Key must be a string not a '+ str(type(data)))
            return False
        return True
    
    def isValidType(data):
        is_type = isinstance(data, str)
        if not data:
            logging.error('validData | isValidType | Type is NULL')
            return False
        if not is_type:
            logging.error('validData | isValidType | Type must be a string not a '+ str(type(data)))
            return False
        return True

    def isValidLimit(data):
        is_limit = isinstance(data, int)
        if not data > 0:
            logging.error('validData | isValidLimit | Limit must be an integer > 0, not ' + str(data))
            return False
        if not is_limit:
            logging.error('validData | isValidLimit | Limit must be an integer not a '+ str(type(data)))
            return False
        return True

    def isValidDate(data):
        is_date = isinstance(data, str)
        if not data:
            logging.error('validData | isValidDate | Date is NULL')
            return False
        if not is_date:
            logging.error('validData | isValidDate | Date must be a string not a '+ str(type(data)))
            return False
        try:
            datetime.strptime(data, '%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            logging.error('validData | isValidDate | data error ' +str(e))
            return False
        return True


    def isValidStartSchedule(data):
        data = datetime.strptime(data, '%Y-%m-%dT%H:%M:%SZ')
        if(data.isoformat() < datetime.utcnow().isoformat()):
            #result = datetime.utcnow() + timedelta(minutes=1)
            result = datetime.utcnow()
            result = result.strftime("%Y-%m-%dT%H:%M:%SZ")
            return result
        return data.strftime("%Y-%m-%dT%H:%M:%SZ")


    def isValidChargingSchedulePeriod(data):
        is_ChargingSchedulePeriod = isinstance(data, list)
        if not data:
            logging.error('validData | isValidChargingSchedulePeriod | Date is NULL')
            return False
        if not is_ChargingSchedulePeriod:
            logging.error('validData | isValidChargingSchedulePeriod | Date must be a list not a '+ str(type(data)))
            return False
        return True


