import tkinter
import tkinter.messagebox
from tkinter.constants import DISABLED, NORMAL, NSEW
import yaml
import simplejson as json
import pprint
import modules.history as hist

from modules.data_checker import check

import modules.logger as log
from modules.rest_api import request as rapi
from http import HTTPStatus

from modules.wm import view


def rungui():
    import tkinter as tk
    import tkinter.ttk as ttk

    pr = list()
    bd = list()
    hd = list()

    lasttext = ""
    viewer = None

    log.dbg("creating a main windows")

    # json.loads()

    def build_viewer(type):
        global viewer
        if type:
            viewer = ttk.Treeview(tab1)
        else:
            viewer = tk.Text(tab1, wrap=tk.WORD, state=DISABLED)
        viewer.rowconfigure(0, weight=1)
        viewer.columnconfigure(0, weight=1)
        viewer.grid(column=1, row=0, sticky="nesw")

        # add a scrollbar
        scrollbar = ttk.Scrollbar(
            tab1, orient=tk.VERTICAL, command=viewer.yview)
        viewer.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky="ns")

    def viewdata():
        global lasttext
        global viewer
        vmode = rvmodevar.get()

        viewer.destroy()

        if vmode == 3:

            build_viewer(True)
            # raw json yaml tree/table
            try:
                data = yaml.safe_load(lasttext)
                view(data, check(data), "name", viewer)
            except:
                tkinter.messagebox.showerror('Treeview error',
                                             'Unable create tree with recieved data!')
            data = ""

        else:
            build_viewer(False)
            # textmode
            viewer.config(state=NORMAL)
            viewer.delete("1.0", tk.END)

            if vmode == 0:
                # raw
                vdata = pprint.pformat(lasttext, sort_dicts=False)
            elif vmode == 1:
                # json
                try:
                    vdata = pprint.pformat(
                        json.loads(lasttext), sort_dicts=False)
                except:
                    tkinter.messagebox.showerror('json error',
                                                 'Unable to parse this data with json!')
                    vdata = ""
            elif vmode == 2:
                # yaml
                try:
                    vdata = pprint.pformat(
                        yaml.safe_load(lasttext), sort_dicts=False)
                except:
                    tkinter.messagebox.showerror('Yaml error',
                                                 'Unable to parse this data with YAML!')
                    vdata = ""
            viewer.insert("1.0", vdata)
            viewer.config(state=DISABLED)

    def show_history():
        history = hist.h_load()
        for child in hviewer.get_children():
            hviewer.delete(child)

        for item in history:
            hviewer.insert("", "end", values=item)
        pass

    def clear_history():
        for child in hviewer.get_children():
            hviewer.delete(child)
            hist.h_clear()

    def item_selected(event):
        global lasttext
        for selected_item in hviewer.selection():
            # dictionary
            item = hviewer.item(selected_item)
            # list
            record = item["values"]
            lasttext = record[7]
            viewdata()
            # TODO: Fill other fields from history
            tabControl.select(tab1)
        """
        newWindow = tk.Toplevel(root)
        newWindow.title("Data view:")
        newWindow.geometry("600x200")
        tk.Label(newWindow, text=f"#:{record[0]}", bg="white").pack(anchor='w',
                                                                    fill='x')
        tk.Label(newWindow, text=f"Method:{record[1]}",
                 bg="lightgray").pack(anchor='w', fill='x')
        tk.Label(newWindow, text=f"URL:{record[2]}",
                 bg="white").pack(anchor='w', fill='x')
        tk.Label(newWindow, text=f"Params:{record[3]}",
                 bg="lightgray").pack(anchor='w', fill='x')
        tk.Label(newWindow, text=f"Request Body:{record[4]}",
                 bg="white").pack(anchor='w', fill='x')
        tk.Label(newWindow, text=f"Status:{record[5]}",
                 bg="lightgray").pack(anchor='w', fill='x')
        """

    def setloglevel(level):
        log.loglevel(level)

    def get_data():
        global lasttext
        if pr:
            dparam = dict()
            for item in pr:
                dparam[item[0].get()] = item[1].get()
        else:
            dparam = None

        if bd:
            dbody = dict()
            for item in bd:
                dbody[item[0].get()] = item[1].get()
        else:
            dbody = None

        if hd:
            dheaders = dict()
            for item in hd:
                dheaders[item[0].get()] = item[1].get()
                dheaders = dheaders
        else:
            dheaders = None

        if username.get():
            if password.get:
                authpar = (username.get(), password.get())
            else:
                authpar = None
        else:
            authpar = None

        data = rapi(
            url.get(),
            method=msel.get(),
            auth=authpar,
            rpar=dparam,
            headers=dheaders,
            data=dbody,
        )
        if isinstance(data["status"], int):
            # http response
            if data["status"] == 200:
                status_bar.configure(
                    text=f"Got response {data['status']} {HTTPStatus(data['status']).phrase} in {data['rtime']} seconds",
                    background="green",
                )
                lasttext = data["text"]
                viewdata()

                # viewer.heading('#0', text="RAW data")
                # viewer.insert('', 0, text=json.dumps(data['text'], indent=3))
            else:
                status_bar.configure(
                    text=f"Got response {data['status']} {HTTPStatus(data['status']).phrase} in {data['rtime']} seconds",
                    background="yellow",
                )
        else:
            # non http Response
            status_bar.configure(
                text=f"Error: {data['status']}", background="RED")

    def elemenpm(action, src, lst):
        if action:
            # add element
            row = len(lst) + 1
            ename = tk.Entry(src)
            ename.grid(column=0, row=row)
            evalue = tk.Entry(src)
            evalue.grid(column=1, row=row)
            lst.append([ename, evalue])
        else:
            # remove element
            if len(lst):
                lst[-1][0].destroy()
                lst[-1][1].destroy()
                del lst[-1]

    root = tk.Tk()
    root.title("Tab Widget")
    root.geometry("800x600")
    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab1.columnconfigure(0, weight=0)
    tab1.columnconfigure(1, weight=1)
    tab1.rowconfigure(0, weight=1)
    tab2.columnconfigure(0, weight=1)
    tab2.rowconfigure(0, weight=0)
    tab2.rowconfigure(1, weight=1)

    tabControl.add(tab1, text="Requests")
    tabControl.add(tab2, text="History")

    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    tabControl.grid(column=0, row=0, sticky=NSEW)

    build_viewer(True)

    status_bar = ttk.Label(root, text="", background="gray")
    status_bar.rowconfigure(1, weight=1)
    status_bar.columnconfigure(0, weight=1)
    status_bar.grid(column=0, columnspan=2, row=1, sticky="swe")

    reqgroup = ttk.LabelFrame(tab1, text="Request settings")
    # reqgroup.pack(expand=YES, fill=X, anchor=NE)
    reqgroup.grid(column=0, row=0, sticky=NSEW)
    reqgroup.columnconfigure(0, weight=1)
    reqgroup.rowconfigure((0, 1, 2, 3, 4), weight=0)

    reqshape = ttk.LabelFrame(reqgroup, text="Shape your request")
    # reqparam.pack(expand=YES, fill=X, anchor=NE)
    reqshape.grid(column=0, row=0, sticky="we")
    reqshape.columnconfigure((1, 2), weight=10)
    reqshape.columnconfigure(0, weight=1)

    msel = ttk.Combobox(
        reqshape, values=["get", "post", "put", "patch", "delete"], width=5
    )
    msel.grid(row=0, column=0, pady=3, padx=3)
    msel.current(0)

    url = tk.Entry(reqshape)
    url.grid(row=0, column=1, sticky="ew")
    send_button = tk.Button(reqshape, text="Send request",
                            command=lambda: get_data())
    send_button.grid(row=0, column=2)

    reqparam = ttk.LabelFrame(reqgroup, text="basic auth")
    reqparam.grid(column=0, row=1, sticky="nwe")

    username = tk.Entry(reqparam)
    username.grid(column=0, row=0)
    password = tk.Entry(reqparam, show="*")
    password.grid(column=1, row=0)

    params = ttk.LabelFrame(reqgroup, text="Params")
    params.grid(column=0, row=2, sticky="nwe")
    # params.columnconfigure(0, weight=0)

    pcontrol = tk.Frame(params)
    pcontrol.grid(columnspan=2, row=0, sticky="ew")
    paramp = tk.Button(
        pcontrol, text="+", command=lambda: elemenpm(True, params, pr)
    ).grid(column=0, row=0)
    paramm = tk.Button(
        pcontrol, text="-", command=lambda: elemenpm(False, params, pr)
    ).grid(column=1, row=0)

    # param1 = tk.Entry(params).grid(column=0, row=1)
    # param2 = tk.Entry(params).grid(column=1, row=1)

    body = ttk.LabelFrame(reqgroup, text="Body")
    body.grid(column=0, row=3, sticky="nwe")

    bcontrol = tk.Frame(body)
    bcontrol.grid(columnspan=2, row=0, sticky="ew")
    paramp = tk.Button(
        bcontrol, text="+", command=lambda: elemenpm(True, body, bd)
    ).grid(column=0, row=0)
    paramm = tk.Button(
        bcontrol, text="-", command=lambda: elemenpm(False, body, bd)
    ).grid(column=1, row=0)

    # body1 = tk.Entry(body).grid(column=0, row=1)
    # body2 = tk.Entry(body).grid(column=1, row=1)

    headers = ttk.LabelFrame(reqgroup, text="Headers")
    headers.grid(column=0, row=4, sticky="nwe")

    hcontrol = tk.Frame(headers)
    hcontrol.grid(columnspan=2, row=0, sticky="ew")
    paramp = tk.Button(
        hcontrol, text="+", command=lambda: elemenpm(True, headers, hd)
    ).grid(column=0, row=0)
    paramm = tk.Button(
        hcontrol, text="-", command=lambda: elemenpm(False, headers, hd)
    ).grid(column=1, row=0)

    # headers1 = tk.Entry(headers)
    # headers1.grid(column=0, row=1)
    # headers2 = tk.Entry(headers)
    # headers2.grid(column=1, row=1)

    loglvl = ttk.LabelFrame(reqgroup, text="loglevel")
    loglvl.grid(column=0, row=5, sticky="nwe")

    loglvlvar = tk.IntVar()
    loglvlvar.set(0)

    loglvl1 = tk.Radiobutton(
        loglvl,
        text="Debug",
        variable=loglvlvar,
        value=0,
        bg="blue",
        command=lambda: setloglevel("DEBUG"),
    ).grid(column=0, row=0)
    loglvl2 = tk.Radiobutton(
        loglvl,
        text="Info",
        variable=loglvlvar,
        value=1,
        bg="green",
        command=lambda: setloglevel("INFO"),
    ).grid(column=1, row=0)
    loglvl3 = tk.Radiobutton(
        loglvl,
        text="Warning",
        variable=loglvlvar,
        value=2,
        bg="yellow",
        command=lambda: setloglevel("WARNING"),
    ).grid(column=2, row=0)

    loglvl4 = tk.Radiobutton(
        loglvl,
        text="Error",
        variable=loglvlvar,
        value=3,
        bg="red",
        command=lambda: setloglevel("ERROR"),
    ).grid(column=3, row=0)

    rvmode = ttk.LabelFrame(reqgroup, text="Response view")
    rvmode.grid(column=0, row=6, sticky="nwe")

    rvmodevar = tk.IntVar()
    rvmodevar.set(0)

    rvmode1 = tk.Radiobutton(
        rvmode, text="RAW", variable=rvmodevar, value=0, command=lambda: viewdata()
    ).grid(column=0, row=0)
    rvmode2 = tk.Radiobutton(
        rvmode,
        text="Pretty JSON",
        variable=rvmodevar,
        value=1,
        command=lambda: viewdata(),
    ).grid(column=1, row=0)
    rvmode3 = tk.Radiobutton(
        rvmode, text="YAML", variable=rvmodevar, value=2, command=lambda: viewdata()
    ).grid(column=2, row=0)
    rvmode4 = tk.Radiobutton(
        rvmode,
        text="Treeview/Table",
        variable=rvmodevar,
        value=3,
        command=lambda: viewdata(),
    ).grid(column=3, row=0)

    histoperations = ttk.LabelFrame(tab2, text="History operations")
    # reqgroup.pack(expand=YES, fill=X, anchor=NE)
    histoperations.grid(column=0, row=0, sticky="NW")
    histoperations.columnconfigure(0, weight=0)
    histoperations.rowconfigure(0, weight=0)

    histshow = tk.Button(
        histoperations, text="Show", command=lambda: show_history()
    ).grid(column=0, row=0, sticky="w")
    histclear = tk.Button(
        histoperations, text="Clear", command=lambda: clear_history()
    ).grid(column=1, row=0, sticky="w")

    columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8")

    hviewer = ttk.Treeview(tab2, show="headings", columns=columns)
    hviewer.rowconfigure(0, weight=1)
    hviewer.columnconfigure(0, weight=1)
    hviewer.grid(column=0, row=1, sticky="nesw")

    hviewer.heading("#1", text="#")
    hviewer.column("#1", width=40, anchor="e")
    hviewer.heading("#2", text="Method")
    hviewer.column("#2", width=50, anchor="center")
    hviewer.heading("#3", text="URL")
    hviewer.column("#3", anchor="w")
    hviewer.heading("#4", text="Params")
    hviewer.column("#4", anchor="w")
    hviewer.heading("#5", text="request body")
    hviewer.column("#5", anchor="w")
    hviewer.heading("#6", text="headers")
    hviewer.column("#6", anchor="w")
    hviewer.heading("#7", text="Status")
    hviewer.column("#7", anchor="w", width=40)
    hviewer.heading("#8", text="")
    hviewer.column("#8", width=0, stretch="false")

    hviewer.bind("<<TreeviewSelect>>", item_selected)

    # add a scrollbars
    hscrollbar = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=hviewer.yview)
    hviewer.configure(yscroll=hscrollbar.set)
    hscrollbar.grid(row=1, column=1, sticky="ens")

    vscrollbar = ttk.Scrollbar(
        tab2, orient=tk.HORIZONTAL, command=hviewer.xview)
    hviewer.configure(xscroll=vscrollbar.set)
    vscrollbar.grid(row=2, column=0, sticky="wes")

    root.mainloop()
