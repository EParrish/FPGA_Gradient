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
-- Testbench created online at:
--   www.doulos.com/knowhow/perl/testbench_creation/
-- Copyright Doulos Ltd
-- SD, 03 November 2002

-- Website where test bench is generated:
-- https://www.doulos.com/knowhow/perl/testbench_creation/

library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity SobelFilter_tb is
end;

architecture bench of SobelFilter_tb is

  component SobelFilter
      generic(n_bits  :   integer := 12);
      port(clk, reset :   in STD_Logic;
          in11, in12, in13, in21, in22, in23, in31, in32, in33  :   in std_logic_vector(n_bits-1 downto 0);
          output      :   out std_logic_vector(n_bits+1 downto 0)
      );
  end component;

  signal n_bits :   integer := 12;
  signal clk, reset: STD_Logic;
  signal in11, in12, in13, in21, in22, in23, in31, in32, in33: std_logic_vector(n_bits-1 downto 0);
  signal output: std_logic_vector(n_bits+1 downto 0) ;

  constant clock_period:    time    :=  14 ns;
  constant reset_period:    time    :=  10 ns;
  signal stop_the_clock: boolean;

begin

  -- Insert values for generic parameters !!
  uut: SobelFilter generic map ( n_bits => n_bits )
                      port map ( clk    => clk,
                                 reset  => reset,
                                 in11   => in11,
                                 in12   => in12,
                                 in13   => in13,
                                 in21   => in21,
                                 in22   => in22,
                                 in23   => in23,
                                 in31   => in31,
                                 in32   => in32,
                                 in33   => in33,
                                 output => output );

  stimulus: process
  begin
  
    -- Put initialisation code here
    
    in11    <=  (others => '0');
    in12    <=  (others => '0');
    in13    <=  (others => '0');
    in21    <=  (others => '0');
    in22    <=  (others => '0');
    in23    <=  (others => '0');
    in31    <=  (others => '0');
    in32    <=  (others => '0');
    in33    <=  (others => '0');

    wait for 9 ns;
    
    in11    <=  (1 => '1', others => '0');
    in12    <=  (1 => '1', 0 => '1', others => '0');
    in13    <=  (3 => '1', 1 => '1', others => '0');
    in21    <=  (1 => '1', 0 => '1', others => '0');
    in22    <=  (3 => '1', others => '0');
    in23    <=  (4 => '1', 3 => '1', others => '0');
    in31    <=  (1 => '1', others => '0');
    in32    <=  (2 => '1', 0 => '1', others => '0');
    in33    <=  (4 => '1', others => '0');
    
    wait for 400 ns;
    
    in11    <=  (1 => '1', others => '0');
    in12    <=  (others => '0');
    in13    <=  (others => '0');
    in21    <=  (others => '0');
    in22    <=  (others => '0');
    in23    <=  (others => '0');
    in31    <=  (others => '0');
    in32    <=  (others => '0');
    in33    <=  (others => '0');    
--    wait for 9 ns;

--    in11    <=  (others => '0');
--    in12    <=  (others => '0');
--    in13    <=  (others => '0');
--    in21    <=  (others => '0');
--    in22    <=  (others => '0');
--    in23    <=  (others => '0');
--    in31    <=  (others => '0');
--    in32    <=  (others => '0');
--    in33    <=  (others => '0');
    
    wait for 500 ns;
    -- Put test bench stimulus code here

    stop_the_clock <= true;
    wait;
  end process;

  clocking: process
  begin
    while not stop_the_clock loop
      clk <= '0', '1' after clock_period / 2;
      wait for clock_period;
    end loop;
    wait;
  end process;

  resets: process
  begin
    while not stop_the_clock loop
      reset <= '0', '1' after clock_period / 2;
      wait for reset_period;
    end loop;
    wait;
  end process;

end;
