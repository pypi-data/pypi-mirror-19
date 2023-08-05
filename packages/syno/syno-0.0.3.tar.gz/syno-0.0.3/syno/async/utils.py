import aiohttp, asyncio, async_timeout, json

async def fetch_json(session, url, js = None, timeout = 60):
    headers = {'accept': 'application/json'}
    with async_timeout.timeout(timeout):
        if not js:
            async with session.get(url, headers=headers) as resp:
                return json.loads(await resp.text())
        else:
            async with session.post(url, headers=headers,data=json.dumps(js, ensure_ascii=False)) as resp:
                return json.loads(await resp.text())
            
async def post_plain(session, url, js, timeout = 60):
    headers = {'accept': 'application/json'}
    with async_timeout.timeout(timeout):
        async with session.post(url, headers=headers, data=js) as resp:
            return json.loads(await resp.text())
            
