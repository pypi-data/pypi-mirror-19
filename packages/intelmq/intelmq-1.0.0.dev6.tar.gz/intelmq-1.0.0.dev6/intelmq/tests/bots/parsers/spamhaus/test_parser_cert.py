# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.spamhaus.parser_cert import SpamhausCERTParserBot

EXAMPLE_REPORT = {"feed.url": "https://portal.spamhaus.org/cert/api.php?cert="
                              "<CERTNAME>&key=<APIKEY>",
                  "raw": "OyBpcCwgYXNuLCBjb3VudHJ5LCBsYXN0c2VlbiwgYm90bmFtZSwg"
                         "ZG9tYWluLCByZW1vdGVfaXAsIHJlbW90ZV9wb3J0LCBsb2NhbF9w"
                         "b3J0LCBwcm90b2NvbAoxMDkuMTI2LjY0LjIsQVMxMjYzNSxBVCwx"
                         "NDQxMDA4OTcwLGFzcHJveCwsLDI1LCx0Y3AKMTA5LjkwLjIzMy4x"
                         "OSxBUzY4MzAsQVQsMTQ0MTAwODM1MSxwYXRjaGVyLGR4eHQuc2lu"
                         "a2hvbGUuZGssMjEyLjIyNy4yMC4xOSw4MCwxMDM2LHRjcAoxMDku"
                         "OTEuMC4yMjcsQVM2ODMwLEFULDE0NDEwMTE2NTcsY29uZmlja2Vy"
                         "LDIxNi42Ni4xNS4xMDksMjE2LjY2LjE1LjEwOSw4MCwxNDMwLHRj"
                         "cAo=",
                  "__type": "Report",
                  "feed.name": "Spamhaus Cert",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENT_TEMPL = {"feed.url": "https://portal.spamhaus.org/cert/api.php?cert="
                           "<CERTNAME>&key=<APIKEY>",
               "feed.name": "Spamhaus Cert",
               "__type": "Event",
               "classification.type": "botnet drone",
               "time.observation": "2015-01-01T00:00:00+00:00",
               "protocol.transport": "tcp",
               "source.geolocation.cc": "AT",
               }
EXAMPLE_EVENTS_PARTS = [{'raw': 'MTA5LjEyNi42NC4yLEFTMTI2MzUsQVQsMTQ0MTAwODk3M'
                                'Cxhc3Byb3gsLCwyNSwsdGNw',
                         'source.ip': '109.126.64.2',
                         'source.asn': 12635,
                         'time.source': '2015-08-31T08:16:10+00:00',
                         'malware.name': 'asprox',
                         'destination.port': 25,
                         },
                        {'raw': 'MTA5LjkwLjIzMy4xOSxBUzY4MzAsQVQsMTQ0MTAwODM1M'
                                'SxwYXRjaGVyLGR4eHQuc2lua2hvbGUuZGssMjEyLjIyNy'
                                '4yMC4xOSw4MCwxMDM2LHRjcA==',
                         'source.ip': '109.90.233.19',
                         'source.asn': 6830,
                         'time.source': '2015-08-31T08:05:51+00:00',
                         'malware.name': 'patcher',
                         'destination.port': 80,
                         'destination.fqdn': 'dxxt.sinkhole.dk',
                         'destination.ip': '212.227.20.19',
                         'extra': '{"destination.local_port": 1036}',
                         },
                        {'raw': 'MTA5LjkxLjAuMjI3LEFTNjgzMCxBVCwxNDQxMDExNjU3L'
                                'GNvbmZpY2tlciwyMTYuNjYuMTUuMTA5LDIxNi42Ni4xNS'
                                '4xMDksODAsMTQzMCx0Y3A=',
                         'source.ip': '109.91.0.227',
                         'source.asn': 6830,
                         'time.source': '2015-08-31T09:00:57+00:00',
                         'malware.name': 'conficker',
                         'destination.port': 80,
                         'destination.ip': '216.66.15.109',
                         'extra': '{"destination.local_port": 1430}',
                         }]


class TestSpamhausCERTParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for SpamhausCERTParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SpamhausCERTParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.run_bot()
        for position, event in enumerate(EXAMPLE_EVENTS_PARTS):
            event.update(EVENT_TEMPL)
            self.assertMessageEqual(position, event)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
