    40000 ADD R8, R0, R0
    40004 J LABEL1
    40008 ADDI R8, R8, -1
LABEL1: 4000C ADDI R8, R8, 1

    40010 ADD R9, R0, R0
    40014 BEQ R9, R0, 1
    40018 ADDI R8, R8, -1
LABEL2: 4001C ADDI R8, R8, 1

    40020 ADDI R9, R0, 1
    40024 BEQ R9, R0, 1
    40028 ADDI R8, R8, -1
LABEL3: 4002C ADDI R8, R8, 1

    40030 ADDI R9, R0, 1
    40034 BNE R9, R0, 1
    40038 ADDI R8, R8, -1
LABEL4: 4003C ADDI R8, R8, 1

