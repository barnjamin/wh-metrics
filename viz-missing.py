import datetime
import matplotlib.pyplot as plt
from consts import CHAINS, CHAINS_BY_ID


def plotski():
    with open("missing-seqs.csv", "r") as f:
        data = f.read()

    data = data.split("\n")

    by_chain: dict[str, dict[int, int]] = {}

    for row in data[1:]:
        [id, start, stop] = row.split(",")
        start, stop = int(start), int(stop)
        mid = start + (stop - start)//2
        if mid < 1690288000:
            continue

        mid = datetime.datetime.fromtimestamp(mid)
        mid = mid.replace(hour=0, minute=0, second=0, microsecond=0)



        [chain_id, emitter, seq] = id.split("/")

        if chain_id not in by_chain:
            by_chain[chain_id] = {} 

        if mid not in by_chain[chain_id]:
            by_chain[chain_id][mid] = 0

        by_chain[chain_id][mid] += 1


    # Plot data by date and number of missed sequences on the same plot with correct
    # axis labels and legend
    # make sure to convert the timestamp to a date so it plots correctly
    plt.figure(figsize=(15, 5))
    plt.xlabel("Date")
    plt.ylabel("Number of missed sequences")
    plt.xticks(rotation=45)
    #plt.tight_layout()
    for chain_id, data in by_chain.items():
        #if chain_id not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        #    continue
        x = data.keys()
        y = data.values()
        plt.bar(x, y, label=CHAINS_BY_ID[int(chain_id)])

    # add legend outside main plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)


    plt.savefig(f"missed.png")



if __name__ == "__main__":
    plotski()