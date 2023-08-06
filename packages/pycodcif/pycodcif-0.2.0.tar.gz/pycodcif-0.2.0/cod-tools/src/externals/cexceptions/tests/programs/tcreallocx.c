/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2015-04-05 08:51:47 +0000 (Sun, 05 Apr 2015) $ 
**$Revision: 3207 $
**$URL: svn://www.crystallography.net/cod-tools/trunk/src/externals/cexceptions/tests/programs/tcreallocx.c $
\*---------------------------------------------------------------------------*/

#include <stdio.h>
#include <stringx.h>
#include <allocx.h>
#include <cexceptions.h>

int main()
{
    int *data = NULL;
    int i;
    const int len = 20;

    for( i = 0; i < len; i++ ) {
        data = creallocx( data, i, i + 1, sizeof(data[0]), NULL );
	data[i] += i;
    }

    for( i = 0; i < len; i++ ) {
        printf( "%d ", data[i] );
    }
    printf( "\n" );

    freex( data );

    return 0;
}
