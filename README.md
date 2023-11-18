# IOC Extractor

## Overview
---
Currently, IOC Extractor is a crude scraper for IOC values in CSV, HTML, and PDF files and outputs `results.csv` file, organized by filename and type of IOC.

### Installation
---
`git clone https://github.com/fractal-mind/ioc-extractor.git`
`chmod +x ioc-extractor-cli.py`

### Usage
---
`./ioc-extractor-cli.py <file1> <file2> <file3> <...>`

TODO:
- [ ] cleanup requirements, setup, etc.
- [ ] implement JSON output
- [ ] clean up/add more pattern regexes
- [ ] add XML input
- [ ] fix poetry installation
