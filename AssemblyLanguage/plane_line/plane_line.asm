.386
.MODEL FLAT


ExitProcess PROTO NEAR32 stdcall, dwExitCode:DWORD


INCLUDE io.h
INCLUDE debug.h

.STACK  4096                    ; reserve 4096-byte stack

.DATA 
data_out 			BYTE	25 DUP(?), 0
final_data			BYTE	35 DUP(?), 0
plane_prompt_x	BYTE	"Enter the x-coordinate of the point on the plane:", CR, LF, 0
plane_prompt_y	BYTE	"Enter the y-coordinate of the point on the plane:", CR, LF, 0
plane_prompt_z	BYTE	"Enter the z-coordinate of the point on the plane:", CR, LF, 0

line_prompt_x	BYTE	"Enter the x-coordinate of the point on the line:", CR, LF, 0
line_prompt_y	BYTE	"Enter the y-coordinate of the point on the line:", CR, LF, 0
line_prompt_z	BYTE	"Enter the z-coordinate of the point on the line:", CR, LF, 0


pax		WORD	?
pay		WORD	?
paz		WORD	?

pbx		WORD	?
pby		WORD	?
pbz		WORD	?

pcx		WORD	?
pcy		WORD	?
pcz		WORD	?

p1x		WORD	?
p1y		WORD	?
p1z		WORD	?

ps1x	WORD	?
ps1y	WORD	?
ps1z	WORD	?

p2x		WORD	?
p2y		WORD	?
p2z		WORD	?

ps2x	WORD	?
ps2y	WORD	?
ps2z	WORD	?

pm1x	WORD	?
pm1y	WORD	?
pm1z	WORD	?



alpha_n	WORD	?
alpha_d	WORD	?

sx1		WORD	?
sy1		WORD	?
sz1		WORD	?

sx2		WORD	?
sy2		WORD	?
sz2		WORD	?



nx		WORD	?
ny		WORD	?
nz		WORD	?
.CODE

_start:

p_subtract	MACRO	x1, y1, z1, x2, y2, z2, dest1, dest2, dest3
					mov ax, x1
					sub ax, x2
					mov dest1, ax
					
					mov ax, y1
					sub ax, y2
					mov dest2, ax
					
					mov ax, z1
					sub ax, z2
					mov dest3, ax
					ENDM	
c_product	MACRO	x1, y1, z1, x2, y2, z2, dest1, dest2, dest3
					
					mov ax, z1
					imul y2
					mov bx, ax
					
					mov ax, y1
					imul z2
					sub ax, bx
					mov dest1, ax
					
					mov ax, x1
					imul z2
					mov bx, ax
					
					mov ax, z1
					imul x2
					sub ax, bx
					mov dest2, ax
					
					mov ax, y1
					imul x2
					mov bx, ax
					
					mov ax, x1
					imul y2
					sub ax, bx
					mov dest3, ax
					ENDM
d_product		MACRO x1, x2, y1, y2, z1, z2, dest		
					mov ax, x1
					imul x2
					
					mov bx, ax
					
					mov ax, y1
					imul y2
				
					mov cx, ax
					mov ax, z1
					imul z2
					add ax, cx
					add ax, bx
					
					mov dest, ax
					ENDM
mul_points		MACRO alpha_n, alpha_d, x1, y1, z1, x2, y2, z2, destx1, desty1, destz1, destx2, desty2, destz2, fdestx, fdesty, fdestz
					
					mov ax, x1
					imul alpha_d
					mov destx1, ax
					
					mov ax, y1
					imul alpha_d
					mov desty1, ax
					
					mov ax, z1
					imul alpha_d
					mov destz1, ax
					
					mov ax, x1
					imul alpha_n
					mov destx2, ax
					
					mov ax, y1
					imul alpha_n
					mov desty2, ax
					
					mov ax, z1
					imul alpha_n
					mov destz2, ax
					
					p_subtract destx1, desty1, destz1, destx2, desty2, destz2, fdestx, fdesty, fdestz
					
					mov ax, x2
					imul alpha_n
					add fdestx, ax
				
					
					mov ax, y2
					imul alpha_n
					add fdesty, ax
					
					mov ax, z2
					imul alpha_n
					add fdestz, ax
					
					ENDM
					
