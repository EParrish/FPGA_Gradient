from ROOT import *
from array import array
import math

def OpenFile(file_path, tree_name,chain ,chainRange1, chainRange2):
    '''
    Opens your file.
    args:
        file_path: Path to your file
        tree_name: Name of the tree
    returns:
        none
    '''
    if chain == True:
        fileList = []
        for i in range(chainRange1,chainRange2):
            print file_path + "%s.root"
            fileList.append(file_path + "%s.root" %(i))

        chain = TChain(tree_name)
        
        for files in fileList:
            chain.AddFile(files)
        
        return chain,chain

    if chain == False:
        File = TFile(file_path)
        tree = File.Get(tree_name)
    
        return (File,tree)

def MakeNewFile(newfile_path, datafile_path, treeName, GradThresh,tChainTrue,ChainRangeMin,ChainRangeMax):

    newFile = TFile(newfile_path, "recreate")
    t = TTree("mytree", "mytree")

    MET_Gradient = array("f", [0.0])
    Truth_MET = array("f", [0.0])
    gTowerGradient = vector('float')(0)
    gTowerN = array("f",[0,0])
    gTowerE = vector('float')(0)
    gTowerEt = vector('float')(0)
    gTowerPhi = vector('float')(0)
    gTowerEta = vector('float')(0)
    CutgTowerN = array("f",[0,0])
    CutgTowerE = vector('float')(0)
    CutgTowerEt = vector('float')(0)
    CutgTowerPhi = vector('float')(0)
    CutgTowerEta = vector('float')(0)
    AntiKt4Truth_n = array("f", [0.0])
    AntiKt4Truth_E = vector('float')(0)
    AntiKt4Truth_pt = vector('float')(0)
    AntiKt4Truth_eta = vector('float')(0)
    AntiKt4Truth_phi = vector('float')(0)
    GradientCut = array("f", [0.0])

    t.Branch("MET_Gradient", MET_Gradient, "MET_Gradient/F")
    t.Branch("Truth_MET", Truth_MET, "Truth_MET/F")
    t.Branch("gTowerGradient", gTowerGradient)
    t.Branch("CutgTowerN", CutgTowerN, "CutgTowerN/F")  
    t.Branch("CutgTowerE", CutgTowerE)  
    t.Branch("CutgTowerEt", CutgTowerEt) 
    t.Branch("CutgTowerPhi", CutgTowerPhi)
    t.Branch("CutgTowerEta", CutgTowerEta)
    t.Branch("gTowerN", gTowerN, "gTowerN/F")  
    t.Branch("gTowerE", gTowerE)  
    t.Branch("gTowerEt", gTowerEt) 
    t.Branch("gTowerPhi", gTowerPhi)
    t.Branch("gTowerEta", gTowerEta)
    t.Branch("AntiKt4Truth_n", AntiKt4Truth_n, "AntiKt4Truth_n/F")
    t.Branch("AntiKt4Truth_E", AntiKt4Truth_E)
    t.Branch("AntiKt4Truth_pt", AntiKt4Truth_pt)
    t.Branch("AntiKt4Truth_eta", AntiKt4Truth_eta)
    t.Branch("AntiKt4Truth_phi", AntiKt4Truth_phi)
    t.Branch("GradientCut", GradientCut, "GradientCut/F")

    DataFile, DataTree = OpenFile(datafile_path,treeName,tChainTrue,ChainRangeMin,ChainRangeMax) 

    NumEntries = DataTree.GetEntries()
    
    print "There are ", NumEntries, " Entries"

    for i in range(NumEntries):
            if i % 100 == 0:
                print i

            ########### START OF GRAD ALGORITHM #############
            
            # Use GeV for Gradient cut Threshold
            GradientThreshold = GradThresh

            # Do you want to include towers with >= 2 neighbors above threshold?
            if NeighborBool == 'y':
                Neighbors = True
            elif NeighborBool == 'n':
                Neighbors = False
            else:
                raise Exception("Please enter y or n for neighboring...")


            gTowers, arrayOfgTowers = GetGTowers(i,datafile_path,treeName,tChainTrue,ChainRangeMin,ChainRangeMax)
            gradArray = SobelEdge(arrayOfgTowers)
            edgeArray = CutandThreshold(gradArray,GradientThreshold,Neighbors)
            finalgTowers = CutTowers(edgeArray,arrayOfgTowers)
            MET, EndgTowers = GetMet(finalgTowers)
            
            ############# END OF GRAD ALGORITHM #############
            
            
            DataTree.GetEntry(i)
            TruthN = DataTree.AntiKt4Truth_n
            TruthPhi = DataTree.AntiKt4Truth_phi
            TruthEta = DataTree.AntiKt4Truth_eta
            TruthPT = DataTree.AntiKt4Truth_pt
            TruthE = DataTree.AntiKt4Truth_E
            TruthMET = CalculateTruthMET(TruthEta,TruthPhi,TruthPT)

            TowerN = DataTree.gTowerN
            TowerPhi = DataTree.gTowerPhi
            TowerEta = DataTree.gTowerEta
            TowerPt = DataTree.gTowerEt



            CutgTowerN[0] = len(EndgTowers)
            AntiKt4Truth_n[0] = TruthN
            MET_Gradient[0] = MET
            Truth_MET[0] = TruthMET
            GradientCut[0] = GradientThreshold
            gTowerN[0] = TowerN


            gTowerGradient.clear()
            AntiKt4Truth_pt.clear()
            AntiKt4Truth_E.clear()
            AntiKt4Truth_eta.clear()
            AntiKt4Truth_phi.clear()
            CutgTowerPhi.clear()
            CutgTowerEta.clear()
            CutgTowerEt.clear()
            CutgTowerE.clear()
            gTowerPhi.clear()
            gTowerEta.clear()
            gTowerEt.clear()

            for m in reversed(range(len(gradArray[0]))):
                for n in reversed(range(len(gradArray))):
                    gTowerGradient.push_back(gradArray[n][m]/1000)
                    
                    
            # print N
            for j in range(len(EndgTowers)):
                CutgTowerEta.push_back(EndgTowers[j].Eta())
                CutgTowerE.push_back(EndgTowers[j].E())
                CutgTowerEt.push_back(EndgTowers[j].Et())
                CutgTowerPhi.push_back(EndgTowers[j].Phi())

            for k in range(int(TruthN)):
                AntiKt4Truth_phi.push_back(TruthPhi[k])
                AntiKt4Truth_eta.push_back(TruthEta[k])
                AntiKt4Truth_pt.push_back(TruthPT[k])
                AntiKt4Truth_E.push_back(TruthE[k])

            for i in range(int(TowerN)):
                gTowerPhi.push_back(TowerPhi[i])
                gTowerEta.push_back(TowerEta[i])
                gTowerEt.push_back(TowerPt[i])
                
                

            t.Fill()

    newFile.cd()
    newFile.Write()
    newFile.Close()
    return
    

