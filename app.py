import os
import asyncio
from binance import AsyncClient, BinanceSocketManager
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket("BTCUSDT")

    numero_trades = 0
    actual = 0
    billetera = 1000000
    lista = []
    # then start receiving messages
    async with ts as tscm:

        while True:
            res = await tscm.recv()

            actual = float(res["p"])

            if len(lista) < 5:
                lista.append(actual)
            else:
                numero_trades = numero_trades + 5
                precio_actual = sum(lista) / len(lista)

                if numero_trades == 5:
                    billetera = billetera / precio_actual
                    print(f"Compraste {billetera}")
                else:
                    profit_loss = ((billetera * precio_actual) - 1000000)
                    print(f"Ahora tienes { billetera * precio_actual}, ${profit_loss}")

                lista = []

    await client.close_connection()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
