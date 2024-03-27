from collections import defaultdict
from enum import StrEnum


class DNSType(StrEnum):
    A = 'A'


class LocalDNS:

    def __init__(self, domain2ip: dict[str, str]):
        self.d2p = domain2ip

    @classmethod
    def from_file(cls, filename: str):
        d2p = defaultdict(list)
        with open(filename, "r") as fp:
            for line in fp:
                if len(line.strip()) == 0:
                    continue
                if line[0] == ";":
                    continue
                name, _, typ, ip = line.split()
                if typ != DNSType.A:
                    continue
                d2p[name].append(ip)
        return cls(d2p)
