from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional

from functools import wraps
import uvicorn, socket, httpx
import inspect

import logging
logging.basicConfig(level=logging.ERROR)

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, 'tuns')

class Message(BaseModel):
    handle: str
    content: str
    session_id: str
    history: Optional[List[Dict[str, str]]] = None

def find_available_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1

import asyncssh, asyncio
async def create_ssh_tunnel(x,y,z='tuns.sh'):
    try:
        async with asyncssh.connect(z,client_keys=[key_path],known_hosts=None) as conn:
            await conn.forward_remote_port(x, 80, 'localhost', y)
            print("✦/✧","tunnel established\n")
            await asyncio.Future()  # run forever
    except (OSError, asyncssh.Error) as e:
        print("✦/✧",f"tunnel disconnected: {e}")

def register(handle, network, url, mode):
    try:
        with httpx.Client() as client:
            response = client.post(f"{network}/register", json={"handle":f"@{handle}", "url":url, "mode":mode})
            if response.status_code==200:
                data = (response.json()).get("content")
                print(f"✦/✧ {data}")
                print("")
            else:
                print("✦/✧ failed to register ⚠️")
    except Exception as e:
        print(f"An error occurred: {e}")

async def run_server(x,y):
    config = uvicorn.Config(x, host="127.0.0.1", port=y, log_level="error")
    server = uvicorn.Server(config)
    await server.serve()

class Cycls:
    def __init__(self,network="https://cycls.com", port=find_available_port(8001),url=""):
        self.handle = None
        self.server = FastAPI()
        self.network = network
        self.port = port
        self.url = url

    def __call__(self, handle):
        self.handle = handle
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper = async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
            self.server.post(f'/@{handle}', name=f"handle")(wrapper)
            return wrapper
        return decorator

    def start(self):
        asyncio.run(self.publish())

    async def publish(self):
        prod=False
        if self.url != "":
            prod=True

        print(f"\n✦/✧ serving at port: {self.port}\n")
        if prod:
            print("✦/✧","production mode",f"url: {self.url}\n")
            register(self.handle, self.network, self.url, "prod")
        else:
            self.url = f"http://{self.handle}-cycls.tuns.sh"
            print("✦/✧","development mode\n")
            print("✦/✧",f"url {self.url}\n")
            register(self.handle, self.network, self.url, "dev")
            t2 = asyncio.create_task(run_server(self.server,self.port))
            
        print("✦/✧",f"visit app: {self.network}/@{self.handle}","\n")

        t1 = asyncio.create_task(create_ssh_tunnel(f"{self.handle}-cycls", self.port))
        await asyncio.gather(t1, t2) if not prod else asyncio.gather(t2)

Text = StreamingResponse