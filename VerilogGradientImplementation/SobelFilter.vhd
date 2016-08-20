----------------------------------------------------------------------------------
-- Company: ATLAS gFEX
-- Engineer: The Spanish Flea
-- 
-- Create Date:    13:01:34 08/10/2016 
-- Design Name: 
-- Module Name:    SobelFilter - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: Magical syntax error near line 62. No idea what is actually happening.
--
----------------------------------------------------------------------------------
library IEEE;
    use IEEE.STD_LOGIC_1164.ALL;
    use IEEE.NUMERIC_STD.ALL;
    use IEEE.STD_LOGIC_UNSIGNED.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity SobelFilter is
    generic(n_bits  :   integer := 8);
    port(clk, reset :   in STD_Logic; --Using clk, might need reset to reset values? not sure
        --in_array  :   in array(8 downto 0) of integer;
        --in_one    :   in std_logic_vector(0 to 2);
        in11, in12, in13, in21, in22, in23, in31, in32, in33  :   in std_logic_vector(n_bits-1 downto 0); --might in the future have one bitstream we need to divide up
        output      :   out std_logic_vector(n_bits-1 downto 0)
        --out_value :   out integer
        --out_one   :   out std_logic_vector(0 to 2)
    );
end entity;

architecture Behavioral of SobelFilter is

    type    mat is array(2 downto 0, 2 downto 0) of std_logic_vector(n_bits-1 downto 0);
    
        
   
begin

    process(clk)
    variable energyMatrix       :   mat;
    variable gradientYMatrix    :   mat;
    variable gradientXMatrix    :   mat;
    variable Gx                 :   std_logic_vector(n_bits-1 downto 0) := (others=>'0');
    variable Gy                 :   std_logic_vector(n_bits-1 downto 0) := (others=>'0');
    variable GxInt              :   integer := 0;
    variable GyInt              :   integer := 0;
    variable Gtemp              :   integer := 0;
    variable G                  :   integer := 0;
    variable outputtemp         :   std_logic_vector(n_bits-1 downto 0) := (others=>'0');
    constant makeNegative       :   std_logic_vector(n_bits-1 downto 0) := (0 => '1', others => '0');
    constant zeroes             :   std_logic_vector(n_bits-1 downto 0) := (others => '0');
    
    begin
 
        gradientYMatrix := (
            (not(in11)+makeNegative,                    not(in12(1 downto 0) & '0')+makeNegative,   not(in13)+makeNegative),
            (zeroes,                                    zeroes,                                     zeroes),
            (in31,                                      in32(1 downto 0) & '0',                     in33)
        );
    
        gradientXMatrix := (
            (not(in11)+makeNegative,                    zeroes,                                     in13),
            (not(in21(1 downto 0) & '0')+makeNegative,  zeroes,                                     in23(1 downto 0) & '0'),
            (not(in31)+makeNegative,                    zeroes,                                     in33)
        );
    
        if rising_edge(clk) then
        
            for i in 0 to 2 loop
                for j in 0 to 2 loop
                    Gx := Gx + gradientXMatrix(i,j);
                    Gy := Gy + gradientYMatrix(i,j);
                end loop;
            end loop;
        end if;
    
        GxInt       :=  to_integer(signed(Gx));
        GyInt       :=  to_integer(signed(Gy));
        
        Gtemp       :=  GxInt*GxInt + GyInt*GyInt;
        outputtemp  :=  std_logic_vector(to_unsigned(Gtemp, n_bits)); --if testbed failes then maybe move this outside process
        output      <=  "00" & outputtemp(n_bits-1 downto 2);
        --variable energyValues is std_logic_vector(0 to 32, 0 to 32);
        --variable yfilter is std_logic_vector(0 to 2, 0 to 2);
    end process;
    --output      <=  "00" & outputtemp(nbits-1 downto 2);
end architecture;
