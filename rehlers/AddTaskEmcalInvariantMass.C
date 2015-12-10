void AddTaskEmcalInvariantMass()
{
    const char * trainRoot = gSystem->Getenv("TRAIN_ROOT");
    if (trainRoot != 0)
    {
        gSystem->AddIncludePath(Form("%s/rehlers", trainRoot));
        Printf("Added rehlers user directory to includes.");
        gSystem->Load(Form("%s/AliAnalysisTaskEmcalInvariantMass.cxx++", trainRoot));
    }
    else
    {
        Printf("Failed to include rehlers user directory");
        return;
    }

    // Use ++ to only compile if necessary
    TString clustersName = "CaloClusters";
    gROOT->LoadMacro("$ALICE_PHYSICS/PWG/EMCAL/macros/AddTaskEmcalInvariantMass.C");
    AliAnalysisTaskEmcalInvariantMass* anaTask = AddTaskEmcalInvariantMass(/*tracksName,*/clustersName, 1);
}
