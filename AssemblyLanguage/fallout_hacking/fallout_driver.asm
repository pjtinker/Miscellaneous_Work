.386
.MODEL FLAT


ExitProcess PROTO NEAR32 stdcall, dwExitCode:DWORD

;;Paul Tinker

include io.h
include debug.h
include strutils.h
include fallout_procs.h



.STACK  4096  

LEN		EQU		13
MAX		EQU		25

.DATA 
word_arr	  BYTE	500 DUP (?)


index_prompt  BYTE	"Enter the index for the test password (1-based): ", CR, LF, 0
match_prompt  BYTE	"Enter the number of exact character matches: ", CR, LF, 0
incoming	  BYTE	LEN DUP (?)
string_prompt BYTE	"Enter a string: "
count		  WORD  0
index		  WORD	0
matches		  WORD  0

num_s_prompt  BYTE  "The number of strings entered is "

.CODE
get_words		MACRO	array
					local begin, done
					lea ebx, array
					mov cx, 0
					mov eax, 0
					
				begin:
					cmp cx, WORD PTR MAX
					je done
					output string_prompt
					input BYTE PTR [ebx], LEN
					output carriage
					mov al, BYTE PTR [ebx]
					cmp al, 78h
					je done
					inc cx
					add ebx, BYTE PTR LEN
					jmp begin
				done:
					mov count, cx
					output num_s_prompt
					outputW count
					;output carriage
				ENDM	
					
disp_arr		MACRO	array, array_sz
					local begin, done
					
					lea ebx, array
					mov cx, array_sz
					;mov al, len
					
				begin:
					cmp cx, 0
					je done
					output [ebx]
					output carriage
					add ebx, BYTE PTR LEN
					dec cx
					jmp begin
						
				done:
				ENDM
_start:
get_words word_arr
;disp_arr word_arr, count
output index_prompt
input index,  LEN
atoi index

mov index, ax
output match_prompt
input matches, LEN
atoi matches
mov matches, ax

mov cx, WORD PTR LEN


outputW index

lea ebx, word_arr
lea esi, [ebx]
add ebx, BYTE PTR LEN
add ebx, BYTE PTR LEN

lea edi, [ebx]
process_guess word_arr, count, cx, index, matches
output carriage
output carriage
;match [esi], [edi], WORD PTR LEN
;outputW ax
;output [esi]
;output carriage
;output [edi]
;output carriage
;mov cx, WORD PTR LEN

;swap [esi], [edi], cx


disp_arr word_arr, count



INVOKE ExitProcess, 0  

PUBLIC _start                      

END
