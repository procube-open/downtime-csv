#!env python

import aiohttp
import asyncio
import time
import sys
import argparse
import csv

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP request script with custom headers and CSV output")
    parser.add_argument("url", help="URL to request")
    parser.add_argument("-H", "--header", action="append", help="Custom header to include in the request", default=[])
    parser.add_argument("-O", "--output-header", action="append", help="Response header to output in CSV", default=[])
    parser.add_argument("-f", "--allow-redirects", action="store_true", help="Follow redirects")
    return parser.parse_args()

def parse_headers(header_list):
    headers = {}
    for header in header_list:
        key, value = header.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers

async def do_query(url, headers, output_headers, allow_redirects):
    async with aiohttp.ClientSession() as session:
        try:
            tat_start = time.time_ns()
            async with session.get(url, headers=headers, allow_redirects=allow_redirects) as resp:
                await resp.text()
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
                print(','.join(map(str, csv_row)))
        except Exception as e:
            print(f"Error occurred: {e}")

async def downtime(url, headers, output_headers, allow_redirects):
    task_list = []
    for i in range(1500):
        task_list.append(asyncio.create_task(do_query(url, headers, output_headers, allow_redirects)))
        await asyncio.sleep(0.2)
    for j in task_list:
        await j

def main():
    args = parse_args()
    headers = parse_headers(args.header)
    output_headers = args.output_header
    allow_redirects = args.allow_redirects
    url = args.url
    asyncio.run(downtime(url, headers, output_headers, allow_redirects))

if __name__ == '__main__':
    main()
