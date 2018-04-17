.NOLIST
.386

EXTRN strcopyproc : Near32
EXTRN appendproc : Near32
EXTRN strlenproc : Near32
EXTRN substringproc : Near32
EXTRN equalsproc : Near32
EXTRN compareproc : Near32
EXTRN replaceproc : Near32
EXTRN toLowerproc : Near32
EXTRN indexOfproc : Near32

strcopy		MACRO source, dest, xtra

                   IFB <source>
                      .ERR <missing "source" operand in strcopy>
                   ELSEIFB <dest>
                      .ERR <missing "dest" operand in strcopy>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in strcopy>
                   ELSE

                      push ebx

                         lea ebx, source
                         push ebx
                         lea ebx, dest
                         push ebx
                         call strcopyproc

                      pop ebx

                   ENDIF

		ENDM

strlen		MACRO source, xtra

                   IFB <source>
                      .ERR <missing "source" operand in strlen>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in strlen>
                   ELSE

                      push ebx

                         lea ebx, source
                         push ebx
                         call strlenproc

                      pop ebx

                   ENDIF

		ENDM

append		MACRO source, dest, xtra

                   IFB <source>
                      .ERR <missing "source" operand in append>
                   ELSEIFB <dest>
                      .ERR <missing "dest" operand in append>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in append>
                   ELSE

                      push ebx

                         lea ebx, source
                         push ebx
                         lea ebx, dest
                         push ebx
                         call appendproc

                      pop ebx

                   ENDIF

		ENDM

substring		MACRO source, dest, start, end, xtra

                   IFB <source>
                      .ERR <missing "source" operand in substring>
                   ELSEIFB <dest>
                      .ERR <missing "dest" operand in substring>
                   ELSEIFB <start>
                      .ERR <missing starting index operand in substring>
                   ELSEIFB <end>
                      .ERR <missing ending index operand in substring>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in substring>
                   ELSE

                      push ebx

                         lea ebx, source
                         push ebx
                         lea ebx, dest
                         push ebx
                         pushw start
                         pushw end
                         call substringproc

                      pop ebx

                   ENDIF

		ENDM

equals		MACRO source, dest, xtra

                   IFB <source>
                      .ERR <missing "source" operand in equals>
                   ELSEIFB <dest>
                      .ERR <missing "dest" operand in equals>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in equals>
                   ELSE

                      push ebx

                         lea ebx, source
                         push ebx
                         lea ebx, dest
                         push ebx
                         call equalsproc

                      pop ebx

                   ENDIF

		ENDM

compare		MACRO source, dest, xtra

                   IFB <source>
                      .ERR <missing "source" operand in compare>
                   ELSEIFB <dest>
                      .ERR <missing "dest" operand in compare>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in compare>
                   ELSE

                      push ebx

                         lea ebx, source
                         push ebx
                         lea ebx, dest
                         push ebx
                         call compareproc

                      pop ebx

                   ENDIF

		ENDM

replace		MACRO oldChar, newChar, dest, xtra

                   IFB <oldChar>
                      .ERR <missing old character operand in replace>
                   ELSEIFB <dest>
                      .ERR <missing new character operand in replace>
                   ELSEIFB <dest>
                      .ERR <missing "dest" operand in replace>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in replace>
                   ELSE

                      push ebx

                         pushw oldChar
                         pushw newChar
                         lea ebx, dest
                         push ebx
                         call replaceproc

                      pop ebx

                   ENDIF

		ENDM

toLower		MACRO source, dest, xtra

                   IFB <source>
                      .ERR <missing "source" operand in toLower>
                   ELSEIFB <dest>
                      .ERR <missing "dest" operand in toLower>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in toLower>
                   ELSE

                      push ebx

                         lea ebx, source
                         push ebx
                         lea ebx, dest
                         push ebx
                         call toLowerproc

                      pop ebx

                   ENDIF

		ENDM

indexOf		MACRO source, char, xtra

                   IFB <source>
                      .ERR <missing "source" operand in indexOf>
                   ELSEIFB <char>
                      .ERR <missing char operand in indexOf>
                   ELSEIFNB <xtra>
                      .ERR <extra operand(s) in indexOf>
                   ELSE

                      push ebx

                         lea ebx, source
                         push ebx
                         pushw char
                         call indexOfproc

                      pop ebx

                   ENDIF

		ENDM


.NOLISTMACRO
.LIST