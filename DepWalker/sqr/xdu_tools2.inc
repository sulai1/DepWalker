

!**+----------------------------------------------------------------------------
!*H|  INCLUDE           : xdu_tools2.inc
!*H|  BETREUER          : ALCH/MOJU/GIWE
!  |----------------------------------------------------------------------------
!*D|  BESCHREIBUNG      : INCLUDE FILE F�R ALLE  LETRA REPORTS
!*D|  			  		  
!  |----------------------------------------------------------------------------
!  |----------------------------------------------------------------------------
!*A|  �NDERUNGEN        :
!*A|----------------------------------------------------------------------------
!*A|  USER DATUM  		: Beschreibung
!*A|  GIWE 04052007 	: MOVE von tmp auf err aktiviert f�r raise_err mit 2
!*A|					     wenn $TmpOutput und $ErrOutput gestezt, wird gemoved
!*A|  GIWE 04052007 	: Error Handling 
!*A|  GIWE 04052007 	: DEPRECATED raise_err,to_adrid			  
!*A|  BETA 20180221  : CR 23384 LINUX Anpassung
!*A|  BETA 20181106  : CR 23384 LINUX Anpassung
!**+----------------------------------------------------------------------------
 
#define XDU2_SCAC 	 5068403
#include 'xdu_tools.inc'

#define asdasfd asdfg  

#define asdasfd

#define asdf 1234

#define asdf 1234.213

#define asdasfd 'YYYY.MM.DD HH24:Mi:ss' 

!******************************************************************************
!******************************************************************************
!******************************************************************************
begin-procedure adr_prt ( #FileNo,$adrid_in, $typ,$sep,$cr )  ! Druckt Adr Daten
!******************************************************************************
show {TOOLS_FLAG} 'adr prt with adrid: ' $adrid_in ' typ ' $typ	
substr(adr_ort,1,35)						&adr_ort

end-select

end-procedure


!******************************************************************************
begin-procedure adr_prt_lcd ( #FileNo,$sdgid, $sep,$cr )  ! Druckt Adr Daten
!******************************************************************************
end-select

end-procedure
