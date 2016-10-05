--Copyright (C) 2016 Siavoosh Payandeh Azad

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_misc.all;
--use IEEE.STD_LOGIC_ARITH.ALL;
--use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity FIFO_credit_based is
    generic (
        DATA_WIDTH: integer := 32
    );
    port (  reset: in  std_logic;
            clk: in  std_logic;
            RX: in std_logic_vector(DATA_WIDTH-1 downto 0); 
            valid_in: in std_logic;  
            read_en_N : in std_logic;
            read_en_E : in std_logic;
            read_en_W : in std_logic;
            read_en_S : in std_logic;
            read_en_L : in std_logic;
            credit_out: out std_logic; 
            empty_out: out std_logic; 
            Data_out: out std_logic_vector(DATA_WIDTH-1 downto 0)
    );
end FIFO_credit_based;

architecture behavior of FIFO_credit_based is
   signal read_pointer, read_pointer_in,  write_pointer, write_pointer_in: std_logic_vector(3 downto 0);
   signal full, empty: std_logic;
   signal read_en, write_en: std_logic;

   signal FIFO_MEM_1, FIFO_MEM_1_in : std_logic_vector(DATA_WIDTH-1 downto 0);
   signal FIFO_MEM_2, FIFO_MEM_2_in : std_logic_vector(DATA_WIDTH-1 downto 0);
   signal FIFO_MEM_3, FIFO_MEM_3_in : std_logic_vector(DATA_WIDTH-1 downto 0);
   signal FIFO_MEM_4, FIFO_MEM_4_in : std_logic_vector(DATA_WIDTH-1 downto 0);

   constant fake_tail :  std_logic_vector := "10000000000000000000000000000001";
   
   alias flit_type :  std_logic_vector(2 downto 0) is RX(DATA_WIDTH-1 downto DATA_WIDTH-3); 
   signal faulty_packet_in, faulty_packet_out: std_logic;
   signal xor_all, fault_out: std_logic;
   type state_type is (Idle, Header_flit, Body_flit, Tail_flit);
   signal  state_out, state_in : state_type;

begin
 --------------------------------------------------------------------------------------------
--                           block diagram of the FIFO!


 --------------------------------------------------------------------------------------------
--  circular buffer structure
--                                   <--- WriteP    
--              ---------------------------------
--              |   3   |   2   |   1   |   0   |
--              ---------------------------------
--                                   <--- readP   
 --------------------------------------------------------------------------------------------

   process (clk, reset)begin
        if reset = '0' then
            read_pointer  <= "0001";
            write_pointer <= "0001";

            FIFO_MEM_1 <= (others=>'0');
            FIFO_MEM_2 <= (others=>'0');
            FIFO_MEM_3 <= (others=>'0');
            FIFO_MEM_4 <= (others=>'0');

            credit_out <= '0';
            faulty_packet_out <= '0';
        elsif clk'event and clk = '1' then
            write_pointer <= write_pointer_in;
            read_pointer  <=  read_pointer_in;
            credit_out <= '0';
            if write_en = '1' then 
                --write into the memory
                  FIFO_MEM_1 <= FIFO_MEM_1_in;
                  FIFO_MEM_2 <= FIFO_MEM_2_in;
                  FIFO_MEM_3 <= FIFO_MEM_3_in;
                  FIFO_MEM_4 <= FIFO_MEM_4_in;                   
            end if;
            faulty_packet_out <= faulty_packet_in;
            if read_en = '1' then 
              credit_out <= '1';
            end if;
        end if;
    end process;


 -- anything below here is pure combinational

 process(valid_in, RX) begin
  if valid_in = '1' then 
    xor_all <= XOR_REDUCE(RX(DATA_WIDTH-1 downto 1));
  else
    xor_all <= '0';
  end if;
end process;

process(valid_in, RX, xor_all)begin 
  fault_out <= '0';
  if valid_in = '1' and  xor_all /= RX(0) then 
    fault_out <= '1';
  end if;
end process;

  process(flit_type, fault_out, faulty_packet_out, state_out, valid_in, write_pointer, FIFO_MEM_1, FIFO_MEM_2, FIFO_MEM_3, FIFO_MEM_4)
