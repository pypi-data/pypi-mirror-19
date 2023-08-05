# -*- coding: utf-8 -*-
import requests


def check(packages, key):
    json = {
        "key": key,
        "dependencies": packages
    }
    r = requests.post("https://api.aws.safetydb.io/", json=json)
    return r.json()["vulns"]
