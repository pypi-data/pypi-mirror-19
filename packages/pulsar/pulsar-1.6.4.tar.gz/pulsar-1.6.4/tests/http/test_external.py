import unittest

from pulsar import get_actor

from tests.http import base


cfg = get_actor().cfg


class ExternalBase(base.TestHttpClientBase):
    with_httpbin = False

    def after_response(self, response):
        pass

    async def test_get_https(self):
        client = self.client()
        response = await client.get('https://github.com/trending')
        self.assertEqual(response.status_code, 200)

    async def test_header_links_and_close(self):
        client = self.client()
        baseurl = 'https://api.github.com/gists/public'
        response = await client.get(baseurl)
        if response.status_code == 403:
            # TODO: this fails in travis for some reason
            return
        self.assertEqual(response.status_code, 200)
        links = response.links
        self.assertTrue(links)
        next = links['next']
        self.assertTrue('rel' in next)
        self.assertTrue('url' in next)
        await client.close()


class ProxyExternal(ExternalBase):

    def after_response(self, response):
        self.assertTrue(response.request.proxy)

    async def test_get_https(self):
        client = self.client()
        response = await client.get('https://github.com/trending')
        self.assertEqual(response.status_code, 200)


@unittest.skipUnless(cfg.http_proxy == '', 'Requires no external proxy')
class Test_HttpClient_NoProxy_External(ExternalBase, unittest.TestCase):
    '''Test external URI when no global proxy server is present.
    '''


@unittest.skipUnless(cfg.http_proxy == '' and cfg.event_loop != 'uv',
                     'Requires no external proxy')
class Test_HttpClient_Proxy_External(ProxyExternal, unittest.TestCase):
    with_proxy = True


@unittest.skipUnless(cfg.http_proxy, 'Requires external proxy')
class Test_HttpClient_ExternalProxy_External(ProxyExternal,
                                             unittest.TestCase):
    pass
