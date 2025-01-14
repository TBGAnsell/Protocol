#!/usr/bin/env python3

import os
import ast

"""
Basic function for establishing paths of simulation data.
"""

def setup(protocol_path, save_dir=None):
    """
    Establish save directory for simulations and data.

    Params:
    -------
    protocol_path: str
        path to LipIDens
    save_dir: str
        input custom directory name to store data
    
    Returns:
    --------
    path: str
        path to location of LipIDens generated data
    """
    if save_dir is None:
        path=os.getcwd()
    else:
        if os.path.isabs(save_dir)==True:
            path=save_dir
        else:
            path=os.path.join(os.getcwd(), save_dir)

    print("Location of data:", path)
    return path

def run_type():
    """
    Choose protocol stage to inititate.

    Returns:
    --------
    input_step: str
        selected stage number of protocol
    """
    steps_d={"1a": "Setup coarse-grained simulations",
             "1b": "Process coarse-grained trajectories",
             "2": "Test PyLipID cut-off values",
             "3": "Run PyLipID analysis",
             "4": "Screen PyLipID data",
             "5": "Rank site lipids",
             "6": "Setup atomistic simulations"}
    print("\nInitialising LipIDens protocol\nProtocol steps:")
    print(*[f"\n{key}: {val}" for key, val in steps_d.items()])
    try:
        input_step=str(input("\nSelect protocol stage number:"))
        if input_step in steps_d:
            print("\nSelected:"+steps_d[input_step])
        else:
            print("Invalid: enter number of required protocol stage")
            exit()
    except Exception as e:
        print(e)
        exit()
    return input_step

def param_check(input_dict, step_str):
    """
    Take a dictionary of default values and loop through changing values based on user input.
    dict={ID number: [variable, value, description, type]}

    Params:
    -------
    input_dict: dict
        parameters to change and/or confirm
    step_str: str
        description of step
    
    Returns:
    --------
    input_dict: dict
        modfied parameters
    """
    print(f"\nDefault variables for {step_str}")
    print(*[f"\n{key}: {val[2]}\n\t{val[0]}: {val[1]}\n" for key, val in input_dict.items()])
    try:
        response=str(input("\nDo you wish to change the default values? (y/n): "))
        if response=="y":
            id_list=list(input("\nList variables you wish to change e.g. '1 2 4': " ).split())
            for id in id_list:
                remove_char=["[", "]", ","]
                if input_dict[id][3] == "str":
                    var=str(input("Change {} to: ".format(input_dict[id][0])))
                elif input_dict[id][3] == "int":
                    var=int(input("Change {} to: ".format(input_dict[id][0])))
                elif input_dict[id][3] == "float":
                    var=float(input("Change {} to: ".format(input_dict[id][0])))
                elif input_dict[id][3] == "list_str":
                    var=input("Change {} to: ".format(input_dict[id][0]))
                    for rc in remove_char:
                        var=var.replace(rc,"")
                    var=list(var.split())
                elif input_dict[id][3] == "list_float":
                    var=input("Change {} to: ".format(input_dict[id][0]))
                    for rc in remove_char:
                        var=var.replace(rc, "")
                    var=list(var.split())
                    var=[float(v) for v in var]
                elif input_dict[id][3] =="bool":
                    var=input("Change {} to: ".format(input_dict[id][0]))
                    while var != "True" or "False":
                        var=input("Must enter 'True' or 'False': ")
                    if var=="True":
                        var=bool(1)
                    elif var=="False":
                        var=bool(0)
                elif input_dict[id][3] =="dict":
                    var=input("Change {} to: ".format(input_dict[id][0]))
                    var=ast.literal_eval(var)
                input_dict[id][1]=var
            print("Variables set")
            print(*[f"\n\t{val[0]}: {val[1]}" for key, val in input_dict.items()])
        elif response=="n":
            input_dict=input_dict
            print("Variables set")
            print(*[f"\n\t{val[0]}: {val[1]}" for key, val in input_dict.items()])
        else:
            print("INVALID: Must enter y/n")
            exit()
    except Exception as e:
        print(e)
        exit()
    return input_dict
