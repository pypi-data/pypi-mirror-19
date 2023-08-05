# copyright: (c) 2016 by Christopher Auer
# license: MIT, see LICENSE for more details.

import nrepl
import argparse
import sys
import os.path
import os
import urlparse
import socket

def get_code(args):

    if len(args.code) > 0:
        if args.form:
            return str.join(" ", args.code)
        else:
            return "(" + args.code[0] + " " + str.join(" ", map(lambda arg: "\"" + arg + "\"", args.code[1:])) + ")"
    else:
        lines = sys.stdin.readlines()
        return str.join(" ", map(lambda line: line[:-1], lines))

def handle_response(response, args):

    if "status" in response:

        if "done" in response["status"]:
            return False

        # if "eval-error" in response["status"]:
            # sys.stderr.write(response["ex"])
    elif not args.no_output and "out" in response:
        args.output.write(response["out"])


    if not args.no_values and "value" in response:
        args.values.write(response["value"] + '\n')

    return True


def eval_code(args):

    code = get_code(args)

    try:
        connection = nrepl.connect("nrepl://" + args.hostname + ":" + str(args.port))
        connection.write({ "op": "eval", "code": code})

        while True:
            response = connection.read()

            if not handle_response(response, args):
                break

    except socket.error as err:
        sys.exit("Error connecting to nREPL: " + err.message)
    finally:
        connection.close()

def check_port_arg(args):
    if args.port == None:
        if os.path.isfile(".nrepl-port"):
            with open(".nrepl-port", "r") as port_file:
                try:
                    args.port = int(port_file.readline())
                except ValueError:
                    sys.exit("Unable to read port number of .nrepl-port")
        else:
            sys.exit("No port given and .nrepl-port not available. Please specify a port to nREPL.")

def check_os_env(args):
    if "NREPL_URL" in os.environ:
        try:
            url = os.environ["NREPL_URL"]
            parse_result = urlparse.urlparse(url)

            if not parse_result.scheme:
                raise ValueError("not a valid URL")

            netloc_parts = parse_result.netloc.split(":")

            if len(netloc_parts) != 2:
                raise ValueError("netlocation not valid, expected hostname:port")

            args.hostname, args.port = netloc_parts[0], int(netloc_parts[1])
        
        except ValueError as error:
            sys.exit("Could not parse NREPL_URL: " + error.message)

def validate_args(args):
    if not args.form and len(args.code) == 0:
        sys.exit("Can only read code from stdin in combination with --form")

def open_fds(args):
    args.output = sys.stdout if args.output_fd < 0 else os.fdopen(args.output_fd, 'w')
    args.values = sys.stdout if args.values_fd < 0 else os.fdopen(args.values_fd, 'w')

def mk_arg_parser():
    parser = argparse.ArgumentParser(description = "Sends boot commands (or general forms) to an nREPL.",\
            epilog = "The environment variable NREPL_URL=nrepl://hostname:port can also be used to define the connection parameters.\
            The command line arguments (and .nrepl-port) OVERWRITE the data from NREPL_URL!")
    parser.add_argument( '--form', '-f', action='store_true', help="treat command as Clojure/Hy/... form instead of call to boot" )
    parser.add_argument( '--hostname', '-H', action='store', type=str, default="localhost", help="hostname or IP address to connect (default is localhost)")
    parser.add_argument( '--port', '-p', action='store', type=int, default=None, help="port where nREPL is running (if not-given .nrepl-port is used)")
    parser.add_argument( '--no-output', '-o', action='store_true', default=False, help="Don't forward console output (e.g. via (print ...))")
    parser.add_argument( '--output-fd', '-O', action='store', type=int, default=-1, help="File descriptor used for output (defaults to stdout)")
    parser.add_argument( '--no-values', '-v', action='store_true', default=False, help="Don't forward values (e.g. returned by functions)")
    parser.add_argument( '--values-fd', '-V', action='store', type=int, default=-1, help="File descriptor used for values (defaults to stdout)")
    parser.add_argument( 'code', nargs=argparse.REMAINDER, help="code sent to the nREPL. If none is given, stdin is used (only works with --form)" )
    return parser

def main():

    parser = mk_arg_parser()
    args = parser.parse_args(sys.argv[1:])

    check_os_env(args)
    check_port_arg(args)
    validate_args(args)
    open_fds(args)

    eval_code(args)

