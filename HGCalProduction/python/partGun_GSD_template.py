import FWCore.ParameterSet.Config as cms

from HGCalValidator.HGCalProduction.GSD_fragment import process

process.maxEvents.input = cms.untracked.int32(DUMMYEVTSPERJOB)

# random seeds
process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(DUMMYSEED)
process.RandomNumberGeneratorService.VtxSmeared.initialSeed = cms.untracked.uint32(DUMMYSEED)
process.RandomNumberGeneratorService.mix.initialSeed = cms.untracked.uint32(DUMMYSEED)

# Input source
process.source.firstLuminosityBlock = cms.untracked.uint32(DUMMYSEED)

# Output definition
process.FEVTDEBUGHLToutput.fileName = cms.untracked.string('file:DUMMYFILENAME')

#DUMMYPUSECTION

gunmode = 'GUNMODE'

if gunmode == 'default':
    process.generator = cms.EDProducer("GUNPRODUCERTYPE",
        AddAntiParticle = cms.bool(True),
        PGunParameters = cms.PSet(
            MaxEta = cms.double(DUMMYETAMAX),
            MaxPhi = cms.double(3.14159265359),
            MAXTHRESHSTRING = cms.double(DUMMYTHRESHMAX),
            MinEta = cms.double(DUMMYETAMIN),
            MinPhi = cms.double(-3.14159265359),
            MINTHRESHSTRING = cms.double(DUMMYTHRESHMIN),
            #DUMMYINCONESECTION
            PartID = cms.vint32(DUMMYIDs)
        ),
        Verbosity = cms.untracked.int32(0),
        firstRun = cms.untracked.uint32(1),
        psethack = cms.string('multiple particles predefined pT/E eta 1p479 to 3')
    )
elif gunmode == 'pythia8':
    process.generator = cms.EDFilter("GUNPRODUCERTYPE",
        maxEventsToPrint = cms.untracked.int32(1),
        pythiaPylistVerbosity = cms.untracked.int32(1),
        pythiaHepMCVerbosity = cms.untracked.bool(True),
        PGunParameters = cms.PSet(
          ParticleID = cms.vint32(DUMMYIDs),
          AddAntiParticle = cms.bool(True),
          MinPhi = cms.double(-3.14159265359),
          MaxPhi = cms.double(3.14159265359),
          MINTHRESHSTRING = cms.double(DUMMYTHRESHMIN),
          MAXTHRESHSTRING = cms.double(DUMMYTHRESHMAX),
          MinEta = cms.double(DUMMYETAMIN),
          MaxEta = cms.double(DUMMYETAMAX)
          ),
        PythiaParameters = cms.PSet(parameterSets = cms.vstring())
    )
elif gunmode == 'closeby':
    process.generator = cms.EDProducer("GUNPRODUCERTYPE",
        AddAntiParticle = cms.bool(False),
        PGunParameters = cms.PSet(
            ControlledByEta = cms.bool(False),
            PartID = cms.vint32(DUMMYIDs),
            EnMin = cms.double(DUMMYTHRESHMIN),
            EnMax = cms.double(DUMMYTHRESHMAX),
            MaxEnSpread = cms.bool(False),
            RMin = cms.double(DUMMYRMIN),
            RMax = cms.double(DUMMYRMAX),
            ZMin = cms.double(DUMMYZMIN),
            ZMax = cms.double(DUMMYZMAX),
            Delta = cms.double(DUMMYDELTA),
            Pointing = cms.bool(DUMMYPOINTING),
            Overlapping = cms.bool(DUMMYOVERLAPPING),
            RandomShoot = cms.bool(DUMMYRANDOMSHOOT),
            NParticles = cms.int32(DUMMYNRANDOMPARTICLES),
            MaxEta = cms.double(DUMMYETAMAX),
            MinEta = cms.double(DUMMYETAMIN),
            MaxPhi = cms.double(3.14159265359),
            MinPhi = cms.double(-3.14159265359)
        ),
        Verbosity = cms.untracked.int32(10),
        psethack = cms.string('single or multiple particles predefined E moving vertex'),
        firstRun = cms.untracked.uint32(1)
    )
elif gunmode == 'physproc':

    # GUNPRODUCERTYPE is a string in the form of proc[:jetColl:threshold:min_jets]
    physicsProcess = 'GUNPRODUCERTYPE'
    proc_cfg = physicsProcess.split(':')
    proc = proc_cfg[0]

    # phase space cuts
    ptMin = DUMMYTHRESHMIN
    ptMax = DUMMYTHRESHMAX

    from reco_prodtools.templates.hgcBiasedGenProcesses_cfi import *

    #define the process
    #print 'Setting process to', proc
    defineProcessGenerator(process, proc=proc, ptMin=ptMin, ptMax=ptMax)

    #set a filter path if it's available
    if len(proc_cfg)==4:
        jetColl = proc_cfg[1]
        thr = float(proc_cfg[2])
        minObj = int(proc_cfg[3])
        #print 'Adding a filter with the following settings:'
        #print '\tgen-jet collection for filtering:', jetColl
        #print '\tpT threshold [GeV]:', thr
        #print '\tmin. number of jets with the above threshold:', minObj
        filterPath = defineJetBasedBias(process, jetColl=jetColl, thr=thr, minObj=minObj)
        process.schedule.extend([filterPath])
        process.FEVTDEBUGHLToutput.SelectEvents.SelectEvents=cms.vstring(filterPath.label())
