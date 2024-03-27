import datetime
import logging
import sys

import asyncio
from cachetools import LRUCache
from dnslib import DNSRecord, RR, QTYPE, A
from local_dns import LocalDNS


logger = logging.getLogger(__name__)


PORT, BIND, REAL_DNS = 7070, "bind.txt", "8.8.8.8"


class SyslogProtocol(asyncio.DatagramProtocol):
    def __init__(self, lru_size=1):
        self.local_dns = LocalDNS.from_file(BIND)
        # domain -> (response, ts)
        self.lru = LRUCache(maxsize=lru_size)
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def handle_remote(self, packet: DNSRecord):
        domain: str = packet.questions[0].qname
        response_rr, validation_ts = self.lru.get(domain,
                                                  (None, datetime.datetime(year=1970, month=1, day=1)))
        if validation_ts < datetime.datetime.now():
            response = DNSRecord.parse(packet.send(dest=REAL_DNS))
            response_rr = response.rr
            ttl = min([r.ttl for r in response_rr] + [3600])
            self.lru[domain] = (response_rr, datetime.datetime.now() + datetime.timedelta(seconds=ttl))
        else:
            logger.warning(f"Using LRU-cache for {domain}")
        packet.add_answer(*response_rr)
        return packet

    def datagram_received(self, data, addr):
        logger.warning("New request !")
        packet = DNSRecord.parse(data)
        domain = str(packet.questions[0].qname).strip(".")
        if domain in self.local_dns.d2p:
            logger.warning(f"Request for local index - {domain}")
            for ip in self.local_dns.d2p[domain]:
                packet.add_answer(RR(domain, QTYPE.A, rdata=A(ip), ttl=3600))
            response = packet
        else:
            logger.warning(f"Request for remote index - {domain}")
            response = self.handle_remote(packet)
        self.transport.sendto(response.pack(), addr)


def parse_args():
    global PORT, BIND, REAL_DNS
    if len(sys.argv) >= 2:
        PORT = sys.argv[1]
    if len(sys.argv) >= 3:
        BIND = sys.argv[2]
    if len(sys.argv) >= 4:
        REAL_DNS = sys.argv[3]


if __name__ == '__main__':
    parse_args()
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(SyslogProtocol, local_addr=('localhost', PORT))
    loop.run_until_complete(t)
    loop.run_forever()
