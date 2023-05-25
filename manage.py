from typing import List
import os
import logging
import uvicorn
import psycopg2 as pg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse
import re

app = FastAPI()

def get_currency_rates():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()


class Converted(BaseModel):
    code: str
    rate: float


class RequestBody(BaseModel):
    baseCurrency: str
    rates: List[Converted]

def check(name):
    cursor.execute("""select id from currency_rates 
                            where base_currency = %s""", (name,))
    data_id = cursor.fetchall()
    data_id = re.sub(r"[^0-9]", r"", str(data_id))
    print(data_id)
    return (data_id)


def get(name):
    id = check(name)
    cursor.execute("""select rate from currency_rates 
                              where  currency_rate_id = %s""", (id,))
    data_id = cursor.fetchall()

    data_id = re.sub(r"[^0-9]", r"", str(data_id))
    return (data_id)


@app.post("/load")
async def payload(Request: RequestBody):
    name = Request.baseCurrency
    rates = Request.rates

    print(name)
    print(rates)
    id_cur = check(name)
    try:
        id_cur == []
        cursor.execute(""" Insert into currency_rates  (base_currency)
                                        values (%s);""", (name,))
        conn.commit()
        id_cur = check(name)
        print(id_cur)
        for i in rates:
            cursor.execute(""" Insert into currency_rates (currency_code,rate,currency_rate_id)
                                         values (%s,%s,%s);""", (i.code, i.rate, id_cur,))
            conn.commit()
        raise HTTPException(200)

    except:
        raise HTTPException(500)


if __name__ == '__main__':
    uvicorn.run(app, port=10620, host='localhost')
