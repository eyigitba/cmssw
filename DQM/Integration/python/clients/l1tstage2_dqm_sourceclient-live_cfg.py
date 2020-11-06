import FWCore.ParameterSet.Config as cms

import sys
from Configuration.Eras.Era_Run3_cff import Run3
# from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
process = cms.Process("L1TStage2DQM", Run3)
# process = cms.Process("L1TStage2DQM", Run2_2018)

process.load('Configuration.StandardSequences.MagneticField_cff')
# process.load('Configuration.StandardSequences.Services_cff')
# process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
# process.load('FWCore.MessageService.MessageLogger_cfi')
# process.load('Configuration.EventContent.EventContent_cff')
# process.load('SimGeneral.MixingModule.mixNoPU_cfi')
# process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
# process.load('Configuration.StandardSequences.MagneticField_cff')
# process.load('Configuration.StandardSequences.RawToDigi_cff')
# process.load('Configuration.StandardSequences.EndOfProcess_cff')
# process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


unitTest = False
if 'unitTest=True' in sys.argv:
    unitTest=True

#--------------------------------------------------
# Event Source and Condition

if unitTest:
    process.load("DQM.Integration.config.unittestinputsource_cfi")
else:
    # Live Online DQM in P5
    process.load("DQM.Integration.config.fileinputsource_cfi")

# # Testing in lxplus
# process.load("DQM.Integration.config.fileinputsource_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
# process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.debugModules = ['L1T']
process.MessageLogger.cout = cms.untracked.PSet(
    # threshold=cms.untracked.string('DEBUG'),
    #threshold = cms.untracked.string('INFO'),
    threshold = cms.untracked.string('ERROR'),
    DEBUG=cms.untracked.PSet(
        limit=cms.untracked.int32(-1)
    ),
    INFO=cms.untracked.PSet(
        limit=cms.untracked.int32(-1)
    ),
    WARNING=cms.untracked.PSet(
        limit=cms.untracked.int32(-1)
    ),
    ERROR=cms.untracked.PSet(
        limit=cms.untracked.int32(-1)
    ),
    default = cms.untracked.PSet( 
        limit=cms.untracked.int32(-1)  
    )
)

# Required to load Global Tag
process.load("DQM.Integration.config.FrontierCondition_GT_cfi") 

# # Condition for lxplus: change and possibly customise the GT
from Configuration.AlCa.GlobalTag import GlobalTag as gtCustomise
# process.GlobalTag = gtCustomise(process.GlobalTag, '110X_mcRun4_realistic_v3', '')
process.GlobalTag = gtCustomise(process.GlobalTag, '110X_mcRun3_2021_realistic_v6', '')


# Required to load EcalMappingRecord
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

#--------------------------------------------------
# DQM Environment

process.load("DQM.Integration.config.environment_cfi")

process.dqmEnv.subSystemFolder = "L1T"
process.dqmSaver.tag = "L1T"

process.dqmEndPath = cms.EndPath(process.dqmEnv * process.dqmSaver)

#--------------------------------------------------
# Standard Unpacking Path

process.load("Configuration.StandardSequences.RawToDigi_cff")    
# process.load("Configuration.StandardSequences.DigiToRaw_cff")    

# remove unneeded unpackers
# process.RawToDigi.remove(process.ecalPreshowerDigis)
# process.RawToDigi.remove(process.muonCSCDigis)
# process.RawToDigi.remove(process.muonDTDigis)
# process.RawToDigi.remove(process.muonRPCDigis)
# process.RawToDigi.remove(process.siPixelDigis)
# process.RawToDigi.remove(process.siStripDigis)
# process.RawToDigi.remove(process.castorDigis)
# process.RawToDigi.remove(process.scalersRawToDigi)
# process.RawToDigi.remove(process.tcdsDigis)
# process.RawToDigi.remove(process.totemTriggerRawToDigi)
# process.RawToDigi.remove(process.totemRPRawToDigi)
# process.RawToDigi.remove(process.ctppsDiamondRawToDigi)
# process.RawToDigi.remove(process.ctppsPixelDigis)

process.rawToDigiPath = cms.Path(process.RawToDigi)
# process.digiToRawPath = cms.Path(process.DigiToRaw)

#--------------------------------------------------
# Stage2 Unpacker and DQM Path

# Filter fat events
from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltFatEventFilter = hltHighLevel.clone()
process.hltFatEventFilter.throw = cms.bool(False)
# HLT_Physics now has the event % 107 filter as well as L1FatEvents
process.hltFatEventFilter.HLTPaths = cms.vstring('HLT_L1FatEvents_v*', 'HLT_Physics_v*')

# This can be used if HLT filter not available in a run
process.selfFatEventFilter = cms.EDFilter("HLTL1NumberFilter",
        invert = cms.bool(False),
        period = cms.uint32(107),
        rawInput = cms.InputTag("rawDataCollector"),
        fedId = cms.int32(1024)
        )

process.load("DQM.L1TMonitor.L1TStage2_cff")

