; In R8, we put the number to raise to the power we put in R9.
      400000 ADDI R8, R0, 2
      400004 ADDI R9, R9, 10
      400008 JAL 1000040
      40000C SYSCALL

power: 400010 ADD R16, R0, R8
loop: 400014 MULT R8, R16
      400018 MFLO R8
      40001C ADDI R9, R9, -1
      400020 ADDI R10, R0, 1
      400024 BNE R9, R10, -5
      400028 JR R31