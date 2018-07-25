import csv
import subprocess
import time

import numpy as np
import schedule

from supporting_methods import support

START = time.time()
PERIOD_OF_TIME_SEC = 20
REPEATING_SCHEDULE_SEC = 6
GRAPH_FILE_NAME = "graph.png"

visits_per_minute = []
line_to_start_read = 0

def count_user_visits():
    global line_to_start_read
    global visits_per_minute
    # TODO: try, catch
    # uncomment below for ssh aws instance logs copy
    # subprocess.call("(scp -i ~/.ssh/metrics ec2-user@34.242.250.224:~/logs/access.log .)", shell=True)
    data = np.genfromtxt('access.log', dtype=str, delimiter='"', usecols=(0,2,5))
    print("line to start " + str(line_to_start_read))
    if line_to_start_read != 0:
        data = data[line_to_start_read:]
    else:
        line_to_start_read = len(data.tolist())

    users = []

    for el in data:
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
    count_user_visits()
    schedule.every(REPEATING_SCHEDULE_SEC).seconds.do(count_user_visits)

    while True:
        schedule.run_pending()
        if time.time() > START + PERIOD_OF_TIME_SEC:
            break

    with open('output/metrics_results.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(('min', 'no of visits'))
        for record in enumerate(visits_per_minute, 1):
            spamwriter.writerow(record)

    x_axis_time = list(x for x in range(1, len(visits_per_minute)+1))
    y_axis_visits = visits_per_minute

    support.draw_chart_and_save_to_picture_format(x_axis_time, y_axis_visits, PERIOD_OF_TIME_SEC, GRAPH_FILE_NAME)

    support.prepare_and_build_HTML_file(GRAPH_FILE_NAME, "output/metrics_results.csv")


if __name__ == "__main__":
    main()
