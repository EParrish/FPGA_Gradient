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
    --use IEEE.STD_LOGIC_UNSIGNED.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity SobelFilter is
    generic(n_bits  :   integer := 12);
    port(clk, reset :   in STD_Logic; --Using clk, might need reset to reset values? not sure
        in11, in12, in13, in21, in22, in23, in31, in32, in33  :   in std_logic_vector(n_bits-1 downto 0); --might in the future have one bitstream we need to divide up
        output      :   out std_logic_vector(n_bits+1 downto 0)
    );
end entity;

architecture Behavioral of SobelFilter is

    type    mat is array(2 downto 0, 2 downto 0) of std_logic_vector(n_bits-1 downto 0);
    
        
   
begin

    process(clk, reset)
    variable energyMatrix       :   mat;
    variable gradientYMatrix    :   mat;
    variable gradientXMatrix    :   mat;
    variable Gx                 :   std_logic_vector(n_bits-1 downto 0);-- := (others=>'0');
    variable Gy                 :   std_logic_vector(n_bits-1 downto 0);-- := (others=>'0');
    variable GxInt              :   integer;-- := 0;
    variable GyInt              :   integer;-- := 0;
    variable Gtemp              :   integer;-- := 0;
    variable G                  :   integer;-- := 0;
    variable outputtemp         :   std_logic_vector(n_bits+3 downto 0);-- := (others=>'0');
    constant makeNegative       :   std_logic_vector(n_bits-1 downto 0) := (0 => '1', others => '0');
    constant zeroes             :   std_logic_vector(n_bits-1 downto 0) := (others => '0');
    
    begin
-- Matrices don't work, but here's a schematic of them: 
--        gradientYMatrix := (
--            (std_logic_vector(signed(not(in11))+signed(makeNegative)),  std_logic_vector(signed(not(in12(n_bits-2 downto 0) & '0'))+signed(makeNegative)),     std_logic_vector(signed(not(in13))+signed(makeNegative))),
--            (zeroes,                                                    zeroes,                                                                         zeroes),
--            (in31,                                                      in32(n_bits-2 downto 0) & '0',                                                  in33)
--        );
    
--        gradientXMatrix := (
--            (std_logic_vector(signed(not(in11))+signed(makeNegative)),                              zeroes,     in13),
--            (std_logic_vector(signed(not(in21(n_bits-2 downto 0) & '0'))+signed(makeNegative)),     zeroes,     in23(n_bits-2 downto 0) & '0'),
--            (std_logic_vector(signed(not(in31))+signed(makeNegative)),                              zeroes,     in33)
--        );
    
        if (reset = '1') then
            output <= (others => '0');
        --end if;
            
        elsif (rising_edge(clk)) then
        
            --for i in 0 to 2 loop
             --   for j in 0 to 2 loop
              --      --Gx := std_logic_vector(signed(Gx) + signed(gradientXMatrix(i,j)));
              --      Gy := std_logic_vector(signed(Gy) + signed(gradientYMatrix(i,j)));
               -- end loop;
            --end loop;
        Gx := std_logic_vector((signed(not(in11))+signed(makeNegative)) + (signed(not(in12(n_bits-2 downto 0) & '0'))+signed(makeNegative)) + (signed(not(in13))+signed(makeNegative)) + signed(in31) + signed(in32(n_bits-2 downto 0) & '0') + signed(in33));
        --Gx := std_logic_vector(signed(in33)-signed(in11)-signed(in12(n_bits-2 downto 0) & '0')-signed(in13) + signed(in31) + signed(in32(n_bits-2 downto 0) & '0'));

        Gy := std_logic_vector((signed(not(in11))+signed(makeNegative)) + signed(in13) + (signed(not(in21(n_bits-2 downto 0) & '0'))+signed(makeNegative)) + signed(in23(n_bits-2 downto 0) & '0') + (signed(not(in31))+signed(makeNegative)) + signed(in33));
        
        --end if;
    
        GxInt       :=  to_integer(signed(Gx));
        GyInt       :=  to_integer(signed(Gy));
        
        Gtemp       :=  GxInt*GxInt + GyInt*GyInt;
        outputtemp  :=  std_logic_vector(to_unsigned(Gtemp, n_bits+4)); --if testbed failes then maybe move this outside process
        output      <=  outputtemp(n_bits+3 downto 2);
        
--        else 
--            output <= (others => '0');
        end if;    

        --variable energyValues is std_logic_vector(0 to 32, 0 to 32);
        --variable yfilter is std_logic_vector(0 to 2, 0 to 2);
    end process;
end architecture;
