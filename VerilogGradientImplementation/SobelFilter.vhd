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
		--in_one 	:	in std_logic_vector(0 to 2);
		in11, in12, in13, in21, in22, in23, in31, in32, in33  :    in std_logic_vector(2 downto 0);
		output    :   out std_logic_vector(2 downto 0);
		--out_value	:	out integer
		--out_one	:	out std_logic_vector(0 to 2)
);
end SobelFilter;

architecture Behavioral of SobelFilter is

type	mat is array(2 downto 0, 2 downto 0) of integer;

variable energyMatrix	    :	mat;
variable gradientYMatrix    :   mat;
variable gradientXMatrix    :   mat;
variable Gx                 :   std_logic_vector(2 downto 0) := "000";
variable Gy                 :   std_logic_vector(2 downto 0) := "000";
variable GxInt              :   integer := 0;
variable GyInt              :   integer := 0;
variable Gtemp              :   integer := 0;
variable G                  :   integer := 0;

begin

energyMatrix <= (
	(in11, in12, in13),
    (in21, in22, in23),
    (in31, in32, in33)
);

gradientYMatrix <= (
    (not(in11)+"001", not(in12 sll 1)+"001", not(in13)+"001"),
    (0, 0, 0),
    (in31, in32 sll 1, in33)
);

gradientXMatrix <= (
    (not(in11)+"001", 0, in13),
    (not(in21 sll 1)+"001", 0, in23),
    (not(in31)+"001", 0, in33)
);

for i in 0 to 2 loop
begin
    for j in 0 to 2 loop
    begin
        Gx := Gx + gradientXMatrix(i,j);
        Gy := Gy + gradientYMatrix(i,j);
    end loop;
end loop;

GxInt := to_integer(signed(Gx));
GyInt := to_integer(signed(Gy));

Gtemp := GxInt*GxInt + GyInt*GyInt

output  <= std_logic_vector(to_unsigned(Gtemp, 3)) srl 2;--variable energyValues is std_logic_vector(0 to 32, 0 to 32);
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

