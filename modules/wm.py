import tkinter as tk
from tkinter.constants import NO
from modules.type_checker import *

line_id = 0
parent_id = {0: ""}


def tree_add_line(obj, dest, level=0, name=""):
    global line_id
    global parent_id
    if isinstance(obj, dict):
        if line_id == 0:
            dest.insert(
                parent=parent_id[level],
                index="end",
                iid=line_id,
                text=str(f"{{{len(obj)}}}"),
            )
            level += 1
            parent_id[level] = line_id
            line_id += 1
        for key, value in obj.items():
            if isinstance(value, dict):
                parent_id[level + 1] = line_id
                dest.insert(
                    parent=parent_id[level],
                    index="end",
                    iid=line_id,
                    text=str(f"{key} {{{len(value)}}}"),
                )
                line_id += 1
                tree_add_line(value, dest, level + 1)
            elif isinstance(value, list):
                tree_add_line(value, dest, level, key)
            else:
                if isinstance(value, str):
                    pval = f'"{value}"'
                else:
                    pval = value
                dest.insert(
                    parent=parent_id[level],
                    index="end",
                    iid=line_id,
                    text=str(f"{key}: {pval}"),
                )
                line_id += 1
    elif isinstance(obj, list):
        parent_id[level + 1] = line_id
        dest.insert(
            parent=parent_id[level],
            index="end",
            iid=line_id,
            text=str(f"{name} [{len(obj)}]"),
        )
        line_id += 1
        for item in obj:
            tree_add_line(item, dest, level + 1)
    else:
        dest.insert(
            parent=parent_id[level], index="end", iid=line_id, text=str(f"{obj}")
        )
        line_id += 1
        level -= 1
    return


def visualize_scalar_list(tree, lst):
    tree["columns"] = [0, 1]
    tree.heading(0, text="")
    tree.heading(1, text="value")
    for index, value in enumerate(lst):
        tree.insert(
            "",
            tk.END,
            values=(index, f'"{value}"' if isinstance(value, str) else str(value)),
        )
    return


def visualize_scalar_dict(tree, vwdata):
    tree["columns"] = [0, 1]
    tree.heading(0, text="")
    tree.heading(1, text="value")
    for key, value in vwdata.items():
        tree.insert(
            "",
            tk.END,
            values=(key, f'"{value}"' if isinstance(value, str) else str(value)),
        )
    return


def visualize_list_scalar_dicts(tree, vwdata):
    if not vwdata:
        return
    # walk through all dicts to collect keys
    all_keys = list(d.keys() for d in vwdata)
    # need to keep order
    unique_keys = list(dict.fromkeys([x for l in all_keys for x in l]))
    tree["columns"] = list(range(len(unique_keys) + 1))
    for index in list(range(len(unique_keys) + 1)):
        tree.column(index, minwidth=0, width=100, stretch=tk.NO)

    tree.heading(0, text="")
    for index in range(1, len(unique_keys) + 1):
        tree.heading(index, text=unique_keys[index - 1])

    for index, d in enumerate(vwdata):
        tree.insert(
            "",
            tk.END,
            values=[str(index)]
            + [
                f'"{d.get(key)}"'
                if isinstance(d.get(key), str)
                else str(d.get(key, ""))
                for key in unique_keys
            ],
        )
    return


def visualize_dict_of_scalar_dicts(tree, vwdata):
    # walk through all dicts to collect keys
    all_keys = list(d.keys() for d in vwdata.values())
    # need to keep order
    unique_keys = list(dict.fromkeys([x for l in all_keys for x in l]))
    tree["columns"] = list(range(len(unique_keys) + 1))

    tree.heading(0, text="")
    for index, header in enumerate(unique_keys):
        tree.heading(index + 1, text=header)

    for key, value in vwdata.items():
        text = []
        if is_scalar(value):
            text = [value]
        elif isinstance(value, dict):
            text = [value.get(k, "") for k in unique_keys]
        tree.insert("", tk.END, values=[key] + text)
    return


def view(vwdata, mode, name, tkroot):
    global line_id
    global parent_id

    tree = tkroot

    if mode == "tree":

        tree.heading("#0")
        line_id = 0
        parent_id = {0: ""}
        tree_add_line(vwdata, tree)
        tree.item("0", open=True)

    else:
        tree.column("#0", stretch=NO, width=0)
        if mode == "dosd":
            visualize_dict_of_scalar_dicts(tree, vwdata)
        elif mode == "los":
            visualize_scalar_list(tree, vwdata)
        elif mode == "sd":
            visualize_scalar_dict(tree, vwdata)
        elif mode == "losd":
            visualize_list_scalar_dicts(tree, vwdata)

    return
