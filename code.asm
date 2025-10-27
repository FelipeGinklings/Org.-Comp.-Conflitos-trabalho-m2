_start:
    # I-type instructions (Immediate)
    addi t0, zero, 15      # t0 = 0 + 15
    addi t1, zero, 7       # t1 = 0 + 7
    nop
    xori t2, t0, 0xFF      # t2 = t0 XOR 0xFF
    nop
    ori  t3, t1, 0x0F      # t3 = t1 OR 0x0F
    andi t4, t0, 0x0F      # t4 = t0 AND 0x0F
    
    # R-type instructions (Register-Register)
    nop
    nop
    add  t5, t0, t1        # t5 = t0 + t1
    sub  t6, t0, t1        # t6 = t0 - t1
    and  s0, t0, t1        # s0 = t0 & t1
    or   s1, t0, t1        # s1 = t0 | t1
    xor  s2, t0, t1        # s2 = t0 ^ t1
    sll  s3, t0, t1        # s3 = t0 << t1
    srl  s4, t0, t1        # s4 = t0 >> t1 (logical)
    
    # S-type instructions (Store)
    # Use stack pointer for storing (sp points to valid memory)
    addi sp, sp, -16       # Allocate stack space
    sw   t0, 0(sp)         # Store t0 at sp[0]
    sh   t1, 4(sp)         # Store halfword t1 at sp[4]
    sb   t2, 8(sp)         # Store byte t2 at sp[8]
    
    # B-type instructions (Branch)
    beq  t0, t1, equal     # Branch if t0 == t1
    bne  t0, t1, not_equal # Branch if t0 != t1
    
equal:
    addi s5, zero, 1       # s5 = 1 (if equal)
    j    after_branch      # Jump over next part
    
not_equal:
    addi s5, zero, 2       # s5 = 2 (if not equal)
    
after_branch:
    blt  t1, t0, less_than # Branch if t1 < t0
    bge  t1, t0, greater_equal # Branch if t1 >= t0
    
less_than:
    addi s6, zero, 1       # s6 = 1
    j    after_branch2
    
greater_equal:
    addi s6, zero, 2       # s6 = 2
    
after_branch2:
    # U-type instructions (Upper Immediate)
    lui  a0, 0x12345       # a0 = 0x12345000
    auipc a1, 0x1000       # a1 = PC + (0x1000 << 12)
    
    # J-type instructions (Jump)
    jal  ra, function      # Jump to function, save return address in ra
    
    # Load what we stored earlier (demonstrating load instructions)
    lw   s7, 0(sp)         # Load word from sp[0]
    lh   s8, 4(sp)         # Load halfword from sp[4]
    lb   s9, 8(sp)         # Load byte from sp[8]
    
    # Clean up stack
    addi sp, sp, 16        # Deallocate stack space
    
    # Exit program
    li   a7, 93            # Exit system call
    li   a0, 0             # Exit code 0
    ecall

function:
    # Simple function that does nothing
    addi a2, zero, 42      # a2 = 42
    ret                    # Return to caller