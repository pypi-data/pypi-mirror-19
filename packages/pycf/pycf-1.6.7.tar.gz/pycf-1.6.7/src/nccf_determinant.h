/**
 * $Id: nccf_determinant.h 1007 2016-10-10 03:36:23Z pletzer $
 */

#include <cf_config.h>

int 
nccf_determinant_TYPE(int ndims, _TYPE mat[], _TYPE *det) {

  *det = 0;
  int info = 1; // error
  
#ifdef HAVE_LAPACK_LIB

  int lda = ndims;
  int ipv[ndims];
  int i, ii;
  _TYPE sgn;

  _GETRF(&ndims, &ndims, &mat[0], &lda,  &ipv[0], &info); 
  if (info == 0) {
    // No error
    *det = 1;
    for (i = 0; i < ndims; ++i) {
      sgn = (ipv[i] != i + 1? -1: 1);
      ii = i + ndims*i;
      *det *= sgn * mat[ii];
    }
  }
#else
#warning HAVE_LAPACK_LIB has not been set
  // no LAPACK
  info = 12345;
#endif

  return info;
}
