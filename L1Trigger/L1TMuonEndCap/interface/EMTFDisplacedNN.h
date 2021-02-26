#ifndef L1TMuonEndCap_EMTFDisplacedNN_h
#define L1TMuonEndCap_EMTFDisplacedNN_h

#include <cstdint>
#include <cstdlib>
#include <cmath>
#include <string>
#include <vector>
#include <array>

#include "L1Trigger/L1TMuonEndCap/interface/Common.h"
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

class EMTFDisplacedNN {
public:
  explicit EMTFDisplacedNN(const L1TMuonEndCapNNCache* cache);
  virtual ~EMTFDisplacedNN();

  void configure(int verbose);

  virtual void call_tensorflow_dxy(const emtf::Feature& feature, emtf::Prediction& prediction) const;


protected:
  int verbose_;

  const L1TMuonEndCapNNCache* cache_;

  std::string inputNameDxy_;
  std::vector<std::string> outputNamesDxy_;

};

#endif