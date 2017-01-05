--Copyright (C) 2016 Siavoosh Payandeh Azad
------------------------------------------------------------
-- This file is automatically generated!
-- Here are the parameters:
-- 	 network size x: 2
-- 	 network size y: 2
-- 	 LV network: False
-- 	 Data width: 32
-- 	 Parity: False
-- 	 Fault injectors: True
------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
USE ieee.numeric_std.ALL; 

entity network_2x2 is
 generic (DATA_WIDTH: integer := 32; DATA_WIDTH_LV: integer := 11);
port (reset: in  std_logic; 
	clk: in  std_logic; 
	--------------
	--------------
	RX_L_0: in std_logic_vector (DATA_WIDTH-1 downto 0);
	credit_out_L_0, valid_out_L_0: out std_logic;
	credit_in_L_0, valid_in_L_0: in std_logic;
	TX_L_0: out std_logic_vector (DATA_WIDTH-1 downto 0);
	--------------
	RX_L_1: in std_logic_vector (DATA_WIDTH-1 downto 0);
	credit_out_L_1, valid_out_L_1: out std_logic;
	credit_in_L_1, valid_in_L_1: in std_logic;
	TX_L_1: out std_logic_vector (DATA_WIDTH-1 downto 0);
	--------------
	RX_L_2: in std_logic_vector (DATA_WIDTH-1 downto 0);
	credit_out_L_2, valid_out_L_2: out std_logic;
	credit_in_L_2, valid_in_L_2: in std_logic;
	TX_L_2: out std_logic_vector (DATA_WIDTH-1 downto 0);
	--------------
	RX_L_3: in std_logic_vector (DATA_WIDTH-1 downto 0);
	credit_out_L_3, valid_out_L_3: out std_logic;
	credit_in_L_3, valid_in_L_3: in std_logic;
	TX_L_3: out std_logic_vector (DATA_WIDTH-1 downto 0);
	--fault injector signals
	FI_Add_2_0, FI_Add_0_2: in std_logic_vector(4 downto 0);
	sta0_0_2, sta1_0_2, sta0_2_0, sta1_2_0: in std_logic;

	FI_Add_3_1, FI_Add_1_3: in std_logic_vector(4 downto 0);
	sta0_1_3, sta1_1_3, sta0_3_1, sta1_3_1: in std_logic;

	FI_Add_1_0, FI_Add_0_1: in std_logic_vector(4 downto 0);
	sta0_0_1, sta1_0_1, sta0_1_0, sta1_1_0: in std_logic;

	FI_Add_3_2, FI_Add_2_3: in std_logic_vector(4 downto 0);
	sta0_2_3, sta1_2_3, sta0_3_2, sta1_3_2: in std_logic;

	--------------
    link_faults_0: out std_logic_vector(4 downto 0);
    turn_faults_0: out std_logic_vector(7 downto 0);
    Rxy_reconf_PE_0: in  std_logic_vector(7 downto 0);
    Cx_reconf_PE_0: in  std_logic_vector(3 downto 0);
    Reconfig_command_0 : in std_logic;

	--------------
    link_faults_1: out std_logic_vector(4 downto 0);
    turn_faults_1: out std_logic_vector(7 downto 0);
    Rxy_reconf_PE_1: in  std_logic_vector(7 downto 0);
    Cx_reconf_PE_1: in  std_logic_vector(3 downto 0);
    Reconfig_command_1 : in std_logic;

	--------------
    link_faults_2: out std_logic_vector(4 downto 0);
    turn_faults_2: out std_logic_vector(7 downto 0);
    Rxy_reconf_PE_2: in  std_logic_vector(7 downto 0);
    Cx_reconf_PE_2: in  std_logic_vector(3 downto 0);
    Reconfig_command_2 : in std_logic;

	--------------
    link_faults_3: out std_logic_vector(4 downto 0);
    turn_faults_3: out std_logic_vector(7 downto 0);
    Rxy_reconf_PE_3: in  std_logic_vector(7 downto 0);
    Cx_reconf_PE_3: in  std_logic_vector(3 downto 0);
    Reconfig_command_3 : in std_logic
            ); 
