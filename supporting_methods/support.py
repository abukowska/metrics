import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def prepare_and_build_HTML_file(graph_file_name, csv_file):
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

def draw_chart_and_save_to_picture_format(x_axis_data, y_axis_data, period_of_time, graph_file_name):
        fig = plt.figure(figsize=(10, 8))
        plt.plot(x_axis_data, y_axis_data, 'go')
        plt.xlabel('time [min]', fontsize=16)
        plt.ylabel('number of visits', fontsize=16)
        plt.grid(axis='y', linestyle='--')
        plt.xticks(np.arange(0, period_of_time/60, 1.0))
        fig.savefig("output/" + graph_file_name)
