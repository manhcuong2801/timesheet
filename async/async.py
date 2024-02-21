import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://10.1.30.171:8000/api/v1/trading/deals/?trading_account_id=1001092299&from_time'
                               '=2022-04-12 00:00:00') as response:

            print('Status: ', response.status)
            print('Content-type: ', response.headers['content-type'])

            html = await response.text()
            print("Body: ", html[:15], "...")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
