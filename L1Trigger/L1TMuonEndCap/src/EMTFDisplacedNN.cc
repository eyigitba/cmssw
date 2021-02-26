#include "L1Trigger/L1TMuonEndCap/interface/EMTFDisplacedNN.h"

#include <cassert>
#include <iostream>
#include <sstream>

#include "helper.h"  // assert_no_abort

EMTFDisplacedNN::EMTFDisplacedNN(const L1TMuonEndCapNNCache* cache) : cache_(cache) {}

EMTFDisplacedNN::~EMTFDisplacedNN() {}

void EMTFDisplacedNN::configure(int verbose) {
  verbose_ = verbose;

  inputNameDxy_ = "batch_normalization_1_input";
  outputNamesDxy_ = {"dense_4/BiasAdd"};

}


void EMTFDisplacedNN::call_tensorflow_dxy(const emtf::Feature& feature, emtf::Prediction& prediction) const {
  tensorflow::Tensor input(tensorflow::DT_FLOAT, {1, emtf::NUM_FEATURES});
  std::vector<tensorflow::Tensor> outputs;
  emtf_assert(feature.size() == emtf::NUM_FEATURES);

  float* d = input.flat<float>().data();
  std::copy(feature.begin(), feature.end(), d);
  tensorflow::run(&(cache_->getSession()), {{inputNameDxy_, input}}, outputNamesDxy_, &outputs);
  emtf_assert(outputs.size() == 1);
  emtf_assert(prediction.size() == emtf::NUM_PREDICTIONS);

  const float reg_pt_scale = 100.0;  // a scale factor applied to regression during training
  const float reg_dxy_scale = 1.0;   // a scale factor applied to regression during training

  prediction.at(0) = outputs[0].matrix<float>()(0, 0);
  prediction.at(1) = outputs[0].matrix<float>()(0, 1);

  // Remove scale factor used during training
  prediction.at(0) /= reg_pt_scale;
  prediction.at(1) /= reg_dxy_scale;
  return;
}

L1TMuonEndCapNNCache::L1TMuonEndCapNNCache(const std::string& graph_file) {

  tensorflow::SessionOptions options;
  tensorflow::setThreading(options, 1);

  graph_ = tensorflow::loadGraphDef(graph_file);
  session_ = tensorflow::createSession(graph_, options);


}

L1TMuonEndCapNNCache::~L1TMuonEndCapNNCache() {
  tensorflow::closeSession(session_);
}
