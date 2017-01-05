# Copyright (C) 2016 Siavoosh Payandeh Azad


def declare_components(noc_file, add_parity, add_FI, add_SHMU, add_lv, add_packet_drop, add_FC, network_dime, 
                       fi_addres_width, lv_ports, add_tracker):
    
    if add_lv :
        noc_file.write("component router_credit_based_parity_lv is\n")
        noc_file.write("    generic (\n")
        noc_file.write("        DATA_WIDTH: integer := 32;\n")
        noc_file.write("        DATA_WIDTH_LV: integer := 11;\n")
        noc_file.write("        current_address : integer := 0;\n")
        noc_file.write("        Cx_rst : integer := 10;\n")
        noc_file.write("        healthy_counter_threshold : integer := 20;\n")
        noc_file.write("        faulty_counter_threshold : integer := 3;\n")
        noc_file.write("        counter_depth : integer := 4;\n")
        noc_file.write("        NoC_size: integer := 4\n")
        noc_file.write("    );\n")
        noc_file.write("    port (\n")
        noc_file.write("    reset, clk: in std_logic;\n")
        noc_file.write("    Rxy_reconf: in  std_logic_vector(7 downto 0);\n")
        noc_file.write("    Reconfig : in std_logic;\n")
        noc_file.write("\n")
        noc_file.write("    RX_N, RX_E, RX_W, RX_S, RX_L : in std_logic_vector (DATA_WIDTH-1 downto 0); \n")
        noc_file.write("    credit_in_N, credit_in_E, credit_in_W, credit_in_S, credit_in_L: in std_logic;\n")
        noc_file.write("    valid_in_N, valid_in_E, valid_in_W, valid_in_S, valid_in_L : in std_logic;\n")
        noc_file.write("    valid_out_N, valid_out_E, valid_out_W, valid_out_S, valid_out_L : out std_logic;\n")
        noc_file.write("    credit_out_N, credit_out_E, credit_out_W, credit_out_S, credit_out_L: out std_logic;\n")
        noc_file.write("    TX_N, TX_E, TX_W, TX_S, TX_L: out std_logic_vector (DATA_WIDTH-1 downto 0);\n")
        noc_file.write("    Faulty_N_in, Faulty_E_in, Faulty_W_in, Faulty_S_in: in std_logic;\n")
        noc_file.write("    Faulty_N_out, Faulty_E_out, Faulty_W_out, Faulty_S_out: out std_logic;\n")
        noc_file.write("    ------------------------- lV network port\n")
        noc_file.write("    -- the router just sends the packets out. no need for any incomming packets support. \n")
        noc_file.write("    -- the output of the LV network will be connected to the PEs\n")
        noc_file.write("\n")
        noc_file.write("    credit_in_LV: in std_logic;\n")
        noc_file.write("    valid_out_LV : out std_logic;\n")
        noc_file.write("    TX_LV: out std_logic_vector (DATA_WIDTH-1 downto 0)\n")
        noc_file.write(" ); \n")
        noc_file.write("end component;\n")

    elif add_packet_drop and add_FC and not add_lv and not add_SHMU:
        noc_file.write("component router_credit_based_PD_C is  --fault classifier plus packet-dropping  \n")
        noc_file.write("    generic ( \n")
        noc_file.write("        DATA_WIDTH: integer := 32; \n")
        noc_file.write("        current_address : integer := 0; \n")
        noc_file.write("        Cx_rst : integer := 10; \n")
        noc_file.write("        healthy_counter_threshold : integer := 8; \n")
        noc_file.write("        faulty_counter_threshold: integer := 2; \n")
        noc_file.write("        counter_depth: integer := 4; \n")
        noc_file.write("        NoC_size: integer := 4 \n")
        noc_file.write("    ); \n")
        noc_file.write("    port ( \n")
        noc_file.write("    reset, clk: in std_logic; \n")
        noc_file.write(" \n")
        noc_file.write("    Rxy_reconf: in  std_logic_vector(7 downto 0); \n")
        noc_file.write("    Reconfig : in std_logic; \n")
        noc_file.write(" \n")
        noc_file.write("    RX_N, RX_E, RX_W, RX_S, RX_L : in std_logic_vector (DATA_WIDTH-1 downto 0);  \n")
        noc_file.write("    credit_in_N, credit_in_E, credit_in_W, credit_in_S, credit_in_L: in std_logic; \n")
        noc_file.write("    valid_in_N, valid_in_E, valid_in_W, valid_in_S, valid_in_L : in std_logic; \n")
        noc_file.write("    valid_out_N, valid_out_E, valid_out_W, valid_out_S, valid_out_L : out std_logic; \n")
        noc_file.write("    credit_out_N, credit_out_E, credit_out_W, credit_out_S, credit_out_L: out std_logic; \n")
        noc_file.write("    TX_N, TX_E, TX_W, TX_S, TX_L: out std_logic_vector (DATA_WIDTH-1 downto 0); \n")
        noc_file.write(" \n")
        noc_file.write("    Faulty_N_in, Faulty_E_in, Faulty_W_in, Faulty_S_in: in std_logic; \n")
        noc_file.write("    Faulty_N_out, Faulty_E_out, Faulty_W_out, Faulty_S_out: out std_logic \n")
        noc_file.write(" \n")
        noc_file.write(" );  \n")
        noc_file.write("end component;  \n")

    elif add_parity and not add_SHMU and not add_lv:
        noc_file.write("-- Declaring router component\n")
        noc_file.write("component router_credit_based_parity is\n")
        noc_file.write("  generic (\n")
        noc_file.write("        DATA_WIDTH: integer := 32; \n")
        noc_file.write("        current_address : integer := 0;\n")
        noc_file.write("        Cx_rst : integer := 10;\n")
        noc_file.write("        NoC_size: integer := 4\n")
        noc_file.write("    );\n")
        noc_file.write("    port (\n")
        noc_file.write("    reset, clk: in std_logic; \n\n")
        noc_file.write("    Rxy_reconf: in  std_logic_vector(7 downto 0);\n")
        noc_file.write("    Reconfig : in std_logic;\n")
        noc_file.write("    RX_N, RX_E, RX_W, RX_S, RX_L : in std_logic_vector (DATA_WIDTH-1 downto 0); \n")
        noc_file.write("    credit_in_N, credit_in_E, credit_in_W, credit_in_S, credit_in_L: in std_logic;\n")
        noc_file.write("    valid_in_N, valid_in_E, valid_in_W, valid_in_S, valid_in_L : in std_logic;\n\n")
        noc_file.write("    valid_out_N, valid_out_E, valid_out_W, valid_out_S, valid_out_L : out std_logic;\n")
        noc_file.write("    credit_out_N, credit_out_E, credit_out_W, credit_out_S, credit_out_L: out std_logic;\n\n")
        noc_file.write("    TX_N, TX_E, TX_W, TX_S, TX_L: out std_logic_vector (DATA_WIDTH-1 downto 0);\n")
        noc_file.write("    faulty_packet_N, faulty_packet_E, faulty_packet_W, faulty_packet_S, "
                       "faulty_packet_L:out std_logic;\n")
        noc_file.write("    healthy_packet_N, healthy_packet_E, healthy_packet_W, healthy_packet_S, "
                       "healthy_packet_L:out std_logic\n")
        noc_file.write("    ); \n")
        noc_file.write("end component; \n")

    elif add_SHMU and not add_lv:
        noc_file.write("component router_credit_based_PD_C_SHMU is  --fault classifier plus packet-dropping \n")
        noc_file.write("    generic (\n")
        noc_file.write("        DATA_WIDTH: integer := 32;\n")
        noc_file.write("        current_address : integer := 0;\n")
        noc_file.write("        Rxy_rst : integer := 10;\n")
        noc_file.write("        Cx_rst : integer := 10;\n")
        noc_file.write("        healthy_counter_threshold : integer := 8;\n")
        noc_file.write("        faulty_counter_threshold: integer := 2;\n")
        noc_file.write("        counter_depth: integer := 4;\n")
        noc_file.write("        NoC_size: integer := 4\n")
        noc_file.write("    );\n")
        noc_file.write("    port (\n")
        noc_file.write("    reset, clk: in std_logic;\n\n")
 
        noc_file.write("    RX_N, RX_E, RX_W, RX_S, RX_L : in std_logic_vector (DATA_WIDTH-1 downto 0); \n")
        noc_file.write("    credit_in_N, credit_in_E, credit_in_W, credit_in_S, credit_in_L: in std_logic;\n")
        noc_file.write("    valid_in_N, valid_in_E, valid_in_W, valid_in_S, valid_in_L : in std_logic;\n")
        noc_file.write("    valid_out_N, valid_out_E, valid_out_W, valid_out_S, valid_out_L : out std_logic;\n")
        noc_file.write("    credit_out_N, credit_out_E, credit_out_W, credit_out_S, credit_out_L: out std_logic;\n")
        noc_file.write("    TX_N, TX_E, TX_W, TX_S, TX_L: out std_logic_vector (DATA_WIDTH-1 downto 0);\n\n")
 
        noc_file.write("    Faulty_N_in, Faulty_E_in, Faulty_W_in, Faulty_S_in: in std_logic;\n")
        noc_file.write("    Faulty_N_out, Faulty_E_out, Faulty_W_out, Faulty_S_out: out std_logic;\n\n")
 
        noc_file.write("    -- should be connected to NI\n")
        noc_file.write("    link_faults: out std_logic_vector(4 downto 0);\n")
        noc_file.write("    turn_faults: out std_logic_vector(7 downto 0);\n\n")
 
        noc_file.write("    Rxy_reconf_PE: in  std_logic_vector(7 downto 0);\n")
        noc_file.write("    Cx_reconf_PE: in  std_logic_vector(3 downto 0);\n")
        noc_file.write("    Reconfig_command : in std_logic\n")
        noc_file.write(" ); \n")
        noc_file.write("end component; \n")

    else:
        noc_file.write("component router_credit_based is\n")
        noc_file.write("  generic (\n")
        noc_file.write("        DATA_WIDTH: integer := 32; \n")
        noc_file.write("        current_address : integer := 0;\n")
        noc_file.write("        Cx_rst : integer := 10;\n")
        noc_file.write("        NoC_size: integer := 4\n")
        noc_file.write("    );\n")
        noc_file.write("    port (\n")
        noc_file.write("    reset, clk: in std_logic; \n\n")
        noc_file.write("    Rxy_reconf: in  std_logic_vector(7 downto 0);\n")
        noc_file.write("    Reconfig : in std_logic;\n")
        noc_file.write("    RX_N, RX_E, RX_W, RX_S, RX_L : in std_logic_vector (DATA_WIDTH-1 downto 0); \n")
        noc_file.write("    credit_in_N, credit_in_E, credit_in_W, credit_in_S, credit_in_L: in std_logic;\n")
        noc_file.write("    valid_in_N, valid_in_E, valid_in_W, valid_in_S, valid_in_L : in std_logic;\n\n")
        noc_file.write("    valid_out_N, valid_out_E, valid_out_W, valid_out_S, valid_out_L : out std_logic;\n")
        noc_file.write("    credit_out_N, credit_out_E, credit_out_W, credit_out_S, credit_out_L: out std_logic;\n\n")
        noc_file.write("    TX_N, TX_E, TX_W, TX_S, TX_L: out std_logic_vector (DATA_WIDTH-1 downto 0)\n")
        noc_file.write("    ); \n")
        noc_file.write("end component; \n")

    noc_file.write("\n\n")

    if add_lv:
        
        noc_file.write("component router_LV is\n")
        noc_file.write("	generic (\n")
        noc_file.write("        DATA_WIDTH: integer := 11;\n")
        noc_file.write("        current_address : integer := 0;\n")
        noc_file.write("        Rxy_rst : integer := 60;\n")
        noc_file.write("        Cx_rst : integer := 10;\n")
        noc_file.write("        NoC_size: integer := 4\n")
        noc_file.write("    );\n")
        noc_file.write("    port (\n")
        noc_file.write("    reset, clk: in std_logic;\n")
        noc_file.write("\n")
        if lv_ports == 4:
            noc_file.write("    RX_N, RX_E, RX_W, RX_S, RX_L : in std_logic_vector (DATA_WIDTH-1 downto 0); \n")
            noc_file.write("\n")
            noc_file.write("    credit_in_N, credit_in_E, credit_in_W, credit_in_S, credit_in_L: in std_logic;\n")
            noc_file.write("    valid_in_N, valid_in_E, valid_in_W, valid_in_S, valid_in_L : in std_logic;\n")
            noc_file.write("\n")
            noc_file.write("    valid_out_N, valid_out_E, valid_out_W, valid_out_S, valid_out_L : out std_logic;\n")
            noc_file.write("    credit_out_N, credit_out_E, credit_out_W, credit_out_S, credit_out_L: out std_logic;\n")
            noc_file.write("\n")
            noc_file.write("    TX_N, TX_E, TX_W, TX_S, TX_L: out std_logic_vector (DATA_WIDTH-1 downto 0)\n")
        elif lv_ports == 2:
            noc_file.write("    RX_E, RX_W, RX_L : in std_logic_vector (DATA_WIDTH-1 downto 0); \n")
            noc_file.write("\n")
            noc_file.write("    credit_in_E, credit_in_W, credit_in_L: in std_logic;\n")
            noc_file.write("    valid_in_E, valid_in_W, valid_in_L : in std_logic;\n")
            noc_file.write("\n")
            noc_file.write("    valid_out_E, valid_out_W, valid_out_L : out std_logic;\n")
            noc_file.write("    credit_out_E, credit_out_W, credit_out_L: out std_logic;\n")
            noc_file.write("\n")
            noc_file.write("    TX_E, TX_W, TX_L: out std_logic_vector (DATA_WIDTH-1 downto 0)\n")
        noc_file.write("    ); \n")
        noc_file.write("end component;\n")
        

        noc_file.write("\n\n")

    if add_FI:
        noc_file.write("component fault_injector is \n")
        noc_file.write("  generic(DATA_WIDTH : integer := 32);\n")
        noc_file.write("  port(\n")
        noc_file.write("    data_in: in std_logic_vector (DATA_WIDTH-1 downto 0);\n")
        noc_file.write("    address: in std_logic_vector("+str(fi_addres_width-1)+" downto 0);\n")
        noc_file.write("    sta_0: in std_logic;\n")
        noc_file.write("    sta_1: in std_logic;\n")
        noc_file.write("    data_out: out std_logic_vector (DATA_WIDTH-1 downto 0)\n")
        noc_file.write("    );\n")
        noc_file.write("end component;\n")

        noc_file.write("\n\n")

    if add_tracker:
        noc_file.write("component flit_tracker is\n")
        noc_file.write("    generic (\n")
        noc_file.write("        DATA_WIDTH: integer := 32;\n")
        noc_file.write("        tracker_file: string :=\"track.txt\"\n")
        noc_file.write("    );\n")
        noc_file.write("    port (\n")
        noc_file.write("        RX: in std_logic_vector (DATA_WIDTH-1 downto 0); \n")
        noc_file.write("        valid_in : in std_logic \n")
        noc_file.write("    );\n")
        noc_file.write("end component;\n")
