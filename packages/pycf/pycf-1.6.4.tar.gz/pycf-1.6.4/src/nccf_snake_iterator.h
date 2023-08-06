/**
 * $Id: nccf_snake_iterator.h $
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */

 struct nccf_snake_iterator_type {
  // flat index 
  int index;

  // number of space dimensions
  int ndims;

  // total number of elements
  int ntot;

  // dimensions along each axis
  int *dims;

  // current index set
  int *inds;

  // to map index set to a flat index
  int *prodDims;
 };

#ifdef __cplusplus
extern "C" {
#endif

 /**
  * Constructor
  * \param ndims number of dimensions
  * \param dims dimensions along each axis
  * \return 0 if no error
  */
 int nccf_def_snake_iterator(struct nccf_snake_iterator_type** self, int ndims, const int dims[]);

 /**
  * Destructor
  * \return 0 if no error
  */
 int nccf_free_snake_iterator(struct nccf_snake_iterator_type** self);

 /**
  * Reset iterator to beginning
  * \return 0 if no error
  */
 int nccf_reset_snake_iterator(struct nccf_snake_iterator_type** self);

 /**
  * Get the numbe of elements
  * \param numElems (output)
  * \return 0 if no error
  */
 int nccf_get_snake_iterator_number_elements(struct nccf_snake_iterator_type** self, int* numElems);

 /**
  * Increment the iterator
  * \return 0 if no error
  */
 int nccf_next_snake_iterator(struct nccf_snake_iterator_type** self);

/**
 * Set the iterator counter
 * \param indx the current unmodified flat count
 * \return 0 if no error
 */
 int nccf_set_snake_iterator_counter(struct nccf_snake_iterator_type** self, int indx);

 /**
  * Get the index set
  * \param indexSnake flat index of the current iteration (output)
  * \param inds index set (output)
  * \return 0 if no error
  */
 int nccf_get_snake_iterator_indices(struct nccf_snake_iterator_type** self,
                                     int* indexSnake, int inds[]);

#ifdef __cplusplus
}
#endif
