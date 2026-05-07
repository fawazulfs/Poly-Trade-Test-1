import os
from fastapi import FastAPI, Request
from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON
from py_clob_client.clob_types import OrderArgs

app = FastAPI()

# Credentials from Render Environment Variables
pk = os.getenv("PRIVATE_KEY")
proxy = os.getenv("PROXY_ADDRESS")

@app.post("/webhook")
async def trade(request: Request):
    data = await request.json()
    
    # Initialize Polymarket Client
    client = ClobClient(POLYGON, key=pk, proxy_address=proxy)
    
    # Place a Limit Order based on TradingView JSON
    resp = client.create_order(OrderArgs(
        price=data.get("price"),
        size=data.get("amount"),
        side=data.get("side"), # "BUY" or "SELL"
        token_id=data.get("token_id")
    ))
    
    return {"status": "success", "response": resp}