end network_2x2; 


architecture behavior of network_2x2 is

component router_credit_based_PD_C_SHMU is  --fault classifier plus packet-dropping 
    generic (
        DATA_WIDTH: integer := 32;
        current_address : integer := 0;
        Rxy_rst : integer := 10;
        Cx_rst : integer := 10;
        healthy_counter_threshold : integer := 8;
        faulty_counter_threshold: integer := 2;
        counter_depth: integer := 4;
        NoC_size: integer := 4
    );
    port (
    reset, clk: in std_logic;

    RX_N, RX_E, RX_W, RX_S, RX_L : in std_logic_vector (DATA_WIDTH-1 downto 0); 
    credit_in_N, credit_in_E, credit_in_W, credit_in_S, credit_in_L: in std_logic;
    valid_in_N, valid_in_E, valid_in_W, valid_in_S, valid_in_L : in std_logic;
    valid_out_N, valid_out_E, valid_out_W, valid_out_S, valid_out_L : out std_logic;
    credit_out_N, credit_out_E, credit_out_W, credit_out_S, credit_out_L: out std_logic;
    TX_N, TX_E, TX_W, TX_S, TX_L: out std_logic_vector (DATA_WIDTH-1 downto 0);

    Faulty_N_in, Faulty_E_in, Faulty_W_in, Faulty_S_in: in std_logic;
    Faulty_N_out, Faulty_E_out, Faulty_W_out, Faulty_S_out: out std_logic;

    -- should be connected to NI
    link_faults: out std_logic_vector(4 downto 0);
    turn_faults: out std_logic_vector(7 downto 0);

    Rxy_reconf_PE: in  std_logic_vector(7 downto 0);
    Cx_reconf_PE: in  std_logic_vector(3 downto 0);
    Reconfig_command : in std_logic
 ); 
end component; 


component fault_injector is 
  generic(DATA_WIDTH : integer := 32);
  port(
    data_in: in std_logic_vector (DATA_WIDTH-1 downto 0);
    address: in std_logic_vector(4 downto 0);
    sta_0: in std_logic;
    sta_1: in std_logic;
    data_out: out std_logic_vector (DATA_WIDTH-1 downto 0)
    );
end component;




