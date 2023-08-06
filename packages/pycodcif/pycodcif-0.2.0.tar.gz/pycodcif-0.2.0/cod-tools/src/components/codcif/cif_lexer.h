/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2015-07-28 17:31:19 +0000 (Tue, 28 Jul 2015) $ 
**$Revision: 3718 $
**$URL: svn://www.crystallography.net/cod-tools/trunk/src/components/codcif/cif_lexer.h $
\*---------------------------------------------------------------------------*/

#ifndef __CIF_LEXER_H
#define __CIF_LEXER_H

#include <stdio.h>
#include <stdlib.h> /* for ssize_t */
#include <cexceptions.h>

int yylex( void );
void yyrestart( void );

int cif_lexer( FILE *in, cexception_t *ex );

void cif_flex_reset_counters( void );

int cif_flex_current_line_number( void );
void cif_flex_set_current_line_number( ssize_t line );
int cif_flex_current_position( void );
void cif_flex_set_current_position( ssize_t pos );
const char *cif_flex_current_line( void );

int cif_flex_previous_line_number( void );
int cif_flex_previous_position( void );
const char *cif_flex_previous_line( void );

int cif_lexer_set_report_long_items( int flag );
int cif_lexer_report_long_items( void );
int cif_lexer_set_line_length_limit( int max_length );
int cif_lexer_set_tag_length_limit( int max_length );

#endif
