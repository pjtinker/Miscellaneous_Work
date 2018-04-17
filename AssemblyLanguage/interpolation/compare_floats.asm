.386
.MODEL FLAT

PUBLIC	compare_floats_proc

; fcom compares st and st(1)
; fcom memory compares st and real number in memory
; result of comparison
; ST > second operand: C3 (bit 14 of status word), C2 (bit 10), C0 (bit 8) are all set to 0
; ST < second operand: C3 set to 0, C2 set to 0, C0 set to 1
; ST = second operand: C3 set to 1, C2 set to 0, C0 set to 0
; thus, check ST < first, then ST equal, otherwise, ST >

; use below to isolate the relevant bits after a comparison
C3 EQU 0100000000000000b
C2 EQU 0000010000000000b
C0 EQU 0000000100000000b

.DATA
zero  REAL4   0.0

.CODE

f1    		EQU [ebp + 16]
f2    		EQU [ebp + 12]
tol     	EQU [ebp + 8]   ; if two floats are within this amount of one another, they are equal

; -1 returned in ax if f1 < f2, 0 if f1 = f2, 1 if f1 > f2
temp    EQU [ebp - 4]

compare_floats_proc		PROC 	Near32

setup:

     	push	ebp
		mov	ebp, esp	   
        pushd   0         
		pushf 			 

        fld DWORD PTR f2
        fld DWORD PTR f1    ; f1 is in st(0), f2 in st(1)
        fsubr               ; f1 - f2
        fld st              ; copy the result of the subtraction on the stack
        fabs				;take absolute value of what is store in st(0)

        fstp DWORD PTR temp ;ambiguious, so we need the DWORD.  
		pushd temp          ; |f1 - f2|
		pushd tol
        call compare_floats_bit_by_bit ;returns -1, 0, or 1 in ax
        fstp DWORD PTR temp ; clear out stack in case we are finished.  Could use REAL4 PTR here also

        cmp ax, 0           ; absolute value of f1 - f2 is less than or equal to tol (return 0 for equality)
        jle equal

        pushd temp          ; (f1 - f2)
        push zero
        call compare_floats_bit_by_bit

        cmp ax, -1          ; if the result is negative, f1 is smaller than f2
        je smaller

larger:

        ; f1 larger
        mov ax, 1
        jmp finish

equal:

        mov ax, 0
        jmp finish

smaller:

        ; f1 smaller
        mov ax, -1

finish:

		popf		
        mov     esp, ebp	
		pop		ebp
		ret		12	

compare_floats_proc		ENDP


compare_floats_bit_by_bit	PROC 	Near32

f1_    	EQU [ebp + 12]
f2_    	EQU [ebp + 8]
; -1 returned in ax if f1 < f2, 0 if f1 = f2, 1 if f1 > f2

setup:

     	push	ebp
		mov		ebp, esp            
		pushf 		

        fld DWORD PTR f2_
        fld DWORD PTR f1_        ; set up to compare f1 to f2 (f1 in st(0), f2 in st(1))
        fcompp 					;compares values 
        fstsw ax				;load the status word into ax.  FP flag.  For bit comparison
        test ax, C0               ; result is 1 if st < second operand.  test does a bitwise and, bit by bit.
									;C0 is a variable set to where the flag we want to compare is located in flags register
        jnz smaller

        test ax, C3               ; result is 1 if st = second operand (exact match)
        jnz equal

larger:

        ; f1 larger
        mov ax, 1
        jmp finish

equal:

        mov ax, 0
        jmp finish

smaller:

        ; f1 smaller
        mov ax, -1

finish:

		popf			
        mov     esp, ebp	
		pop		ebp
		ret		8	

compare_floats_bit_by_bit	ENDP

END

