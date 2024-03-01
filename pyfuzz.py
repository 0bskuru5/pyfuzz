import argparse
import requests
import concurrent.futures
import os
import csv

class PyFuzz:
    def __init__(self, target_url, wordlist, output_file):
        self.target_url = target_url
        self.wordlist = wordlist
        self.output_file = output_file
        self.results = []

    def send_request(self, url):
        try:
            response = requests.get(url)
            self.results.append((url, response.status_code, response.text))
        except requests.RequestException as e:
            pass

    def fuzz(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.send_request, self.generate_urls())
        
        self.save_results()

    def generate_urls(self):
        with open(self.wordlist, 'r') as f:
            for line in f:
                yield self.target_url + line.strip()

    def save_results(self):
        with open(self.output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['URL', 'Status Code', 'Response Body'])
            for result in self.results:
                csv_writer.writerow(result)

def main():
    parser = argparse.ArgumentParser(description='PyFuzz - Advanced Web Fuzzing Tool')
    parser.add_argument('url', type=str, help='Target URL')
    parser.add_argument('wordlist', type=str, help='Path to wordlist')
    parser.add_argument('-o', '--output', type=str, default='output.csv', help='Output file to store results (default: output.csv)')
    args = parser.parse_args()

    fuzzer = PyFuzz(args.url, args.wordlist, args.output)
    fuzzer.fuzz()

    print("Fuzzing completed. Results saved to", args.output)

if __name__ == "__main__":
    main()
