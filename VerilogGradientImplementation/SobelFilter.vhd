----------------------------------------------------------------------------------
-- Company: ATLAS gFEX
-- Engineer: Elliot Parrish
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
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity SobelFilter is
port(	clk, reset:	in STD_Logic;
		--in_array	:	in array(8 downto 0) of integer;
		in_one 	:	in std_logic_vector(0 to 2);
		out_value	:	out integer
		--out_one	:	out std_logic_vector(0 to 2)
);
end SobelFilter;

architecture Behavioral of SobelFilter is

type	mat is array(2 downto 0, 2 downto 0) of integer;

variable energyMatrix	:	mat;

energyMatrix := (
	(in_array(0), in_array(1), in_array(2)),
	(in_array(3), in_array(4), in_array(5)),
	(in_array(6), in_array(7), in_array(8))
);
begin

--variable energyValues is std_logic_vector(0 to 32, 0 to 32);
--variable yfilter is std_logic_vector(0 to 2, 0 to 2);
--yfilter(0,0) := -1;
--yfilter(1,0) := -2;
--yfilter(2,0) := -1;
--yfilter(0,1) :=  0;
--yfilter(1,1) :=  0;
--yfilter(2,1) :=  0;
--yfilter(0,2) :=  1;
--yfilter(1,2) :=  2;
--yfilter(2,2) :=  1;
--variable xfilter is std_logic_vector(0 to 2, 0 to 2) of integer;
--xfilter(0,0) := -1;
--xfilter(1,0) :=  0;
--xfilter(2,0) :=  1;
--xfilter(0,1) := -2;
--xfilter(1,1) :=  0;
--xfilter(2,1) :=  2;
--xfilter(0,2) := -1;
--xfilter(1,2) :=  0;
--xfilter(2,2) :=  1;

end Behavioral;

