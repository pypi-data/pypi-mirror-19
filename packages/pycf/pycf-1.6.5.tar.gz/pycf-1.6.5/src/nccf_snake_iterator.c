/**
 * $Id: nccf_snake_iterator.c $
 *
 * \author Alexander Pletzer, NeSI.
 */

#include <stdlib.h>
#include <stdio.h>
#include "nccf_snake_iterator.h"
#include <nccf_utility_functions.h>

/**
 * Compute the modified set index
 * \param dims dimsensions along each axis
 * \param i axis index
 * \param inds index set corresponding to the unmodified flat index
 * \return modified set index for axis i
 */
int getModifiedSetIndex(const int dims[], int i, const int inds[]) {
  int odd, n, ii, ip, j;
  ii = inds[i];
  // ip is the sum of all previous indices
  ip = 0;
  for (j = 0; j < i; ++j) {
    ip += inds[j];
  }
  odd = ip % 2; // 0 for even index, 1 for off index
  n = dims[i];
  return (1 - odd)*ii + odd*(n - 1 - ii);
}

int nccf_def_snake_iterator(struct nccf_snake_iterator_type** self, int ndims, const int dims[]) {
  int i;
  *self = malloc(sizeof(struct nccf_snake_iterator_type));
  (*self)->ndims = ndims;
  (*self)->ntot = 1;
  (*self)->dims = malloc(ndims * sizeof(int));
  (*self)->inds = malloc(ndims * sizeof(int));
  (*self)->prodDims = malloc(ndims * sizeof(int));
  for (i = 0; i < ndims; ++i) {
    (*self)->dims[i] = dims[i];
    (*self)->ntot *= dims[i];
    (*self)->inds[i] = 0;
  }
  (*self)->prodDims[ndims - 1] = 1;
  for (i = ndims - 2; i >= 0; --i) {
    (*self)->prodDims[i] = (*self)->prodDims[i + 1] * dims[i + 1];
  }
  (*self)->index = 0;
  return 0;
}

int nccf_free_snake_iterator(struct nccf_snake_iterator_type** self) {
  if ((*self)->dims) {
    free((*self)->dims);
    free((*self)->inds);
    free((*self)->prodDims);
  }
  free(*self);
  return 0;
}

int nccf_reset_snake_iterator(struct nccf_snake_iterator_type** self) {
  int i;
  for (i = 0; i < (*self)->ndims; ++i) {
    (*self)->inds[i] = 0;
  }
  (*self)->index = 0;
  return 0;
}

int nccf_get_snake_iterator_number_elements(struct nccf_snake_iterator_type** self, int* numElems) {
  *numElems = (*self)->ntot;
  return 0;
}

int nccf_next_snake_iterator(struct nccf_snake_iterator_type** self) {

  // increment the counter
  (*self)->index++;

  // check if reached end of iterations
  if ((*self)->index >= (*self)->ntot) {
    // end
    return 1;
  }

  // compute the index set for this flat index
  nccf_get_multi_index((*self)->ndims, (*self)->dims, (*self)->index, (*self)->inds);

  return 0;
}

int nccf_set_snake_iterator_counter(struct nccf_snake_iterator_type** self, int indx) {
  
  (*self)->index = indx;
  nccf_get_multi_index((*self)->ndims, (*self)->dims, (*self)->index, (*self)->inds);

  return 0;
}

int nccf_get_snake_iterator_indices(struct nccf_snake_iterator_type** self,
	                                int* indexSnake, int inds[]) {

  int i, modifiedSetIndex;

  // nothing to do if no dimensions
  if ((*self)->ndims <= 0) return 0;

  for (i = 0; i < (*self)->ndims; ++i) {
    inds[i] = (*self)->inds[i];
  }

  *indexSnake = (*self)->prodDims[0] * inds[0];
  for (i = 1; i < (*self)->ndims; ++i) {
    modifiedSetIndex = getModifiedSetIndex((*self)->dims, i, inds);
    inds[i] = modifiedSetIndex;
    *indexSnake += (*self)->prodDims[i] * modifiedSetIndex;
  }

  // map the modified flat index back to an index set
  nccf_get_multi_index((*self)->ndims, (*self)->dims, *indexSnake, inds);

  return 0;
}
