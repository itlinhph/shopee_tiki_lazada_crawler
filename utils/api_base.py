import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class APIBase:
    def __init__(self, method="https"):
        self.req_session = requests.Session()
        self.default_url = None
        if method == "http":
            self.method = "http"
        else:
            self.method = "https"

    def add_header(self, header):
        self.req_session.headers.update(header)

    def set_default_url(self, url):
        self.default_url = url

    def set_max_retry(self, retry_time=3, backoff_factor=0.1,
                      method_whitelist=False):
        retries = Retry(
            total=retry_time,
            backoff_factor=backoff_factor,
            method_whitelist=method_whitelist
        )
        method_mount = "{}://".format(self.method)
        self.req_session.mount(method_mount, HTTPAdapter(max_retries=retries))

    def get(self, url=None, param=None, timeout=10):
        if url is None:
            url = self.default_url
        req = self.req_session.get(url, params=param, timeout=timeout)
        return req
