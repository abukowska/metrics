import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def prepare_and_build_HTML_report(graph_file_name, csv_file):
    """Prepares an HTML report based on csv file name/path
    and an already generated graph/chart. File generated in output dir.

    Keyword arguments:
    graph_file_name -- graph path/name to be embedded in HTML file
    csv_file -- file name/path to data that will be used for report
    """
    df = pd.read_csv(csv_file)
    summary_table = df.describe()
    summary_table = summary_table.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">')

    html_string = '''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>body{margin:0 100; background:whitesmoke;}</style>
        </head>
        <body>
            <h1>Server visits per each minute</h1>
            <iframe width="1000" height="550" frameborder="0" seamless="seamless" \
            scrolling="no" src="''' + graph_file_name + '''"></iframe>
            <p></p>

            <h3>Summary table:</h3>
            ''' + summary_table + '''
        </body>
    </html>'''

    with open('output/html_metric_results.html', 'w') as htmlfile:
        htmlfile.write(html_string)

def draw_chart_and_save_to_picture_format(x_axis_data, y_axis_data, period_of_time, graph_file_name, x_label_name, y_label_name):
    """Draws a chart/graph based on provided data per each x, y axis, their label names,
    execution time of the script (axis x range) under expected filepath.

    Keyword arguments:
    x_axis_data -- data for x axis
    y_axis_data -- data for y axis
    period_of_time -- execution time of the script, helps to render desired x axis arange
    x_label_name, y_label_name -- descripions of axes with their units
    """
    fig = plt.figure(figsize=(10, 8))
    plt.plot(x_axis_data, y_axis_data, 'go')
    plt.xlabel(x_label_name, fontsize=16)
    plt.ylabel(y_label_name, fontsize=16)
    plt.grid(axis='y', linestyle='--')
    plt.xticks(np.arange(0, period_of_time/60, 1.0))
    fig.savefig("output/" + graph_file_name)

def save_output_data_as_csv_enumerated_data(data):
    """Saves provided data as csv formatted file under expected filepath.
    First column represents minute values, starting from 1; the second one provided data.
    File generated in output dir.

    Keyword arguments:
    data -- data used for csv generation purposes
    """
    with open('output/metrics_results.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(('min', 'no of visits'))
        for record in enumerate(data, 1):
            spamwriter.writerow(record)
