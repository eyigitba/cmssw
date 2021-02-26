#ifndef L1TMuonEndCap_PtAssignmentEngineDxy_h
#define L1TMuonEndCap_PtAssignmentEngineDxy_h

#include <cstdint>
#include <cstdlib>
#include <cmath>
#include <string>
#include <vector>
#include <array>

#include "L1Trigger/L1TMuonEndCap/interface/Common.h"
#include "L1Trigger/L1TMuonEndCap/interface/PtAssignmentEngineAux2017.h"
#include "L1Trigger/L1TMuonEndCap/interface/EMTFDisplacedNN.h"

class PtAssignmentEngineDxy {
public:
  explicit PtAssignmentEngineDxy(EMTFDisplacedNN* emtf_displaced_nn);
  virtual ~PtAssignmentEngineDxy();

  void configure(int verbose);

  const PtAssignmentEngineAux2017& aux() const;

  virtual void calculate_pt_dxy(const EMTFTrack& track, emtf::Feature& feature, emtf::Prediction& prediction) const;

  virtual void preprocessing_dxy(const EMTFTrack& track, emtf::Feature& feature) const;

protected:
  int verbose_;

  EMTFDisplacedNN* emtf_displaced_nn_;

};

#endif
