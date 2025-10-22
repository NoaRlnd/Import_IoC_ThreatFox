# ThreatFox
ThreatFox is an open threat intelligence sharing platform, allowin anyone to share indicators of compromise (IOCs). This repository provides some sample python3 scripts on how to interact with the ThreatFox API.

## Obtain an Auth-Key
In order to query the ThreatFox API, you need to obtain an ```Auth-Key```.  If you don't have an Auth-Key yet, you can get one at https://auth.abuse.ch/ for free.

## Query recent IOCs
This script calls ThreatFox's [recent IOC endpoint](https://threatfox.abuse.ch/api/#recent-iocs) which returns the most recent IOCs added to ThreatFox. The example below queries the endpoint for IOCs added to the database whithin the past day:
```
python3 threatfox_query_recent-iocs.py <YOUR-AUTH-KEY> 1
```

Pro tip: if you want to stay up to date with the most recent IOCs you may also want to have a look at ThreatFox's [data export](https://threatfox.abuse.ch/export/) which are generated regularely.

## Query IOCs for a given malware family
This script calls ThreatFox's [malware endpoint](https://threatfox.abuse.ch/api/#malware) which returns recent IOCs associated with a certain malware family. The example below shows the 50 most recent IOCs associated with Cobalt Strike
```
python3 threatfox_query_malware.py <YOUR-AUTH-KEY> CobaltStrike 50
```

## Query IOCs associated with a given tag
This script calls ThreatFox's [tag endpoint](https://threatfox.abuse.ch/api/#taginfo) which returns a list of recent IOcs associated with a certain tag. The example below shows the most recent IOCs having the tag "AS_DELIS" set:
```
python3 threatfox_query_tag.py <YOUR-AUTH-KEY> AS_DELIS
```

## Search an IOC
This script calls ThreatFox's [search endpoint](https://threatfox.abuse.ch/api/#search-ioc) which seaches the database for a given IOCs. The example below searches the database for ```ntpjson.monster```:
```
python3 threatfox_search_ioc.py <YOUR-AUTH-KEY> ntpjson.monster
``` 

## Submit an IOC
This script is used to submit IOCs to ThreatFox by calling ThreatFox's [submission endpoint](https://threatfox.abuse.ch/api/#share). Before you submit IOCs to ThreaFox, make sure that you have read our [submission policy](https://threatfox.abuse.ch/api/#policy).

## API documentation

The documentation for the ThreatFox API is available here:

https://threatfox.abuse.ch/api/

# La séquence qui suit est rédigé en anglais par IA
Je me suis dit que ça faisait plus de sens si on restais en anglais mais j'ai pas le vocabulaire pour le faire en peu de temps et aussi bien donc voici :

## Implémentation pour Bitdefender :
par NoaRlnd

# ThreatFox to GravityZone Integration

This project automates the process of fetching Indicators of Compromise (IoCs) from ThreatFox and importing them into Bitdefender GravityZone.

## Project Structure

```
ThreatFox/
├── README.md
├── .env                                    # API keys and configuration
├── requirements.txt                        # Project dependencies
├── threatfox_query_recent-iocs.py         # Fetches IoCs from ThreatFox
├── threatfox_filter_hash.py               # Filters and formats hashes
├── send_to_gravityzone.py                 # Sends formatted IoCs to GravityZone
└── pipeline_ioc_to_gravityzone.py         # Main pipeline orchestrator
```

## Setup

1. Create and activate a virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies:
```powershell
python -m pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
THREATFOX_AUTH_KEY=your_threatfox_key
GZ_API_KEY=your_gravityzone_key
GZ_API_URL=your_gravityzone_url
```

## Usage

### Run the Complete Pipeline

```powershell
python pipeline_ioc_to_gravityzone.py
```

This will:
1. Fetch recent IoCs from ThreatFox
2. Filter for supported hash types (MD5, SHA1, SHA256)
3. Format and send to GravityZone's blocklist

### Individual Scripts

Each component can be run independently:

```powershell
# Fetch IoCs (last 2 days)
python threatfox_query_recent-iocs.py <AUTH-KEY> 2

# Filter hashes only
python threatfox_filter_hash.py

# Send to GravityZone
python send_to_gravityzone.py
```

## Logs

- Pipeline execution logs: `pipeline_log.txt`
- GravityZone API logs: `log.txt`

## Notes

- Rate limits: GravityZone API has strict rate limits (~10 requests/minute)
- Deduplication: The system attempts to avoid duplicate hash submissions
- Supported IoCs: Currently only handles hash-based IoCs (MD5, SHA1, SHA256)

## Future Improvements

- [ ] Add support for additional IoC types (domains, URLs, IPs)
- [ ] Implement proper rate limiting and retry logic
- [ ] Add hash validation and deduplication
- [ ] Improve error handling and logging
- [ ] Add dry-run mode for testing
- [ ] Implement proper testing

// ...existing code...