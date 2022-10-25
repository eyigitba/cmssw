import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('L1TMuonEndCap',Run3)

# Message logger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.cerr.INFO.limit = -1

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(

'/store/data/Run2022F/EphemeralHLTPhysics0/RAW/v1/000/360/820/00000/05d31751-710d-45c1-b838-624c0180d678.root',

  ),

)

# Output module
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("emtf_run3_test.root"),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_simEmtfDigis_*_*",
        "keep *_simEmtfDigisData_*_*",
    )
)

process.options = cms.untracked.PSet()

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
# GlobalTag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_v10', '')

# Plugin: simEmtfDigis
process.load("L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi")
process.simEmtfDigisData.CSCComparatorInput = "emtfStage2Digis"
process.simEmtfDigisData.DTPhiInput = "emtfStage2Digis"
process.simEmtfDigisData.DTThetaInput = "emtfStage2Digis"
process.simEmtfDigisData.GEMInput = "emtfStage2Digis"
process.simEmtfDigisData.ME0Input = "emtfStage2Digis"
process.simEmtfDigisData.RPCInput = "emtfStage2Digis"
# Paths
process.emtf_raw2digi_step = cms.Path(process.emtfStage2Digis)
process.emtf_step = cms.Path(process.simEmtfDigisData)
process.e = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.emtf_raw2digi_step, process.emtf_step, process.e)