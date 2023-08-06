import requests


class BrevisClient(object):
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        self.session = session or requests.Session()

    def _make_request(self, method, endpoint, data):
        url = '{}{}'.format(self.base_url, endpoint)
        r = requests.Request(method=method, url=url, json=data)
        p = r.prepare()
        s = self.session
        resp = s.send(p)

        if resp.status_code != 200:
            return resp.raise_for_status()
        return resp.json()

    def shorten(self, url):
        data = {
            'url': url
        }
        return self._make_request('POST', '/shorten', data)

    def unshorten(self, short_url):
        if short_url.startswith(self.base_url):
            try:
                short_url = short_url.rsplit('/', 1)[1]
            except IndexError:
                pass
        data = {
            'shortUrl': short_url
        }
        return self._make_request('POST', '/unshorten', data)
