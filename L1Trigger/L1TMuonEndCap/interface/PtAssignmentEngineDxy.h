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
#include "PhysicsTools/TensorFlow/interface/TensorFlow.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

class L1TMuonEndCapNNCache {
  public:

    L1TMuonEndCapNNCache(const std::string& graph_file);
    ~L1TMuonEndCapNNCache();

    // A Session allows concurrent calls to Run(), though a Session must
    // be created / extended by a single thread.
    tensorflow::Session& getSession() const { return *session_; }
    tensorflow::GraphDef& getGraph() const { return *graph_; }

  private:
    tensorflow::GraphDef* graph_;
    tensorflow::Session* session_;
};

class PtAssignmentEngineDxy {
public:
  explicit PtAssignmentEngineDxy(const L1TMuonEndCapNNCache* cache);
  virtual ~PtAssignmentEngineDxy();

  void configure(int verbose, const std::string pbFileNameDxy);

  const PtAssignmentEngineAux2017& aux() const;

  virtual void calculate_pt_dxy(const EMTFTrack& track, emtf::Feature& feature, emtf::Prediction& prediction) const;

  virtual void preprocessing_dxy(const EMTFTrack& track, emtf::Feature& feature) const;

  virtual void call_tensorflow_dxy(const emtf::Feature& feature, emtf::Prediction& prediction) const;

protected:
  int verbose_;

  // tensorflow::GraphDef* graphDefDxy_;
  // tensorflow::Session* sessionDxy_;
  const L1TMuonEndCapNNCache* cache_;

  std::string pbFileNameDxy_;
  std::string pbFilePathDxy_;
  std::string inputNameDxy_;
  std::vector<std::string> outputNamesDxy_;
};

#endif