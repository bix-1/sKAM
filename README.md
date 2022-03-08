# sKAM project 2021
Script for checking room availability at [KAM VUTBR dorms](http://www.kam.vutbr.cz/) - the KAM ~~scam~~ scan

## Description
Python script for fetching the data from [KAM VUTBR dorms DB](https://www.kn.vutbr.cz/) and checking _anonymized_ updates on room availability. Created due to unwillingness of the dorm's administration to allow students to check the room availability apart from __asking at their office *in person*__.

## Authors
- Jakub Bartko jbartkoj@gmail.com

## Installation
- Clone repo
- Install requirements using `pip install -r requirements.txt`

## Usage
- **Run** using `./sKAM.py`
- If using outside of KolejNet network, provide your user credentials (username, password) to access the information system
- See `./sKAM.py --help` for detailed usage
- Updates are printed on standard output
  - Data is stored in `data` folder
