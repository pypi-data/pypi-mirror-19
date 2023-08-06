  /**
 * $Id: nccf_linear_interp_mod.h 1013 2016-10-17 01:36:42Z pletzer $
 */

int nccf_linear_interp_mod_TYPE(int ndims, const int dims[],
                                const _TYPE f_nodes[],
                                _TYPE f_ref, 
                                _TYPE f_periodicity, 
                                const _TYPE dindices[],
                                const _TYPE weights[],
                                _TYPE fill_value,
                                _TYPE *f_interp) {
  int i, j;

  // find the lower corner set of indices
  // and the number of nodes in the cell
  int loCornerIndx[ndims];
  int nNodes = 1;
  int ntot = 1;
  for (i = 0; i < ndims; ++i) {
    loCornerIndx[i] = (int) floor(dindices[i]);
    nNodes *= 2;
    ntot *= dims[i];
  }
  
  // set the interpolation value to fill_value if all the 
  // weights are zero. This can happen if there are invalid
  // function values.
  _TYPE sum_weights = 0;
  for (j = 0; j < nNodes; ++j) {
    sum_weights += weights[j];
  }
  if (sum_weights == 0) {
    *f_interp = fill_value;
    return NC_NOERR;
  }
  
  // iterate over all nodes of the cell
  _TYPE f_store[nNodes];
  int bigIndex;
  int indx[ndims];
  int prodDims[ndims];
  prodDims[ndims - 1] = 1; 
  for (i = ndims - 2; i >= 0; --i) {
    prodDims[i] = prodDims[i + 1] * 2;
  }

  *f_interp = 0.0;
  for (j = 0; j < nNodes; ++j) {

    // compute the index set of the node
    for (i = 0; i < ndims; ++i) {
      indx[i] = loCornerIndx[i] + (j / prodDims[i] % 2);
    }

    bigIndex = nccf_get_flat_index(ndims, dims, indx);
    bigIndex = (bigIndex > ntot - 1? ntot - 1: bigIndex);
    bigIndex = (bigIndex < 0? 0: bigIndex);

    // modulo operation, adjust periodicity so as to 
    // minimize the distance from f_ref (typically the
    // target coordinate value)
    f_store[j] = f_nodes[bigIndex];
    if (fabs((double)(f_store[j] + f_periodicity - f_ref)) < 
        fabs((double)(f_store[j] - f_ref))) {
      f_store[j] += f_periodicity;
    }
    if (fabs((double)(f_store[j] - f_periodicity - f_ref)) < 
        fabs((double)(f_store[j] - f_ref))) {
      f_store[j] -= f_periodicity;
    }
    
  }

  for (j = 0; j < nNodes; ++j) {
    // add the contribution of each partial volume
    *f_interp += weights[j] * f_store[j];
  }
  
  return NC_NOERR;
}
