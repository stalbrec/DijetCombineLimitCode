void MiniTreeSignalProducerUHH(int samplemin=0, int samplemax=2, int dMass=2000){

 string dir = "";
  double mgg, mjj,evWeight, mtot, normWeight;
 int categories;

 evWeight = 1.0;
 normWeight = 1;

 for (int iSample = samplemin; iSample < samplemax; iSample++){
   
   string inFile;
   if (iSample == 0) inFile = string("graviton");
   if (iSample == 1) inFile = string("radion");

   string outFile;
   if (iSample == 0) outFile = string("dijetUHH_13TeV_graviton");
   if (iSample == 1) outFile = string("dijetUHH_13TeV_radion");
   
     string sInFile = dir+"input/" + inFile + Form("Interpolated%d.root", dMass);
     cout << sInFile.c_str() << endl;
     TFile file0(sInFile.c_str(), "read");

     string sOutFile = dir+"MiniTrees/SignalUHH/" + outFile + Form("Interpolated%d_miniTree.root", dMass);
     TFile f1(sOutFile.c_str(), "recreate");
     f1.cd();

     TTree *TCVARS = new TTree("TCVARS", "VV selection");
     TCVARS->Branch("mgg13TeV",&mgg,"mgg/D");

     TCVARS->Branch("evWeight",&evWeight,"evWeight/D");
     TCVARS->Branch("normWeight",&normWeight,"normWeight/D");
     
     TCVARS->Branch("categories",&categories,"categories/I");

     for (int iCat = 0; iCat < 2; iCat++){
       TH1D* hMass;
       string hname;
       if (iCat == 0) hname = "_invMass;1";
       if (iCat == 1) hname = "_invMass_afterVBFsel;1";
       cout << hname << endl;
       hMass = (TH1D*) file0.Get(hname.c_str());
       if(!hMass) continue;
       
       TAxis* Axis =   hMass->GetXaxis();
       for (int i = 1 ; i < hMass->GetNbinsX()+1; i++){
	 //if (hMass->GetBinCenter(i) < dMass*0.75 || hMass->GetBinCenter(i) > dMass*1.25) continue;
	 int N = abs(hMass->GetBinContent(i));
	 if (i%1000 == 0) cout << "i = " << i << " N = " << N << endl;
	 
	 mgg = Axis->GetBinCenter(i);
	 
         categories = iCat;
	 for (int k = 0; k < N; k++) {
	   TCVARS->Fill();
	 }
       }
     }
		 TCVARS->Write();
     f1.Close();
     file0.Close();
     

 }


}
