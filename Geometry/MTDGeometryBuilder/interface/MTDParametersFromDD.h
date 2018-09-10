#ifndef MTDGeometryBuilder_MTDParametersFromDD_h
#define MTDGeometryBuilder_MTDParametersFromDD_h

#include <vector>
#include "CondFormats/GeometryObjects/interface/PMTDParameters.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

class DDCompactView;
class PMTDParameters;

class MTDParametersFromDD {
 public:
  MTDParametersFromDD() {}
  MTDParametersFromDD(const edm::ParameterSet& );
  virtual ~MTDParametersFromDD() {}

  bool build( const DDCompactView*,
	      PMTDParameters& );
 private:
  void putOne( int, std::vector<int> &, PMTDParameters& );
  std::vector<PMTDParameters::Item> items_;
  std::vector<int> pars_;
};

#endif