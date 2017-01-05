# Copyright (C) 2016 Siavoosh Payandeh Azad

import sys

from CB_FC_Package import CreditBasedPackage
from CB_compoments import declare_components
from Signal_declaration import declare_signals
from ACII_art import generate_ascii_art
from Instantiate_components import  instantiate_routers, instantiate_lv_routers
from network_entity import generate_entity


CB_Package = CreditBasedPackage()
if CB_Package.sort_out_parameters(sys.argv[1:]):
    sys.exit()
CB_Package.parameters_sanity_check()
file_path = CB_Package.generate_file_name(sys.argv[1:])

noc_file = open(file_path, 'w')


noc_file.write("--Copyright (C) 2016 Siavoosh Payandeh Azad\n")
noc_file.write("------------------------------------------------------------\n")
noc_file.write("-- This file is automatically generated!\n")
noc_file.write("-- Here are the parameters:\n")
noc_file.write("-- \t network size x: "+str(CB_Package.network_dime)+"\n")
noc_file.write("-- \t network size y: "+str(CB_Package.network_dime)+"\n")
noc_file.write("-- \t LV network: "+str(CB_Package.add_LV)+"\n")
noc_file.write("-- \t Data width: "+str(CB_Package.data_width)+"\n")
noc_file.write("-- \t Parity: "+str(CB_Package.add_parity)+"\n")
noc_file.write("-- \t Fault injectors: "+str(CB_Package.add_FI)+"\n")
noc_file.write("------------------------------------------------------------\n\n")

noc_file.write("library ieee;\n")
noc_file.write("use ieee.std_logic_1164.all;\n")
noc_file.write("use IEEE.STD_LOGIC_ARITH.ALL;\n")
noc_file.write("use IEEE.STD_LOGIC_UNSIGNED.ALL;\n")
noc_file.write("USE ieee.numeric_std.ALL; \n")
noc_file.write("\n")

generate_entity(noc_file, CB_Package.network_dime, CB_Package.add_FI, CB_Package.add_SHMU, 
                CB_Package.fi_addres_width, CB_Package.add_LV)

noc_file.write("\n\n")
noc_file.write("architecture behavior of network_"+str(CB_Package.network_dime)+"x" +
               str(CB_Package.network_dime)+" is\n\n")

# declaring components, signals and making ascii art!!!
declare_components(noc_file, CB_Package.add_parity, CB_Package.add_FI, CB_Package.add_SHMU, CB_Package.add_LV, 
                   CB_Package.add_packet_drop, CB_Package.add_FC, CB_Package.network_dime, CB_Package.fi_addres_width, 
                   CB_Package.lv_ports, CB_Package.add_tracker)

declare_signals(noc_file, CB_Package.network_dime, CB_Package.add_parity, CB_Package.add_LV, CB_Package.add_packet_drop,
                CB_Package.add_FC, CB_Package.add_SHMU, CB_Package.lv_ports)

generate_ascii_art(noc_file, CB_Package.network_dime, CB_Package.add_FI)


noc_file.write("begin\n\n\n")

#todo: One should be able to control the threshold values!

instantiate_routers(noc_file, CB_Package.network_dime, CB_Package.add_parity, CB_Package.add_LV, CB_Package.add_packet_drop,
                    CB_Package.add_FC, CB_Package.add_SHMU, CB_Package.healthy_counter_threshold, CB_Package.faulty_counter_threshold, CB_Package.counter_depth)

if CB_Package.add_LV:
    instantiate_lv_routers(noc_file, CB_Package.network_dime, CB_Package.lv_ports)

