from proxy import Proxy
from proxy_events import ProxyEvents

proxy_events = ProxyEvents()
proxy = Proxy(proxy_events, 8080)
proxy.run()
