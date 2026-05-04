
import asyncio
import logging
from chargePoint import ChargePoint


class CentralSystem:
    def __init__(self):
        self._chargers = {}

    def register_charger(self, cp: ChargePoint) -> asyncio.Queue:
        """ Registra um novo carregador no CSMS. A função retorna uma
        fila. O CSMS irá colocar uma mensagem na fila, o CSMS também 
        pode controlar as tasks dos carregadores podendo matar-las
        """
        queue = asyncio.Queue(maxsize=1)

        # Armazena a referencia da task dos carregadores
        task = asyncio.create_task(self.start_charger(cp, queue))
        self._chargers[cp] = task

        return queue

    async def start_charger(self, cp, queue):
        """ Inicia a escuta por mensagens dos carregadores. """
        try:
            await cp.start()
        except Exception as e:
            logging.info('Carregador %s desconectado: %s', cp.id, e)
        finally:
            del self._chargers[cp]
            await queue.put(True)

    async def change_configuration(self, charger_id: str, key: str, value: str):
        for cp in self._chargers:
            if cp.id == charger_id:
                response = await cp.change_configuration(key, value)
                return response
        return('Carregador '+ charger_id + ' não conectado')


    def disconnect_charger(self, charger_id: str):
        for cp, task in self._chargers.items():
            if cp.id == charger_id:
                task.cancel()
                return
        

    async def reset(self, charger_id: str, value: str):
        for cp in self._chargers:
            if (cp.id == charger_id and (value == "Hard" or value == "Soft")):
                response = await cp.reset(value)
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def get_configuration(self, charger_id: str):
        for cp in self._chargers:
            if cp.id == charger_id:
                response = await cp.get_configuration()
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def remote_start_transaction(self, charger_id: str, connector_id: int):
        for cp in self._chargers:
            if cp.id == charger_id:
                response = await cp.remote_start_transaction(charger_id, connector_id)
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def remote_stop_transaction(self, charger_id: str, transaction_id: int):
        for cp in self._chargers:
            if cp.id == charger_id:
                response = await cp.remote_stop_transaction(transaction_id)
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def unlock_connector(self, charger_id: str, connector_id: int):
        for cp in self._chargers:
            if cp.id == charger_id:
                response = await cp.unlock_connector(connector_id)
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def availability_type(self, charger_id: str, connector_id: int, type: str):
        for cp in self._chargers:
            if (cp.id == charger_id and (type == "Inoperative" or type == "Operative")):
                response = await cp.availability_type(connector_id, type)
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def clear_cache(self, charger_id: str):
        for cp in self._chargers:
            if (cp.id == charger_id):
                response = await cp.clear_cache()
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def set_charge_max_prof(self, charger_id, connector_id, startSchedule, limit):
        for cp in self._chargers:
            if cp.id == charger_id:
                response = await cp.set_charge_max_prof(connector_id, startSchedule, limit)
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def set_charge_max_prof_rec(self, charger_id, connector_id, chargingSchedulePeriod):
        for cp in self._chargers:
            if cp.id == charger_id:
                response = await cp.set_charge_max_prof_rec(connector_id, chargingSchedulePeriod)
                return response
        return('Carregador '+ charger_id + ' não conectado')


    async def clear_configuration_profile(self, charger_id: str):
        for cp in self._chargers:
            if cp.id == charger_id:
                response = await cp.clear_configuration_profile()
                return response
        return('Carregador '+ charger_id + ' não conectado')