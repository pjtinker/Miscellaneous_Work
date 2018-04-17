.386
.MODEL FLAT


ExitProcess PROTO NEAR32 stdcall, dwExitCode:DWORD

;;Paul Tinker
include sort_points.h
include move_to_index.h
include float.h
include compare_floats.h
include sort_points.h
include io.h
include debug.h
include compute_bs.h
include interpolate.h


.STACK  4096  
                
MAX_VAL		EQU		500

.DATA 
num1 		BYTE	10 DUP (?)
num2 		BYTE	10 DUP(?)
inp_p 		BYTE	"Give it to me... ", CR, LF, 0
f_array		DWORD	20 DUP(?)
x_coord 	DWORD	?
degree 		WORD 	?
m			WORD	0
temp 		DWORD	?
num_points	WORD	?
dis			WORD	6
tol			REAL4	0.0001
index1		WORD	4
index2		WORD	4
answer		DWORD	?



.CODE

getNums			MACRO	array
					local begin, done
					
					input num1, 8
					atof num1, temp
					fld temp
					fstp x_coord
					
					input num1, 8
					atoi num1
					mov degree, ax
					
					
					mov cx, 0
					mov cl, 20
					mov dx, 0
					lea ebx, array
					
				begin:
					
					cmp cl, 0
					je done
					input num1, 8
					
					
					mov al, num1
					cmp al, 71h
					je done
					
					dec cl
					
					
					
					atof num1, REAL4 PTR [ebx]
					
					inc dx
					ftoa [ebx], 4, 20, num2
					
					add ebx, 4
					jmp begin
					
					
					
				done:
					shr dx, 1
					mov num_points, dx
					;mov num_points, dx
					
					
				ENDM
				
print_arr		MACRO array, sz
					local begin, done
						
						lea ebx, array
						mov cx, sz
					begin:
						cmp cx, 0
						je done
						
						ftoa [ebx], 3, 20, num1
						output num1
						output carriage
						add ebx, 4
						dec cx
						jmp begin
						
					done:
					
					ENDM
						

_start:

getNums f_array
;print_points f_array, num_points
sort_points f_array, x_coord, tol, num_points
print_points f_array, num_points
;print_points f_array, num_points
;lea ebx, f_array

;compute_bs ebx, degree, m
;fstp answer
;ftoa answer, 6, 20, num1
;output num1
interpolate f_array, degree, x_coord

fstp answer
ftoa answer, 6, 20, num1
output num1

;print_points f_array, num_points

INVOKE ExitProcess, 0  

PUBLIC _start                      

END