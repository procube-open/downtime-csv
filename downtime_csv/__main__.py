#!env python

import argparse
import asyncio
import aiohttp
import time
import csv
import io

def parse_args():
    parser = argparse.ArgumentParser(description="Send many HTTP requests and output the response times in CSV format")
    parser.add_argument("url", help="URL to request")
    parser.add_argument("-H", "--header", action="append", help="Custom header to include in the request", default=[])
    parser.add_argument("-O", "--output-header", action="append", help="Response header to output in CSV", default=[])
    parser.add_argument("-f", "--allow-redirects", action="store_true", help="Follow redirects")
    parser.add_argument("-i", "--interval", type=int, default=200, help="Interval between requests in milliseconds")
    parser.add_argument('-n', '--num-requests', type=int, default=1500, help='Number of requests to make')
    return parser.parse_args()

def parse_headers(header_list):
    headers = {}
    if header_list:
        for header in header_list:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def format_csv_row(row):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(row)
    return output.getvalue().strip()

async def do_query(url, headers, output_headers, allow_redirects):
    async with aiohttp.ClientSession() as session:
        try:
            tat_start = time.time_ns()
            async with session.get(url, headers=headers, allow_redirects=allow_redirects) as resp:
                # discard the response body
                await resp.read()
                tat_end = time.time_ns()
                tat = tat_end - tat_start
                mlsec = int(tat_start % 1000000000 / 1000000)
                csv_row = [
                    f'{time.strftime("%X", time.localtime(tat_start/1000000000))}.{str(mlsec).zfill(3)}',
                    int(tat/1000000),
                    resp.status
                ]
                for header in output_headers:
                    csv_row.append(resp.headers.get(header, ''))
                print(format_csv_row(csv_row))
        except Exception as e:
            print(f"Error occurred: {e}")

async def downtime(url, headers, output_headers, allow_redirects, interval, n):
    task_list = []
    for i in range(n):
        task_list.append(asyncio.create_task(do_query(url, headers, output_headers, allow_redirects)))
        await asyncio.sleep(interval / 1000.0)
    for j in task_list:
        await j

def main():
    args = parse_args()
    headers = parse_headers(args.header)
    output_headers = args.output_header if args.output_header else []
    # Print CSV header
    csv_header = ["Time", "TAT(ms)", "Status"] + output_headers
    print(format_csv_row(csv_header))
    asyncio.run(downtime(args.url, headers, output_headers, args.allow_redirects, args.interval, args.num_requests))

if __name__ == "__main__":
    main()
