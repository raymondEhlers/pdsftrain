void LoadLibs(){
	/*
	 * Loading fastjet libraries - Required for jet libraries
	 */

	TString libs[] = {"CGAL","fastjet","siscone","siscone_spherical","fastjetplugins","fastjettools","fastjetcontribfragile"};
    /*TString extension = ".so";
    if (gSystem->GetFromPipe("uname -s") == "Darwin")
    {
        extension = ".dylib";
    }*/
	for(TString *libiter = libs; libiter < libs + sizeof(libs)/sizeof(TString); libiter++){
		gSystem->Load(Form("lib%s", libiter->Data()));
	}
}
