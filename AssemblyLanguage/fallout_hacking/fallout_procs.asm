.386
.MODEL FLAT

INCLUDE io.h
INCLUDE debug.h
INCLUDE strutils.h
PUBLIC match_proc, swap_proc, disp_arr_proc, process_guess_proc

.CODE

;wordOne EQU [ebp + 16]
;wordTwo EQU [ebp + 12]
;len		EQU [ebp + 10]
;arr_sz  EQU [ebp + 8]


match_proc		PROC	NEAR32
;returns the count of matches found between two strings.
;returns the matches found in ax
wordOne EQU [ebp + 14]
wordTwo EQU [ebp + 10]
len		EQU [ebp + 8]
			push ebp
			mov ebp, esp
			
			push edi
			push esi
			push ecx
			pushf
			
			mov esi, wordOne

			mov edi, wordTwo

			mov ecx, 0
			mov eax, 0
		
			mov cx, ax
			mov ax, 0
			mov cx, len
			dec cx
			dec cx
			cld
			
	begin:
			repne cmpsb
			jz count
		
			jmp finish
			
	count:
			inc ax
			jmp begin
			
	finish:
			
			popf
			pop ecx
			pop esi
			pop edi
			
			mov esp, ebp
			pop ebp
			ret 10
			
match_proc		ENDP


swap_proc	PROC	NEAR32

wordOne EQU [ebp + 14]
wordTwo EQU [ebp + 10]
len		EQU [ebp + 8]


			push ebp
			mov ebp, esp
			push edi
			push esi
			push ecx
			push eax
			pushfd
				mov ecx, 0
				mov esi, wordOne
				mov edi, wordTwo
				mov cx, len
				dec cx;why does this change anything?
				dec cx
				cld
				
		begin:  
				cmp cx, 0
				je finish
				lodsb
				mov ah, BYTE PTR [edi]
				;dec esi
				;movsb
				stosb
				dec esi
				;dec edi
				;stosb
				mov BYTE PTR [esi], ah
				inc esi
				dec cx
				jmp begin
		finish:
				output [esi]
				output carriage
				output [edi]
				output carriage

			pop ax
			popfd
			pop eax
			pop ecx
			pop esi
			pop edi
			
			mov esp, ebp
			pop ebp
			ret 10
			

swap_proc   ENDP

process_guess_proc	PROC	NEAR32

array_addy	EQU	[ebp + 16]
array_sz	EQU [ebp + 14]
len			EQU [ebp + 12]
index		EQU [ebp + 10]
num_match	EQU [ebp + 8]
		
		push ebp
		mov ebp, esp
		push eax
		push ecx
		push edx
		push esi
		push edi
		pushfd
				mov eax, 0
				mov edx, 0
				mov ecx, 0
				mov cx, WORD PTR index
				dec cx
				mov ax, len
				mul cx
				mov edx, array_addy
				add edx, eax
				mov ebx, array_addy
				mov cx, 0
				mov cl, array_sz
				mov esi, edx
				;output [esi]
				;output carriage
				;mov edi, ebx
				;output [edi]
				;output carriage
				
			begin:
				cmp cl, 0
				je finish
				
				push ebx
				push edx
				push WORD PTR len
				call match_proc
				outputW ax
				cmp ax, num_match
				
				je swap
				add bl, len
				dec cl
				jmp begin
				
			swap:
				;push ebx
				;push edx
				;push WORD PTR len
				;call swap_proc
				;mov esi, ebx
				;output [esi]
				;add ebx, len
				;dec cl
				;jmp begin
			finish:
				
		
		popfd
		pop edi
		pop esi
		pop edx
		pop ecx
		pop eax
		mov esp, ebp
		pop ebp
		ret 12
process_guess_proc  ENDP

disp_arr_proc		PROC	
array_addy	EQU	[ebp + 12]
array_sz	EQU	[ebp + 10]
len			EQU [ebp + 8]
					
		push ebp
		mov ebp, esp
		push eax
		push ecx
		pushfd
					mov cx, array_sz
					;mov al, BYTE PTR len
					
					
				begin:
					cmp cx, 0
					je done
					output BYTE PTR [ebx]
					output carriage
					add bl, len
					dec cx
					jmp begin
						
				done:
				
		popfd
		pop ecx
		pop eax
		mov esp, ebp
		pop ebp
		ret 8
disp_arr_proc      ENDP
				
END