-- generating bulk signals. not all of them are used in the design...
	signal credit_out_N_0, credit_out_E_0, credit_out_W_0, credit_out_S_0: std_logic;
	signal credit_out_N_1, credit_out_E_1, credit_out_W_1, credit_out_S_1: std_logic;
	signal credit_out_N_2, credit_out_E_2, credit_out_W_2, credit_out_S_2: std_logic;
	signal credit_out_N_3, credit_out_E_3, credit_out_W_3, credit_out_S_3: std_logic;

	signal credit_in_N_0, credit_in_E_0, credit_in_W_0, credit_in_S_0: std_logic;
	signal credit_in_N_1, credit_in_E_1, credit_in_W_1, credit_in_S_1: std_logic;
	signal credit_in_N_2, credit_in_E_2, credit_in_W_2, credit_in_S_2: std_logic;
	signal credit_in_N_3, credit_in_E_3, credit_in_W_3, credit_in_S_3: std_logic;

	signal RX_N_0, RX_E_0, RX_W_0, RX_S_0 : std_logic_vector (DATA_WIDTH-1 downto 0);
	signal RX_N_1, RX_E_1, RX_W_1, RX_S_1 : std_logic_vector (DATA_WIDTH-1 downto 0);
	signal RX_N_2, RX_E_2, RX_W_2, RX_S_2 : std_logic_vector (DATA_WIDTH-1 downto 0);
	signal RX_N_3, RX_E_3, RX_W_3, RX_S_3 : std_logic_vector (DATA_WIDTH-1 downto 0);

	signal valid_out_N_0, valid_out_E_0, valid_out_W_0, valid_out_S_0: std_logic;
	signal valid_out_N_1, valid_out_E_1, valid_out_W_1, valid_out_S_1: std_logic;
	signal valid_out_N_2, valid_out_E_2, valid_out_W_2, valid_out_S_2: std_logic;
	signal valid_out_N_3, valid_out_E_3, valid_out_W_3, valid_out_S_3: std_logic;

	signal valid_in_N_0, valid_in_E_0, valid_in_W_0, valid_in_S_0: std_logic;
	signal valid_in_N_1, valid_in_E_1, valid_in_W_1, valid_in_S_1: std_logic;
	signal valid_in_N_2, valid_in_E_2, valid_in_W_2, valid_in_S_2: std_logic;
	signal valid_in_N_3, valid_in_E_3, valid_in_W_3, valid_in_S_3: std_logic;

	signal TX_N_0, TX_E_0, TX_W_0, TX_S_0 : std_logic_vector (DATA_WIDTH-1 downto 0);
	signal TX_N_1, TX_E_1, TX_W_1, TX_S_1 : std_logic_vector (DATA_WIDTH-1 downto 0);
	signal TX_N_2, TX_E_2, TX_W_2, TX_S_2 : std_logic_vector (DATA_WIDTH-1 downto 0);
	signal TX_N_3, TX_E_3, TX_W_3, TX_S_3 : std_logic_vector (DATA_WIDTH-1 downto 0);
	signal Faulty_N_out0,Faulty_E_out0,Faulty_W_out0,Faulty_S_out0: std_logic;
	signal Faulty_N_in0,Faulty_E_in0,Faulty_W_in0,Faulty_S_in0: std_logic;
	signal Faulty_N_out1,Faulty_E_out1,Faulty_W_out1,Faulty_S_out1: std_logic;
	signal Faulty_N_in1,Faulty_E_in1,Faulty_W_in1,Faulty_S_in1: std_logic;
	signal Faulty_N_out2,Faulty_E_out2,Faulty_W_out2,Faulty_S_out2: std_logic;
	signal Faulty_N_in2,Faulty_E_in2,Faulty_W_in2,Faulty_S_in2: std_logic;
	signal Faulty_N_out3,Faulty_E_out3,Faulty_W_out3,Faulty_S_out3: std_logic;
	signal Faulty_N_in3,Faulty_E_in3,Faulty_W_in3,Faulty_S_in3: std_logic;



--        organizaiton of the network:
--     x --------------->
--  y         ----       ----
--  |        | 0  | -*- | 1  |
--  |         ----       ----
--  |          *          *
--  |         ----       ----
--  |        | 2  | -*- | 3  |
--  v         ----       ----
--                         
begin


R_0: router_credit_based_PD_C_SHMU 
    generic map (DATA_WIDTH =>DATA_WIDTH,         current_address => 0, Rxy_rst => 60,
        Cx_rst =>  10, NoC_size => 2, healthy_counter_threshold => 15, faulty_counter_threshold => 3, counter_depth => 4)
    port map(
    reset, clk,
	RX_N_0, RX_E_0, RX_W_0, RX_S_0, RX_L_0,
	credit_in_N_0, credit_in_E_0, credit_in_W_0, credit_in_S_0, credit_in_L_0,
	valid_in_N_0, valid_in_E_0, valid_in_W_0, valid_in_S_0, valid_in_L_0,
	valid_out_N_0, valid_out_E_0, valid_out_W_0, valid_out_S_0, valid_out_L_0,
	credit_out_N_0, credit_out_E_0, credit_out_W_0, credit_out_S_0, credit_out_L_0,
	TX_N_0, TX_E_0, TX_W_0, TX_S_0, TX_L_0,
	Faulty_N_in0,Faulty_E_in0,Faulty_W_in0,Faulty_S_in0,
	Faulty_N_out0,Faulty_E_out0,Faulty_W_out0,Faulty_S_out0,
	-- should be connected to NI
	link_faults_0, turn_faults_0,
	Rxy_reconf_PE_0, Cx_reconf_PE_0, Reconfig_command_0
 ); 
