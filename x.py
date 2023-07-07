import requests
from datetime import datetime
base = "https://api.wormscan.io/api/v1/observations/6/00000000000000000000000009fb06a271faff70a651047395aaeb6265265f13/147"


def getTime(o):
    raw = o["indexedAt"]
    idx = raw.find(".")


    return datetime.strptime(raw[:idx],'%Y-%m-%dT%H:%M:%S')


sequence = 300500

uniques = {}
for x in range(1):
    seq = str(sequence + x)
    result = requests.get(base+"?pageSize=20")
    obs = result.json()

    if len(obs)  == 0: 
        print(f"No observations for {seq}")
        break


    mx, mn = getTime(obs[0]), getTime(obs[0])
    for o in obs:
        t = getTime(o)
        if t>mx:
            mx = t
        if t<mn:
            mn = t

        addr = o["guardianAddr"]
        if addr not in uniques:
            uniques[addr] = 0
        uniques[addr] += 1
    print(f"{seq} - Total: {len(obs)} Max: {mx} Min: {mn} Delta: {mx-mn}")



gset = [
  {
    "pubkey": '0x58CC3AE5C097b213cE3c81979e1B9f9570746AA5',
    "name": 'Jump Crypto',
  },
  {
    "pubkey": '0xfF6CB952589BDE862c25Ef4392132fb9D4A42157',
    "name": 'Staked',
  },
  {
    "pubkey": '0x114De8460193bdf3A2fCf81f86a09765F4762fD1',
    "name": 'Figment',
  },
  {
    "pubkey": '0x107A0086b32d7A0977926A205131d8731D39cbEB',
    "name": 'ChainodeTech',
  },
  {
    "pubkey": '0x8C82B2fd82FaeD2711d59AF0F2499D16e726f6b2',
    "name": 'Inotel',
  },
  {
    "pubkey": '0x11b39756C042441BE6D8650b69b54EbE715E2343',
    "name": 'HashQuark',
  },
  {
    "pubkey": '0x54Ce5B4D348fb74B958e8966e2ec3dBd4958a7cd',
    "name": 'Chainlayer',
  },
  {
    "pubkey": '0x15e7cAF07C4e3DC8e7C469f92C8Cd88FB8005a20',
    "name": 'xLabs',
  },
  {
    "pubkey": '0x74a3bf913953D695260D88BC1aA25A4eeE363ef0',
    "name": 'Forbole',
  },
  {
    "pubkey": '0x000aC0076727b35FBea2dAc28fEE5cCB0fEA768e',
    "name": 'Staking Fund',
  },
  {
    "pubkey": '0xAF45Ced136b9D9e24903464AE889F5C8a723FC14',
    "name": 'MoonletWallet',
  },
  {
    "pubkey": '0xf93124b7c738843CBB89E864c862c38cddCccF95',
    "name": 'P2P Validator',
  },
  {
    "pubkey": '0xD2CC37A4dc036a8D232b48f62cDD4731412f4890',
    "name": '01Node',
  },
  {
    "pubkey": '0xDA798F6896A3331F64b48c12D1D57Fd9cbe70811',
    "name": 'MCF',
  },
  {
    "pubkey": '0x71AA1BE1D36CaFE3867910F99C09e347899C19C3',
    "name": 'Everstake',
  },
  {
    "pubkey": '0x8192b6E7387CCd768277c17DAb1b7a5027c0b3Cf',
    "name": 'Chorus One',
  },
  {
    "pubkey": '0x178e21ad2E77AE06711549CFBB1f9c7a9d8096e8',
    "name": 'Syncnode',
  },
  {
    "pubkey": '0x5E1487F35515d02A92753504a8D75471b9f49EdB',
    "name": 'Triton',
  },
  {
    "pubkey": '0x6FbEBc898F403E4773E95feB15E80C9A99c8348d',
    "name": 'Staking Facilities',
  },
]


xxx = {
    "0x000aC0076727b35FBea2dAc28fEE5cCB0fEA768e": "2023-07-06T16:22:07.022165833Z",
    "0x107A0086b32d7A0977926A205131d8731D39cbEB": "2023-07-06T16:22:06.562518353Z",
    "0x114De8460193bdf3A2fCf81f86a09765F4762fD1": "2023-07-06T16:22:06.552574041Z",
    "0x11b39756C042441BE6D8650b69b54EbE715E2343": "2023-07-06T16:22:07.536147068Z",
    "0x15e7cAF07C4e3DC8e7C469f92C8Cd88FB8005a20": "2023-07-06T16:22:07.343166605Z",
    "0x178e21ad2E77AE06711549CFBB1f9c7a9d8096e8": "2023-07-06T16:22:06.861937865Z",
    "0x54Ce5B4D348fb74B958e8966e2ec3dBd4958a7cd": "2023-07-06T16:22:06.643948275Z",
    "0x58CC3AE5C097b213cE3c81979e1B9f9570746AA5": "2023-07-06T16:22:06.572680686Z",
    "0x5E1487F35515d02A92753504a8D75471b9f49EdB": "2023-07-06T16:22:06.61929637Z",
    "0x6FbEBc898F403E4773E95feB15E80C9A99c8348d": "2023-07-06T16:22:06.473212536Z",
    "0x71AA1BE1D36CaFE3867910F99C09e347899C19C3": "2023-07-06T16:22:06.58509558Z",
    "0x74a3bf913953D695260D88BC1aA25A4eeE363ef0": "2023-07-06T16:22:06.957843033Z",
    "0x8192b6E7387CCd768277c17DAb1b7a5027c0b3Cf": "2023-07-06T16:22:05.698879334Z",
    "0x8C82B2fd82FaeD2711d59AF0F2499D16e726f6b2": "2023-07-06T16:22:06.827766556Z",
    "0xAF45Ced136b9D9e24903464AE889F5C8a723FC14": "2023-07-06T16:22:06.681446141Z",
    "0xD2CC37A4dc036a8D232b48f62cDD4731412f4890": "2023-07-06T16:22:06.775277432Z",
    "0xDA798F6896A3331F64b48c12D1D57Fd9cbe70811": "2023-07-06T16:22:06.900034715Z",
    "0xf93124b7c738843CBB89E864c862c38cddCccF95": "2023-07-06T16:22:06.655084231Z",
    "0xfF6CB952589BDE862c25Ef4392132fb9D4A42157": "2023-07-06T16:22:06.68166438Z"
  }


for g in gset:

    if g["pubkey"] in uniques:
        if g["pubkey"] in xxx:
            print("gotem")
        print(f'{g["name"]} observed {uniques[g["pubkey"]]}')
    else:
        if g["pubkey"] in xxx:
            print("gotem")
        print(f'\t{g["name"]} observed 0')

import json
print(json.dumps(uniques))


