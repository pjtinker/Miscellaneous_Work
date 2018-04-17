.386
.MODEL FLAT


ExitProcess PROTO NEAR32 stdcall, dwExitCode:DWORD

;;Paul Tinker
INCLUDE io.h
INCLUDE debug.h

.STACK  4096  
                
MAX_VAL		EQU		500

.DATA 
inp_prompt		BYTE 	" ", CR, LF, 0
path			WORD 	MAX_VAL DUP(0)
pctr			WORD	0
r				WORD	"r"
d				WORD	"d"
total_nodes		WORD	?
down			WORD	?
right			WORD	?
currR			WORD	?
currC			WORD	?
currI			WORD	?
rowCount		WORD	?
colCount		WORD	?
prows			WORD	?
pcols			WORD	?
rows			WORD	?
cols			WORD	?
matrix			WORD	MAX_VAL DUP(0)
matrix2			WORD	MAX_VAL DUP(0)
array_addy		WORD	?
output_val		WORD	?
index			WORD	?
what			WORD	200
truth			WORD	?
.CODE

index_conv		MACRO ro, co
					mov ax, 0
					mov ax, ro
					dec ax
					imul cols
					
					add ax, co
					dec ax	

				ENDM
				
set_element		MACRO ro, co, val, mat
				
					
					mov eax, 0
					index_conv ro, co
					mov cx, 2
					imul cx
					lea ebx, mat
					add ebx, eax
					mov ax, [ebx]
					add ax, val
					mov [ebx], ax

				ENDM
get_element		MACRO ro, co, mat
					mov eax, 0
					index_conv ro, co
					
					mov cx, 2
					imul cx
					lea ebx, mat
					add ebx, eax
					mov ax, [ebx]
						
				ENDM
				
create_matrix	MACRO mat, mat2, ind
					local _begin_loop, _copy
					
				inputW inp_prompt, rows
				inputW inp_prompt, cols
				
				mov ax, rows
				mov prows, ax
				mov cx, cols
				mov pcols, cx
				lea ebx, mat
				imul cx
				mov total_nodes, ax
				mov ind, ax

				
				_begin_loop:
					inputW inp_prompt, [ebx]
					add ebx, 2
					dec ind
					cmp ind, 0
					jg _begin_loop

					lea ebx, mat
					lea edx, mat2
					mov ax, 0
					mov cx, total_nodes
					
				_copy:
					mov eax, [ebx]
					mov [edx], eax
					add ebx, 2
					add edx, 2
					dec cx
					cmp cx, 0
					jg _copy
				
				ENDM
downBound		MACRO mat
				local oob, done
					mov cx, currR
					inc cx
					index_conv cx, currC
					cmp ax, total_nodes
					jg oob
					mov ax, 1
					jmp done
					oob:

						mov ax, 0
					done:
				ENDM
				
rightBound		MACRO mat
				local oob, done
					mov ax, currR
					dec ax
					imul cols
					mov cx, currC

					add ax, cx
					mov index, ax
					
					mov ax, currR
					dec ax
					imul cols
					mov cx, cols
					dec cx
					add ax, cx
					mov cx, index

					cmp ax, cx
					jl oob
					
					mov ax, 1
					jmp done
					oob:
						
						mov ax, 0
					done:
						
				ENDM
				
disp_matrix MACRO mat
	local outer, begin, done, fini
	mov ax, rows
	mov cx, cols
	lea ebx, mat
	jmp begin
	outer:
	
		mov cx, cols
		dec ax
		cmp ax, 0
		je fini
		output carriage
	begin:
		itoa output_val, [ebx]
		output output_val
		add ebx, 2
		
		dec cx
		cmp cx, 0
		je outer
		jmp begin
		fini:
		output carriage
		output carriage
	ENDM
	
solve		MACRO mat, mat2
			local begin, done, getRight, getDown, compare, tidyUp, addRight, addDown, resetRow, downB
			
			mov ax, rows
			mov currR, ax
			mov rowCount, ax
			mov ax, cols

			mov colCount, ax
			mov currC, ax
			
			
			index_conv rows, cols
			;mov currI, ax
			jmp begin
			
			resetRow:

				dec rowCount
				dec currR
				cmp rowCount, 0
				je done
				
				mov ax, pcols
				mov colCount, ax
				mov currC, ax
				
			
			begin:
				rightBound mat

				cmp ax, 0
				jne getRight
				mov right, ax
			downB:
				downBound mat

				cmp ax, 0
				jne getDown
				mov down, ax
				
			compare:

				mov cx, right
				mov ax, down

				cmp cx, ax
				jl addDown
				jmp addRight
			getRight:
				mov cx, currC
				inc cx
				get_element currR, cx, mat
				mov right, ax

				jmp downB
			getDown:
				mov cx, currR
				inc cx
				get_element cx, currC, mat

				mov down, ax
				jmp compare
			
			addRight:

				set_element currR, currC, right, mat
				jmp tidyUp
			addDown:

				set_element currR, currC, down, mat
			tidyUp:

				dec currC
				;dec currI
				dec colCount
				mov cx, colCount
				cmp cx, 0
				jle resetRow
				jmp begin
			done:
			
			ENDM
get_path	MACRO mat, pat
				local begin, done, getRight, getDown, compare, tidyUp, addRight, addDown, resetRow, downB
			
			mov ax, 1
			mov currR, ax
			mov rowCount, ax
			mov colCount, ax
			mov currC, ax
			
			
			jmp begin
			
			resetRow:
				
				inc rowCount
			
				mov ax, rowCount
				cmp ax, rows
				jg done
				
				mov ax, 1
				mov colCount, ax
			
				
				
			begin:
				rightBound mat
				cmp ax, 0
				je done
				cmp ax, 0
				jne getRight
				mov right, ax
			downB:
				downBound mat
				cmp ax, 0
				je done
				cmp ax, 0
				jne getDown
				mov down, ax
				
			compare:
				
				mov cx, right
				mov ax, down

				cmp cx, ax
				jl addDown
				jmp addRight
			getRight:
				mov cx, currC
				inc cx
				get_element currR, cx, mat
				
				mov right, ax

				jmp downB
			getDown:
				mov cx, currR
				inc cx
				get_element cx, currC, mat
				cmp ax, 0
				je done
				mov down, ax
				jmp compare
			
			addRight:
				inc currC
				add_path pat, r
				jmp tidyUp
			addDown:
				inc currR
				add_path pat, d
			tidyUp:

			
			
				inc colCount
				mov cx, colCount
				cmp cx, cols
				jl begin
				jmp resetRow
			done:
			
			ENDM

add_path	MACRO mat, dir
			
			lea ebx, mat
			mov eax, 0
			mov ax, pctr
			add ebx, eax
			mov ax, dir
			mov[ebx], ax
			
			add pctr, 2
			inc currI
			ENDM
			
disp_path	MACRO pat
			
			lea ebx, pat
			mov cx, 0
			begin:
		
			output [ebx]
				add ebx, 2
				inc cx
				cmp cx, currI
				jle begin
				output carriage
			ENDM
				
_start:
		create_matrix matrix, matrix2, index
	
		
		solve matrix, matrix2
		disp_matrix matrix2
	
		disp_matrix matrix
		get_path matrix, path
		disp_path path
		

INVOKE ExitProcess, 0  

PUBLIC _start                      

END