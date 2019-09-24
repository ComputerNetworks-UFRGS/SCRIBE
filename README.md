# SCRIBE
SCRIBE (SeCuRity Intent-Based Extractor)

### Instalation

Our solutions runs on top of FWS. Firstly, the FWS must installed and running in your machine. 

##### Step #1: Clone FWS repository:

    git clone https://github.com/rafaelhribeiro/fws

##### Step #2: Install FWS

Follow installation instructions from the FWS repository, as described in the following link
https://github.com/rafaelhribeiro/fws-export#installation

##### Step #3: Clone this repo

After FWS is running, clone our repository inside FWS solution:

    cd fws
    git clone https://github.com/rafaelhribeiro/SCRIBE
    
#### Step #4: Install Pipenv

Follow installation instructions from the Pipenv official repository in the following link https://github.com/pypa/pipenv#installation

### Configuration

SCRIBE expects a JSON file indicating the CSV for filtering and NAT, an alias file for interfaces (optional) and the network prefixes. A configuration example is listed below:

    {
        "alias_file":"interface_aliases",
        "filtering":[
            "FILTER.csv"
        ],
        "network_prefixes":[
            "172.16.1.0/24"
        ]
    }

   
