void MiniTreeSignalProducerqV13TeV(int samplemin, int samplemax){


  double mgg, mjj,evWeight, mtot, normWeight;
 int categories;

 evWeight = 1.0;
 normWeight = 1;

 for (int iSample = samplemin; iSample < samplemax; iSample++){
   
   string inFile("WprimeToWZ");
   if (iSample == 1) inFile = string("RS1WW");
   if (iSample == 2) inFile = string("RS1ZZ"); // Fake ZZ signal
   if (iSample == 3) inFile = string("QstarQW");
   if (iSample == 4) inFile = string("QstarQZ");
   if (iSample == 5) inFile = string("BulkWW");
   if (iSample == 6) inFile = string("BulkZZ");
   if (iSample == 7) inFile = string("ZprimeWW");
   if (iSample == 8) inFile = string("WprimeWZ");

   string outFile("dijetVV_13TeV_WZ");
   if (iSample == 1) outFile = string("dijetVV_13TeV_RS1WW");
   if (iSample == 2) outFile = string("dijetVV_13TeV_RS1ZZ");
   if (iSample == 3) outFile = string("dijetVV_13TeV_QstarQW");
   if (iSample == 4) outFile = string("dijetVV_13TeV_QstarQZ");
   if (iSample == 5) outFile = string("dijetVV_13TeV_BulkWW");
   if (iSample == 6) outFile = string("dijetVV_13TeV_BulkZZ");
   if (iSample == 7) outFile = string("dijetVV_13TeV_ZprimeWW");
   if (iSample == 8) outFile = string("dijetVV_13TeV_WZ");
   
   int massrange=60;

   for (int iMass = 0; iMass<massrange; iMass++){

     string sInFile = "input/" + inFile + "_13TeV_10k_" + Form("OUT%dGeV.root", 1000+iMass*100);
     cout << sInFile.c_str() << endl;
     TFile file0(sInFile.c_str(), "read");

     string sOutFile = "MiniTrees/Signal_qV_13TeV/" + outFile + Form("OUT%d_miniTree.root", 1000+iMass*100);
     TFile f1(sOutFile.c_str(), "recreate");
     f1.cd();
     std::cout << sOutFile << std::endl;
     TTree *TCVARS = new TTree("TCVARS", "VV selection");
     TCVARS->Branch("mgg13TeV",&mgg,"mgg/D");

     TCVARS->Branch("evWeight",&evWeight,"evWeight/D");
     TCVARS->Branch("normWeight",&normWeight,"normWeight/D");
     
     TCVARS->Branch("categories",&categories,"categories/I");

  
     double dMass = 1000.+iMass*100.;

     
     for (int iCat = 8; iCat < 14; iCat++){
       TH1D* hMass = (TH1D*) file0.Get("DijetMassHighPuriVV;1");

    
       if (iCat == 8) hMass = (TH1D*) file0.Get("DijetMassHighPuriqV;1");
       if (iCat == 9) hMass = (TH1D*) file0.Get("DijetMassLowPuriqV;1");

       if (iCat == 10) hMass = (TH1D*) file0.Get("DijetMassHighPuriqW;1");
       if (iCat == 11) hMass = (TH1D*) file0.Get("DijetMassLowPuriqW;1");

       if (iCat == 12) hMass = (TH1D*) file0.Get("DijetMassHighPuriqZ;1");
       if (iCat == 13) hMass = (TH1D*) file0.Get("DijetMassLowPuriqZ;1");

       
       if(!hMass) continue;
       
       TAxis* Axis =   hMass->GetXaxis();
       for (int i = 1 ; i < hMass->GetNbinsX()+1; i++){
         //std::cout << " loop over mass bins " << i << std::endl;
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


}


