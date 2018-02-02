#include "TH2.h"
#include <sstream>
#include <iostream>
#include <fstream>

using namespace std;
#define Channels 2
#define Categories 2
#define cutTau 5
#define cutEta 4
#define MassPoints 3

//less /nfs/dust/cms/user/abenecke/scripts/plots/Limit_2d.C


bool print=true; 
TString dir = "/nfs/dust/cms/user/zoiirene/CombineTutorial/CMSSW_8_1_0/src/DijetCombineLimitCode/LimitTxt/Collage/";



void Limit2D(){

  TString channel[Channels];
  channel[0] = "graviton";
  channel[1] = "radion";

  TString category[Categories];
  category[0] = "invMass";
  category[1] = "invMass_afterVBFsel";
  
  
  TString cut_tau21[cutTau];
  cut_tau21[0] = "tau21";
  cut_tau21[1] = "tau21_04";
  cut_tau21[2] = "tau21_05";
  cut_tau21[3] = "tau21_06";
  cut_tau21[4] = "tau21_07";
  

  TString cut_deta[cutEta];

// cut_deta[0] = "DijetM500"; //NB need to modify ouptut txt!!!
// cut_deta[1] = "DijetM1000";
// cut_deta[2] = "DijetM1500";
// cut_deta[3] = "DijetM2000";
  
  cut_deta[0] = "deta"; //NB need to modify ouptut txt!!!
//  cut_deta[0] = ""; //NB need to modify ouptut txt!!!
  cut_deta[1] = "deta4";
  cut_deta[2] = "deta5";
  cut_deta[3] = "deta6";
  
  TString Mass[MassPoints];
  Mass[0] = "1200";
  Mass[1] = "2000";
  Mass[2] = "4000";
  

 
  std::vector<TString> mass = {"1200","2000","4000"};
  std::vector<TString> channels = {"graviton","radion"};
  std::vector<TString> tau21cut = {"0.35","0.4","0.5","0.6","0.7"};
  std::vector<TString> detacut = {"3","4","5","6"};
  


  typedef std::map<std::pair<int, int>, double > Maptype;

  Maptype Limit_graviton_1200;
  Maptype Limit_graviton_2000;
  Maptype Limit_graviton_4000;
  Maptype Limit_radion_1200;
  Maptype Limit_radion_2000;
  Maptype Limit_radion_4000;
 
  double limit[MassPoints];   
  TString filename;
 
  //get limits from file
  for(int i=0;i<channels.size();i++)
    {
      for(int j=0;j<cutTau;j++)
	{
	  for(int k=0;k<cutEta;k++)
	    {
	      filename = dir+channel[i]+"__"+category[1]+"_"+cut_tau21[j]+"_"+cut_deta[k]+"_new_combined_Limit.txt";
	      //	      if(k==0) filename = dir+channel[i]+"__"+category[1]+"_"+cut_tau21[j]+"_new_combined_Limit.txt";
	      cout << filename << endl;
	      ifstream stream(filename);
	      std::string line;
	      if(!stream.is_open())	      
		{
		  limit[0]=0;
		  limit[1]=0;
		  limit[2]=0;
		  cout << " File " << filename << " not opened" << endl;
		}
	      else
		{
		  std::getline(stream,line);
		  if(print) cout << " first line " << line << endl; 
		  while(!stream.eof())
		    stream  >> limit[0]  >> limit[1] >> limit[2];
		  
		}
		  cout << "Limit for channel " << channel[i] << " category  " << category[1] << " and cuts " << cut_tau21[j]<< " " << cut_deta[k] << " : " << endl;
		  for(int l=0;l<MassPoints;l++)
		    cout << " Mass " << Mass[l] << " -> " << limit[l] << endl;

	      if(i==0)
		{
		  Limit_graviton_1200.insert( std::make_pair(std::make_pair( j,k ), limit[0]) );
		  Limit_graviton_2000.insert( std::make_pair(std::make_pair( j,k ), limit[1]) );
		  Limit_graviton_4000.insert( std::make_pair(std::make_pair( j,k ), limit[2]) );

		  cout << "Limit for channel graviton_1200[" << j  << "]["<< k << "] : "<< Limit_graviton_1200[std::make_pair( j,k )];
		  cout << "Limit for channel graviton_2000[" << j  << "]["<< k << "] : "<< Limit_graviton_2000.begin()->second << endl;
		  cout << "Limit for channel graviton_4000[" << j  << "]["<< k << "] : "<< Limit_graviton_4000.begin()->second << endl;

		}
	      if(i==1)
		{
		  Limit_radion_1200.insert( std::make_pair(std::make_pair( j,k ), limit[0]) );
		  Limit_radion_2000.insert( std::make_pair(std::make_pair( j,k ), limit[1]) );
		  Limit_radion_4000.insert( std::make_pair(std::make_pair( j,k ), limit[2]) );
		  cout << "Limit for channel radion_1200[" << j  << "]["<< k << "] : "<< Limit_radion_1200.begin()->second << endl;
		  cout << "Limit for channel radion_2000[" << j  << "]["<< k << "] : "<< Limit_radion_2000.begin()->second << endl;
		  cout << "Limit for channel radion_4000[" << j  << "]["<< k << "] : "<< Limit_radion_4000.begin()->second << endl;
		}


	    }//cut eta
	}//cut tau
    }//channels



  //histograms and canvas
  for(int i=0;i<channels.size();i++)
    {
    for(int j=0;j<mass.size();j++)
      {
	
	TH2F *limit_hist = new TH2F("limit_hist","Limit hist",tau21cut.size(),0,5,detacut.size(),0,4);

	cout << " tau21cut.size() " << tau21cut.size() << " and detacut.size() " << detacut.size() << endl; 

       	for(int l=0;l<tau21cut.size();l++){
	//if(j==0) detacut = {"700","900","1200"};

	  for(int k=0;k<detacut.size();k++){
	    // someMap.find(someKey)->second
	      if(channel[i]=="graviton" && Mass[j]=="1200")limit_hist->Fill(tau21cut[l],detacut[k],Limit_graviton_1200.find(std::make_pair(l,k))->second);
	    if(channel[i]=="graviton" && Mass[j]=="2000")limit_hist->Fill(tau21cut[l],detacut[k],Limit_graviton_2000[std::make_pair(l,k)]);
	    if(channel[i]=="graviton" && Mass[j]=="4000")limit_hist->Fill(tau21cut[l],detacut[k],Limit_graviton_4000[std::make_pair(l,k)]);
	    if(channel[i]=="radion" && Mass[j]=="1200")limit_hist->Fill(tau21cut[l],detacut[k],Limit_radion_1200[std::make_pair(l,k)]);
	    if(channel[i]=="radion" && Mass[j]=="2000")limit_hist->Fill(tau21cut[l],detacut[k],Limit_radion_2000[std::make_pair(l,k)]);
	    if(channel[i]=="radion" && Mass[j]=="4000")limit_hist->Fill(tau21cut[l],detacut[k],Limit_radion_4000[std::make_pair(l,k)]);
	  
	  }//detacut
	}//tau21cut

	//save result
	TCanvas *c1= new TCanvas("c1","c1",10,10,600,600);
	c1->Clear();
	c1->cd();
	gPad->SetTickx();
	gPad->SetTicky();
	gStyle->SetOptStat(0);
	c1->SetTopMargin(0.05);
	c1->SetBottomMargin(0.15); 
	c1->SetRightMargin(0.15);
	c1->SetLeftMargin(0.1);
	limit_hist->SetTitle("");
	limit_hist->GetXaxis()->SetTitle("#tau_{21}");
	limit_hist->GetYaxis()->SetTitle("|#Delta #eta_{VBF}|");
	limit_hist->Draw("colz");
	limit_hist->Draw("same TEXT");

	// TPaveText *pt = new TPaveText(.625,.16,.84,.26,"nbNDC");
	// pt->SetFillColor(0);
	// if(decays[i]=="HT")pt->AddText("T ' #rightarrow H t");
	// if(decays[i]=="ZT")pt->AddText("T ' #rightarrow Z t");
	// if(decays[i]=="WB")pt->AddText("T ' #rightarrow W b");
	// pt->Draw();


	c1->Print(dir+"Limit_new_"+channel[i]+"_"+Mass[j]+".eps");




      }//mass
    }//channels

}//limits 2D
