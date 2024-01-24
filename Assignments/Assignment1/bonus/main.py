import psutil
import argparse
import threading
from prettytable import PrettyTable
import matplotlib.pyplot as plt

script_finished = False
all_cpu_usage = []


def cpu_measure():
    while not script_finished:
        measure = psutil.cpu_percent(interval=1, percpu=True)
        all_cpu_usage.append(measure)


def recollect_args() -> argparse.Namespace:
    # argsparse
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description="Measure the CPU usage of a python script per core"
    )
    # add a required argument script, it is not a flag it is a positional argument
    parser.add_argument("script", help="Script to measure CPU usage of")
    # add a flag to set the interval at which the CPU usage is to be measured
    parser.add_argument(
        "-i",
        "--interval",
        help="Interval at which the CPU usage is to be measured in seconds",
        type=int,
    )
    # add a flog to show results in a plot (true or false)
    parser.add_argument(
        "--plot",
        help="Plot the CPU usage of each core",
        action="store_true",
    )
    # add flag to write results to a file
    parser.add_argument(
        "-o",
        "--output",
        help="Write the CPU usage of each core to a file",
        type=str,
    )
    return parser.parse_args()


def show_results():
    table = PrettyTable()
    num_cores = len(all_cpu_usage[0])
    # Add the headers
    cores_header = ["Core {}".format(i) for i in range(num_cores)]
    table.field_names = ["Interval", *cores_header]

    for interval, usage in enumerate(all_cpu_usage, start=0):
        # Add the interval and the cpu usage of each core
        table.add_row([interval, *usage])

    # Imprimir la tabla
    return table


def plot_results():
    # plot the cpu usage
    plt.plot(all_cpu_usage)
    plt.xlabel("Interval")
    plt.ylabel("CPU usage (%)")
    plt.title("CPU usage of each core")
    plt.legend(["Core {}".format(i) for i in range(len(all_cpu_usage[0]))])
    plt.show()


if __name__ == "__main__":
    args = recollect_args()
    # run the script and conccurently measure the cpu usage, when script is done, stop measuring
    script_content = open(args.script).read()
    cpu_measure_thread = threading.Thread(target=cpu_measure)

    cpu_measure_thread.start()

    # Wait for the script thread to finish
    try:
        exec(script_content)
    except Exception as e:
        print("Error while executing the script")
        print(e)
        exit(1)
    script_finished = True

    # print all_cpu_usage in a table
    if args.output:
        # write the cpu usage to a file
        with open(args.output, "w") as f:
            f.write(str(show_results()))
    else:
        # print the cpu usage
        print(show_results())

    if args.plot:
        # plot the cpu usage
        plot_results()
