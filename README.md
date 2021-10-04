# ENDGAME Python REST API client

## DESCRIPTION:

API allows work with html requests GET, POST, PUT, PATCH, DELETE and visualize the data of the request and response in few formats. 

## PREREQUISITES:

The following programs and add-ons are required for use:

Installed Python 3:
To install in WINDOWS:
```python
https://www.python.org/downloads/windows/ - the official site where you can download.
```
To install in UNIX systems with Tkinter framework:
```python
sudo apt-get install python3 python3-tk
```
To install in macOS:
```python
https://www.python.org/downloads/mac-osx/ - the official site where you can download.
```

YAML extension instalation:
```python
$ pip3 install pyyaml
```
Simplejson module instalation:
```python
$ pip3 install simplejson
```
Requests module instalation:
```python
$ pip3 install requests
```
# Usage:
```python
Program operation through the console:
python3 endgame.py [-g, --gui]

To display a help list.
python3 endgame.py [-h, --help] 

  -h, --help            show this help message and exit
  -m {get,post,put,patch,delete}, --method {get,post,put,patch,delete}
                        Set request method
  --history {show,clear}
                        Show 10 last requests or clear all
  -l {debug,info,warning,error}, --loglevel {debug,info,warning,error}
                        Set logging level
  -e ENDPOINT, --endpoint ENDPOINT
                        Set endpoint of request
  -p param1=value1 [param2=value2 ...], --params param1=value1 [param2=value2 ...]
                        Set params of request
  -hd header1=value1 [header2=value2 ...], --headers header1=value1 [header2=value2 ...]
                        Set headers of request
  -b bodyparam1=value1 [bodyparam2=value2 ...], --body bodyparam1=value1 [bodyparam2=value2 ...]
                        Set body of request
  -a username password, --auth username password
                        Set username and password
  -v {json,yaml}, --view {json,yaml}
                        Set view mode json or yaml

Author: 
Andrey Sheiko  - asheiko@student.ucode.world 



