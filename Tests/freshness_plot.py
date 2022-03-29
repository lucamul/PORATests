from os import listdir
import string
from sys import argv
import matplotlib.pyplot as plt
import matplotlib
from os import system

algos = ["LIST","LORA","STAMP"]
marks = {}
marks["LIST"] = "o"
marks["STAMP"] = "v"
marks["LORA"] = "x"
marks["BLOOM"] = "^"
names = {}
names["LIST"] = "RAMP-F"
names["STAMP"] = "RAMP-S"
names["BLOOM"] = "RAMP-H"
names["LORA"] = "LORA"

staleness = [10,20,30,40,50,100,150,200,500,1000,3000]


def freshness_RAMPF(type_exp: string, distr: string):
    final_results = {}
    final_results["LIST"] = {}
    tot = 0
    for stale in staleness:
        final_results["LIST"][stale] = 0
    for f in listdir(argv[1]):
        if f.find("LIST") == -1:
            continue
        if f.find(distr) == -1:
            continue
        if f.find(".tar") != -1:
            continue
        f = argv[1] + '/' + f
        for g in listdir(f):
            if g.find("S") == -1:
                continue
            lastAp = {}
            lastFresh = {}
            g = f + '/' + g
            key = ""
            s = g.split("/S")[1]
            for line in open(g + "/server-0.log"):
                if line.find("Freshness") == -1:
                    continue
                lookoutKey = False
                lookout = False
                for word in line.split():
                    if(word == "key:"):
                        lookoutKey = True
                        key = ""
                    elif lookoutKey:
                        lookoutKey = False
                        key = word
                    if(word == "="):
                        lookout = True
                    elif lookout:
                        lookout = False
                        if(lastAp.get(key) is None):
                            if(line.find("Round 2") != -1):
                                lastAp[key] = 2
                                lastFresh[key] = int(word)
                                for stale in staleness:
                                    if(int(word) <= stale):
                                        final_results["LIST"][stale] += 1
                                tot += 1
                            else:
                                lastAp[key] = 1
                                lastFresh[key] = int(word)
                        else:
                            if lastAp[key] == 2:
                                if(line.find("Round 2") != -1):
                                    lastFresh[key] = int(word)
                                    for stale in staleness:
                                        if(int(word) <= stale):
                                            final_results["LIST"][stale] += 1
                                    tot += 1
                                else:
                                    lastFresh[key] = int(word)
                                    lastAp[key] = 1
                            else:
                                if(line.find("Round 2") != -1):
                                    lastFresh[key] = int(word)
                                    lastAp[key] = 2
                                    for stale in staleness:
                                        if(int(word) <= stale):
                                            final_results["LIST"][stale] += 1
                                    tot += 1
                                else:
                                    for stale in staleness:
                                        if(int(word) <= stale):
                                            final_results["LIST"][stale] += 1
                                    tot += 1
                                    lastAp[key] = 1
                                    lastFresh[key] = int(word)
            for key in lastAp:
                if lastAp[key] == 1:
                    for stale in staleness:
                        if(lastFresh[key] <= stale):
                            final_results["LIST"][stale] += 1
                    tot += 1
    y_axis = []
    for stale in staleness:
        y_axis.append(float(final_results["LIST"][stale]/tot))
    return y_axis
    

def freshness_STAMP_LORA(type_exp: string, algo: string, distr : string):
    final_results = {}
    final_results[algo] = {}
    tot = 0
   
    for stale in staleness:
        final_results[algo][stale] = 0
    for f in listdir(argv[1]):
        if f.find(algo) == -1:
            continue
        if f.find(distr) == -1:
            continue
        if f.find(".tar") != -1:
            continue
        f = argv[1] + '/' + f
        
        for g in listdir(f):
            if g.find("S") == -1:
                continue
            g = f + '/' + g
            s = g.split("/S")[1]
            for line in open(g + "/server-0.log"):
                if line.find("Freshness") == -1:
                    continue
                lookout = False
                for word in line.split():
                    if(word == "="):
                        lookout = True
                    elif lookout:
                        lookout = False
                        for stale in staleness:
                            if(int(word) <= stale):
                                final_results[algo][stale] += 1
                        tot += 1
    y_axis = []
    for stale in staleness:
        y_axis.append(float(final_results[algo][stale]/tot))
    return y_axis
                
def plot_freshness(tlen : string, kspace : string, rprop: string, distribution: string):
    
    type_exp = "-" + tlen + "-" + "THREADS1000-RPROP" + rprop +"-VS1-TXN" + tlen + "-NC5-NS5-NK" + kspace + "-DCP0.000000-CCD-1-IT"
    y_axis_rampF = freshness_RAMPF("LIST" + type_exp, distribution)
    y_axis_LORA = freshness_STAMP_LORA("LORA" + type_exp, "LORA", distribution)
    y_axis_STAMP = freshness_STAMP_LORA("STAMP" + type_exp, "STAMP", distribution)
    fig = plt.figure(1)
    ax = plt.axes()
    plt.ylabel("Read Staleness")
    plt.xlabel("staleness (ms)")
    plt.title("Staleness of reads with Key Space of size " + kspace + " read proportion " + rprop + " txn size " + tlen)
    ax.plot(staleness,y_axis_rampF, marker = marks["LIST"], label = names["LIST"] + " " + distribution)
    ax.plot(staleness,y_axis_STAMP, marker = marks["STAMP"], label = names["STAMP"] + " " + distribution)
    ax.plot(staleness,y_axis_LORA, marker = marks["LORA"], label = names["LORA"] + " " + distribution)
    ax.legend()
    #plt.show()


kss = ["100000"]
tlens = ["8"]
rprops = ["0.75"]
distributions = ["uniform","zipfian"]

if __name__ == "__main__":
    for ks in kss:
        for tlen in tlens:
            for rprop in rprops:
                for distr in distributions:
                    plot_freshness(tlen,ks,rprop,distr)
            plt.show()