import aiohttp, asyncio
from .utils import *

SYNO_API_AUTH = '/auth.cgi?api=SYNO.API.Auth&version=2'
SYNO_API_DSM = '/DownloadStation/task.cgi'
SYNO_API_DSM_NAME = 'SYNO.DownloadStation.Task'
SYNO_API_DSM_GET = SYNO_API_DSM + '?api=' + SYNO_API_DSM_NAME + '&version=1'

class API:
    def __init__(self, url, user, password, session):
        self.user = user
        self.password = password
        if not url.endswith('webapi'):
            self.url = url + '/webapi'

        self.session = session
        self.sid = None
        
        self.http = None
        self.logged = False


    def from_json(js):
        self.http = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
        self = API(js['url'], js['user'], js['password'], js['session'])
        self.sid = js['sid']
        self.logged = True

    def to_json(self):
        return {
            'url': self.url,
            'user': self.user,
            'password': self.password,
            'session': self.session,
            'sid': str(self.sid)
        }
        
    async def login(self):
        self.http = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
        res = await fetch_json(self.http,
            url = self.url + SYNO_API_AUTH + '&method=login&format=sid' +
                            '&session=' + self.session +
                            '&account=' + self.user +
                            '&passwd=' + self.password
        )
        self.sid = res['data']['sid']
        self.logged = True
        return self.sid

    async def logout(self):
        await fetch_json(self.http,
            url = self.url + SYNO_API_AUTH + '&method=logout&' +
                            '&session=' + self.session +
                            '&_sid=' + self.sid
        )
        self.http.close()

    async def ds_download(self, uri):
        return (await post_plain(self.http,
            url = self.url + SYNO_API_DSM,
            js = {'api': SYNO_API_DSM_NAME, 'version': 1, 'uri': uri, 'method': 'create', '_sid': self.sid}
        )).get('success', False)

    async def _meta_call(self, call, ids = None, addon=""):
        return await fetch_json(self.http,
                    url = self.url + SYNO_API_DSM_GET + '&method=' + call +
                        (('&id=' + ids) if ids else "") +
                        '&_sid=' + self.sid +
                        addon
        )

    async def ds_pause(self, ids):
        res = await self._meta_call('pause', ids)
        return res.get('success', False)

    async def ds_resume(self, ids):
        res = await self._meta_call('resume', ids)
        return res.get('success', False)

    async def ds_delete(self, ids, force=False):
        res = await self._meta_call('delete',
                        addon = ('&force_complete=true' if force else ''))
        return res.get('success', False)

    async def ds_list(self):
        res = await self._meta_call('list')
        if res.get('success', False):
            return res['data']['tasks']
        return []


    async def ds_info(self, ids):
        info = await self._meta_call('getinfo', ids,
                                     addon = '&additional=detail,transfer')
        if info.get('success', False):
            return info['data']['tasks']
        return {}

if __name__ == '__main__':
    api = API('http://192.168.1.29:5000', 'misha', 'marina-karina', 'wague')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(api.login())

    loop.run_until_complete(api.logout())
