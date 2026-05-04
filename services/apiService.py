import json
from aiohttp import web
import logging
import sys

sys.path.insert(0, '/app/utils')
from utils.validData import validData

"""------------------- Funções -------------------"""

class Service:
    async def f_change_config(request):
        """ HTTP handler usado para alterar as configurações do carregador. """
        data = await request.json()
        csms = request.app["csms"]
        
        try:
            data_charger_id = data['charger_id']
            data_key = data['key']
            data_value = data['value']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id) and validData.isValidKey(data_key) and validData.isValidValue(data_value)):
            response = await csms.change_configuration(data_charger_id, data_key, data_value)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')
        


    async def f_disconnect_charger(request):
        """ HTTP handler para desconectar  um carregador, irá matar a task do OCPP que está na fila do CMSM."""
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id)):
            response = await csms.disconnect_charger(data_charger_id)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')   
        

    async def f_reset(request):
        """ HTTP handler para reset do dispositivo. """
        data = await request.json()
        csms = request.app["csms"]
        
        try:
            data_charger_id = data['charger_id']
            data_value = data['value']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id) and validData.isValidValue(data_value)):
            response = await csms.reset(data_charger_id, data_value)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')


    async def f_get_config(request):
        """ HTTP handler retornar todas as configurações do carregador. """
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id)):
            response = await csms.get_configuration(data_charger_id)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')   
        

    async def f_remote_start(request):
        """ HTTP handler para iniciar a recarga via OCPP. 
        ***OBS: A recarga só pode ser inicializada se o carregador estiver operante (parametro que pode ser setado no f_availability_type) """
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
            data_connector_id = data['connector_id']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id) and validData.isValidConnectorId(data_connector_id)):
            response = await csms.remote_start_transaction(data_charger_id, data_connector_id)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')   


    async def f_remote_stop(request):
        """ HTTP handler para interromper a recarga via OCPP. """
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
            data_transaction_id = data['transaction_id']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id) and validData.isValidTransactionId(data_transaction_id)):
            response = await csms.remote_stop_transaction(data_charger_id, data_transaction_id)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')
        

    async def f_unlock_connector(request):
        """ HTTP handler para liberar o plug caso ele fique preso. ***OBS: Não usar esse comando para interromper a carga remotamente."""
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
            data_connector_id = data['connector_id']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id) and validData.isValidConnectorId(data_connector_id)):
            response = await csms.unlock_connector(data_charger_id, data_connector_id)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')   
        

    async def f_availability_type(request):
        """ HTTP handler para alterar a disponibilidade do plug de carregamento. """
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
            data_connector_id = data['connector_id']
            data_type = data['type']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id) and validData.isValidConnectorId(data_connector_id) and validData.isValidType(data_type)):
            response = await csms.availability_type(data_charger_id, data_connector_id, data_type)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')   
        

    async def f_clear_cache(request):
        """ HTTP handler para limpar o cache de alguma coisa. """
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id)):
            response = await csms.clear_cache(data_charger_id)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong') 
        

    async def f_set_charge_max_prof(request):
        """ HTTP handler para setar a configurção do perfil de carregamento. """
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
            data_connector_id = data['connector_id']
            data_startSchedule = data['startSchedule']
            data_limit = data['limit']
            
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id) and validData.isValidConnectorId(data_connector_id) and validData.isValidDate(data_startSchedule) and validData.isValidLimit(data_limit)):
            data_startSchedule = validData.isValidStartSchedule(data_startSchedule)
            response = await csms.set_charge_max_prof(data_charger_id, data_connector_id, data_startSchedule, data_limit)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong') 


    async def f_set_charge_max_prof_rec(request):
        """ HTTP handler para setar a configurção do perfil de carregamento. """
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
            data_connector_id = data['connector_id']
            data_chargingSchedulePeriod = data['chargingSchedulePeriod']
            
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id) and validData.isValidConnectorId(data_connector_id) and validData.isValidChargingSchedulePeriod(data_chargingSchedulePeriod)):
            response = await csms.set_charge_max_prof_rec(data_charger_id, data_connector_id, data_chargingSchedulePeriod)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong')
        

    async def f_clear_config_profile(request):
        """ HTTP handler para limpar a configurção do perfil de carregamento. """
        data = await request.json()
        csms = request.app["csms"]
        try:
            data_charger_id = data['charger_id']
        except Exception as e:
            return web.Response(text='data ' +str(e)+ ' is missing')
        
        if (validData.isValidChargerId(data_charger_id)):
            response = await csms.clear_configuration_profile(data_charger_id)
            return web.Response(text=response)
        else:
            return web.Response(status=404, text='Something in your call is wrong') 
        
