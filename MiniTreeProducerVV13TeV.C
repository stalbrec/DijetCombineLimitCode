void MiniTreeProducerVV13TeV(string infile){


  double mgg, mjj,evWeight, mtot, normWeight;
 int categories;

 evWeight = 1.0;
 normWeight = 1.;



 string sInFile = infile;//"/shome/dschafer/ExoDiBosonAnalysis/results/ReRecoData_VVdijet.root";
 //string sInFile = "/shome/dschafer/ExoDiBosonAnalysis/results/QCD_pythia8_VV_summer16.root";
 cout << sInFile.c_str() << endl;
 TFile file0(sInFile.c_str(), "read");
 

 //string sOutFile("MiniTrees/Data_qV_13TeV/dijetqV_13TeV_miniTree.root");
 string suffix ="";
 if (infile.Contains("QCD") or infile.Contains("MC"))
 {
  suffix = "_MC";   
 }
 string sOutFile  = "MiniTrees/Data_qV_13TeV/dijetqV_13TeV_miniTree"+suffix+".root";
 int nCategorie = 8;
 int maxCategorie = 14;
 if (sInFile.find("VV")!=std::string::npos)
 {
    nCategorie = 0;
    maxCategorie  = 8;
    sOutFile ="MiniTrees/Data_VV_13TeV/dijetVV_13TeV_miniTree"+suffix+".root";
 }
 TFile f1(sOutFile.c_str(), "recreate");
 f1.cd();
 
 TTree *TCVARS = new TTree("TCVARS", "VV selection");
 TCVARS->Branch("mgg13TeV",&mgg,"mgg/D");
 
 TCVARS->Branch("evWeight",&evWeight,"evWeight/D");
 TCVARS->Branch("normWeight",&normWeight,"normWeight/D");
 
 TCVARS->Branch("categories",&categories,"categories/I");
 TH1D* hMass;
 for (int iCat = nCategorie; iCat < maxCategorie; iCat++){
   if (iCat ==0 ) hMass = (TH1D*) file0.Get("DijetMassHighPuriVV;1");
   if (iCat == 1) hMass = (TH1D*) file0.Get("DijetMassLowPuriVV;1");
   
   if (iCat == 2) hMass = (TH1D*) file0.Get("DijetMassHighPuriWW;1");
   if (iCat == 3) hMass = (TH1D*) file0.Get("DijetMassLowPuriWW;1");
   
   if (iCat == 4) hMass = (TH1D*) file0.Get("DijetMassHighPuriWZ;1");
   if (iCat == 5) hMass = (TH1D*) file0.Get("DijetMassLowPuriWZ;1");
   
   if (iCat == 6) hMass = (TH1D*) file0.Get("DijetMassHighPuriZZ;1");
   if (iCat == 7) hMass = (TH1D*) file0.Get("DijetMassLowPuriZZ;1");

   if (iCat == 8) hMass = (TH1D*) file0.Get("DijetMassHighPuriqV;1");
   if (iCat == 9) hMass = (TH1D*) file0.Get("DijetMassLowPuriqV;1");

   if (iCat == 10) hMass = (TH1D*) file0.Get("DijetMassHighPuriqW;1");
   if (iCat == 11) hMass = (TH1D*) file0.Get("DijetMassLowPuriqW;1");

   if (iCat == 12) hMass = (TH1D*) file0.Get("DijetMassHighPuriqZ;1");
   if (iCat == 13) hMass = (TH1D*) file0.Get("DijetMassLowPuriqZ;1");
   //
   // if (iCat == 14) hMass = (TH1D*) file0.Get("DijetMassNoPuriVV;1");
   // if (iCat == 15) hMass = (TH1D*) file0.Get("DijetMassNoPuriWW;1");
   // if (iCat == 16) hMass = (TH1D*) file0.Get("DijetMassNoPuriWZ;1");
   // if (iCat == 17) hMass = (TH1D*) file0.Get("DijetMassNoPuriZZ;1");
   // if (iCat == 18) hMass = (TH1D*) file0.Get("DijetMassNoPuriqV;1");
   // if (iCat == 19) hMass = (TH1D*) file0.Get("DijetMassNoPuriqW;1");
   // if (iCat == 20) hMass = (TH1D*) file0.Get("DijetMassNoPuriqZ;1");    
  
   std::cout<<"Histogram = " << hMass->GetName() << "  category " << iCat<< std::endl;
   TAxis* Axis =   hMass->GetXaxis();
   std::cout << hMass->GetEntries() << std::endl;
   for (int i = 1 ; i < hMass->GetNbinsX()+1; i++){
     double N = abs(hMass->GetBinContent(i));
 
     //if (i%10 == 0) cout << "i = " << i << "N = " << N << " binCenter = " << hMass->GetBinCenter(i) << endl;
     mgg = Axis->GetBinCenter(i);
     
     normWeight = N;
     categories = iCat;
     if (N > 1e-10) TCVARS->Fill();
     // if (N > 0) TCVARS->Fill();
   }
 }

 

 TCVARS->Write();
 f1.Close();
 file0.Close();
 

}


