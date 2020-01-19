#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


def send_to_wx(text, desp='如题'):
    params = {"text": text, "desp": desp}
    requests.get('https://sc.ftqq.com/SCU74589Tae55d0bd4ac97f20b7483a0c0c98ff385e0aee2e3114f.send', params=params)


if __name__ == '__main__':
    send_to_wx("helloworld")
