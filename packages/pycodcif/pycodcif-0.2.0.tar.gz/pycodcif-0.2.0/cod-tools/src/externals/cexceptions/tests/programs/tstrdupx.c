/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2015-04-05 08:51:47 +0000 (Sun, 05 Apr 2015) $ 
**$Revision: 3207 $
**$URL: svn://www.crystallography.net/cod-tools/trunk/src/externals/cexceptions/tests/programs/tstrdupx.c $
\*---------------------------------------------------------------------------*/

#include <stdio.h>
#include <stringx.h>
#include <allocx.h>
#include <cexceptions.h>

int main()
{
    char *str;

    str = strdupx( "test string", NULL_EXCEPTION );
    printf( "Duplicated string: %s\n", str );
    freex( str );

    return 0;
}
