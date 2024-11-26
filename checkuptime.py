import pycurl
import yaml
import argparse
from io import BytesIO
import time

def load_sites_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data['sites']

def check_site_uptime(url, method, body=None, headers=None):

    buffer = BytesIO()  # Define the buffer before using it
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.FOLLOWLOCATION, True)

    if headers is None:
        headers = []
    elif isinstance(headers, str):
        headers = [headers]
    elif isinstance(headers, list):
        # Ensure all elements in the list are strings
        headers = [str(header) for header in headers]
    if headers:
        c.setopt(c.HTTPHEADER, headers)

    if method == "POST":
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, body)
    else:
        c.setopt(c.HTTPGET, 1)

    try:
        c.perform()
        http_code = c.getinfo(c.RESPONSE_CODE)
        response_time = c.getinfo(c.TOTAL_TIME) * 1000

        if http_code == 200 and response_time < 500:
            return True, response_time
        else:
            return False, response_time
    finally:
        c.close()

def monitor_uptime(sites, interval=15):
    uptime_stats = {site['url']: {'up': 0, 'total': 0, 'response_times': [], 'url': site['url']} for site in sites}

    while True:
        for site in sites:
            method = site.get('method', 'GET')
            url = site['url']
            body = site.get('body', None)
            headers = site.get('headers', [])
            is_up, response_time = check_site_uptime(url, method, body, headers)

            uptime_stats[url]['total'] += 1
            if is_up:
                uptime_stats[url]['up'] += 1
            uptime_stats[url]['response_times'].append(response_time)

        time.sleep(interval)

        display_uptime(uptime_stats)

def display_uptime(uptime_stats):
    for site_url, stats in uptime_stats.items():
        uptime_percentage = (stats['up'] / stats['total']) * 100 if stats['total'] > 0 else 0
        avg_response_time = sum(stats['response_times']) / len(stats['response_times']) if stats['response_times'] else 0
        print(f"{site_url} has {uptime_percentage:.2f}% availability percentage")

def parse_arguments():
    parser = argparse.ArgumentParser(description="YAML to import URLs, site names, etc, from")
    parser.add_argument(
        '--yaml',
        type=str,
        required=True,
        help="Path to YAML file"
    )
    return parser.parse_args()

# Main execution
if __name__ == "__main__":
    try:
        args = parse_arguments()
        yaml_file = args.yaml
        sites = load_sites_from_yaml(yaml_file)
        monitor_uptime(sites, interval=15)
    finally:
        c.close()
