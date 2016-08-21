----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/21/2016 01:00:19 PM
-- Design Name: 
-- Module Name: SobelFilter_tb - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity SobelFilter_tb is
--  Port ( );
end SobelFilter_tb;

architecture Behavioral of SobelFilter_tb is

    component SobelFilter is
        generic(n_bits  :   integer := 8);
        
        port(   clk, reset :   in STD_Logic; --Using clk, might need reset to reset values? not sure
                in11, in12, in13, in21, in22, in23, in31, in32, in33  :   in std_logic_vector(n_bits-1 downto 0); --might in the future have one bitstream we need to divide up
                output      :   out std_logic_vector(n_bits-1 downto 0)
 
        );
        
        signal in11s, in12s, in13s, in21s, in22s, in23s, in31s, in32s, in33s, outputs   :   std_logic_vector(n_bits-1 downto 0);

begin
    mapping SobelFilter port map(in11s, in12s, in13s, in21s, in22s, in23s, in31s, in32s, in33s, outputs);

    process
    begin
    
    in11s <= (others=>'0');
    in12s <= (others=>'0');
    in13s <= (others=>'0');
    in21s <= (others=>'0');
    in22s <= (others=>'0');
    in23s <= (others=>'0');
    in31s <= (others=>'0');
    in32s <= (others=>'0');
    in33s <= (others=>'0');

    wait for 1 ns;

    end process;
    

end Behavioral;
