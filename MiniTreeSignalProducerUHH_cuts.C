void MiniTreeSignalProducerUHH_cuts(int samplemin=0, int samplemax=2, int dMass=2000, string sSelection=""){
     std::cout << " MiniTreeSignalProducerUHH" << std::endl;

 string dir = "";
  double mgg, mjj,evWeight, mtot, normWeight;
 int categories;

 evWeight = 1.0;
 normWeight = 1;
     std::cout << " After weight" << std::endl;
     std::cout << " samplemin " << samplemin << " samplemax "<< samplemax << std::endl;

 for (int iSample = samplemin; iSample < samplemax; iSample++){
     std::cout << " for on sample" << std::endl;
   
     string inFile;
     if (iSample == 0) inFile = string("graviton_");
     if (iSample == 1) inFile = string("radion_");
     if (iSample == 10) inFile = "";

     string outFile;
     if (iSample == 0) outFile = string("dijetUHH_13TeV_graviton");
     if (iSample == 1) outFile = string("dijetUHH_13TeV_radion");
     if (iSample == 10) outFile = string("dijetUHH_13TeV");

     string sInFile = dir+"input/" + inFile + Form("%s.root", sSelection.c_str());
     if(dMass>0)
       string sInFile = dir+"input/" + inFile + Form("%s%d.root", sSelection.c_str(), dMass);

     std::cout << sInFile.c_str() << std::endl;
     TFile file0(sInFile.c_str(), "read");

     string sOutFile = "MiniTrees/SignalUHH/" + outFile + Form("_%s_miniTree.root",sSelection.c_str());
     if(dMass>0)
       string sOutFile = "MiniTrees/SignalUHH/" + outFile + Form("_%s%d_miniTree.root",sSelection.c_str(), dMass);
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
       if (iCat == 0) hname = "radion_invMass;1";
       if (iCat == 1) hname = "radion_invMass_afterVBFsel;1";
       cout << hname << endl;
       hMass = (TH1D*) file0.Get(hname.c_str());
       if(!hMass) continue;
       
       TAxis* Axis =   hMass->GetXaxis();
       for (int i = 1 ; i < hMass->GetNbinsX()+1; i++){
	 //if (hMass->GetBinCenter(i) < dMass*0.75 || hMass->GetBinCenter(i) > dMass*1.25) continue;
	 int N = abs(hMass->GetBinContent(i));
	 if(iSample)
	    N = abs(hMass->GetBinContent(i)*100);
	 if (i%100 == 0) cout << "i = " << i << " N = " << N << endl;
	 
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
     std::cout << " After for" << std::endl;


}