R_1: router_credit_based_PD_C_SHMU 
    generic map (DATA_WIDTH =>DATA_WIDTH,         current_address => 1, Rxy_rst => 60,
        Cx_rst =>  12, NoC_size => 2, healthy_counter_threshold => 15, faulty_counter_threshold => 3, counter_depth => 4)
    port map(
    reset, clk,
	RX_N_1, RX_E_1, RX_W_1, RX_S_1, RX_L_1,
	credit_in_N_1, credit_in_E_1, credit_in_W_1, credit_in_S_1, credit_in_L_1,
	valid_in_N_1, valid_in_E_1, valid_in_W_1, valid_in_S_1, valid_in_L_1,
	valid_out_N_1, valid_out_E_1, valid_out_W_1, valid_out_S_1, valid_out_L_1,
	credit_out_N_1, credit_out_E_1, credit_out_W_1, credit_out_S_1, credit_out_L_1,
	TX_N_1, TX_E_1, TX_W_1, TX_S_1, TX_L_1,
	Faulty_N_in1,Faulty_E_in1,Faulty_W_in1,Faulty_S_in1,
	Faulty_N_out1,Faulty_E_out1,Faulty_W_out1,Faulty_S_out1,
	-- should be connected to NI
	link_faults_1, turn_faults_1,
	Rxy_reconf_PE_1, Cx_reconf_PE_1, Reconfig_command_1
 ); 
R_2: router_credit_based_PD_C_SHMU 
    generic map (DATA_WIDTH =>DATA_WIDTH,         current_address => 2, Rxy_rst => 60,
        Cx_rst =>  3, NoC_size => 2, healthy_counter_threshold => 15, faulty_counter_threshold => 3, counter_depth => 4)
    port map(
    reset, clk,
	RX_N_2, RX_E_2, RX_W_2, RX_S_2, RX_L_2,
	credit_in_N_2, credit_in_E_2, credit_in_W_2, credit_in_S_2, credit_in_L_2,
	valid_in_N_2, valid_in_E_2, valid_in_W_2, valid_in_S_2, valid_in_L_2,
	valid_out_N_2, valid_out_E_2, valid_out_W_2, valid_out_S_2, valid_out_L_2,
	credit_out_N_2, credit_out_E_2, credit_out_W_2, credit_out_S_2, credit_out_L_2,
	TX_N_2, TX_E_2, TX_W_2, TX_S_2, TX_L_2,
	Faulty_N_in2,Faulty_E_in2,Faulty_W_in2,Faulty_S_in2,
	Faulty_N_out2,Faulty_E_out2,Faulty_W_out2,Faulty_S_out2,
	-- should be connected to NI
	link_faults_2, turn_faults_2,
	Rxy_reconf_PE_2, Cx_reconf_PE_2, Reconfig_command_2
 ); 
R_3: router_credit_based_PD_C_SHMU 
    generic map (DATA_WIDTH =>DATA_WIDTH,         current_address => 3, Rxy_rst => 60,
        Cx_rst =>  5, NoC_size => 2, healthy_counter_threshold => 15, faulty_counter_threshold => 3, counter_depth => 4)
    port map(
    reset, clk,
	RX_N_3, RX_E_3, RX_W_3, RX_S_3, RX_L_3,
	credit_in_N_3, credit_in_E_3, credit_in_W_3, credit_in_S_3, credit_in_L_3,
	valid_in_N_3, valid_in_E_3, valid_in_W_3, valid_in_S_3, valid_in_L_3,
	valid_out_N_3, valid_out_E_3, valid_out_W_3, valid_out_S_3, valid_out_L_3,
	credit_out_N_3, credit_out_E_3, credit_out_W_3, credit_out_S_3, credit_out_L_3,
	TX_N_3, TX_E_3, TX_W_3, TX_S_3, TX_L_3,
	Faulty_N_in3,Faulty_E_in3,Faulty_W_in3,Faulty_S_in3,
	Faulty_N_out3,Faulty_E_out3,Faulty_W_out3,Faulty_S_out3,
	-- should be connected to NI
	link_faults_3, turn_faults_3,
	Rxy_reconf_PE_3, Cx_reconf_PE_3, Reconfig_command_3
 ); 

