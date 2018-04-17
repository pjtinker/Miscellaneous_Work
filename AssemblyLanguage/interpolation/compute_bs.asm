 .386
.MODEL FLAT

EXTRN compare_floats_proc : Near32

INCLUDE compare_floats.h
INCLUDE debug.h
INCLUDE float.h
INCLUDE io.h



PUBLIC compute_bs_start, compute_bs_proc


array_addy	EQU	 [ebp + 12]
m			EQU  [ebp + 10];m is lower index
degree		EQU  [ebp + 8];degree is n
words		EQU  [ebp - 4]
storage		EQU  [ebp - 8]




.CODE

compute_bs_start    PROC	NEAR32
			
			push ebp
			mov ebp, esp
			pushd 0
			pushd 0
			push eax
			push ebx
			push ecx
			
			
			pushfd
			
			pushd array_addy
			pushw m
		
			pushw degree
		
			call compute_bs_proc
			
			popfd
			
			pop ecx
			pop ebx
			pop eax
			mov esp, ebp
			pop ebp
			
			ret 8
			
compute_bs_start	ENDP

compute_bs_proc		PROC	NEAR32
			push ebp
			mov ebp, esp
			pushd 0
			pushd 0
			pushfd
			mov ax, 0
			mov bx, 0
			mov ax, m
			mov bx, degree
			
			cmp ax, bx
			je	retrieve
			
			inc ax
			mov m, ax
			
			pushd array_addy
			pushw m
			pushw degree
			call compute_bs_proc
			
			mov ax, m
			dec ax
			mov m, ax
			
			mov ax, degree
			dec ax
			mov degree, ax
			
			pushd array_addy
			pushw m
			pushw degree
			call compute_bs_proc
			
			mov ax, degree
			inc ax
			mov degree, ax
			;at this point b0 should be at st(1)
			;b1 at st(0)
			fsub ;now stores numerator
			fstp REAL4 PTR words
			
			mov eax, 0
			mov ebx, array_addy
			mov al, degree
			shl al, 3
			
			fld REAL4 PTR [ebx + [eax]]
		
			output storage
			mov eax, 0
			mov al, m
		
			shl al, 3
			
			fld REAL4 PTR [ebx + [eax]]
			
			fsub
			fld REAL4 PTR words
			fdivr
		
			
			jmp fini
			

retrieve:    ;here we're getting the y value for b0
			mov eax, 0
			mov ebx, array_addy
			;outputW degree
			mov al, degree;this overshoots second pull!
			inc al
			shl al, 1
			dec al
			shl al, 2
			
			
			fld REAL4 PTR [ebx + [eax]] 
			
		
fini:
			
			
			popfd
			
			mov esp, ebp
			pop ebp
			ret 8
		
compute_bs_proc			ENDP

END