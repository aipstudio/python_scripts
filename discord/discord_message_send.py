#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import datetime

p1 = sys.argv[1]
p2 = sys.argv[2]
p3 = sys.argv[3]

CHANNEL_WEBHOOK = "https://discordapp.com/api/webhooks/"

MESSAGE = {
    'embeds': [
        {
            'color': 16007990,
            'title': 'Zabbix alerting',
            'fields': [
                {
                    'name': 'Текущее время',
                    'value': datetime.datetime.now(),
                    'inline': True
                },{
                    'name': 'Кому',
                    'value': p1,
                    'inline': True
                },{
                    'name': 'Тема',
                    'value': p2,
                    'inline': True
                },{
                    'name': 'Тело',
                    'value': p3,
                    'inline': True
                }
            ]
        }
    ]
}

if __name__ == '__main__':
    result = requests.post(CHANNEL_WEBHOOK, json=MESSAGE).text
