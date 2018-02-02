void MiniTreeProducerDataUHH_cut(string selection){

 double mgg, mjj,evWeight, mtot, normWeight;
 int categories;
 string infile="input/radion_"+selection+"_2000.root";
 evWeight = 1.0;
 normWeight = 1.;

 string sInFile = infile;
 cout << sInFile.c_str() << endl;
 TFile file0(sInFile.c_str(), "read");
 

 string suffix ="";
 string sOutFile  = "MiniTrees/DataUHH/dijetUHH_13TeV_miniTree"+suffix+"_"+selection+".root";
 int minCategorie = 0;
 int maxCategorie = 2;//irene, before 1
 TFile f1(sOutFile.c_str(), "recreate");
 f1.cd();
 
 TTree *TCVARS = new TTree("TCVARS", "VV selection");
 TCVARS->Branch("mgg13TeV",&mgg,"mgg/D");
 
 TCVARS->Branch("evWeight",&evWeight,"evWeight/D");
 TCVARS->Branch("normWeight",&normWeight,"normWeight/D");
 
 TCVARS->Branch("categories",&categories,"categories/I");
 TH1D* hMass;
 for (int iCat = minCategorie; iCat < maxCategorie; iCat++){
   if (iCat == 0) hMass = (TH1D*) file0.Get("data_invMass;1");
   if (iCat == 1) hMass = (TH1D*) file0.Get("data_invMass_afterVBFsel;1");
  
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
