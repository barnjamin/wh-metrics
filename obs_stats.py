import requests
import numpy as np
from datetime import datetime
from consts import TS_FMT, UPDATED_FMT, GUARDIAN_KEYS


OBS_BASE_URL = "https://api.wormscan.io/api/v1/observations"


def getObsTime(data: dict)->int:
    try:
        indexed = datetime.strptime(data["indexedAt"], UPDATED_FMT)
    except Exception:
        indexed = datetime.strptime(data["indexedAt"], TS_FMT)

    return int(indexed.timestamp())


def get_observations(chain_id: int):

    observations: dict[str, list[tuple[str, int]]] = {}
    for page in range(50):
        result = requests.get(f"{OBS_BASE_URL}/{chain_id}?page={page}")
        obs = result.json()

        if len(obs) == 0: 
            break

        for o in obs:
            id_chunks = o["id"].split("/")
            id = "/".join(id_chunks[:3])
            if id not in observations:
                observations[id] = []
            observations[id].append((o["guardianAddr"], getObsTime(o)))

    deltas: dict[str, list[int]] = {name:[] for name in GUARDIAN_KEYS.values()}


    for id, obs in observations.items():
        ts = np.array([o[1] for o in obs])
        names = [GUARDIAN_KEYS[o[0]] for o in obs]

        min_time = ts.min()
        for idx in range(len(ts)):
            deltas[names[idx]].append(ts[idx] - min_time)

    for n, ds in deltas.items():
        if len(ds) == 0:
            continue

        d = np.array(ds)
        print(f"{n:<20}:\t{len(d)}\t{d.mean():.2f}\t{d.std():.2f}\t{d.max()}")


if __name__ == "__main__":
    get_observations(1)
