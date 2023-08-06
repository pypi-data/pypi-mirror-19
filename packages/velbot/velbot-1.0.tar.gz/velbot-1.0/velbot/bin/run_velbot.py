#!/usr/bin/env python
from argparse import ArgumentParser
from flask import Flask, request, Response
from velbot import VelBot
import sys
import os
import time
import yaml
import socket
from threading import Thread

sys.path.append(os.getcwd())
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

app = Flask(__name__)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()

def run():
    app.run(host=socket.gethostname()+'.verizon.com',debug=True,use_reloader=False)

@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        bot.process_input(request.form)
    return Response(), 200

def main(args=None):
    global bot
    # load args with config path if not specified
    if not args:
        args = parse_args()

    config = yaml.load(open(args.config or 'velbot.conf', 'r'))
    bot = VelBot(config)
    bot.start()
    try:
        job_thread = Thread(target = bot.process_jobs,)
        job_thread.daemon = True
        job_thread.start()
        run()

    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == "__main__":
    main()