def MakeZeroArray():
    H = []

    for p in range(32):
        temp = []
        for e in range(32):
            temp.append(0)
            
        H.append(temp)
        
    return H
    
def GetGTowers(eventNum,datafile_path,treeName,tChainTrue,ChainRangeMin,ChainRangeMax):

    #file, tree = OpenFile('/scratch/eparrish/ZPrimeSamples/PileupSkim_Pythia8_AU2MSTW2008LO_zprime5000_tt_0.root','mytree')
    
    File, tree = OpenFile(datafile_path,treeName,tChainTrue,ChainRangeMin,ChainRangeMax)

    #File = DataFile
    #tree = DataTree
    
    
    H = MakeZeroArray()        
    
    tree.SetBranchStatus('*', 0)
    tree.SetBranchStatus('gTowerE', 1)
    tree.SetBranchStatus('gTowerN', 1)
    tree.SetBranchStatus('gTowerEt', 1)
    tree.SetBranchStatus('gTowerPhi', 1)
    tree.SetBranchStatus('gTowerEta', 1)

    tree.GetEntry(eventNum)
    nentries = tree.GetEntries()
    ngTowers = int(tree.gTowerN)
    es = tree.gTowerE
    ets = tree.gTowerEt
    etas = tree.gTowerEta
    phis = tree.gTowerPhi
    gTowers = []
    Event = eventNum

    for i in range(ngTowers):
        gTowers.append(TLorentzVector(0,0,0,0))
        gTowers[i].SetPtEtaPhiM(ets[i],etas[i],phis[i],0)

    n = 0
    for p in range(32):
        for e in range(32):
            
            H[e][p] = gTowers[n].Pt()
            
            n = n + 1

    H = Reverse(H)
    
    return gTowers, H