if CB_Package.add_FI:
    noc_file.write("-- instantiating the Fault injectors\n")
    noc_file.write("-- vertical FIs\n")
    for i in range(0, CB_Package.network_dime**2):
        node_x = i % CB_Package.network_dime
        node_y = i / CB_Package.network_dime
        if node_y != CB_Package.network_dime-1:
            noc_file.write("FI_"+str(i)+"_"+str(i+CB_Package.network_dime) +
                           ": fault_injector generic map(DATA_WIDTH => DATA_WIDTH) \n")
            noc_file.write(" port map(\n")
            noc_file.write("    data_in => TX_S_"+str(i)+",\n")
            noc_file.write("    address => FI_Add_"+str(i)+"_"+str(i+CB_Package.network_dime)+",\n")
            noc_file.write("    sta_0 => sta0_"+str(i)+"_"+str(i+CB_Package.network_dime)+",\n")
            noc_file.write("    sta_1 => sta1_"+str(i)+"_"+str(i+CB_Package.network_dime)+",\n")
            noc_file.write("    data_out => RX_N_"+str(i+CB_Package.network_dime)+" \n")
            noc_file.write("    );\n")

            noc_file.write("FI_"+str(i+CB_Package.network_dime)+"_"+str(i) +
                           ": fault_injector generic map(DATA_WIDTH => DATA_WIDTH) \n")
            noc_file.write(" port map(\n")
            noc_file.write("    data_in => TX_N_"+str(i+CB_Package.network_dime)+",\n")
            noc_file.write("    address => FI_Add_"+str(i+CB_Package.network_dime)+"_"+str(i)+",\n")
            noc_file.write("    sta_0 => sta0_"+str(i+CB_Package.network_dime)+"_"+str(i)+",\n")
            noc_file.write("    sta_1 => sta1_"+str(i+CB_Package.network_dime)+"_"+str(i)+",\n")
            noc_file.write("    data_out => RX_S_"+str(i)+"\n")
            noc_file.write("    );\n")
    noc_file.write("\n")

    noc_file.write("-- horizontal FIs\n")
    for i in range(0, CB_Package.network_dime**2):
        node_x = i % CB_Package.network_dime
        node_y = i / CB_Package.network_dime
        if node_x != CB_Package.network_dime-1:
            noc_file.write("FI_"+str(i)+"_"+str(i+1)+": fault_injector generic map(DATA_WIDTH => DATA_WIDTH) \n")
            noc_file.write(" port map(\n")
            noc_file.write("    data_in => TX_E_"+str(i)+",\n")
            noc_file.write("    address => FI_Add_"+str(i)+"_"+str(i+1)+",\n")
            noc_file.write("    sta_0 => sta0_"+str(i)+"_"+str(i+1)+",\n")
            noc_file.write("    sta_1 => sta1_"+str(i)+"_"+str(i+1)+",\n")
            noc_file.write("    data_out =>  RX_W_"+str(i+1)+"\n")
            noc_file.write("    );\n")

            noc_file.write("FI_"+str(i+1)+"_"+str(i)+": fault_injector generic map(DATA_WIDTH => DATA_WIDTH) \n")
            noc_file.write(" port map(\n")
            noc_file.write("    data_in => TX_W_"+str(i+1)+",\n")
            noc_file.write("    address => FI_Add_"+str(i+1)+"_"+str(i)+",\n")
            noc_file.write("    sta_0 => sta0_"+str(i+1)+"_"+str(i)+",\n")
            noc_file.write("    sta_1 => sta1_"+str(i+1)+"_"+str(i)+",\n")
            noc_file.write("    data_out => RX_E_"+str(i)+"\n")
            noc_file.write("    );\n")
else:
    noc_file.write("---------------------------------------------------------------\n")
    noc_file.write("-- binding the routers together\n")
    noc_file.write("-- vertical ins/outs\n")
    for i in range(0, CB_Package.network_dime**2):
        node_x = i % CB_Package.network_dime
        node_y = i / CB_Package.network_dime
        if node_y != CB_Package.network_dime-1:
            noc_file.write("-- connecting router: "+str(i)+" to router: " +
                           str(i+CB_Package.network_dime)+" and vice versa\n")
            noc_file.write("RX_N_"+str(i+CB_Package.network_dime)+"<= TX_S_"+str(i)+";\n")
            noc_file.write("RX_S_"+str(i)+"<= TX_N_"+str(i+CB_Package.network_dime)+";\n")
            noc_file.write("-------------------\n")
    noc_file.write("\n")
    noc_file.write("-- horizontal ins/outs\n")
    for i in range(0, CB_Package.network_dime**2):
        node_x = i % CB_Package.network_dime
        node_y = i / CB_Package.network_dime
        if node_x != CB_Package.network_dime-1:
            noc_file.write("-- connecting router: "+str(i)+" to router: "+str(i+1)+" and vice versa\n")
            noc_file.write("RX_E_"+str(i)+" <= TX_W_"+str(i+1)+";\n")
            noc_file.write("RX_W_"+str(i+1)+" <= TX_E_"+str(i)+";\n")
            noc_file.write("-------------------\n")

if CB_Package.add_tracker:
    noc_file.write("-- instantiating the flit trackers\n")
    for i in range(0, CB_Package.network_dime**2):
        node_x = i % CB_Package.network_dime
        node_y = i / CB_Package.network_dime
        for input_port  in ['N', 'E', 'W', 'S', 'L']:
            noc_file.write("F_T_"+str(i)+"_"+input_port+": flit_tracker  generic map (\n")
            noc_file.write("        DATA_WIDTH: integer => DATA_WIDTH, \n")
            noc_file.write("        tracker_file =>\"traces/track"+str(i)+"_"+input_port+".txt\"\n")
            noc_file.write("    );\n")
            noc_file.write("    port map (\n")
            noc_file.write("        RX => RX_"+input_port+"_"+str(i)+", \n")
            noc_file.write("        valid_in => valid_in_"+input_port+"_"+str(i)+"\n")
            noc_file.write("    );\n")


