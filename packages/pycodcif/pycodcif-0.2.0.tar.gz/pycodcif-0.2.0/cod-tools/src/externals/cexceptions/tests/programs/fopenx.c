/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2015-07-21 14:39:27 +0000 (Tue, 21 Jul 2015) $ 
**$Revision: 3587 $
**$URL: svn://www.crystallography.net/cod-tools/trunk/src/externals/cexceptions/tests/programs/fopenx.c $
\*---------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdiox.h>
#include <cexceptions.h>

int main( int argc, char *argv[] )
{
    cexception_t inner;
    char *progname = argv[0];
    char *filename = "nonexistent.txt";
    FILE * volatile fp = NULL;

    cexception_try( inner ) {
        fp = fopenx( filename, "r", &inner );
        fclosex( fp, &inner );
    }
    cexception_catch {
        fprintf( stderr, "%s: %s: %s - %s\n",
                 progname, filename, 
                 cexception_message( &inner ),
                 cexception_explanation( &inner ));
        exit(1);
    }

    return 0;
}
