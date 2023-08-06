/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2011-03-09 08:34:46 +0000 (Wed, 09 Mar 2011) $ 
**$Revision: 1595 $
**$URL: svn://www.crystallography.net/cod-tools/trunk/src/components/codcif/common.h $
\*---------------------------------------------------------------------------*/

#ifndef __COMMON_H
#define __COMMON_H

#include <stdlib.h>

char *strclone( const char *s );
char *strnclone( const char *s, size_t length );
char *strappend( char *s, const char *suffix );
char *process_escapes( char *str );
char translate_escape( char **s );

#endif
