import subprocess
import sys
import time

import numpy as np
import schedule

from supporting_methods import support

START = time.time()
REPEATING_SCHEDULE_SEC = 6  # we'd like to mesure data every 1 min
PERIOD_OF_TIME_SEC = REPEATING_SCHEDULE_SEC * 4  # script is going to work for 5 mins
GRAPH_FILE_NAME = "graph.png"
visits_per_minute = []
line_to_start_read = 0

def count_user_visits():
    """Counts unique users server visits basing on copied server logs (via ssh or local file).
    Requests with statuses 400 or similar or visits by Googlebot are excluded from the user list.
    Unique users are identified by IP address and User Agent.
    """
    global line_to_start_read
    global visits_per_minute
    users = []
    try:
        # uncomment below for ssh aws instance logs copy
        # subprocess.call("(scp -i ~/.ssh/metrics ec2-user@34.242.250.224:~/logs/access.log .)", shell=True)
        data = np.genfromtxt('access.log', dtype=str, delimiter='"', usecols=(0,2,5))
    except IOError as ioe:
        print("IOError, can't find or read data.")
        sys.exit(1)

    print("line to start " + str(line_to_start_read))

    if line_to_start_read != 0:
        newly_gen_data = data[line_to_start_read:]
    else:
        newly_gen_data = data

    line_to_start_read = len(data.tolist())  # new last file line number assigned

    for el in newly_gen_data:
        user_agent = el[2].strip()
        status_code = el[1].strip().split()[0]

        if "googlebot" in user_agent.lower() or status_code.startswith("4"):
            continue

        ip_address = el[0].strip().split()[0]
        one_unique_user = (ip_address, user_agent)
        users.append(one_unique_user)

    unique_users = list(set([tuple(t) for t in users]))
    visits_per_minute.append(len(unique_users))
    print("unique users:" + str(len(unique_users)))
    print("------------")


def main():
    """Counts unique users server visits through time.
    Report is presented as HTML file in output directory.
    There is also csv data file and a graph generated.
    """
    count_user_visits()

    # schedule instead of cron
    schedule.every(REPEATING_SCHEDULE_SEC).seconds.do(count_user_visits)
    while True:
        schedule.run_pending()
        if time.time() > START + PERIOD_OF_TIME_SEC:
            break

    support.save_output_data_as_csv_enumerated_data(visits_per_minute)

    x_axis_time = list(x for x in range(1, len(visits_per_minute)+1))
    y_axis_visits = visits_per_minute

    support.draw_chart_and_save_to_picture_format(x_axis_time, y_axis_visits, GRAPH_FILE_NAME, 'time [min]', 'number of visits')

    support.prepare_and_build_HTML_report(GRAPH_FILE_NAME, "output/metrics_results.csv")


if __name__ == "__main__":
    main()
