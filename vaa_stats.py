import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import base64

from vaa import VAA
from consts import CHAINS

VAA_BASE_URL = "https://api.wormscan.io/api/v1/vaas"
UPDATED_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'
TS_FMT = '%Y-%m-%dT%H:%M:%SZ'

def getVAATimes(data: dict)->tuple[float, float]:
    ts = datetime.strptime(data["timestamp"], TS_FMT)
    try:
        indexed = datetime.strptime(data["indexedAt"], UPDATED_FMT)
    except Exception:
        indexed = datetime.strptime(data["indexedAt"], TS_FMT)

    return (ts.timestamp(), indexed.timestamp())

def getVAAs(chainId: int, page: int = 0)->dict[str, list[tuple[int, int]]]:
    print(f"Getting VAAs for page {page}")
    result = requests.get(f"{VAA_BASE_URL}/{chainId}?page={page}")
    vaas = result.json()["data"]

    if len(vaas)  == 0: 
        print(f"No VAAs for {chainId} on page {page}")
        return

    deltas: dict[str, list[int]] = {}

    for vaa in vaas:
        ts, updated = getVAATimes(vaa)
        
        parsed_vaa = VAA.parse(base64.b64decode(vaa["vaa"]))
        seg = parsed_vaa.segment()
        if seg not in deltas:
            deltas[seg] = []

        delta = round(updated - ts)

        if delta > 10000:
            continue

        deltas[seg].append((round(ts), delta))

    return deltas



if __name__ == "__main__":

    for name, id in CHAINS.items():

        all_vaa_stats: dict[str, list[tuple[int, int]]] = {}
        for page in range(30):
            vaas = getVAAs(id, page)
            if vaas is None:
                break

            for seg, data in vaas.items():
                if seg not in all_vaa_stats:
                    all_vaa_stats[seg] = []
                all_vaa_stats[seg].extend(data)


        max_y = 100

        plt.figure(figsize=(10,5))
        for seg, data in all_vaa_stats.items():
            ts = [datetime.fromtimestamp(x[0]) for x in data]
            delta = np.array([x[1] for x in data])

            if len(delta) == 0:
                continue

            ylim = delta.mean() + 3*delta.std()
            if ylim>max_y:
                max_y = ylim

            plt.scatter(ts, delta, label=f"...{seg[-8:]}")
            plt.legend()

        plt.ylim([0, max_y])

        plt.savefig(f"plots/{name}_times.png")