-- instantiating the Fault injectors
-- vertical FIs
FI_0_2: fault_injector generic map(DATA_WIDTH => DATA_WIDTH) 
 port map(
    data_in => TX_S_0,
    address => FI_Add_0_2,
    sta_0 => sta0_0_2,
    sta_1 => sta1_0_2,
    data_out => RX_N_2 
    );
FI_2_0: fault_injector generic map(DATA_WIDTH => DATA_WIDTH) 
 port map(
    data_in => TX_N_2,
    address => FI_Add_2_0,
    sta_0 => sta0_2_0,
    sta_1 => sta1_2_0,
    data_out => RX_S_0
    );
FI_1_3: fault_injector generic map(DATA_WIDTH => DATA_WIDTH) 
 port map(
    data_in => TX_S_1,
    address => FI_Add_1_3,
    sta_0 => sta0_1_3,
    sta_1 => sta1_1_3,
    data_out => RX_N_3 
    );
FI_3_1: fault_injector generic map(DATA_WIDTH => DATA_WIDTH) 
 port map(
    data_in => TX_N_3,
    address => FI_Add_3_1,
    sta_0 => sta0_3_1,
    sta_1 => sta1_3_1,
    data_out => RX_S_1
    );

-- horizontal FIs
FI_0_1: fault_injector generic map(DATA_WIDTH => DATA_WIDTH) 
 port map(
    data_in => TX_E_0,
    address => FI_Add_0_1,
    sta_0 => sta0_0_1,
    sta_1 => sta1_0_1,
    data_out =>  RX_W_1
    );
FI_1_0: fault_injector generic map(DATA_WIDTH => DATA_WIDTH) 
 port map(
    data_in => TX_W_1,
    address => FI_Add_1_0,
    sta_0 => sta0_1_0,
    sta_1 => sta1_1_0,
    data_out => RX_E_0
    );
FI_2_3: fault_injector generic map(DATA_WIDTH => DATA_WIDTH) 
 port map(
    data_in => TX_E_2,
    address => FI_Add_2_3,
    sta_0 => sta0_2_3,
    sta_1 => sta1_2_3,
    data_out =>  RX_W_3
    );
FI_3_2: fault_injector generic map(DATA_WIDTH => DATA_WIDTH) 
 port map(
    data_in => TX_W_3,
    address => FI_Add_3_2,
    sta_0 => sta0_3_2,
    sta_1 => sta1_3_2,
    data_out => RX_E_2
    );
---------------------------------------------------------------
-- binding the routers together
-- connecting router: 0 to router: 2 and vice versa
valid_in_N_2 <= valid_out_S_0;
valid_in_S_0 <= valid_out_N_2;
credit_in_S_0 <= credit_out_N_2;
credit_in_N_2 <= credit_out_S_0;
-------------------
-- connecting router: 1 to router: 3 and vice versa
valid_in_N_3 <= valid_out_S_1;
valid_in_S_1 <= valid_out_N_3;
credit_in_S_1 <= credit_out_N_3;
credit_in_N_3 <= credit_out_S_1;
-------------------

-- connecting router: 0 to router: 1 and vice versa
valid_in_E_0 <= valid_out_W_1;
valid_in_W_1 <= valid_out_E_0;
credit_in_W_1 <= credit_out_E_0;
credit_in_E_0 <= credit_out_W_1;
-------------------
-- connecting router: 2 to router: 3 and vice versa
valid_in_E_2 <= valid_out_W_3;
valid_in_W_3 <= valid_out_E_2;
credit_in_W_3 <= credit_out_E_2;
credit_in_E_2 <= credit_out_W_3;
-------------------
Faulty_S_in0 <= Faulty_N_out2;
Faulty_E_in0 <= Faulty_W_out1;
Faulty_S_in1 <= Faulty_N_out3;
Faulty_W_in1 <= Faulty_E_out0;
Faulty_N_in2 <= Faulty_S_out0;
Faulty_E_in2 <= Faulty_W_out3;
Faulty_N_in3 <= Faulty_S_out1;
Faulty_W_in3 <= Faulty_E_out2;
end;
