import aiohttp, asyncio, async_timeout, json
from .utils import *

SYNO_API_QC = 'http://@.quickconnect.to/Serv.php'
SYNO_API_QC_PING = '/webman/pingpong.cgi'
SYNO_API_QC_PING_TIMEOUT = 3
        
async def get_server(name):
    qc_url = SYNO_API_QC.replace('@', name)
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as http:
        for vid in ['dsm_portal', 'dsm_portal_https']:
            urls = set()
            req = [{"version":1, "command":"get_server_info", "id":vid, "serverID":name}]

            data = (await fetch_json(http, qc_url, js = req))[0]
            if 'errinfo' in data:
                continue
            proto = 'http' + ('s' if vid.endswith('s') else '')

            if data['service']['pingpong'] == 'CONNECTED':
                port = data['service']['ext_port']
                if not port:
                    port = data['service']['port']
                # Local address. Yes, just that straightforward
                urls.add(proto + '://' + data['server']['interface'][0]['ip'] + ':' + str(port))

                urls.add(proto + '://' + data['server']['external']['ip'] + ':' + str(port))
            for url in urls:
                try:
                    ping = await fetch_json(http, url + SYNO_API_QC_PING, timeout = SYNO_API_QC_PING_TIMEOUT)
                    if ping['success']:
                        return url
                except:
                    pass
    return None


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(get_server('misha')))
