import requests, json
from datetime import timedelta
SYNO_API_QC = 'http://@.quickconnect.to/Serv.php'
SYNO_API_QC_PING = '/webman/pingpong.cgi'
SYNO_API_QC_PING_TIMEOUT = 3
        
def get_server(name):
    qc_url = SYNO_API_QC.replace('@', name)
    res = None
    
    for vid in ['dsm_portal', 'dsm_portal_https']:
        urls = set()
        req = [{"version":1, "command":"get_server_info", "id":vid, "serverID":name}]

        data = requests.post(qc_url, data = json.dumps(req, ensure_ascii=False)).json()[0]
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
        min = timedelta(hours=1)

        for url in urls:
            try:
                ping_req = requests.get(url + SYNO_API_QC_PING, timeout = SYNO_API_QC_PING_TIMEOUT)
                if ping_req.elapsed < min:
                    ping = ping_req.json()
                    if ping['success']:
                        min = ping_req.elapsed
                        res = url
            except:
                pass
    return res


if __name__ == '__main__':
    print(get_server('casabobuk'))
