# -*- coding: utf-8 -*-
import requests

def get_data():
    try:
        # Es probable que esto no funcione hasta que se ponga en produccion
        url = ' /api/'
        r = requests.get(url)
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        print('exception caught', e)