begin
    case( write_pointer ) is
          when "0001" => FIFO_MEM_1_in <= RX;         FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
          when "0010" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= RX;         FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
          when "0100" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= RX;         FIFO_MEM_4_in <= FIFO_MEM_4; 
          when "1000" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= RX;                  
          when others => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
      end case ;
  --if valid_in = '1' then 
    case(state_out) is
          when Idle =>
            
            if fault_out = '1' then 
              -- new flit is faulty
              faulty_packet_in <= '1';
              FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
              state_in <= Header_flit;
            else
              -- all is good
              faulty_packet_in <= '0';

              if flit_type = "001" then
                state_in <= Header_flit;
              else
                state_in <= state_out;
              end if;
            end if;
 

          when Header_flit =>
            if faulty_packet_out = '1' then
              -- packet is already faulty
              faulty_packet_in <= faulty_packet_out;
              FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
              if flit_type = "100" then
                  state_in <= Idle;
                  if fault_out = '1' then 
                      faulty_packet_in <= '1';
                  else
                      faulty_packet_in <= '0';
                  end if;
              else
                  state_in <= state_out;
              end if;
            else
              -- we got a healthy header in the previous step!
              if fault_out = '1' then 
                -- new flit is faulty which should be a body! so we put a tail there
                faulty_packet_in <= '1';
                case( write_pointer ) is
                    when "0001" => FIFO_MEM_1_in <= fake_tail;  FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
                    when "0010" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= fake_tail;  FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
                    when "0100" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= fake_tail;  FIFO_MEM_4_in <= FIFO_MEM_4; 
                    when "1000" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= fake_tail;                  
                    when others => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
                end case ;
                state_in <= Body_flit;
              else
                -- all is good
                if flit_type = "010" then
                  state_in <= Body_flit;
                else
                  state_in <= state_out;
                end if;
              end if;
            end if;

          when Body_flit =>
             if faulty_packet_out = '1' then
              -- packet is already faulty
              faulty_packet_in <= faulty_packet_out;
              FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
              if flit_type = "100" then
                  -- the tial also has been dumped! we can just move to ordinary execution of things!
                  state_in <= Idle;
              elsif flit_type = "001" then
                  -- the tail has been faulty and since we came back here, we figured out that a header flit is waiting... 
                  state_in <= Header_flit;
                  if fault_out = '1' then 
                      -- is this new header flit ok?
                      faulty_packet_in <= '1';
                  else
                      faulty_packet_in <= '0';
                  end if;
              else
                  state_in <= state_out;
              end if;
            else
              if fault_out = '1' then 
                -- new flit is faulty
                -- we dont care, we just add a fake tail!
                faulty_packet_in <= '1';
                case( write_pointer ) is
                    when "0001" => FIFO_MEM_1_in <= fake_tail;  FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
                    when "0010" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= fake_tail;  FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
                    when "0100" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= fake_tail;  FIFO_MEM_4_in <= FIFO_MEM_4; 
                    when "1000" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= fake_tail;                  
                    when others => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
                end case ;
                state_in <= state_out;
              else
                -- all is good
                if flit_type = "100" then
                  state_in <= Tail_flit;
                else
                  state_in <= state_out;
                end if;
              end if;
            end if;
          
          when Tail_flit =>
            if fault_out = '1' then 
              -- new header flit is faulty
              faulty_packet_in <= '1';
              FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
            else
              faulty_packet_in <= '0';
              -- all is good
              if flit_type = "001" then
                state_in <= Header_flit;
              else
                state_in <= Idle;
              end if;
            end if;
 

          when others => state_in <= state_out;
      end case;
    --else
    --    state_in <= state_out;
    --end if; 
end process;

   -- combinatorial part
 

  process(read_pointer, FIFO_MEM_1, FIFO_MEM_2, FIFO_MEM_3, FIFO_MEM_4)begin
    case( read_pointer ) is
        when "0001" => Data_out <= FIFO_MEM_1;
        when "0010" => Data_out <= FIFO_MEM_2;
        when "0100" => Data_out <= FIFO_MEM_3;
        when "1000" => Data_out <= FIFO_MEM_4;
        when others => Data_out <= FIFO_MEM_1; 
    end case ;
  end process;

  read_en <= (read_en_N or read_en_E or read_en_W or read_en_S or read_en_L) and not empty; 
  empty_out <= empty;
  

  process(write_en, write_pointer)begin
    if write_en = '1'then
       write_pointer_in <= write_pointer(2 downto 0)&write_pointer(3); 
    else
       write_pointer_in <= write_pointer; 
    end if;
  end process;

  process(read_en, empty, read_pointer)begin
       if (read_en = '1' and empty = '0') then
           read_pointer_in <= read_pointer(2 downto 0)&read_pointer(3); 
       else 
           read_pointer_in <= read_pointer; 
       end if;
  end process;

  process(full, valid_in) begin
     if valid_in = '1' and full ='0' then
         write_en <= '1';
     else
         write_en <= '0';
     end if;        
  end process;
                        
  process(write_pointer, read_pointer) begin
      if read_pointer = write_pointer  then
              empty <= '1';
      else
              empty <= '0';
      end if;
      --      if write_pointer = read_pointer>>1 then
      if write_pointer = read_pointer(0)&read_pointer(3 downto 1) then
              full <= '1';
      else
              full <= '0'; 
      end if; 
  end process;

end;