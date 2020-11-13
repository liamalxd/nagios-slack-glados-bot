#!/usr/bin/python3

import os
import sys
import json
import logging
import random
import requests

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
WEBHOOK_URL = "https://hooks.slack.com/services/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
IMP_NOTIFY_USER = "<@slackuser>"
QUOTES_FILE = "quotes.txt"
NEW_LINE = "\n"
LINE_BREAK = "---------------------------------------------------------------------------------------------------"
SLACK_CRITS = ['UNREACHABLE','CRITICAL','DOWN']
SLACK_WARNS = ['WARNING','UNKNOWN']
SLACK_OKS = ['OK', 'UP']

def random_glados_quote():
    try:
        lines = open(SCRIPT_DIR + "/" + QUOTES_FILE).read().splitlines()

        return random.choice(lines)
    except Exception:
        return ""

def submit_payload(webhook_url, slack_payload):
    try:
        response = requests.post(
            webhook_url, data=json.dumps(slack_payload),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
    except Exception as e:
        logger.info("Failed to submit payload\n %s") % (e)

def main():
    try:
        slack_imp = sys.argv[1]
        try:
            slack_data = sys.argv[2]
        except Exception:
            logging.info("Error: Argument not passed in for text, exiting")
            sys.exit(1)
    except Exception:
        logging.info("Error: Argument not passed in for importance, exiting")
        sys.exit(1)

    if slack_imp in SLACK_OKS:
        slack_payload = {'text': LINE_BREAK + 
        NEW_LINE + NEW_LINE + NEW_LINE + random_glados_quote() +
        NEW_LINE + NEW_LINE + NEW_LINE + slack_data +
        NEW_LINE + NEW_LINE + NEW_LINE + LINE_BREAK}
    elif slack_imp in SLACK_WARNS:
        slack_payload = {'text': LINE_BREAK + 
        NEW_LINE + NEW_LINE + NEW_LINE + random_glados_quote() +
        NEW_LINE + NEW_LINE + NEW_LINE + slack_data +
        NEW_LINE + NEW_LINE + NEW_LINE + LINE_BREAK}
    elif slack_imp in SLACK_CRITS:
        slack_payload = {'text': LINE_BREAK + 
        NEW_LINE + NEW_LINE + NEW_LINE + random_glados_quote() +
        NEW_LINE + NEW_LINE + NEW_LINE + IMP_NOTIFY_USER +
        NEW_LINE + NEW_LINE + NEW_LINE + slack_data}
    else:
        logging.info("argument passed for importance not recognised, exiting...")
        slack_payload = {'text': LINE_BREAK + 
        NEW_LINE + NEW_LINE + NEW_LINE + "Unable to parse arguments passed to script, arguments:" +
        NEW_LINE + NEW_LINE + NEW_LINE + "severity: " + slack_imp +
        NEW_LINE + NEW_LINE + NEW_LINE + "data: " + slack_data}

    submit_payload(WEBHOOK_URL, slack_payload)

if __name__ == "__main__":
    main()
