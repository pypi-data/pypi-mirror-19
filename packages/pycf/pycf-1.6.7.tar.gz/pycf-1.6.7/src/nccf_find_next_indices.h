/**
 * $Id: nccf_find_next_indices.h 1024 2016-10-31 23:17:39Z pletzer $
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */

int
nccf_find_next_indices_TYPE(int ndims, const int dims[], 
			                      const _TYPE **coordData,
                            const _TYPE coord_periodicity[],
                            const _TYPE targetPos[],
                            const _TYPE dIndices_in[],
                            _TYPE dIndices_out[], 
                            _TYPE position_out[]) {

  int status, i, j, k;
  int totError = 0;
  const _TYPE h = 1;

  _TYPE jac[ndims * ndims];
  _TYPE idxDispl[ndims];
  _TYPE posDispl[ndims];
  _TYPE offsetPositionLo[ndims];
  _TYPE offsetPositionHi[ndims];
  _TYPE offsetIndicesLo[ndims];
  _TYPE offsetIndicesHi[ndims];

  status = nccf_get_position_TYPE(ndims, dims, coordData, 
                                  coord_periodicity, targetPos,
                                  dIndices_in, position_out);
  totError += abs(status);

  // set the right hand side vector
  for (i = 0; i < ndims; ++i) {
    offsetIndicesLo[i] = dIndices_in[i];
    offsetIndicesHi[i] = dIndices_in[i];
    posDispl[i] = targetPos[i] - position_out[i];
  }


  /* compute the Jacobian, evaluate the differences at the index location */
  for (j = 0; j < ndims; ++j) {
    offsetIndicesLo[j] = dIndices_in[j] - 0.5*h; //(double) floor(dIndices_in[j]);
    offsetIndicesLo[j] = (offsetIndicesLo[j] >= dims[j] - 1 - h? dims[j] - 1 - h: offsetIndicesLo[j]);
    offsetIndicesLo[j] = (offsetIndicesLo[j] < 0? 0: offsetIndicesLo[j]);
    offsetIndicesHi[j] = offsetIndicesLo[j] + h;
    status = nccf_get_position_TYPE(ndims, dims, coordData,
                                    coord_periodicity, targetPos,
                                    offsetIndicesLo, offsetPositionLo);
    status = nccf_get_position_TYPE(ndims, dims, coordData,
                                    coord_periodicity, targetPos,
                                    offsetIndicesHi, offsetPositionHi);
    for (i = 0; i < ndims; ++i) {
      k = j + ndims*i;
      // factor 1.01 will make sure we're not overshooting
      jac[k] = 1.01 * (offsetPositionHi[i] - offsetPositionLo[i])/h;
    }

    /* reset */
    offsetIndicesLo[j] = dIndices_in[j];
    offsetIndicesHi[j] = dIndices_in[j];
  }

  /* compute the increment */
  status = nccf_solve_TYPE(ndims, jac, posDispl, idxDispl);
  totError += abs(status);

  /* compute the new index position */
  for (i = 0; i < ndims; ++i) {
    dIndices_out[i] = dIndices_in[i] + idxDispl[i];
  }
  
  return totError;
}
