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

def plot_lat_vs_tsize():
    d = argv[1]
    var = "AverageLatency"    

    if var == "AverageLatency":
        var += "(us),"
    final_results = {}
    fr_read = {}
    fr_write = {}
    tlens = ["4","8","32","64","256"]
    for algo in algos:
        final_results[algo] = {}
        fr_read[algo] = {}
        fr_write[algo] = {}
        for tlen in tlens:
            final_results[algo][tlen] = 0
            fr_read[algo][tlen] = 0
            fr_write[algo][tlen] = 0

    for f in listdir(argv[1]):
        if f.find("IT0") == -1:
            continue
        f = argv[1]+'/'+f
        a = ""
        tlen = ""
        for algo in algos:
            if f.find("READ_ATOMIC_" + algo) != -1:
                a = algo
                break

        for l in tlens:
            if f.find(a + "-" + l + "-") != -1:
                tlen = l
                break
        
        if tlen == "":
            continue
        results = {}
        rr = {}
        rw = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
                rr[c] = 0
                rw[c] = 0
            lookout = False
            opr = 0
            opw = 0
            latr = 0
            latw = 0
            for line in open(g+"/run_out.log"):
                if line.find("Operations,") != -1:
                    for word in line.split():
                        if word == "Operations,":
                            lookout = True
                        elif lookout:
                            lookout = False
                            if line.find("[UPDATE-TXN]") != -1:
                                opw = float(word)
                            else:
                                opr = float(word)
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            lookout = False
                            if line.find("[UPDATE-TXN]") != -1:
                                latw = float(word)
                            else:
                                latr = float(word)
            if opr + opw == 0:
                results[c] += 0
                rr[c] += 0
                rw[c] += 0
            else:
                results[c] += (opr*latr*pow(10,-3) + opw+latw*pow(10,-3))/(opr+opw)
                rr[c] += latr*pow(10,-3)
                rw[c] += latw*pow(10,-3)
        for c in results:
            final_results[a][tlen] += results[c]
            fr_read[a][tlen] += rr[c]
            fr_write[a][tlen] += rw[c]

    x_axis = [4,8,32,64,256]
    fig = plt.figure()
    ax = plt.axes()
    ax.set_yscale('log', base = 10)
    plt.ylabel("Average Latency (ms)")
    plt.xlabel("Txn Len")
    plt.title("Avg Lat vs Tlen")

    for algo in algos:
        y_axis = []
        for tlen in tlens:
            y_axis.append(float(final_results[algo][tlen]/5))
        ax.plot(x_axis,y_axis,marker = marks[algo],label = names[algo])
        ax.legend()

    plt.show()


    fig = plt.figure()
    ax = plt.axes()
    ax.set_yscale('log', base = 10)
    plt.ylabel("Average Latency (ms)")
    plt.xlabel("Txn Len")
    plt.title("Avg Lat Read vs Tlen")

    for algo in algos:
        y_axis = []
        for tlen in tlens:
            y_axis.append(float(fr_read[algo][tlen]/5))
        ax.plot(x_axis,y_axis,marker = marks[algo],label = names[algo])
        ax.legend()

    plt.show()

    fig = plt.figure()
    ax = plt.axes()
    ax.set_yscale('log', base = 10)
    plt.ylabel("Average Latency (ms)")
    plt.xlabel("Txn Len")
    plt.title("Avg Lat Updates vs Tlen")

    for algo in algos:
        y_axis = []
        for tlen in tlens:
            y_axis.append(float(fr_write[algo][tlen]/5))
        ax.plot(x_axis,y_axis,marker = marks[algo],label = names[algo])
        ax.legend()

    plt.show()



accepted_args = ["txnlen","threads","rprop","valuesize","numkeys","lora"]

if __name__ == "__main__":
    if argv[2] == "txnlen":
        plot_lat_vs_tsize()
    else:
        print("Could not recognize arg: " + argv[2])
        print("Usage: python analyze_logs.py /path/to/dir argv[2] where argv[2] one of:")
        print(accepted_args)