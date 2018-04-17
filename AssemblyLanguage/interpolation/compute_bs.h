.NOLIST
.386

EXTRN compute_bs_proc : Near32
EXTRN compute_bs_start : Near32

;compute the b's recursively.  Returns b in st(0)
;array name and degree are 
compute_bs		MACRO	array_name, degree, m
					;push ebx 
					
						;lea ebx, array_name
						;will return ebp to this point!
						;push ebx
						push array_name	;[ebp + 12]
						push m		;[ebp + 10]
						push degree ;[ebp + 8]
						call compute_bs_start
						;fxch st(1) ;exchanging to check value
						;fstp ans
					
					;pop ebx
				ENDM