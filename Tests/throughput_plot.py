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

def plot_txnlen_vs_throughput():
    d = argv[1]
    var = "Throughput(ops/sec),"
    final_results = {}
    ts = ["4","8","32","64","256"]

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
                for sz in ts:
                    if f.find(algo + "-" + sz) != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            


    x_axis = [4,8,32,64,256]
    fig = plt.figure()
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("txn size (ops)")
    ax.set_xscale('log',base = 2)
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()

    plt.show()


def plot_perc_reads_vs_throughput():
    d = argv[1]
    var = "Throughput"
    final_results = {}
    ts = ["1", "0.75", "0.5","0.25", "0"]
    for algo in algos:
        final_results[algo] = {}
    if var == "Throughput":
        var += "(ops/sec),"
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        #print f
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
                for sz in ts:
                    if f.find(algo + "-4-THREADS1000-RPROP" + sz + "-") != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            


    x_axis = [1, 0.75, 0.5, 0.25, 0]
    fig = plt.figure(4)
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("read proportion")
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()

    plt.show()

def plot_numkeys_vs_throughput():
    d = argv[1]
    var = "Throughput"
    final_results = {}
    ts = ["10", "100", "1000","10000", "100000","10000000"]
    for algo in algos:
        final_results[algo] = {}
    if var == "Throughput":
        var += "(ops/sec),"
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
            if f.find("READ_ATOMIC_" + algo) != -1:
                for sz in ts:
                    if f.find("-4-THREADS1000-RPROP0.95-VS1-TXN4-NC5-NS5-NK" + sz + "-DCP0.000000-CCD-1-IT") != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]

    x_axis = [10, 100, 1000, 10000]
    fig = plt.figure(7)
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("Num keys")
    
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            if sz == "10000000" or sz == "100000":
                continue
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()
    plt.show()

def plot_value_size_vs_throughput():
    d = argv[1]
    var = "Throughput"
    final_results = {}
    ts = ["10", "100", "1000","10000", "100000","10000000"]
    for algo in algos:
        final_results[algo] = {}
    if var == "Throughput":
        var += "(ops/sec),"
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        #print f
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
                for sz in ts:
                    if f.find(algo + "-4-THREADS1000-RPROP0.95-VS" + sz + "-") != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            


    x_axis = [10, 100, 1000, 10000, 100000, 10000000]
    fig = plt.figure(3)
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("Value size (bytes)")
    
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()

    plt.show()    



accepted_args = ["txnlen","threads","rprop","valuesize","numkeys","lora"]

if __name__ == "__main__":
    if argv[2] == "txnlen":
        plot_txnlen_vs_throughput()
    elif argv[2] == "rprop":
        plot_perc_reads_vs_throughput()
    elif argv[2] == "valuesize":
        plot_value_size_vs_throughput()
    elif argv[2] == "numkeys":
        plot_numkeys_vs_throughput()
    else:
        print("Could not recognize arg: " + argv[2])
        print("Usage: python analyze_logs.py /path/to/dir argv[2] where argv[2] one of:")
        print(accepted_args)


