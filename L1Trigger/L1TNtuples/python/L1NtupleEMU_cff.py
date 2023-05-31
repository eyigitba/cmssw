import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Modifier_stage2L1Trigger_cff import stage2L1Trigger
from Configuration.Eras.Modifier_run3_GEM_cff import run3_GEM

from L1Trigger.L1TNtuples.l1CaloTowerTree_cfi import *
from L1Trigger.L1TNtuples.l1UpgradeTfMuonTree_cfi import *
from L1Trigger.L1TNtuples.l1UpgradeTfMuonShowerTree_cfi import *
from L1Trigger.L1TNtuples.l1UpgradeTree_cfi import *
from L1Trigger.L1TNtuples.l1EventTree_cfi import *
from L1Trigger.L1TNtuples.l1uGTTree_cfi import *


l1UpgradeTfMuonEmuTree = l1UpgradeTfMuonTree.clone()
l1UpgradeTfMuonEmuTree.bmtfMuonToken = cms.untracked.InputTag("simBmtfDigis","BMTF")
l1UpgradeTfMuonEmuTree.bmtf2MuonToken = cms.untracked.InputTag("simKBmtfDigis","BMTF")
l1UpgradeTfMuonEmuTree.omtfMuonToken = cms.untracked.InputTag("simOmtfDigis","OMTF")
l1UpgradeTfMuonEmuTree.emtfMuonToken = cms.untracked.InputTag("simEmtfDigis","EMTF")
l1UpgradeTfMuonEmuTree.isEMU = cms.bool(True)

l1UpgradeTfMuonShowerEmuTree = l1UpgradeTfMuonShowerTree.clone()
l1UpgradeTfMuonShowerEmuTree.emtfMuonShowerToken = cms.untracked.InputTag("simEmtfShowers","EMTF")

l1CaloTowerEmuTree = l1CaloTowerTree.clone()
l1CaloTowerEmuTree.ecalToken = cms.untracked.InputTag("simEcalTriggerPrimitiveDigis")
l1CaloTowerEmuTree.hcalToken = cms.untracked.InputTag("simHcalTriggerPrimitiveDigis")
l1CaloTowerEmuTree.l1TowerToken = cms.untracked.InputTag("simCaloStage2Layer1Digis")
l1CaloTowerEmuTree.l1ClusterToken = cms.untracked.InputTag("simCaloStage2Digis", "MP")

l1UpgradeEmuTree = l1UpgradeTree.clone(
    egToken = "simCaloStage1FinalDigis",
    tauTokens = ["simCaloStage1FinalDigis:rlxTaus"],
    jetToken = "simCaloStage1FinalDigis",
    muonToken = "simGtDigis",
    sumToken = "simCaloStage1FinalDigis",
)
stage2L1Trigger.toModify(l1UpgradeEmuTree,
    egToken = "simCaloStage2Digis",
    tauTokens = ["simCaloStage2Digis"],
    jetToken = "simCaloStage2Digis",
    muonToken = "simGmtStage2Digis",
    #muonToken = "muonLegacyInStage2FormatDigis",
    sumToken = "simCaloStage2Digis"
)

run3_GEM.toModify(l1UpgradeEmuTree,
    muonShowerToken = "simGmtShowerDigis"
)

#l1legacyMuonEmuTree = l1UpgradeTree.clone()
#l1legacyMuonEmuTree.muonToken = cms.untracked.InputTag("muonLegacyInStage2FormatDigis","imdMuonsLegacy")

l1uGTEmuTree = l1uGTTree.clone()
l1uGTEmuTree.ugtToken = cms.InputTag("simGtStage2Digis")

L1NtupleEMU = cms.Sequence(
  l1EventTree
  +l1UpgradeTfMuonEmuTree
  +l1UpgradeTfMuonShowerEmuTree
  +l1CaloTowerEmuTree
  +l1UpgradeEmuTree
#  +l1MuonEmuTree
  +l1uGTEmuTree
)
