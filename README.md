# downtime-csv

This tool is used to measure how long a website is down from the user's perspective, such as when it is restarted. It continues to send HTTP requests for 5 minutes every 200ms, and outputs the start time, response time, and status of each request to standard output as CSV.

## Requirements

Python >= 3.7 

## Install

You can download and install this tool from pypi with the command below.

```shell
pip install downtime-csv
```

## Usage

You can collect data for that URL with the command below. The data is printed to standard output.

```
downtime-csv URL
```

## Example

Using the command below, you can obtain the results of accessing google.com every 200ms for 5 minutes as test.csv. Load this into Excel and analyze it.

```shell
downtime-csv google.com > test.csv
```

The first column is the start time, but it has millisecond precision, so please set it to display milliseconds in Excel as well.
Note that the output is in the order the requests finished. If you want to order by request start, sort the entire range by the value of the first column.
