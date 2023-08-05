import requests, json

SYNO_API_AUTH = '/auth.cgi?api=SYNO.API.Auth&version=2'
SYNO_API_DSM = '/DownloadStation/task.cgi'
SYNO_API_DSM_NAME = 'SYNO.DownloadStation.Task'
SYNO_API_DSM_GET = SYNO_API_DSM + '?api=' + SYNO_API_DSM_NAME + '&version=1'

class API:
    def __init__(self, url, user, password, session):
        self.user = user
        self.password = password
        self.url = url + ('' if url.endswith('/webapi') else '/webapi')

        self.session = session
        self.sid = None
        
        self.http = None
        self.logged = False


    def from_json(js):
        self = API(js['url'], js['user'], js['password'], js['session'])
        self.sid = js['sid']
        self.logged = True
        return self

    def to_json(self):
        return {
            'url': self.url,
            'user': self.user,
            'password': self.password,
            'session': self.session,
            'sid': str(self.sid)
        }
        
    def login(self):
        res = requests.get(
            self.url + SYNO_API_AUTH + '&method=login&format=sid' +
                            '&session=' + self.session +
                            '&account=' + self.user +
                            '&passwd=' + self.password).json()
        try:
            self.sid = res['data']['sid']
        except:
            return None
        self.logged = True
        return self.sid

    def logout(self):
        return requests.get(
            self.url + SYNO_API_AUTH + '&method=logout&' +
                            '&session=' + self.session +
                            '&_sid=' + self.sid)

    def ds_download(self, uri):
        print(uri)
        res = requests.post(
            self.url + SYNO_API_DSM,
            data = {'api': SYNO_API_DSM_NAME, 'version': 1, 'uri': uri, 'method': 'create', '_sid': self.sid}
        ).json()
        print(res)
        return res.get('success', False)

    def _meta_call(self, call, ids = None, addon=""):
        url = self.url + SYNO_API_DSM_GET + '&method=' + call + \
            (('&id=' + ids) if ids else "") + \
            '&_sid=' + self.sid + \
            addon
        return requests.get(
            url
        ).json()

    def ds_pause(self, ids):
        res = self._meta_call('pause', ids)
        return res.get('success', False)

    def ds_resume(self, ids):
        res = self._meta_call('resume', ids)
        return res.get('success', False)

    def ds_delete(self, ids, force=False):
        res = self._meta_call('delete', ids,
                        addon = ('&force_complete=true' if force else ''))
        return res.get('success', False)

    def ds_list(self):
        res = self._meta_call('list')
        if res.get('success', False):
            return res['data']['tasks']
        return []


    def ds_info(self, ids):
        info = self._meta_call('getinfo', ids,
                               addon = '&additional=detail,transfer')
        if info.get('success', False):
            return info['data']['tasks']
        return {}

if __name__ == '__main__':
    api = API('http://192.168.1.29:5000', 'bobuk', 'shmobuk', 'wague-sync')
