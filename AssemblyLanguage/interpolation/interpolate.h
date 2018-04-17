.NOLIST
.386

EXTRN interpolate : Near32

interpolate		MACRO	array_name, degree, x_coord
					push ebx
						lea ebx, array_name
						;push array_name	;[ebp + 14]
						push ebx
						push x_coord ;[ebp + 10]
						push degree ;[ebp + 8]
						call interpolate
						;fstp ans
					pop ebx
				ENDM