noc_file.write("---------------------------------------------------------------\n")
noc_file.write("-- binding the routers together\n")
 
for i in range(0, CB_Package.network_dime**2):
    node_x = i % CB_Package.network_dime
    node_y = i / CB_Package.network_dime
    if node_y != CB_Package.network_dime-1:
        noc_file.write("-- connecting router: "+str(i)+" to router: " +
                       str(i+CB_Package.network_dime)+" and vice versa\n")
        noc_file.write("valid_in_N_"+str(i+CB_Package.network_dime)+" <= valid_out_S_"+str(i)+";\n")
        noc_file.write("valid_in_S_"+str(i)+" <= valid_out_N_"+str(i+CB_Package.network_dime)+";\n")
        noc_file.write("credit_in_S_"+str(i)+" <= credit_out_N_"+str(i+CB_Package.network_dime)+";\n")
        noc_file.write("credit_in_N_"+str(i+CB_Package.network_dime)+" <= credit_out_S_"+str(i)+";\n")
        noc_file.write("-------------------\n")
noc_file.write("\n")
 
for i in range(0, CB_Package.network_dime**2):
    node_x = i % CB_Package.network_dime
    node_y = i / CB_Package.network_dime
    if node_x != CB_Package.network_dime-1:
        noc_file.write("-- connecting router: "+str(i)+" to router: "+str(i+1)+" and vice versa\n")
        noc_file.write("valid_in_E_"+str(i)+" <= valid_out_W_"+str(i+1)+";\n")
        noc_file.write("valid_in_W_"+str(i+1)+" <= valid_out_E_"+str(i)+";\n")
        noc_file.write("credit_in_W_"+str(i+1)+" <= credit_out_E_"+str(i)+";\n")
        noc_file.write("credit_in_E_"+str(i)+" <= credit_out_W_"+str(i+1)+";\n")
        noc_file.write("-------------------\n")

