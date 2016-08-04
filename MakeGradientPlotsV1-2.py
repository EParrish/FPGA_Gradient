from ROOT import *

def OpenFile(file_path, tree_name):
    '''
    Opens your file.
    args:
        file_path: Path to your file
        tree_name: Name of the tree
    returns:
        none
    '''
    File = TFile(file_path)
    tree = File.Get(tree_name)
    return File,tree

def GetInfo(file_path,tree_name,GradThresh,EventNumber):

    File, tree = OpenFile(file_path,tree_name)
    
    nentries = tree.GetEntries()
    
    _Gradient_MET = []      #
    _Truth_MET = []         #
    _MET_Diff = []          #
    
    _CutgTowerEt = []       #
    _CutgTowerEta = []      #
    _CutgTowerPhi = []      #
    _CutgTowerN = []        #
    
    _gTowerGradient = []    #
    _gTowerN = []           #
    _gTowerEt = []          #
    _gTowerEta = []         #
    _gTowerPhi = []         #
    
    
    for event in range(nentries):
        if event % 100 == 0:
            print "Processing Event: " + str(event)
            
        tree.GetEntry(event)
        
        gTowerNs = tree.gTowerN
        
        Gradient_METs = tree.MET_Gradient
        Truth_METs = tree.Truth_MET
        CutgTowerNs = tree.CutgTowerN

        CutgTowerEts = tree.CutgTowerEt
        CutgTowerEtas = tree.CutgTowerEta
        CutgTowerPhis = tree.CutgTowerPhi

        gTowerGradients = tree.gTowerGradient
        gTowerEts = tree.gTowerEt
        gTowerPhis = tree.gTowerPhi
        gTowerEtas = tree.gTowerEta
        MET_Difference = (Truth_METs - Gradient_METs)
        
        _gTowerN.append(gTowerNs)
        _Truth_MET.append(Truth_METs)

        if CutgTowerNs != 0:
            _MET_Diff.append(MET_Difference)
            _Gradient_MET.append(Gradient_METs)
            _CutgTowerN.append(CutgTowerNs)

        for j in range(int(CutgTowerNs)):
            _CutgTowerEt.append(CutgTowerEts[j])
            _CutgTowerEta.append(CutgTowerEtas[j])
            _CutgTowerPhi.append(CutgTowerPhis[j])

        for i in range(int(gTowerNs)):
            _gTowerEt.append(gTowerEts[i])
            _gTowerEta.append(gTowerEtas[i])
            _gTowerPhi.append(gTowerPhis[i])
            _gTowerGradient.append(gTowerGradients[i])


    if len(_gTowerEt) != len(_gTowerGradient):
        raise Exception('Something went very wrong: A gradient was not calculated for each gTower...')


    H1 = HistoMaker1D(_Gradient_MET,"#Delta%s GeV E_{T}^{Miss}" %(GradThresh),"E_{T}^{Miss} [GeV]","Number of Events / (8 GeV)",100,0,800,"GradientMET")
    H2 = HistoMaker1D(_Truth_MET,"Truth E_{T}^{Miss}","E_{T}^{Miss} [GeV]","Number of Events / (8 GeV)",100,0,800,"TruthMET")
    H3 = HistoMaker1D(_CutgTowerEt,"#Delta%s GeV Cut gTower E_{T}" %(GradThresh),"E_{T} [GeV]","gTowers / (8 GeV)",100,0,800,"GradientgTowerEt")
    H4 = HistoMaker1D(_CutgTowerEta,"#Delta%s GeV Cut" %(GradThresh),"#eta","gTowers / 0.2 ",50,-5,5,"GradientgTowerEta")
    H5 = HistoMaker1D(_CutgTowerPhi,"#Delta%s GeV Cut" %(GradThresh),"#phi","gTowers / 0.2 ",50,-5,5,"GradientgTowerPhi")
    H6 = HistoMaker1D(_CutgTowerN,"#Delta%s GeV Cut" %(GradThresh),"Number of gTowers","Number of Events / (5 gTowers)",30,0,150,"GradientNgTowers")
    H7 = HistoMaker1D(_MET_Diff,"#Delta%s GeV Cut" %(GradThresh),"Truth E_{T}^{Miss} - Gradient E_{T}^{Miss} [GeV]","Number of Events / (8 GeV)",100,-400,400,"METDifference")
    H8 = HistoMaker1D(_gTowerGradient,"#Delta E_{T}","#Delta E_{T} [#Delta GeV/Tower]","Number of Events / (2 #Delta GeV/Tower)",200,0,400,"gTowerGradient")
    H9 = TH2F("", "gTower #Delta E_{T} vs. gTower E_{T}; gTower E_{T} [GeV]; gTower #Delta E_{T}",800,-800,800,400,0,800)

    


    for i in range(len(_gTowerEt)):
        if _gTowerGradient != 0:
            H9.Fill(_gTowerEt[i],_gTowerGradient[i])
    ###
    
    H10 = HistoMaker1D(_gTowerEt,"No Cut gTowerET","E_{T} [GeV]","gTowers / (8 GeV)",200,-800,800,"AllgTowerEt")


    H1.SaveAs("/export/home/llisi/ZHPlots/GradientMET%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H2.SaveAs("/export/home/llisi/ZHPlots/TruthMET%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H3.SaveAs("/export/home/llisi/ZHPlots/CutGradientgTowerEt%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H4.SaveAs("/export/home/llisi/ZHPlots/CutGradientgTowerEta%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H5.SaveAs("/export/home/llisi/ZHPlots/CutGradientgTowerPhi%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H6.SaveAs("/export/home/llisi/ZHPlots/CutGradientNgTowers%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H7.SaveAs("/export/home/llisi/ZHPlots/METDifference%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H8.SaveAs("/export/home/llisi/ZHPlots/gTowerGradient%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H9.SaveAs("/export/home/llisi/ZHPlots/gTowerGradientVSEt%sGeV-%s" %(GradThresh, EventNumber) + '.root')
    H10.SaveAs("/export/home/llisi/ZHPlots/AllgTowerEt%sGeV-%s" %(GradThresh, EventNumber) + '.root')


    
def HistoMaker2D(DataSetX,DataSetY,Title,xAxis,yAxis,Binning,xMin,xMax,SaveTitle):
    histo = TH2F("", Title + ";" +  xAxis + ";"  + yAxis, Binning, xMin, xMax)
    c1 = TCanvas('SaveTitle')
    
    for data in DataSet:
        histo.Fill(data)
    
    return histo

def HistoMaker1D(DataSet,Title,xAxis,yAxis,Binning,xMin,xMax,SaveTitle):
    histo = TH1F("", Title + ";" +  xAxis + ";"  + yAxis, Binning, xMin, xMax)
    c1 = TCanvas('SaveTitle')
    
    for data in DataSet:
        histo.Fill(data)
    
    return histo

gradList = [2,3,4,5,7,10,15]

GradBool = raw_input('Would you like to use the default grad cut list or single event? y/n or s for single: ')


if GradBool == "y":
    for i in gradList:
        print "########### Gradient Treshold %s ##############" %(i)
        GetInfo("/export/home/llisi/ZHGradientSamples/ZHGradient%sGeV.root" %(i),"mytree",i,'All')

elif GradBool == "n":
    GradThresh = int(raw_input('What gradient threshold would you like? '))
    GetInfo("/export/home/llisi/ZHGradientSamples/ZHGradient%sGeV.root" %(GradThresh),"mytree",GradThresh,'All')

elif GradBool == "s":
    GradThresh = int(raw_input('What gradient threshold would you like? '))
    EventNum = int(raw_input('Which event would you like? '))
    GetInfo("/export/home/llisi/SingleEventInfo/ZHGradient%sGeV-Event%s.root" %(GradThresh,EventNum),"mytree",GradThresh,EventNum)

else:
    print "Please specify y or n"