def Reverse(array):

    array.reverse()
    
    for ar in array:
        ar.reverse()
    return array
    
def plotArray(arrayOfgTowers):

    H = arrayOfgTowers
    
    Histo = TH2F("Event Display","Event Display: E_{T} in Eta vs. Phi;#eta;#phi",32,-3.2,3.2,32,-3.2,3.2)

    etas = []
    phis = []
    for p in range(32):
        for e in range(32):
            phi = 0.2 * p - math.pi
            eta = 0.2 * e - math.pi

            etas.append(eta)
            phis.append(phi)
            Histo.Fill(eta,phi,H[p][e]/1000)

    
    c2 = TCanvas("TopoClus")
    Histo.Draw("colz")
    c2.SetLogz()
    gStyle.SetOptStat('0')
    raw_input("Press anything to quit ")


def SobelEdge(array):
    '''
        Give this function a 32x32 array representing our gTower map.  
        Each entry is a gTower with some Et. The rows represent phi, starting with -pi
        and the columns represent eta, starting with -3.2.
        
        This function returns a 32x32 array with values of gradient.

    '''
    #################################
    # Sobel Matrix will be 3x3 and looks as follows:
    # [-1 -2 -1]  [-1 0 1]
    # [ 0  0  0]  [-2 0 2]
    # [ 1  2  1]  [-1 0 1]
    #################################

    # This is the "Working Array" (hence wArray). It is the input to thefile
    wArray = array

    # Makes a 32x32 array full of zeros.  We dont deal with 4-vectors; just arrays.
    
    gArray = MakeZeroArray()

    # Loop through rows, phi, and then columns, eta, and look at Et values in the working array (wArray)
    # We DO NOT calculate the gradient at eta edges (-3.2,3.2) as it wouldn't make any sense.
    # Wrapping in phi is included
    
    for p in range(32):
        for e in range(32):

            Gx = 0
            Gy = 0

            # Gradient set to 0 for edges in eta
            
            if e == 0 or e == 31:
                continue

            # When phi is -Pi we need to wrap
            elif p == 0:
            
                Gx = (0*wArray[p][e] + 0*wArray[p+1][e] + 0*wArray[31][e] + 2*wArray[p][e+1] + -2*wArray[p][e-1] + 1*wArray[p+1][e+1] + -1*wArray[31][e-1] + -1*wArray[p+1][e-1] + 1*wArray[31][e+1])/4
                Gy = (0*wArray[p][e] + 2*wArray[p+1][e] + -2*wArray[31][e] + 0*wArray[p][e+1] + 0*wArray[p][e-1] + 1*wArray[p+1][e+1] + -1*wArray[31][e-1] + 1*wArray[p+1][e-1] + -1*wArray[31][e+1])/4

                G = math.sqrt(Gx ** 2 + Gy ** 2)
                gArray[p][e] = G

                continue
            
            # When phi is Pi we also need to wrap 
            elif p == 31:
                
                Gx = (0*wArray[p][e] + 0*wArray[0][e] + 0*wArray[p-1][e] + 2*wArray[p][e+1] + -2*wArray[p][e-1] + 1*wArray[0][e+1] + -1*wArray[p-1][e-1] + -1*wArray[0][e-1] + 1*wArray[p-1][e+1])/4
                Gy = (0*wArray[p][e] + 2*wArray[0][e] + -2*wArray[p-1][e] + 0*wArray[p][e+1] + 0*wArray[p][e-1] + 1*wArray[0][e+1] + -1*wArray[p-1][e-1] + 1*wArray[0][e-1] + -1*wArray[p-1][e+1])/4

                G = math.sqrt(Gx ** 2 + Gy ** 2)
                gArray[p][e] = G

                continue

            # All other cases not at an edge
            else:
                Gx = (0*wArray[p][e] + 0*wArray[p+1][e] + 0*wArray[p-1][e] + 2*wArray[p][e+1] + -2*wArray[p][e-1] + 1*wArray[p+1][e+1] + -1*wArray[p-1][e-1] + -1*wArray[p+1][e-1] + 1*wArray[p-1][e+1])/4
                Gy = (0*wArray[p][e] + 2*wArray[p+1][e] + -2*wArray[p-1][e] + 0*wArray[p][e+1] + 0*wArray[p][e-1] + 1*wArray[p+1][e+1] + -1*wArray[p-1][e-1] + 1*wArray[p+1][e-1] + -1*wArray[p-1][e+1])/4

                G = math.sqrt(Gx ** 2 + Gy ** 2)
                gArray[p][e] = G
                    
    return gArray

