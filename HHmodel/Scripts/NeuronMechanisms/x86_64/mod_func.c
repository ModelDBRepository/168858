#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _kvz_nature_reg(void);
extern void _max_reg(void);
extern void _naz_nature_reg(void);
extern void _origlen_reg(void);
extern void _peak_reg(void);
extern void _vsource_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," kvz_nature.mod");
    fprintf(stderr," max.mod");
    fprintf(stderr," naz_nature.mod");
    fprintf(stderr," origlen.mod");
    fprintf(stderr," peak.mod");
    fprintf(stderr," vsource.mod");
    fprintf(stderr, "\n");
  }
  _kvz_nature_reg();
  _max_reg();
  _naz_nature_reg();
  _origlen_reg();
  _peak_reg();
  _vsource_reg();
}
