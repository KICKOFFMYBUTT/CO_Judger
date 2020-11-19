`timescale 1ns/1ps
module tb_mips;
    reg clk;
    reg reset = 1;

    mips uut (
        .clk(clk), 
        .reset(reset)
    );

    initial begin
        clk = 0;
        #10 reset = 0;
        #50000000 $finish;
    end
    always #5 clk = ~clk;
endmodule