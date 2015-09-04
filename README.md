# slack-dm-export

Exports slack direct messages, private groups, and general channels to json.

## Usage

Insert API key to yours and change dates you want to get message history within.

You can get API key on the [Slack website](https://api.slack.com/web).

Install the slacker library: `pip install slacker`.

## Syntax

`python3 im.py [-h] [-t SLACK_TOKEN] [-d] [-g] [-c] [-s START_DATE] [-e END_DATE] [-o DESTINATION]`

```
required arguments:
  -t, --token           Your slack web api token

optional arguments:
  -h, --help            Show this help message and exit
  -d, --direct          Export direct messages
  -g, --groups          Export private groups
  -c, --channels        Export channels (default: only #general)
  -s START_DATE, --start START_DATE
                        Start date (format: YYYY.MM.DD)
  -e END_DATE, --end END_DATE
                        End date (format: YYYY.MM.DD)
  -o OUTPUT, --output OUTPUT
                        Output folder for the json files (default: ./export)
```

## Example

`python im.py -t xxxx -d -g --start 2015.04.26 --end 2015.05.13`
