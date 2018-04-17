.386
.MODEL FLAT

EXTRN compare_floats_proc : Near32

INCLUDE compare_floats.h
INCLUDE debug.h
INCLUDE float.h
INCLUDE io.h
INCLUDE compute_bs.h

PUBLIC interpolate

array_addy 	EQU		[ebp + 14]
x_coord		EQU		[ebp + 10]
degree		EQU		[ebp + 8]
words		EQU		[ebp - 4]
storage		EQU		[ebp - 8]
zeros		EQU		[ebp - 12]

.CODE

interpolate_proc	PROC	NEAR32

			push ebp
			mov ebp, esp
			pushd 0
			pushd 0
			pushw 0
			push eax
			push ebx
			push ecx 
			pushf
			fldz
		
			mov ebx, array_addy
			
comp_b:		
			 
			
			compute_bs array_addy, WORD PTR degree, WORD PTR words
			;fstp DWORD PTR words
			mov al, degree
			dec al
			mov degree, al
			
			;ftoa words, 6, 20, storage
			;output storage
			
			;mov eax, 0
			;mov al, degree
			cmp al, 0
			je last
			;dec al
			shl al, 3
			fld REAL4 PTR [ebx + [eax]]
			;fstp REAL4 PTR words
			;ftoa words, 6, 20, storage
			;output storage
			fld REAL4 PTR x_coord
			fsub
			;fld REAL4 PTR words
			fmul
next_x:
			cmp al, 0
			je addi
			dec al
			shl al, 3
			fld REAL4 PTR [ebx + [eax]]
			fld REAL4 PTR x_coord
			fsub
			fmul
			jmp next_x
			

addi:	
			fld REAL4 PTR storage
			fadd
			fstp REAL4 PTR storage
			jmp comp_b
last:
			;fld REAL4 PTR words
			fadd REAL4 PTR storage
			fst REAL4 PTR words
			ftoa words, 6, 20, storage
			output storage
			fstp REAL4 PTR storage
finish:			
			popf
			pop ecx
			pop ebx
			pop eax
			mov esp, ebp
			pop ebp
			
			ret 10
			

interpolate_proc	ENDP



END