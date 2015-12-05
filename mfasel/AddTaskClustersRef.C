void AddTaskClustersRef(){
	  gROOT->LoadMacro(Form("%s/PWGJE/EMCALJetTasks/macros/AddTaskEmcalClusterRefSystematics.C", gSystem->Getenv("ALICE_PHYSICS")));
	  EMCalTriggerPtAnalysis::AliAnalysisTaskEmcalClustersRef *clustertask = AddTaskEmcalClusterRefSystematics("EmcCaloClusters", "sys");
	  clustertask->SetRequestAnalysisUtil(false);
	  gROOT->LoadMacro(Form("%s/PWGJE/EMCALJetTasks/macros/AddTaskEMCALDCALTrigger2015.C", gSystem->Getenv("ALICE_PHYSICS")));
	  EMCalTriggerPtAnalysis::AliAnalysisTaskEMCALDCALTrigger2015 *triggertask = AddTaskEMCALDCALTrigger2015("EmcCaloClusters");

	  gROOT->LoadMacro(Form("%s/PWGJE/EMCALJetTasks/macros/AddTaskEmcalPatchesRefSystematics.C", gSystem->Getenv("ALICE_PHYSICS")));
	  EMCalTriggerPtAnalysis::AliAnalysisTaskEmcalPatchesRef *patchtask = AddTaskEmcalPatchesRefSystematics("sys", "emcdc");
	  patchtask->SetRequestAnalysisUtil(false);
}
