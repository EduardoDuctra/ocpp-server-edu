from chargePoint import ChargePoint
from centralSystem import CentralSystem
import websockets
from aiohttp import web
from aiohttp_jwt import JWTMiddleware
from functools import partial
import logging
from services import apiService
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')


async def on_connect(websocket, path, csms):
    print("Subprotocol recebido:", websocket.subprotocol)
    print("PATH recebido:", path)

    charge_point_id = path.strip("/").split("/")[-1]

    cp = ChargePoint(charge_point_id, websocket)

    logging.info('Carregador %s conectado.', cp.id)
    print(f"Carregador {cp.id} conectado!")

    queue = csms.register_charger(cp)
    await queue.get()


async def create_websocket_server(csms: CentralSystem):
    handler = partial(on_connect, csms=csms)
    return await websockets.serve(handler, "0.0.0.0", 9000, subprotocols=["ocpp1.6"])



async def create_http_server(csms: CentralSystem):
    app = web.Application(
        middlewares=[
            JWTMiddleware(SECRET_KEY),
        ]
    )
    app.add_routes([web.post("/changeconfig", apiService.Service.f_change_config)])
    app.add_routes([web.post("/disconnect", apiService.Service.f_disconnect_charger)])
    app.add_routes([web.post("/reset", apiService.Service.f_reset)])
    app.add_routes([web.post("/getconfig", apiService.Service.f_get_config)])
    app.add_routes([web.post("/remotestart", apiService.Service.f_remote_start)])
    app.add_routes([web.post("/remotestop", apiService.Service.f_remote_stop)])
    app.add_routes([web.post("/unlockconnector", apiService.Service.f_unlock_connector)])
    app.add_routes([web.post("/changeavai", apiService.Service.f_availability_type)])
    app.add_routes([web.post("/clearcache", apiService.Service.f_clear_cache)])
    app.add_routes([web.post("/setchargemaxprof", apiService.Service.f_set_charge_max_prof)])
    app.add_routes([web.post("/setchargemaxprofrec", apiService.Service.f_set_charge_max_prof_rec)])
    app.add_routes([web.post("/clearconfprof", apiService.Service.f_clear_config_profile)])

    app["csms"] = csms

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 8090)
    await site.start()

    print("HTTP rodando na porta 8090")
