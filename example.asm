irmovq $15,%rbx
rrmovq %rbx,%rcx
loop
rmmovq %rcx,-3(%rbx)
addq %rbx,%rcx
jmp loop
