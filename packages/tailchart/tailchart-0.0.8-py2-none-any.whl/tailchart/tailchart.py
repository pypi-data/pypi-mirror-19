#!/usr/bin/env python
#coding: gbk

import SimpleHTTPServer
import SocketServer
import threading, thread
import sys, re
import urlparse
import collections
import json
import argparse


data = collections.OrderedDict()
mutex = threading.Lock()

def readData(args):
    split_re = re.compile(r"[\w]+")
    start = 1
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        mutex.acquire()
        data[start] = [int(x) for x in re.findall(split_re, line)]
        if args.scatter and len(data[start]) != 2:
            print("only 2 dimension data is allowed in scatter mode!")
            sys.exit(0)
        if len(data[start]) != len(args.series):
            print("malformed data", data[start])
            sys.exit(0)

        if args.debug:
            print " ".join(str(x) for x in data[start])

        start += 1
        mutex.release()

get_re = re.compile("/get(\?(.+))?")

class MyServer(SocketServer.TCPServer):
    allow_reuse_address = True

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        elif get_re.match(self.path):
            ret = urlparse.urlparse(self.path)
            query = urlparse.parse_qs(ret.query)
            ts = int(query["ts"][0])
            self.sendHeader()
            mutex.acquire()
            lts = len(data.keys())
            d = {"data": [data[k] for k in data.keys() if k > ts], "ts": lts}
            mutex.release()
            self.wfile.write(json.dumps(d))
            return
        elif self.path == "/init":
            self.sendHeader()
            self.wfile.write(self.args.json_config)
            return
        else:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        pass

    def sendHeader(self):
        self.protocol_version = "HTTP/1.1"
        self.send_response(200, "OK")
        self.send_header('Content-Type', "application/json")
        self.end_headers()


def run():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--scatter", action="store_true", help="use catter chart")
    arg_parser.add_argument("--debug", action="store_true", help="print debug msg")
    arg_parser.add_argument("--series", type=str, help="series info, seperate by comma", default="")
    arg_parser.add_argument("--port", type=int, help="listen http port", default=8080)
    args = arg_parser.parse_args()
    args.series = args.series.split(",")

    if args.scatter:
        mode = "scatter"
    else:
        mode = "line"

    args.json_config = json.dumps({"mode": mode, "series": args.series})

    if args.debug:
        print "config: ", args.json_config

    print "Series[%s] Mode[%s]"%(args.series, mode)
    print "Server Listening on : 0.0.0.0:%d"%(args.port, )

    thread.start_new_thread(readData, (args, ))

    Handler = MyRequestHandler
    Handler.args = args
    httpd = MyServer(("", args.port), Handler)
    httpd.serve_forever()
if __name__ == "main":
    run()
