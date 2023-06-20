from __future__ import print_function
from __future__ import absolute_import
# from builtins import range
import FWCore.ParameterSet.Config as cms

# Parameters for runType
import FWCore.ParameterSet.VarParsing as VarParsing
import sys
# import fnmatch
from .dqmPythonTypes import *

# part of the runTheMatrix magic
# from Configuration.Applications.ConfigBuilder import filesFromDASQuery

options = VarParsing.VarParsing("analysis")

options.register(
    "runkey",
    "pp_run",
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
    "Run Keys of CMS"
)

# Parameter for frontierKey
options.register('runUniqueKey',
    'InValid',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
    "Unique run key from RCMS for Frontier")

options.register('runNumber',
                 368822,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Run number. This run number has to be present in the dataset configured with the dataset option.")

options.register('maxLumi',
                 2000,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Only lumisections up to maxLumi are processed.")

options.register('minLumi',
                 1,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Only lumisections starting from minLumi are processed.")

options.register('lumiPattern',
                 '*0',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Only lumisections with numbers matching lumiPattern are processed.")

options.register('dataset',
                 'auto',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Dataset name like '/ExpressPhysicsPA/PARun2016D-Express-v1/FEVT', or 'auto' to guess it with a DAS query. A dataset_cfi.py that defines 'readFiles' and 'secFiles' (like a DAS Python snippet) will override this, to avoid DAS queries.")

options.register('noDB',
                 True, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "Don't upload the BeamSpot conditions to the DB")

options.parseArguments()

# try:
#   # fixed dataset, DAS 'py' snippet
#   from dataset_cfi import readFiles, secFiles
#   print("Using filenames from dataset_cfi.py.")
# except:
#   if options.dataset == 'auto':
#     print("Querying DAS for a dataset...")
#     import subprocess
#     out = subprocess.check_output("dasgoclient --query 'dataset run=%d dataset=/*Express*/*/*FEVT*'" % options.runNumber, shell=True)
#     dataset = out.splitlines()[-1]
#     print("Using dataset=%s." % dataset)
#   else:
#     dataset = options.dataset

#   print("Querying DAS for files...")
#   readFiles = cms.untracked.vstring()
#   secFiles = cms.untracked.vstring()
#   # this outputs all results, which can be a lot...
#   read, sec = filesFromDASQuery("file run=%d dataset=%s" % (options.runNumber, dataset), option=" --limit 10000 ")
#   readFiles.extend(read)
#   secFiles.extend(sec)

# print("Got %d files." % len(readFiles))

# runstr = str(options.runNumber)
# runpattern = "*" + runstr[0:3] + "/" + runstr[3:] + "*"
# readFiles = cms.untracked.vstring([f for f in readFiles if fnmatch.fnmatch(f, runpattern)])
# secFiles = cms.untracked.vstring([f for f in secFiles if fnmatch.fnmatch(f, runpattern)])
# lumirange =  cms.untracked.VLuminosityBlockRange(
#   [ str(options.runNumber) + ":" + str(ls) 
#       for ls in range(options.minLumi, options.maxLumi+1)
#       if fnmatch.fnmatch(str(ls), options.lumiPattern)
#   ]
# )

# print("Selected %d files and %d LS." % (len(readFiles), len(lumirange)))

source = cms.Source ("PoolSource",

fileNames = cms.untracked.vstring(
  
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/dda003f4-9559-4111-bbb2-665aa48f7569.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/0f3d39a0-b5ab-48f6-bab2-3057b36c6f36.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/123e041d-9ee0-45ec-9100-f6126a1c0303.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/9f420f76-8b58-4d86-a21f-5695169a6b12.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/9b204fe2-41a2-4521-b899-16f634977b3f.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/28ba0f9d-1393-4043-bae7-4cd42ebe2012.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/4e093e8b-d982-4515-ae44-ae4a6f452158.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/43c14a18-7344-47f1-9d99-07e38ad704c0.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/7c66854c-5e32-4c83-91c3-9979a74ae9a3.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/51a9ed31-ca41-454b-9c28-f49ade122302.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/713be0e2-aecd-4559-b8b4-35ad192b09ad.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/c162ce83-4ccc-4b78-ba49-45bd15288140.root',
'/store/data/Run2023C/Muon1/RAW-RECO/ZMu-PromptReco-v4/000/368/822/00000/b3ec4c69-0c9a-48a4-b949-59042aeec297.root',
  
  
  
  
  ),




)
maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

# Fix to allow scram to compile
#if len(sys.argv) > 1:
#  options.parseArguments()

runType = RunType()
if not options.runkey.strip():
    options.runkey = "pp_run"

runType.setRunType(options.runkey.strip())
