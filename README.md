# Performance metrics -- server requests

This project allows you to measure visits on your server and presents the results of it on a chart.

## Getting Started

Copy this repository on your local machine and feel free to use it :)

### Prerequisites

This code requires Linux OS (any distro), Python 3 and some third-party libraries.

### Installing

Use attached *library_requirements* file for compliant libraries:
pip3 install -r library_requirements

THEN: python3 metrics_main.py

As you woudn't have the access to aws instance with logs, the line within above mentioned main file has the code with copying logs via ssh commented. To simulate having those logs ready, I've placed the access.log file with some logs.

### Additional Info
Under *output* directory you already find some results for greater picture of what you can get using my project. 

## Authors

* **Asia Zawadzka**