def CutandThreshold(array,gThresh,neighbor):
    
    '''
    Give this function an array, some threshold and a boolean (respectively) telling the fuction
    whether or not to include the 2 neighbor secondary condition.

    This function returns fArray which is a "final array" setting entries that do not pass the cut to zero
    '''

    gThresh = gThresh * 1000
    wArray = array

    fArray = MakeZeroArray()
    
    for p in range(32):
        for e in range(32):
            
            neighbors = 0
            
            if e == 0 or e == 31:
                continue

            elif p == 0:
                
                if wArray[p][e] >= gThresh:
                    fArray[p][e] = wArray[p][e]
                
                elif neighbor == True:
                    
                    if wArray[p+1][e] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[31][e] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[p][e+1] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[p][e-1] >= gThresh:
                        neighbors = neighbors + 1                        
                    if neighbors >= 2:
                        fArray[p][e] = wArray[p][e]
                
                
                continue

            elif p == 31:
                
                if wArray[p][e] >= gThresh:
                    fArray[p][e] = wArray[p][e]
                    
                 
                elif neighbor == True:
                    
                    if wArray[0][e] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[p-1][e] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[p][e+1] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[p][e-1] >= gThresh:
                        neighbors = neighbors + 1                        
                    if neighbors >= 2:
                        fArray[p][e] = wArray[p][e]
                
                
                continue
            
            
            else:
                
                if wArray[p][e] >= gThresh:
                    fArray[p][e] = wArray[p][e]
                    
                
                elif neighbor == True:
                    
                    if wArray[p+1][e] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[p-1][e] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[p][e+1] >= gThresh:
                        neighbors = neighbors + 1
                    if wArray[p][e-1] >= gThresh:
                        neighbors = neighbors + 1                        
                    if neighbors >= 2:
                        fArray[p][e] = wArray[p][e]
                
                    
    return fArray


def CutTowers(edgeArray,arrayOfgTowers):
    
    finalgTowers = MakeZeroArray()
    
    for p in range(32):
        for e in range(32):
            if edgeArray[p][e] != 0:
                finalgTowers[p][e] = arrayOfgTowers[p][e]

    return finalgTowers


