# Performance metrics -- server requests

This project allows you to measure visits on your server and presents the results of it on a chart, collects data as csv and prepares html report.
Unique users are identified by IP address and User Agent. Requests with statuses 400 or similar or visits by Googlebot are excluded from the user list.

## Getting Started

Copy this repository on your local machine and feel free to use it :)

### Prerequisites

This code requires Linux OS (any distro), Python 3.x and some third-party Python libraries.

### Installing

1) Use attached *library_requirements* file for compliant libraries:
pip3 install -r library_requirements

2) then: python3 metrics_main.py

If you wouldn't have the access to any server with logs, the line within above mentioned main file has the code with copying server logs via ssh commented. To simulate having those logs ready, I've placed the access.log file in this project.

### Additional Info
Under *output* directory you can already find some results for greater picture of what you can get using my project.
I wanted to omit setting up cron for this script so the repetition of the script for a period of time is simulated using *schedule* library.

## Authors

* **Asia Zawadzka**
