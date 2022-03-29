from os import listdir
from sys import argv
import matplotlib.pyplot as plt
import matplotlib

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

set = ["0.25","0.5","0.75","0.95"]
str_search = "RPROP"
x_axis = [0.25,0.5,0.75,0.95]
x_label = "read proportion"
def plot_throughput():
    d = argv[1]
    var = "Throughput(ops/sec),"
    final_results = {}

    for algo in algos:
        final_results[algo] = {}
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        f = argv[1]+'/'+f
        results = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
            lookout = False
            for line in open(g+"/run_out.log"):
                
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            results[c] += float(word)
                            lookout = False
        for algo in algos:
            if f.find(algo) != -1:
                for sz in set:
                    if f.find(str_search + sz) != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            

    fig = plt.figure()
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel(x_label)
    #ax.set_xscale('log',base = 2)
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in set:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()

    plt.show()

if __name__ == "__main__":
    plot_throughput()


