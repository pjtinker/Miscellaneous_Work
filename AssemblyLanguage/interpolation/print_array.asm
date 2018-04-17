.386
.MODEL FLAT

INCLUDE debug.h
INCLUDE float.h

PUBLIC print_array_proc

array_addr 		EQU 		[ebp+10]
array_size		EQU			[ebp+8]
t			EQU			[ebp-10]

.CODE

print_array_proc       PROC   Near32
			; entry code
			push ebp ;we must push ebp on  the stack.  
			mov ebp, esp ;move stack pointer address to ebp
			;local vars here
			pushd 0
			
			push eax
			push ebx
			push ecx
			;push registers (which ones should be saved?)
			pushf

					mov ecx, 0
					mov cx, array_size
					mov ebx, array_addr

print_loop:
					;mov eax, [ebx]
					ftoa [ebx], 3, 20, t
					output t    
					add ebx, 4 
					output carriage
					loop print_loop
			
			; exit code
			popf
			;pop registers
			pop ecx
			pop ebx
			pop eax
			mov esp, ebp
			pop ebp
			ret 6
print_array_proc      ENDP

END                    

