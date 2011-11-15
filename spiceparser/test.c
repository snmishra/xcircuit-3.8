#include <stdio.h>
#include "debug.h"
#include "scanner.h"
#include "netlist_spice.h"

int ReadSpice (FILE *fp);

int ReadSpice(FILE *fp)
{
   scanner_t scan;
   spice_t *spice;

   scanner_init(&scan);
   scanner_input_newfp(&scan, fp);
   spice = spice_new(&scan);
   spice_release(spice);
   return 0;
}

int main() 
{
  FILE *fp;
  fp = fopen("../../test.sp", "r");
  ReadSpice(fp);
}
  
