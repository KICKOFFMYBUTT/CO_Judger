L0: j JB
L1: ori $t0 $0 50
L2: addiu $t1 $t0 100
L3: andi $t2 $t1 200
L4: ori $t3 $t2 300
L5: xori $t4 $t3 400
j END
JB:
j L1

END:
nop
