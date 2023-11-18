#!/bin/python3

import json
import csv
from parsers import fileparse
import re
import sys
from icecream import ic


# Extract text from files
def get_file_contents(files: list) -> dict:  
    # Convert to dict of filenames and content
    data = {}
    for file in files:
        if ".pdf" in file:
            pdf_text = fileparse.get_pdf_text(file)
            data.update({file: pdf_text})
        elif ".html" in file:
            html_str_content = fileparse.get_html_text(file, as_string = True)
            data.update({file: html_str_content})
        else:
            with open(file, 'r') as file:
                csv_content = file.read()
            data.update({file.name: csv_content})
    return data

# Grab IOCs from content
def extract_iocs(data):
    # Define our regexes
    md5_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])")
    sha1_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
    sha256_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
    sha512_pattern = re.compile(r"[0-9a-f]{128}")
    ipv4_pattern = re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
    #domain_pattern = re.compile(r"(?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,}")
    better_domain = re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[A-Za-z]{2,}(?<!\.exe|\.bat)(?<!\.sh)\b")
    url_pattern = re.compile(r"https?://(?:[A-Za-z0-9\-]+\.)+[A-Za-z0-9]{2,}(?::\d{1,5})?[/A-Za-z0-9\-%?=\+\.]+")
    #email_pattern
    #executable_pattern
    #onion_address_pattern
    #ioc_filename_pattern
    #file_extension_pattern

    results = {}

    # Loop through our strings
    # Convert our findings to sets to deduplicate
    for key, value in data.items():
        if isinstance(value, list):
            for content in value:
                results[key] = {
                    "md5": list(set(md5_pattern.findall(content))),
                    "sha1": list(set(sha1_pattern.findall(content))),
                    "sha256": list(set(sha256_pattern.findall(content))),
                    "sha512": list(set(sha512_pattern.findall(content))),
                    "ipv4": list(set(ipv4_pattern.findall(content))),
                    "domain": list(set(better_domain.findall(content))),
                    "url": list(set(url_pattern.findall(content))),
                }    
        else:
            content = value
            results[key] = {
                "md5": list(set(md5_pattern.findall(content))),
                "sha1": list(set(sha1_pattern.findall(content))),
                "sha256": list(set(sha256_pattern.findall(content))),
                "sha512": list(set(sha512_pattern.findall(content))),
                "ipv4": list(set(ipv4_pattern.findall(content))),
                "domain": list(set(better_domain.findall(content))),
                "url": list(set(url_pattern.findall(content))),
            }
    return results

# output to CSV or JSON
# Columns: File, Type, Value
def csv_output(results):
    output_file: str = 'results.csv'
    headers = ['File', 'Type', 'Value']

    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for filename in results:
            result = results[filename]
            for ioc_type in result:
                iocs = result[ioc_type]
                rows = [[filename, ioc_type, i] for i in iocs]
                writer.writerows(rows)

    print(f'{output_file} written')

def main(argv):
    if len(argv) < 2:
        raise SystemExit(f'Usage: {argv[0]} ' 'file1 file2 file3 ...')

    imported_content = get_file_contents(sys.argv[1:])

    extracted_iocs = extract_iocs(imported_content)

    csv_output(extracted_iocs)

if __name__ == '__main__':
    import sys
    main(sys.argv)