if CB_Package.add_LV:
    if CB_Package.lv_ports == 4:
        noc_file.write("---------------------------------------------------------------\n")
        noc_file.write("-- binding the routers together\n")
        noc_file.write("-- vertical ins/outs\n")
        for i in range(0, CB_Package.network_dime**2):
            node_x = i % CB_Package.network_dime
            node_y = i / CB_Package.network_dime
            if node_y != CB_Package.network_dime-1:
                noc_file.write("-- connecting router: "+str(i)+" to router: " +
                               str(i+CB_Package.network_dime)+" and vice versa\n")
                noc_file.write("RX_LV_N"+str(i+CB_Package.network_dime)+"<= TX_LV_S"+str(i)+";\n")
                noc_file.write("RX_LV_S"+str(i)+"<= TX_LV_N"+str(i+CB_Package.network_dime)+";\n")
                noc_file.write("valid_in_LV_N"+str(i+CB_Package.network_dime)+" <= valid_out_LV_S"+str(i)+";\n")
                noc_file.write("valid_in_LV_S"+str(i)+" <= valid_out_LV_N"+str(i+CB_Package.network_dime)+";\n")
                noc_file.write("credit_in_LV_S"+str(i)+" <= credit_out_LV_N"+str(i+CB_Package.network_dime)+";\n")
                noc_file.write("credit_in_LV_N"+str(i+CB_Package.network_dime)+" <= credit_out_LV_S"+str(i)+";\n")
                noc_file.write("-------------------\n")
        noc_file.write("\n")
        noc_file.write("-- horizontal ins/outs\n")
        for i in range(0, CB_Package.network_dime**2):
            node_x = i % CB_Package.network_dime
            node_y = i / CB_Package.network_dime
            if node_x != CB_Package.network_dime-1:
                noc_file.write("-- connecting router: "+str(i)+" to router: "+str(i+1)+" and vice versa\n")
                noc_file.write("RX_LV_E"+str(i)+" <= TX_LV_W"+str(i+1)+";\n")
                noc_file.write("RX_LV_W"+str(i+1)+" <= TX_LV_E"+str(i)+";\n")
                noc_file.write("valid_in_LV_E"+str(i)+" <= valid_out_LV_W"+str(i+1)+";\n")
                noc_file.write("valid_in_LV_W"+str(i+1)+" <= valid_out_LV_E"+str(i)+";\n")
                noc_file.write("credit_in_LV_W"+str(i+1)+" <= credit_out_LV_E"+str(i)+";\n")
                noc_file.write("credit_in_LV_E"+str(i)+" <= credit_out_LV_W"+str(i+1)+";\n")
                noc_file.write("-------------------\n")

    elif CB_Package.lv_ports == 2:
        noc_file.write("---------------------------------------------------------------\n")
        noc_file.write("-- binding the routers together\n")
        noc_file.write("-- vertical ins/outs\n")
        for i in range(0, CB_Package.network_dime**2):
            node_x = i % CB_Package.network_dime
            node_y = i / CB_Package.network_dime
            if node_y != CB_Package.network_dime-1:
                if node_y % 2 == 1:
                    if node_x == 0:
                        noc_file.write("-- connecting router: "+str(i)+" to router: "+str(i+CB_Package.network_dime)+" and vice versa\n")
                        noc_file.write("RX_LV_W"+str(i)+" <= TX_LV_W"+str(i+CB_Package.network_dime)+";\n")
                        noc_file.write("RX_LV_W"+str(i+CB_Package.network_dime)+" <= TX_LV_W"+str(i)+";\n")
                        noc_file.write("valid_in_LV_W"+str(i)+" <= valid_out_LV_W"+str(i+CB_Package.network_dime)+";\n")
                        noc_file.write("valid_in_LV_W"+str(i+CB_Package.network_dime)+" <= valid_out_LV_W"+str(i)+";\n")
                        noc_file.write("credit_in_LV_W"+str(i+CB_Package.network_dime)+" <= credit_out_LV_W"+str(i)+";\n")
                        noc_file.write("credit_in_LV_W"+str(i)+" <= credit_out_LV_W"+str(i+CB_Package.network_dime)+";\n")            
                else:
                    if node_x == CB_Package.network_dime - 1:
                        noc_file.write("-- connecting router: "+str(i)+" to router: " +
                                       str(i+CB_Package.network_dime)+" and vice versa\n")
                        noc_file.write("RX_LV_E"+str(i+CB_Package.network_dime)+" <= TX_LV_E"+str(i)+";\n")
                        noc_file.write("RX_LV_E"+str(i)+" <= TX_LV_E"+str(i+CB_Package.network_dime)+";\n")
                        noc_file.write("valid_in_LV_E"+str(i+CB_Package.network_dime)+" <= valid_out_LV_E"+str(i)+";\n")
                        noc_file.write("valid_in_LV_E"+str(i)+" <= valid_out_LV_E"+str(i+CB_Package.network_dime)+";\n")
                        noc_file.write("credit_in_LV_E"+str(i)+" <= credit_out_LV_E"+str(i+CB_Package.network_dime)+";\n")
                        noc_file.write("credit_in_LV_E"+str(i+CB_Package.network_dime)+" <= credit_out_LV_E"+str(i)+";\n")
                        noc_file.write("-------------------\n")

        noc_file.write("\n")
        noc_file.write("-- horizontal ins/outs\n")
        for i in range(0, CB_Package.network_dime**2):
            node_x = i % CB_Package.network_dime
            node_y = i / CB_Package.network_dime
            if node_x != CB_Package.network_dime-1:
                noc_file.write("-- connecting router: "+str(i)+" to router: "+str(i+1)+" and vice versa\n")
                noc_file.write("RX_LV_E"+str(i)+" <= TX_LV_W"+str(i+1)+";\n")
                noc_file.write("RX_LV_W"+str(i+1)+" <= TX_LV_E"+str(i)+";\n")
                noc_file.write("valid_in_LV_E"+str(i)+" <= valid_out_LV_W"+str(i+1)+";\n")
                noc_file.write("valid_in_LV_W"+str(i+1)+" <= valid_out_LV_E"+str(i)+";\n")
                noc_file.write("credit_in_LV_W"+str(i+1)+" <= credit_out_LV_E"+str(i)+";\n")
                noc_file.write("credit_in_LV_E"+str(i)+" <= credit_out_LV_W"+str(i+1)+";\n")
                noc_file.write("-------------------\n")

        noc_file.write("\n")
         



if CB_Package.add_LV or (CB_Package.add_packet_drop and CB_Package.add_FC):
    for i in range(0, CB_Package.network_dime**2):
        north_node = i - CB_Package.network_dime
        south_node = i + CB_Package.network_dime
        west_node = i - 1
        east_node = i + 1

        node_x = i % CB_Package.network_dime
        node_y = i / CB_Package.network_dime


        if node_y > 0:
            noc_file.write("Faulty_N_in"+str(i)+" <= Faulty_S_out"+str(north_node)+";\n")

        if node_y < CB_Package.network_dime-1:
            noc_file.write("Faulty_S_in"+str(i)+" <= Faulty_N_out"+str(south_node)+";\n")

        if node_x > 0:
            noc_file.write("Faulty_W_in"+str(i)+" <= Faulty_E_out"+str(west_node)+";\n")    
        
        if node_x < CB_Package.network_dime-1:
            noc_file.write("Faulty_E_in"+str(i)+" <= Faulty_W_out"+str(east_node)+";\n")  
noc_file.write("end;\n")
