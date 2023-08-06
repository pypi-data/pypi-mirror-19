/**
 * $Id: nccf_find_next_indices.h 905 2011-12-29 04:56:48Z pletzer $
 *
 * \author Alexander Pletzer, Tech-X Corp.
 */

int
nccf_get_shortest_displ_TYPE(_TYPE startPos, _TYPE endPos,
                             _TYPE periodicityLength, 
                             _TYPE *displ) {

  _TYPE absDispl, displ1, displ2;

  /* take the shortest distance between startPos and endPos in
     physical space. periodicityLength should be huge when there
     is no periodicity. */
  *displ = endPos - startPos;
  

  if (periodicityLength < _HUGE_TYPE) {
    displ1 = *displ + periodicityLength;
    displ2 = *displ - periodicityLength;
    absDispl = fabs(*displ);
    *displ = (fabs(displ1) < absDispl? displ1: *displ);
    absDispl = fabs(*displ);
    *displ = (fabs(displ2) < absDispl? displ2: *displ);
  }

  return 0;
}