def plotAllArrays(arrayOfgTowers,gArray,eArray,fArray):

    a1 = arrayOfgTowers
    a3 = gArray
    a4 = eArray
    a5 = fArray
    
    H1 = TH2F("Event Display","Full Event Display: E_{T} in Eta vs. Phi;#eta;#phi",32,-3.2,3.2,32,-3.2,3.2)
    H3 = TH2F("Event Display","#Delta E_{T} in Eta vs. Phi;#eta;#phi",32,-3.2,3.2,32,-3.2,3.2)
    H4 = TH2F("Event Display","#Delta E_{T} Cut in Eta vs. Phi;#eta;#phi",32,-3.2,3.2,32,-3.2,3.2)
    H5 = TH2F("Event Display","Final E_{T} in Eta vs. Phi;#eta;#phi",32,-3.2,3.2,32,-3.2,3.2)

    etas = []
    phis = []
    for p in range(32):
        for e in range(32):
            phi = 0.2 * p - math.pi
            eta = 0.2 * e - math.pi

            etas.append(eta)
            phis.append(phi)
            H1.Fill(eta,phi,a1[p][e]/1000)
            H3.Fill(eta,phi,a3[p][e]/1000)
            H4.Fill(eta,phi,a4[p][e]/1000)
            H5.Fill(eta,phi,a5[p][e]/1000)

    c1 = TCanvas("Full")
    H1.Draw("colz")
    gStyle.SetOptStat('0')
    c1.SetLogz()
    
    c3 = TCanvas("Gradient")
    H3.Draw("colz")
    gStyle.SetOptStat('0')
    c3.SetLogz()
    
    c4 = TCanvas("Edge")
    H4.Draw("colz")
    gStyle.SetOptStat('0')
    c4.SetLogz()
    
    c5 = TCanvas("Final")
    H5.Draw("colz")
    gStyle.SetOptStat('0')
    c5.SetLogz()
    
    raw_input("Press anything to quit ")

def GetMet(finalTowers):

    total = TLorentzVector(0,0,0,0)
    EndgTowers = []

    for p in range(32):
        for e in range(32):
            if finalTowers[p][e] != 0:
                tower = TLorentzVector(0,0,0,0)
                phi = 0.2 * p - math.pi
                eta = 0.2 * e - math.pi
                tower.SetPtEtaPhiM(finalTowers[p][e],eta,phi,0)
                EndgTowers.append(tower)
                total = total + tower


    MET = total.Pt()/1000
    return MET, EndgTowers

def CalculateTruthMET(tEtas,tPhis,tPts):
    
    total = TLorentzVector(0,0,0,0)

    for i in range(len(tEtas)):
        tower = TLorentzVector(0,0,0,0)
        tower.SetPtEtaPhiM(tPts[i],tEtas[i],tPhis[i],0)
        total = total + tower

    tMET = total.Pt()/1000
    return tMET

gradList = [2,3,4,5,7,10,15]

NeighborBool = raw_input('Would you like to use neighboring? y/n: ')
GradBool = raw_input('Would you like to use the default grad cut list? y/n: ')


if GradBool == "y":
    for gThresh in gradList:
        print "########### Gradient Treshold %s ##############" %(gThresh)
        MakeNewFile('/export/home/llisi/ZHnoNeighborSamps/ZHGradient%sGeV.root' %(gThresh), '/headprv/atlas/local/eparrish/Samples/V11/ZH/TempZHnunubb.root','mytree',gThresh,False,0,10)

elif GradBool == "n":
    gThresh = int(raw_input('What gradient threshold would you like? '))
    MakeNewFile('/export/home/llisi/ZHnoNeighborSamps/ZHGradient%sGeV.root' %(gThresh), '/headprv/atlas/local/eparrish/Samples/V11/ZH/TempZHnunubb.root','mytree',gThresh,False,0,10)

else:
    print "Please specify y or n"
