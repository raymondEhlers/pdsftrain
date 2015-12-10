void AddTaskEmcalInvariantMass()
{
    const char * trainRoot = gSystem->Getenv("TRAIN_ROOT");
    if (trainRoot != 0)
    {
        gSystem->AddIncludePath(Form("%s/rehlers", trainRoot));
        Printf("Added rehlers user directory to includes.");
        gSystem->Load(Form("%s/rehlers/AliAnalysisTaskEmcalInvariantMass.cxx++", trainRoot));
        
        // Use ++ to only compile if necessary
        TString clustersName = "CaloClusters";
        gROOT->LoadMacro(Form("%s/rehlers/AddTaskEmcalInvariantMass.C", trainRoot);
        AliAnalysisTaskEmcalInvariantMass* anaTask = AddTaskEmcalInvariantMass(/*tracksName,*/clustersName, 1);
    }
    else
    {
        Printf("Failed to include rehlers user directory");
    }
}
