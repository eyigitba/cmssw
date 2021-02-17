#include "L1TMuonEndCapTrackProducer.h"

L1TMuonEndCapTrackProducer::L1TMuonEndCapTrackProducer(const edm::ParameterSet& iConfig, const L1TMuonEndCapCache *cache)
    : track_finder_(new TrackFinder(iConfig, consumesCollector(), cache)),
      uGMT_converter_(new MicroGMTConverter()),
      config_(iConfig) {
  // Make output products
  produces<EMTFHitCollection>("");                      // All CSC LCTs and RPC clusters received by EMTF
  produces<EMTFTrackCollection>("");                    // All output EMTF tracks, in same format as unpacked data
  produces<l1t::RegionalMuonCandBxCollection>("EMTF");  // EMTF tracks output to uGMT
}

L1TMuonEndCapTrackProducer::~L1TMuonEndCapTrackProducer() {}

std::unique_ptr<L1TMuonEndCapCache> L1TMuonEndCapTrackProducer::initializeGlobalCache(const edm::ParameterSet& iConfig) {
  // auto spPAParams16 = iConfig.getParameter<edm::ParameterSet>("spPAParams16");
  // std::string pbFileNameDxy_ = spPAParams16.getParameter<std::string>("ProtobufFileName");

  // std::string pbFilePathDxy_ = "L1Trigger/L1TMuon/data/emtf_luts/" + pbFileNameDxy_;

  std::string pbFilePathDxy_ = "model_graph.displ.5.1.pb";

  L1TMuonEndCapCache* cache = new L1TMuonEndCapCache();
  cache->graphDefDxy_ = tensorflow::loadGraphDef(edm::FileInPath(pbFilePathDxy_).fullPath());
  return std::unique_ptr<L1TMuonEndCapCache>(cache);
}

void L1TMuonEndCapTrackProducer::globalEndJob(const L1TMuonEndCapCache* cache) {
  // reset the graphDef
  if (cache->graphDefDxy_ != nullptr) {
    delete cache->graphDefDxy_;
  }
}

void L1TMuonEndCapTrackProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // Create pointers to output products
  auto out_hits_tmp = std::make_unique<EMTFHitCollection>();  // before zero suppression
  auto out_hits = std::make_unique<EMTFHitCollection>();      // after zero suppression
  auto out_tracks = std::make_unique<EMTFTrackCollection>();
  auto out_cands = std::make_unique<l1t::RegionalMuonCandBxCollection>();

  // Main EMTF emulator process, produces tracks from hits in each sector in each event
  track_finder_->process(iEvent, iSetup, *out_hits_tmp, *out_tracks);

  // Apply zero suppression: only sectors with at least one CSC LCT are read out
  // In Run 2, it means RPC hits are only saved if there is at least one CSC LCT in the sector
  emtf::sector_array<bool> good_sectors;
  good_sectors.fill(false);

  for (const auto& h : *out_hits_tmp) {
    if (h.Is_CSC()) {
      good_sectors.at(h.Sector_idx()) = true;
    }
  }

  for (const auto& h : *out_hits_tmp) {
    if (good_sectors.at(h.Sector_idx())) {
      out_hits->push_back(h);
    }
  }

  // Convert into uGMT format
  uGMT_converter_->convert_all(iEvent, *out_tracks, *out_cands);

  // Fill the output products
  iEvent.put(std::move(out_hits), "");
  iEvent.put(std::move(out_tracks), "");
  iEvent.put(std::move(out_cands), "EMTF");
}

// Fill 'descriptions' with the allowed parameters
void L1TMuonEndCapTrackProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  // The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// Define this as a plug-in
DEFINE_FWK_MODULE(L1TMuonEndCapTrackProducer);
