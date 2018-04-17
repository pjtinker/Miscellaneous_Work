.386
.MODEL FLAT

PUBLIC move_to_index_proc

						; the address will be returned in ebx (assumes a WORD array)
array_addr      	EQU [ebp + 10]   ; the address of index 0 of the array (DWORD)
index           	EQU [ebp + 8]    ; the requested index (WORD) 1-based

.CODE

move_to_index_proc      PROC   Near32

     	push	ebp
		mov		ebp, esp	      
		push    eax		     
		pushf 			   

               ; get the address in the array (random access)
               mov ebx, array_addr
               mov eax, 0 
               mov ax, index      
               dec ax             		; adjust for 1 indexing (index passed is 1-based)
               add eax, eax       	; multiply ax by 2 for the correct address in the array
											; (or add eax to itself) 
               add ebx, eax

		popf			    
		pop		eax
        mov		esp, ebp	      
		pop		ebp
		ret		6		      ; return, discarding parameters by moving ESP up 6 (4 + 2 bytes were added as parameters)

move_to_index_proc      ENDP

END                    

