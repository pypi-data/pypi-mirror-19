# -*- coding: utf-8 -*-
import requests
from .errors import LicenseKeyError, ServerError


def check(packages, key):
    json = {
        "key": key,
        "dependencies": packages
    }

    r = requests.post("https://api.aws.safetydb.io/", json=json)
    data = r.json()
    if r.status_code == 200:
        return data["vulns"]
    elif r.status_code == 400:
        if "error" in data:
            raise ServerError(data["error"])
    elif r.status_code == 403:
        raise LicenseKeyError()
    r.raise_for_status()
