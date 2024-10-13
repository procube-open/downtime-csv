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

## Add custom header

The downtim-csv command allows you to add headers to HTTP requests using the -H option, similar to curl.

```shell
downtime-csv https://example.com -H "Authorization: Bearer token" -H "Custom-Header: Value"
```

The headers given by default are as follows:

```
User-Agent: aiohttp/<version> python/<version>
Accept-Encoding: gzip, deflate
Accept: */*
```

These headers are what aiohttp adds to requests by default. If you add a custom header, it will not override these default headers, but if you specify a header with the same name, the custom header will take precedence.