import argparse
import yaml
import sys
import simplejson as json
from http import HTTPStatus

from yaml.error import YAMLError
from modules import history
import modules.logger as log
from modules.rest_api import request as rapi
from modules.gui import rungui

# log.dbg("test")

lasttext = " "

# INFO: main entry
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="endgame.py")
    parser.add_argument("-g",
                        "--gui",
                        action="store_true",
                        help="Activate GUI mode")
    parser.add_argument(
        "-m",
        "--method",
        choices=["get", "post", "put", "patch", "delete"],
        help="Set request method",
    )
    parser.add_argument(
        "--history",
        choices=["show", "clear"],
        help="Show 10 last requests or clear all",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        choices=["debug", "info", "warning", "error"],
        help="Set logging level",
    )
    parser.add_argument("-e",
                        "--endpoint",
                        type=str,
                        help="Set endpoint of request")
    parser.add_argument(
        "-p",
        "--params",
        nargs="+",
        type=str,
        metavar=("param1=value1", "param2=value2"),
        help="Set params of request",
    )
    parser.add_argument(
        "-hd",
        "--headers",
        nargs="+",
        type=str,
        metavar=("header1=value1", "header2=value2"),
        help="Set headers of request",
    )
    parser.add_argument(
        "-b",
        "--body",
        nargs="+",
        type=str,
        metavar=("bodyparam1=value1", "bodyparam2=value2"),
        help="Set body of request",
    )
    parser.add_argument(
        "-a",
        "--auth",
        metavar=("username", "password"),
        nargs=2,
        type=str,
        help="Set username and password",
    )
    parser.add_argument("-v",
                        "--view",
                        choices=["json", "yaml"],
                        help="Set view mode json or yaml")
    arguments = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        exit()

    log.init()
    log.loglevel("DEBUG")
    log.inf("=== Main process started ===")
    llvl = arguments.loglevel
    if llvl in ["debug", "info", "warning", "error"]:
        log.inf(f"Debug level is set to {llvl.upper()} mode.")
        log.loglevel(llvl.upper())
    else:
        log.inf("loglevel is not selected, setting to DEBUG.")
        log.loglevel("DEBUG")

    history.h_init()
    """
    prtdata = history.h_load()[0]
    prtdata = list(prtdata)
    prtdata[5] = prtdata[5][:30]
    prtdata = tuple(prtdata)
    print(prtdata)
    """
    if arguments.gui:
        log.inf("entering gui mode...")
        rungui()
        pass
    else:
        if arguments.history:
            log.dbg("History mode")
            # history mode
            if arguments.history == "clear":
                history.h_clear()

            else:
                # show history
                histitems = history.h_load()
                command = 0
                while True:
                    # infinite loop
                    print(
                        f"There is {len(histitems)} in history, last 10 is displayed:"
                    )
                    lastten = histitems[-9:]
                    items = dict()
                    if not int(command):
                        print("{:<4} {:<8} {:<25} {:<25} {:<25} {:<25} {:<8}".
                              format(
                                  "..",
                                  "Method",
                                  "URL",
                                  "Params",
                                  "Request body",
                                  "Request headers",
                                  "status",
                              ))

                        for item in lastten:
                            i = list(item)
                            for num in range(0, len(i)):
                                if not i[num]:
                                    i[num] = ""
                                elif isinstance(i[num], str):
                                    i[num] = i[num][:25]

                            items[i[0]] = i[1:]
                            print(
                                "{:<4} {:<8} {:<25} {:<25} {:<25} {:<25} {:<8}"
                                .format(i[0], i[1], i[2], i[3], i[4], i[5],
                                        i[6]))

                    command = input(
                        'Enter request index to view full info, "0" to list index , or "q" to quit:'
                    )
                    if command == "q":
                        break
                    elif int(command) <= len(lastten) and int(command) > 0:
                        c = int(command)

                        print(f"---Request {command}---")
                        print("{:<20} {:<100}".format("Method:", items[c][0]))
                        print("{:<20} {:<100}".format("URL:", items[c][1]))
                        print("{:<20} {:<100}".format("Params:", items[c][2]))
                        print("{:<20} {:<100}".format("Request body:",
                                                      items[c][3]))
                        print("{:<20} {:<100}".format("Request headers:",
                                                      items[c][4]))
                        print("{:<20} {:<100}".format("Status:", items[c][5]))
                        print("=" * 100)
                        print("---Response--")
                        print(items[c][5])
                        print("---Response body--")

                    else:
                        print("!!!Wrong input!!!")

        else:
            # tuple(arguments.auth)
            log.inf("entering console mode...")
            if not arguments.endpoint:
                parser.error(
                    "argument -e/--endpoint is required in console mode.")
            if not arguments.method:
                parser.error(
                    "argument -m/--method is required in console mode.")
            if arguments.auth:
                auth = tuple(arguments.auth)
            else:
                auth = None

            if arguments.headers:
                headers = dict()
                for header in arguments.headers:
                    hsplit = header.split("=")
                    headers[hsplit[0]] = header[len(hsplit[0]) + 1:]
            else:
                headers = None

            if arguments.params:
                params = dict()
                for param in arguments.params:
                    psplit = param.split("=")
                    params[psplit[0]] = param[len(psplit[0]) + 1:]
            else:
                params = None

            if arguments.body:
                bodys = dict()
                for body in arguments.body:
                    bsplit = body.split("=")
                    bodys[bsplit[0]] = body[len(bsplit[0]) + 1:]
            else:
                bodys = None

            result = rapi(
                arguments.endpoint,
                method=arguments.method,
                headers=headers,
                data=bodys,
                rpar=params,
                auth=auth,
            )
            status = result["status"]
            if isinstance(status, int):
                # http request
                print(
                    f"---Got response {result['status']} {HTTPStatus(result['status']).phrase} in {result['rtime']} seconds--"
                )
                if result["status"] == 200:
                    pdata = None
                    if arguments.view == "json":
                        try:
                            pdata = json.dumps(json.loads(result["text"]),
                                               indent=3)
                        except:
                            print(
                                "!!!Recieved data is not possible to parse with json!!!"
                            )
                    elif arguments.view == "yaml":
                        try:
                            pdata = yaml.dump(yaml.safe_load(result["text"]))
                        except yaml.YAMLError:
                            print(
                                "!!!Recieved data is not possible to parse with yaml!!!"
                            )
                    else:
                        print("---Response body---")
                        print(result["text"])
                        pass
                    if pdata:
                        print("---Response body---")
                        print(pdata)
            else:
                print(f"Error:{result['status']}")
            # print(result)

    log.loglevel("INFO")
    log.inf("=== Main process stopped ===")