div_points		MACRO alpha_d, pm1x, pm1y, pm1z, qx, qy, qz, rx, ry, rz
				
					mov bx, alpha_d
					mov ax, pm1x
					mov cx, 100
					cwd
					imul cx
					idiv bx
					cwd
					idiv cx
					mov qx, ax
					mov rx, dx
					
					
					
					mov ax, pm1y
					cwd
					imul cx
					idiv bx
					cwd
					idiv cx
					mov qy, ax
					mov ry, dx
					
					mov ax, pm1z
					cwd
					imul cx
					idiv bx
					cwd
					idiv cx
					mov qz, ax
					mov rz, dx
					ENDM
display_data	MACRO x, y, z, array
					mov array, '('	
					itoa array + 1, x
					mov array + 7, ','
					itoa array + 8, y
					mov array + 14, ','
					itoa array + 15, z
					mov array + 21, ')'
					mov array + 22, CR
					mov array + 23, LF
					output array
				
				ENDM
				
display_result	MACRO xq, yq, zq, xr, yr, zr, array
					mov array + 30, ')'
					itoa array + 24, zr
					mov array + 27, '.'
					itoa array + 21, zq
					mov array + 20, ','
					itoa array + 14, yr
					mov array + 17, '.'
					itoa array + 11, yq
					mov array + 10, ','
					itoa array + 4, xr
					mov array + 7, '.'
					itoa array + 1, xq
					mov array, '('
					output array
					output carriage
					
					ENDM
					
					
			inputW plane_prompt_x, pax		
			inputW plane_prompt_y, pay
			inputW plane_prompt_z, paz
			output carriage
		
			display_data pax, pay, paz, data_out
			
			inputW plane_prompt_x, pbx
			inputW plane_prompt_y, pby		
			inputW plane_prompt_z, pbz
			output carriage
			
			display_data pbx, pby, pbz, data_out
			
			inputW plane_prompt_x, pcx
			inputW plane_prompt_y, pcy		
			inputW plane_prompt_z, pcz
			output carriage
			
			display_data pcx, pcy, pcz, data_out
			
			inputW line_prompt_x, p1x
			inputW line_prompt_y, p1y
			inputW line_prompt_z, p1z
			output carriage
			
			display_data p1x, p1y, p1z, data_out
			
			inputW line_prompt_x, p2x
			inputW line_prompt_y, p2y
			inputW line_prompt_z, p2z
			output carriage
			
			display_data p2x, p2y, p2z, data_out
			output carriage
			output carriage
			
			p_subtract pbx, pby, pbz, pax, pay, paz, sx1, sy1, sz1
			p_subtract pcx, pcy, pcz, pax, pay, paz, sx2, sy2, sz2
			
			c_product sx1, sy1, sz1, sx2, sy2, sz2, nx, ny, nz
			
			p_subtract pcx, pcy, pcz, p1x, p1y, p1z, ps1x, ps1y, ps1z 
			p_subtract p2x, p2y, p2z, p1x, p1y, p1z, ps2x, ps2y, ps2z
			
			d_product nx, ps1x, ny, ps1y, nz, ps1z, alpha_n
			d_product nx, ps2x, ny, ps2y, nz, ps2z, alpha_d
			
			
			mul_points alpha_n, alpha_d, p1x, p1y, p1z, p2x, p2y, p2z, sx1, sy1, sz1, sx2, sz2, sy2, pm1x, pm1y, pm1z
			
			div_points alpha_d, pm1x, pm1y, pm1z, sx1, sy1, sz1, sx2, sy2, sz2
			
			display_result sx1, sy1, sz1, sx2, sy2, sz2, final_data
			
INVOKE ExitProcess, 0  

PUBLIC _start                      

END

				
