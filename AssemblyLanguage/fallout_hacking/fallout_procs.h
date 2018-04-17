.NOLIST
.386

EXTRN match_proc : Near32
EXTRN swap_proc  : Near32
EXTRN disp_arr_proc	: Near32
EXTRN process_guess_proc : Near32

match		MACRO word_addy1, word_addy2, len, xtra
				IFB <word_addy1>
					.ERR <missing address for word one in match>
				ELSEIFB <word_addy2>
					.ERR <missing address for word two in match>
				ELSEIFB <len>
					.ERR <missing length of strings in match>
				ELSEIFNB <xtra>
					.ERR <extra operand(s) in match>
				ELSE
				
					push ebx
					
						lea ebx, word_addy1
						push ebx
						lea ebx, word_addy2
						push ebx
						push len
						call match_proc
						
					pop ebx
				ENDIF
		    ENDM
			
swap		MACRO word1, word2, len, arr_sz, xtra
				IFB <word1>
					.ERR <missing address for word one in match>
				ELSEIFB <word2>
					.ERR <missing address for word two in match>
				ELSEIFB <len>
					.ERR <missing length of strings in match>
				ELSEIFNB <xtra>
					.ERR <extra operand(s) in match>
				ELSE
					
					push ebx
						lea ebx, word1
						push ebx
						lea ebx, word2
						push ebx
						push len
						call swap_proc
					pop ebx
				ENDIF
			ENDM
disp_arr	MACRO	array, array_sz, len, xtra
				IFB <array>
					.ERR <missing array address in disp_arr>
				ELSEIFB <array_sz>
					.ERR <missing array size in disp_arr>
				ELSEIFB <len>
					.ERR <missing length in disp_arr>
				ELSEIFNB<xtra>
					.ERR <extra operand(s) in match>
				ELSE
					push ebx
						lea ebx, array
						push ebx
						push array_sz
						push len
						call disp_arr_proc
					pop ebx
				ENDIF
			ENDM
process_guess	MACRO	array, array_sz, len, word_index, num_matches, xtra
				IFB <array>
					.ERR <missing array address in process_guess>
				ELSEIFB <array_sz>
					.ERR <missing array size in process_guess>
				ELSEIFB <len>
					.ERR <missing length in process_guess>
				ELSEIFB <word_index>
					.ERR <missing guess index in process_guess>
				ELSEIFB <num_matches>
					.ERR <missing number of matches in process_guess>
				ELSEIFNB <xtra>
					>ERR <extra operand(s) in process_guess>
				ELSE
					push ebx
						lea ebx, array
						push ebx
						push array_sz
						push len
						push word_index
						push num_matches
						call process_guess_proc
					pop ebx
				ENDIF
			ENDM
				