process.l1tMonitorPath = cms.Path(
    # process.l1tStage2OnlineDQM
    process.l1tStage2Emtf
    # process.hltFatEventFilter +
#    process.selfFatEventFilter +
    # process.l1tStage2OnlineDQMValidationEvents
)

# Remove DQM Modules
# process.l1tStage2OnlineDQM.remove(process.l1tStage2CaloLayer1)
# process.l1tStage2OnlineDQM.remove(process.l1tStage2CaloLayer2)
# process.l1tStage2OnlineDQM.remove(process.l1tStage2Bmtf)
# process.l1tStage2OnlineDQM.remove(process.l1tStage2BmtfSecond)
# process.l1tStage2OnlineDQM.remove(process.l1tStage2BmtfZeroSupp)
# process.l1tStage2OnlineDQM.remove(process.l1tStage2Omtf)
#process.l1tStage2OnlineDQM.remove(process.l1tStage2Emtf)
# process.l1tStage2OnlineDQM.remove(process.l1tStage2uGMT)
# process.l1tStage2OnlineDQM.remove(process.l1tStage2uGt)

#--------------------------------------------------
# Stage2 Quality Tests
process.load("DQM.L1TMonitorClient.L1TStage2MonitorClient_cff")
process.l1tStage2MonitorClientPath = cms.Path(process.l1tStage2MonitorClient)

#--------------------------------------------------
# Customize for other type of runs

# Cosmic run
if (process.runType.getRunType() == process.runType.cosmic_run):
    # Remove Quality Tests for L1T Muon Subsystems since they are not optimized yet for cosmics
    process.l1tStage2MonitorClient.remove(process.l1TStage2uGMTQualityTests)
    process.l1tStage2MonitorClient.remove(process.l1TStage2EMTFQualityTests)
    #process.l1tStage2MonitorClient.remove(process.l1TStage2OMTFQualityTests)
    process.l1tStage2MonitorClient.remove(process.l1TStage2BMTFQualityTests)
    process.l1tStage2MonitorClient.remove(process.l1TStage2MuonQualityTestsCollisions)
    process.l1tStage2EventInfoClient.DisableL1Systems = cms.vstring("EMTF", "OMTF", "BMTF", "uGMT")

# Heavy-Ion run
if (process.runType.getRunType() == process.runType.hi_run):
    process.onlineMetaDataDigis.onlineMetaDataInputLabel = cms.InputTag("rawDataRepacker")
    process.onlineMetaDataRawToDigi.onlineMetaDataInputLabel = cms.InputTag("rawDataRepacker")
    process.castorDigis.InputLabel = cms.InputTag("rawDataRepacker")
    process.ctppsDiamondRawToDigi.rawDataTag = cms.InputTag("rawDataRepacker")
    process.ctppsPixelDigis.inputLabel = cms.InputTag("rawDataRepacker")
    process.ecalDigis.InputLabel = cms.InputTag("rawDataRepacker")
    process.ecalPreshowerDigis.sourceTag = cms.InputTag("rawDataRepacker")
    process.hcalDigis.InputLabel = cms.InputTag("rawDataRepacker")
    process.muonCSCDigis.InputObjects = cms.InputTag("rawDataRepacker")
    process.muonDTDigis.inputLabel = cms.InputTag("rawDataRepacker")
    process.muonRPCDigis.InputLabel = cms.InputTag("rawDataRepacker")
    process.muonGEMDigis.InputLabel = cms.InputTag("rawDataRepacker")
    process.scalersRawToDigi.scalersInputTag = cms.InputTag("rawDataRepacker")
    process.siPixelDigis.InputLabel = cms.InputTag("rawDataRepacker")
    process.siStripDigis.ProductLabel = cms.InputTag("rawDataRepacker")
    process.tcdsDigis.InputLabel = cms.InputTag("rawDataRepacker")
    process.tcdsRawToDigi.InputLabel = cms.InputTag("rawDataRepacker")
    process.totemRPRawToDigi.rawDataTag = cms.InputTag("rawDataRepacker")
    process.totemTriggerRawToDigi.rawDataTag = cms.InputTag("rawDataRepacker")
    process.totemTimingRawToDigi.rawDataTag = cms.InputTag("rawDataRepacker")
    process.csctfDigis.producer = cms.InputTag("rawDataRepacker")
    process.dttfDigis.DTTF_FED_Source = cms.InputTag("rawDataRepacker")
    process.gctDigis.inputLabel = cms.InputTag("rawDataRepacker")
    process.gtDigis.DaqGtInputTag = cms.InputTag("rawDataRepacker")
    process.twinMuxStage2Digis.DTTM7_FED_Source = cms.InputTag("rawDataRepacker")
    process.bmtfDigis.InputLabel = cms.InputTag("rawDataRepacker")
    process.omtfStage2Digis.inputLabel = cms.InputTag("rawDataRepacker")
    process.emtfStage2Digis.InputLabel = cms.InputTag("rawDataRepacker")
    process.gmtStage2Digis.InputLabel = cms.InputTag("rawDataRepacker")
    process.caloLayer1Digis.InputLabel = cms.InputTag("rawDataRepacker")
    process.caloStage1Digis.InputLabel = cms.InputTag("rawDataRepacker")
    process.caloStage2Digis.InputLabel = cms.InputTag("rawDataRepacker")
    process.gtStage2Digis.InputLabel = cms.InputTag("rawDataRepacker")
    process.l1tStage2CaloLayer1.fedRawDataLabel = cms.InputTag("rawDataRepacker")
    process.l1tStage2uGMTZeroSupp.rawData = cms.InputTag("rawDataRepacker")
    process.l1tStage2uGMTZeroSuppFatEvts.rawData = cms.InputTag("rawDataRepacker")
    process.l1tStage2BmtfZeroSupp.rawData = cms.InputTag("rawDataRepacker")
    process.l1tStage2BmtfZeroSuppFatEvts.rawData = cms.InputTag("rawDataRepacker")
    process.selfFatEventFilter.rawInput = cms.InputTag("rawDataRepacker")
    process.rpcTwinMuxRawToDigi.inputTag = cms.InputTag("rawDataRepacker")
    process.rpcCPPFRawToDigi.inputTag = cms.InputTag("rawDataRepacker")

