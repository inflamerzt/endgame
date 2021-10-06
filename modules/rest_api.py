import requests
import re
import modules.history as hist

# from requests import auth
import modules.logger as log


def request(url, **params):
    par = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    if isinstance(url, str) and re.match(par, url):
        try:
            global session
            if "rpar" in params.keys():
                rparams = params["rpar"]
            else:
                rparams = None

            if "headers" in params.keys():
                rheaders = params["headers"]
            else:
                rheaders = None

            if "data" in params.keys():
                rdata = params["data"]
            else:
                rdata = None

            if "auth" in params.keys():
                auth = params["auth"]
                if isinstance(auth, tuple) and len(auth) == 2:
                    rauth = auth
                else:
                    log.err("auth credentials in wrong format")
                    rauth = None
            else:
                rauth = None

            if "method" in params.keys():
                method = params["method"]
                log.inf(f"Using method {method.upper()}")
                if method == "get":
                    response = requests.get(
                        url,
                        auth=rauth,
                        data=rdata,
                        params=rparams,
                        headers=rheaders,
                        timeout=5,
                    )
                elif method == "post":
                    response = requests.post(
                        url,
                        auth=rauth,
                        data=rdata,
                        params=rparams,
                        headers=rheaders,
                        timeout=5,
                    )
                elif method == "put":
                    response = requests.put(
                        url,
                        auth=rauth,
                        data=rdata,
                        params=rparams,
                        headers=rheaders,
                        timeout=5,
                    )
                elif method == "patch":
                    response = requests.patch(
                        url,
                        auth=rauth,
                        data=rdata,
                        params=rparams,
                        headers=rheaders,
                        timeout=5,
                    )
                elif method == "delete":
                    response = requests.delete(
                        url,
                        auth=rauth,
                        data=rdata,
                        params=rparams,
                        headers=rheaders,
                        timeout=5,
                    )
                else:
                    log.err("Method is unknown!!!")

                    return {"status": "Wrong HTTP method"}
                rtime = round(response.elapsed.total_seconds(), 2)
            else:
                log.err("No method is defined")

                return {"status": "No method is defined"}
            response.raise_for_status()
            # Code here will only run if the request is successful
            log.inf(f"{response.status_code} {method.upper()} {url}")
            hist.h_save(
                method=method.upper(),
                url=url,
                params=str(rparams),
                rbody=str(rdata),
                status=response.status_code,
                response=response.text,
            )
            return {
                "status": response.status_code,
                "rtime": rtime,
                "text": response.text,
                "headers": response.headers,
            }

        except requests.exceptions.HTTPError as errh:
            log.err(f"{response.status_code} {method.upper()} {url}")
            hist.h_save(
                method=method.upper(),
                url=url,
                params=rparams,
                rbody=rdata,
                status=response.status_code,
            )
            rtime = round(response.elapsed.total_seconds(), 2)
            return {"status": response.status_code, "rtime": rtime}
        except requests.exceptions.ConnectionError as errc:
            log.err(f"ConnectionEroor:{errc}")
            return {"status": "Connection error"}
        except requests.exceptions.Timeout as errt:
            log.err(f"Timeout:{errt}")
            return {"status": "Timeout"}
        except requests.exceptions.RequestException as err:
            log.err(f"RequestException:{err}")
            return {"status": "request exception"}

    else:
        return {"status": "url format is invalid"}