#--------------------------------------------------
# L1T Online DQM Schedule
process.load('L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi')
process.load('EventFilter.L1TRawToDigi.emtfStage2Digis_cfi')

process.load('L1Trigger.L1TGEM.simGEMDigis_cff')

process.load('L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi')
process.simCscTriggerPrimitiveDigis = process.cscTriggerPrimitiveDigis.clone()
process.simCscTriggerPrimitiveDigis.CSCComparatorDigiProducer = cms.InputTag('muonCSCDigis', 'MuonCSCComparatorDigi')
process.simCscTriggerPrimitiveDigis.CSCWireDigiProducer       = cms.InputTag('muonCSCDigis', 'MuonCSCWireDigi')

# process.simCscTriggerPrimitiveDigis.GEMPadDigiProducer       = cms.InputTag('muonGEMPadDigis')
# process.simCscTriggerPrimitiveDigis.GEMPadDigiClusterProducer       = cms.InputTag('muonGEMPadDigiClusters')


# process.simCscTriggerPrimitiveDigis.GEMPadDigiProducer = cms.InputTag("")
# process.simCscTriggerPrimitiveDigis.GEMPadDigiClusterProducer = cms.InputTag("")
# process.simCscTriggerPrimitiveDigis.commonParam = cms.untracked.PSet(
#   # isSLHC = False,
#   runME11Up = cms.bool(False),
#   runME11ILT = cms.bool(False),
#   useClusters = cms.bool(False),
#   enableAlctSLHC = cms.bool(False)),
 # clctSLHC = dict(clctNplanesHitPattern = 3),
 # me11tmbSLHCGEM = me11tmbSLHCGEM,
 # copadParamGE11 = copadParamGE11




# process.simEmtfDigisMC.verbosity  = cms.untracked.int32(0)
# process.simEmtfDigisMC.CPPFEnable = cms.bool(False)

# process.simEmtfDigisMC.FWConfig = cms.bool(True)

# process.simEmtfDigisMCSimHit = process.simEmtfDigisMC.clone()

# process.simEmtfDigisMCSimHit.CSCInput = cms.InputTag('simCscTriggerPrimitiveDigis','MPCSORTED') ## Re-emulated CSC LCTs
# process.simEmtfDigisMCSimHit.CSCInputBXShift = cms.int32(-8) ## Only for re-emulated CSC LCTs (vs. -6 default)
# process.simEmtfDigisMCSimHit.CPPFEnable = cms.bool(False)

process.muonGEMDigis.useDBEMap = False

process.simMuonGEMPadSeq = cms.Sequence(process.simMuonGEMPadTask)

process.simMuonGEMPadDigis.InputCollection = cms.InputTag('muonGEMDigis')
# process.simMuonGEMPadDigis.InputCollection = cms.InputTag('muonGEMDigis')


RawToDigi_AWB = cms.Sequence(
    process.muonGEMDigis             + ## Unpacked GEM digis
    process.muonRPCDigis             + ## Unpacked RPC hits from RPC PAC
    process.muonCSCDigis             + ## Unpacked CSC LCTs (and raw strip and wire?) from TMB
    
    # process.simMuonGEMPadTask +
    process.simMuonGEMPadSeq +
    process.simCscTriggerPrimitiveDigis + ## To get re-emulated CSC LCTs

    # process.csctfDigis               + ## Necessary for legacy studies, or if you use csctfDigis as input
    process.emtfStage2Digis          + 
    process.simEmtfDigis         
    # process.simEmtfDigisMCSimHit   +
    # process.csc2DRecHits +
    # process.cscSegments +
    # process.FlatNtupleMC
    )

process.raw2digi_step = cms.Path(RawToDigi_AWB)


process.schedule = cms.Schedule(
    # process.digiToRawPath,
    # process.rawToDigiPath,
    process.raw2digi_step,
    process.l1tMonitorPath,
    process.l1tStage2MonitorClientPath,
#    process.l1tMonitorEndPath,
    process.dqmEndPath
)

#--------------------------------------------------
# Process Customizations

from DQM.Integration.config.online_customizations_cfi import *
process = customise(process)

