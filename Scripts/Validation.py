import sys
import os
import platform
import socket
import shutil
import subprocess
import time
from datetime import date,datetime
import urllib


# RESTA A FAIRE : 
# note du 15 jin 2008
# - Cywin et MinGW OK
# - Visual : find pathe command_visual + Make clean + make install ne fonctionne pas.
# IMPORTANT cf mail Emmanuel: Pouvoir envoyer par mail a otb-dev le fichier CRT et CMakeCache.txt !!!!!
# REMARQUE sur l'appel au nvironnement fenetres Cygwin et MinGW : on pass par un shell car l'appel ne prend qu'un parametre 

# DESCRIPTION
# locale DIRECTOR (ex: ..../OTB-NIGHTLY-VALIDATION/sources/otb-hg-msdos
#                                                         /otb-hg-mingw     
#                                                         /otb-hg-cygwin
#                                                         /otb-hg-linux
#                                                         /otb-hg 'si aucune ambiguite comande svn (linux, unix)
#                                                 /"testConfigurationDir"/ (ex: visual-static-release-itk-internal-fltk-internal)
#                                                                        /binaries/OTB (make install in /install/standard dir)
#                                                                                 /OTB-Applications (make install in /install/standard dir)
#                                                                                 /OTB-Applications-with-install-OTB (make install in /install-with_install_OTB dir)
#                                        
#                                                                        /install-standard
#                                                                        /install-with-install-OTB    
#
# The "testConfigurationDir" directory is automatically destroy when we select the option SetGenerateMakefiles(True) 
# Tools directories
# mode       : cygwin, mingw, visual7, visual8, unix, linux, macosx, ou "vide" si pas d'ambiguite de platforme
# build_type : release, debug, debugwall, 
#                      ..../OTB-OUTILS/gdal/"+mode+"-install"
#                                     /itk/sources/InsightToolkit-"itk_version
#                                     /itk/binaries-" +mode + "-" + build_type
#                                     /itk/install-" +mode + "-" + build_type + "/lib/InsightToolkit"
#                                     /fltk/binaries-" + mode + "-" + build_type
#                                     /vtk/install-" +mode + "-" + build_type + "/lib/vtk-5.0"



class TestProcessing:
    # Specifics platforms configuration 
    __python_mingw_command__ = "/c/Python25/python "
    __python_cygwin_command__ = "/cygdrive/c/Python25/python "
    __python_msdos_command__ = "c:\Python25\python.exe "
    
    __svn_mingw_command__ = "/c/Python25/python "
    
    # Define possible Visual command define on the host platform
    __use_to_detect_visual_7_command__ = "C:\Program Files\Microsoft Visual Studio .NET 2003\Common7\IDE\devenv.com"
#modif 1 octobre 2008 : pour "check_call"
    __use_to_running_visual_7_command__ = 'C:/PROGRA~1/MICROS~1.NET/Common7/IDE/devenv.com'
#    __use_to_running_visual_7_command__ = 'C:\\PROGRA~1\\MICROS~1.NET\\Common7\\IDE\\devenv.com'
    __use_to_detect_visual_8_command__ = "C:\Program Files\Microsoft Visual Studio 8\Common7\IDE\devenv.com"
    __use_to_running_visual_8_command__ = 'C:/PROGRA~1/MICROS~4/Common7/IDE/devenv.com'
    __use_to_detect_visual_express9_command__ = "C:\Program Files\Microsoft Visual Studio 9.0\Common7\IDE\VCExpress.exe"
    __use_to_running_visual_express9_command__ = 'C:\PROGRA~1\MICROS~1.0\Common7\IDE\VCExpress.exe'

    __use_to_running_visual_express2008_command__ = 'C:\PROGRA~1\MICROS~3\Common7\IDE\VCExpress.exe'
    __use_to_detect_visual_express2008_command__ = 'C:\Program Files\Microsoft Visual Studio 9.0\Common7\IDE\VCExpress.exe'

    __use_to_running_visual_express2005_command__ = 'C:\PROGRA~1\MICROS~3\Common7\IDE\VCExpress.exe'
    __use_to_detect_visual_express2005_command__ = 'C:\Program Files\Microsoft Visual Studio 8\Common7\IDE\VCExpress.exe'
	
    # Mingw call system command
    __mingw_system_command__ = 'C:/msys/1.0/bin/rxvt -backspacekey  -sl 2500 -fg Navy -bg LightYellow -sr -fn Courier-12 -tn msys -geometry 80x25 -e /bin/sh --login -i '
    # Cygwin call system command
#    __cygwin_system_command__ = 'c:\\cygwin\\bin\\bash.exe --login -i '
#    __cygwin_system_command__ = 'c:/cygwin/cygwin.bat '
    __cygwin_system_command__ = 'c:/cygwin/bin/bash.exe --login -i '

    


    # Global parameters
    __crt_file__ = "Undefined"
    __list_binary_components__ = []
 #   __list_otb_components__ = []
    __list_otb_name_components__ = []

    # Users parameters
    __makeClean__ = False
    __makeCleanAfterCTest__ = False
    __cleanTestingResultsAfterCTest__ = False
    __disableCTest__ = False
    __disableBuildExamples__ = False
    __disableUseVtk__ = False
    __disableTestOTBApplicationsWithInstallOTB___ = True
    __disableGlUseAccel__ = True
    __genMakefiles__ = False
    __testConfigurationDir__ = "Undefined"
    __prefix_build_name__ = ""
    __distrib_name__ = ""
    __itkVersion__ = "3.10.1"
    __fltkVersion__ = "1.1.9"
    __vtkVersion__ = "5.0"
    __homeDir__ = ""
    __homeBaseDirOutils__ = ""
    __homeDirOutils__ = ""
    __homeBaseSourcesDir__ = ""
    __homeBaseRunDir__ = "local"
    __homeSourcesName__ = "WWW.ORFEO-TOOLBOX.ORG-CS-NIGHTLY"
    __fileLibNightlyNumber__ = ""
    __libNightlyNumber__ = ""
    __fileApplicationsNightlyNumber__ = ""
    __applicationsNightlyNumber__ = ""
    __homeOutilsName__ = "OTB-OUTILS"
    __homeRunName__ = "OTB-NIGHTLY-VALIDATION"
    __homeOtbSourceDir__ = ""
    __homeOtbApplicationsSourceDir__ = ""
    __homeOtbDataSourceDir__ = ""
    __homeOtbDataSourceName__ = ""
    __homeOtbDataLargeInputSourceDir__ = ""
    __enableUseOtbDataLargeInput__ = True
    __visual_command__ = ""
    
    __svn_username__ = "otbval"
    __svn_password__ = "otbval"
    # Modiy by the administrator 
    # Set to True to suppress svn update error when the OTB/Utilities/ITK source dir was updated. !!!!
    __cleanItkSourceDir__ = False 
    __update_nightly_sources__ = False
    __update_current_sources__ = False

    __geotiff_include_dirs__ = ""
    __tiff_include_dirs__ = ""
    __jpeg_include_dirs__ = ""
    __gdal_library__ = ""
    __geotiff_library__ = ""
    
    __tu_continuous_testing__ = "TU_CONTINUOUS_TESTING"
    __full_nightly_testing__ = "FULL_NIGHTLY_TESTING"
    __full_continuous_testing__ = "FULL_CONTINUOUS_TESTING"
    __configurationRunTesting__ = __full_nightly_testing__
    
   
    def __init__(self):


        self.__list_binary_components__.append("OTB")
        self.__list_binary_components__.append("OTB-Applications")
        self.__list_binary_components__.append("OTB-Applications-with-install-OTB")
        self.__list_otb_name_components__.append("OTB")
        self.__list_otb_name_components__.append("OTB-Applications")
        self.__list_otb_name_components__.append("OTB-Applications")
	
	# Default value
#	self.SetExperimental()



    #########################################################################################################"
    #########################################################################################################"
    ####                                                                                                  ###"
    ####                                                                                                  ###"
    ####                             M  A  I  N           R  U  N                                         ###"
    ####                                                                                                  ###"
    ####                           L O C A L   H O S T   S Y S T E M                                      ###"
    ####                                                                                                  ###"
    #########################################################################################################"
    #########################################################################################################"
    def RunLocalHostSytem(self,TestConfigurationDir):
        # Create CRT file
        home_dir = os.getcwd()
        crt_file = self.FindCrtFileName(TestConfigurationDir)
        if os.path.exists(crt_file):
                os.remove(crt_file)

        self.SetCrtFile(crt_file)

        # For MinGW and Cygwin, call system_command with this .py file (recursive call)
        # Attention : pou Cygwin, le fichhier doit etre en mode UNIX 
        # => solution, copy d'un fichier en UNIX et ecriture dedans
        # => autre solution a faire : dos2unix !!!

        # dos2unix transform temporary file (necessary for Cygwin)
        if os.path.exists(home_dir+"/tmp") == 0:
                os.mkdir(home_dir+"/tmp")
        tmpFileName =  os.path.abspath(home_dir+'/tmp/'+TestConfigurationDir+'.sh') #self.FindTemporayFileName()
#        tmpFileNameUnix = os.path.abspath(home_dir+'/otb-auto-unix-'+TestConfigurationDir+'.sh')
#        fileDos2Unix = os.path.abspath(home_dir+'/dos2unix.sh')
        dos2unix = os.path.abspath(home_dir+'/DOS2UNIX.exe')

        if TestConfigurationDir.find("mingw") != -1:
                print "Call Mingw X-server..."
                self.GenerateTemporaryShell(tmpFileName, self.__python_mingw_command__, TestConfigurationDir)
#                shell=home_dir + "/otb-internal.sh " + self.__python_mingw_command__ + " " + os.getcwd() + " " + TestConfigurationDir +" "+ self.GetTypeTest() +" "+  self.GetStringMakeClean()
#                tmpFileName="/e/travail/shell-test-otb/otb-internal-otb-auto.sh"
                self.CallCommand("Run Testing on MinGW plaform",self.__mingw_system_command__ + tmpFileName )
        else:
                if TestConfigurationDir.find("cygwin") != -1:
                        print "Call Cygwin X-server..."
                        self.GenerateTemporaryShell(tmpFileName, self.__python_cygwin_command__, TestConfigurationDir)
                        self.CallCommand("Run dos2unix on Cygwin plaform",dos2unix + ' ' + tmpFileName )
                        self.CallCommand("Run Testing on Cygwin plaform",self.__cygwin_system_command__ + ' "' + tmpFileName +'"')
                else:
                        print "RunHostPlatform"
                        self.Run(TestConfigurationDir)
        if os.path.exists(tmpFileName):
                os.remove(tmpFileName)
        

  
    # In HOST SYSTEM 
    #########################################################################################################"
    #########################################################################################################"
    ####                                                                                                  ###"
    ####                                                                                                  ###"
    ####                             M  A  I  N           R  U  N                                         ###"
    ####                                                                                                  ###"
    ####                              H O S T   P L A T F O R M                                           ###"
    ####                                                                                                  ###"
    #########################################################################################################"
    #########################################################################################################"
    def RunUpdateSources(self):
        # Get CrtFile
        crt_file = self.FindCrtFileName("update_sources")
        self.SetCrtFile(crt_file)
        # Set TestConfiguration 
        self.SetTestConfigurationDir("update_sources")

        self.PrintTitle('Run Update sources !')

        # Set and Check directories
        if self.__homeBaseRunDir__ == "local":
                self.__homeDir__ = os.path.abspath(os.getcwd())
        else:
                value = os.path.normpath(self.__homeBaseRunDir__+"/"+self.__homeRunName__)
                self.CallCheckDirectoryExit(self.__homeRunName__ +" dir",value)
                self.__homeDir__ = value

#        self.InitOutilsDir()
        self.InitSourcesDir()
        self.UpdateSources()
    
    def Run(self,TestConfigurationDir):
        # Get CrtFile
        crt_file = self.FindCrtFileName(TestConfigurationDir)
        self.SetCrtFile(crt_file)
        # Set TestConfiguration 
        self.SetTestConfigurationDir(TestConfigurationDir)



        self.PrintTitle('Run Host Platform process for "'+self.GetTestConfigurationDir()+'" testing !')
    

        # ------------------------------------------------------------
        self.PrintTitle("1/6  :  Check directories  ... ")
        # ------------------------------------------------------------
        # Set and Check directories
        if self.__homeBaseRunDir__ == "local":
                self.__homeDir__ = os.path.abspath(os.getcwd())
        else:
                value = os.path.normpath(self.__homeBaseRunDir__+"/"+self.__homeRunName__)
                self.CallCheckDirectoryExit(self.__homeRunName__ +" dir",value)
                self.__homeDir__ = value

        self.InitOutilsDir()
        self.InitSourcesDir()
#        self.SetHomeDir(os.getcwd())
#        self.SetOtbSourceDir(self.GetHomeDir())
#        self.SetOtbDataSourceDir(self.GetHomeDir())
#        self.SetHomeDirOutils(self.GetHomeDir())
 
        self.InitSetVisualCommand()

        binary_home_dir=os.path.normpath(self.GetHomeDir()+"/"+self.GetTestConfigurationDir())

        self.PrintMsg("Get Initial version of OTB sources ...")
        initial_version_otb_source_dir = self.CallGetVersion(self.GetOtbSourceDir())
        initial_version_otb_applications_source_dir = self.CallGetVersion(self.GetOtbApplicationsSourceDir())
        initial_version_otb_data_source_dir = self.CallGetVersion(self.GetOtbDataSourceDir())

        # Check ITK installation
        # ================================================================
        if self.GetTestConfigurationDir().find("itk-exter") != -1:
                self.CheckItkInstallation()
        # Check  FLTK installation
        # ================================================================
        if self.GetTestConfigurationDir().find("fltk-exter") != -1:
                self.CheckFltkInstallation()
        # Check  VTK installation
        # ================================================================
        if self.__disableUseVtk__ == False:
                self.CheckVtkInstallation()

        # ------------------------------------------------------------
        self.PrintTitle("2/6  :  Update sources  ... ")
        # ------------------------------------------------------------
#        self.CallChangeDirectory("otb source",self.GetHomeDir() )
        if self.GetUpdateNightlySources() == True:
                self.UpdateNightlySources()
        elif self.GetUpdateCurrentSources() == True:
                self.UpdateCurrentSources()
        else:
                self.PrintMsg("Update sources DISABLE !!")

        self.CallChangeDirectory("otb source",self.GetHomeDir() )

        # ------------------------------------------------------------
        self.PrintTitle("3/6  :  Cleans/Creates operations  ... ")
        # ------------------------------------------------------------
        if self.GetGenerateMakefiles() == True:
                self.CallRemoveDirectory("Main test",binary_home_dir)
                self.CallCreateDirectory(self.__list_binary_components__[0]+" binary",binary_home_dir+"/binaries/"+self.__list_binary_components__[0])
                self.CallCreateDirectory(self.__list_binary_components__[1]+" binary",binary_home_dir+"/binaries/"+self.__list_binary_components__[1])
                self.CallCreateDirectory(self.__list_binary_components__[2]+" binary",binary_home_dir+"/binaries/"+self.__list_binary_components__[2])
                self.CallCreateDirectory("Install standard",binary_home_dir+"/install-standard")
                self.CallCreateDirectory("Install with install OTB",binary_home_dir+"/install-with-install-OTB")
        
        else:
                # ---  Clean the Install directory   ----------------------------------
                self.CallRemoveDirectory("Install standard",binary_home_dir+"/install-standard")
                self.CallRemoveDirectory("Install with install OTB",binary_home_dir+"/install-with-install-OTB")

        if self.__cleanItkSourceDir__ == True:
                self.CallRemoveDirectory(" ******************  ATTENTION *******************  =>  OTB/Utilities/ITK (to suppress error svn because ITK version had been updated",os.path.normpath(self.GetOtbSourceDir()+'/OTB/Utilities/ITK'))
                self.__cleanItkSourceDir__ = False
        
                

	# ---  Processing test for alls modules   ----------------------------------

        # Read hg current version 
        current_version_otb_source_dir = self.CallGetVersion(self.GetOtbSourceDir())
        current_version_otb_applications_source_dir = self.CallGetVersion(self.GetOtbApplicationsSourceDir())
        current_version_otb_data_source_dir = self.CallGetVersion(self.GetOtbDataSourceDir())
        self.PrintMsg("OTB Version before " + initial_version_otb_source_dir + " and current " +current_version_otb_source_dir+".")
        self.PrintMsg("OTB-Applications Version before " + initial_version_otb_applications_source_dir + " and current " +current_version_otb_applications_source_dir+".")
        self.PrintMsg("OTB-Data Version before " + initial_version_otb_data_source_dir + " and current " +current_version_otb_data_source_dir+".")
        component_cpt=0
        self.PrintTitle(str(component_cpt+4)+"/6  :  "+self.__list_binary_components__[component_cpt]+" processing  ... ")
#        self.RunProcessTesting(self.__list_otb_components__[component_cpt],self.__list_binary_components__[component_cpt],self.__list_otb_name_components__[component_cpt])
        is_up_to_date = True
        if initial_version_otb_data_source_dir != current_version_otb_data_source_dir:
            is_up_to_date = False
        elif initial_version_otb_source_dir != current_version_otb_source_dir:
            is_up_to_date = False
        self.RunProcessTesting(self.__list_binary_components__[component_cpt],self.__list_otb_name_components__[component_cpt],is_up_to_date)
        component_cpt = component_cpt + 1
        self.PrintTitle(str(component_cpt+4)+"/6  :  "+self.__list_binary_components__[component_cpt]+" processing  ... ")

        is_up_to_date = True
        if initial_version_otb_data_source_dir != current_version_otb_data_source_dir:
            is_up_to_date = False
        elif initial_version_otb_applications_source_dir != current_version_otb_applications_source_dir:
            is_up_to_date = False
        self.RunProcessTesting(self.__list_binary_components__[component_cpt],self.__list_otb_name_components__[component_cpt],is_up_to_date)
        component_cpt = component_cpt + 1
        self.PrintTitle(str(component_cpt+4)+"/6  :  "+self.__list_binary_components__[component_cpt]+" processing  ... ")
        if self.__disableTestOTBApplicationsWithInstallOTB___ == False:
                self.RunProcessTesting(self.__list_binary_components__[component_cpt],self.__list_otb_name_components__[component_cpt],is_up_to_date)
        else:
                self.PrintMsg("Testing OTB-Applications with install OTB dir is DISABLE")

        self.CallChangeDirectory("Home",self.GetHomeDir())



    # =====================================================================================================================================
    # ===  Run Process Testing for a component
    # =====================================================================================================================================
    def RunSubProcessTesting(self,current_module,current_name_module,comment_ctest_call_command,ctest_call_command,is_up_to_date):
        if is_up_to_date == False or self.IsDisableCTest() == True:
                binary_home_dir=os.path.normpath(self.GetHomeDir()+"/"+self.GetTestConfigurationDir())
                current_binary_dir=binary_home_dir + "/binaries/"+current_module
                self.CallChangeDirectory(current_module,current_binary_dir )

                if self.GetGenerateMakefiles() == True:
                        self.GenerateMakefiles(current_module,current_name_module)
                else:
                        self.CallRemoveDirectory("Testing/Temporary",current_binary_dir + "/Testing/Temporary")
                        if self.GetMakeClean() == True:
                                if self.GetTestConfigurationDir().find("visual") != -1:
                                        self.CallCommand("Make Clean", self.GetVisualCommand() + " " + current_name_module+".sln /clean "+self.GetCmakeBuildType() +" /project ALL_BUILD")
                                else:
                                        self.CallCommand("Make Clean", "make clean")
                                self.CallRemoveDirectory("/bin",current_binary_dir + "/bin")
 
                # ctest ...
                if self.IsDisableCTest() == False:
                    self.PrintWarning(comment_ctest_call_command)
                    self.CallCommand("CTest execution",ctest_call_command)
                # make install
                if self.GetTestConfigurationDir().find("visual") != -1:
                        self.CallCommand("Make Install", self.GetVisualCommand() + " " + current_name_module+".sln /build "+self.GetCmakeBuildType() +"   /project INSTALL")
                else:
                        self.CallCommand("Make Install", "make install")
                if self.__makeCleanAfterCTest__ == True:
                        if self.GetTestConfigurationDir().find("visual") != -1:
                                self.CallCommand("Make Clean (After CTest)", self.GetVisualCommand() + " " + current_name_module+".sln /clean "+self.GetCmakeBuildType() +" /project ALL_BUILD")
                        else:
                                self.CallCommand("Make Clean (After CTest)", "make clean")
                        self.CallRemoveDirectory("/bin",current_binary_dir + "/bin")
                if self.__cleanTestingResultsAfterCTest__ == True:
                        self.CallRemoveDirectory("Testing/Temporary (After CTest)",current_binary_dir + "/Testing/Temporary")

        if self.IsDisableCTest() == True:
                self.PrintMsg("CTest execution DISABLE")
        if is_up_to_date == True:
                self.PrintMsg("CTest execution disable: the source code was UP TO DATE !")
    
    
    # =====================================================================================================================================
    # ===  Run Process Testing for a component
    # =====================================================================================================================================
    def RunProcessTesting(self,current_module,current_name_module,is_up_to_date):
        if self.__configurationRunTesting__ == self.__tu_continuous_testing__:
            self.RunSubProcessTesting(current_module,current_name_module,"CTest Continuous testing with only Tu (ctest -R ..Tu)", "CTest Continuous testing with only Tu (ctest -R ..Tu)", is_up_to_date )
        elif self.__configurationRunTesting__ == self.__full_continuous_testing__:
            self.RunSubProcessTesting(current_module,current_name_module,
            "CTest Full Continuous testing","ctest -D Experimental --track Continuous",is_up_to_date)
        elif self.__configurationRunTesting__ == self.__full_nightly_testing__:
            self.RunSubProcessTesting(current_module,current_name_module, "CTest Full Nightly testing","ctest -D Experimental --track Nightly",False) # false -> Force execution 
        else:
            self.RunSubProcessTesting(current_module,current_name_module, "CTest Full Nightly testing", "ctest -D Experimental --track Nightly",False)

    
    # =====================================================================================================================================
    # ===  Update Nightly sources method
    # =====================================================================================================================================
    def UpdateNightlySources(self):
#        os.environ['http_proxy'] = 'http://proxycs-toulouse.si.c-s.fr:8080'
        self.PrintMsg("Update Nightly Sources ...")
        
	# ---  HG update OTB  ----------------------------------
        revisionValue=urllib.urlopen('http://www.orfeo-toolbox.org/nightly/libNightlyNumber').read()
        self.PrintMsg("OTB revision: "+revisionValue)
        self.CallChangeDirectory("OTB",self.GetOtbSourceDir())
        self.CallCommand("Purge OTB ...","hg purge")
        self.CallCommand("Pull OTB ...","hg pull")
        self.CallCommand("Update OTB ...","hg update -r "+revisionValue)

        # ---  HG update OTB-Applications   ----------------------------------
        revisionValue=urllib.urlopen('http://www.orfeo-toolbox.org/nightly/applicationsNightlyNumber').read()
        self.PrintMsg("OTB-Application revision: "+revisionValue)

        self.CallChangeDirectory("OTB-Applications",self.GetOtbApplicationsSourceDir())
        self.CallCommand("Pull OTB-Applications ...","hg pull")
        self.CallCommand("Update OTB-Applications ...","hg update -r "+revisionValue)

        # ---  SVN update OTB-Data / LargeInput   ----------------------------------
#        if self.__homeOtbDataLargeInputSourceDir__ != "disable":
#           	self.CallCommand("Update OTB-Data-LargeInput..."," svn update " + self.GetOtbDataLargeInputSourceDir() +" --username "+self.GetSvnUsername() + " --password "+self.GetSvnPassword())

        # ---  HG update OTB-Data (ou OTB-Data)  ----------------------------------
        self.CallChangeDirectory("OTB-Data",self.GetOtbDataSourceDir() )
        self.CallCommand("Pull OTB-Data ...","hg pull")
        self.CallCommand("Update OTB-Data ...","hg update default")
        
        self.DisableUpdateNightlySources()
        
        
        
    # =====================================================================================================================================
    # ===  Update Current sources method
    # =====================================================================================================================================
    def UpdateCurrentSources(self):
        self.PrintMsg("Update Current Sources ...")
    	
	# ---  HG update OTB  ----------------------------------
        self.CallChangeDirectory("OTB",self.GetOtbSourceDir())
        self.CallCommand("Purge OTB ...","hg purge")
        self.CallCommand("Pull OTB ...","hg pull")
        self.CallCommand("Update OTB ...","hg update default")

        # ---  HG update OTB-Applications   ----------------------------------
        self.CallChangeDirectory("OTB-Applications",self.GetOtbApplicationsSourceDir())
        self.CallCommand("Pull OTB-Applications ...","hg pull")
        self.CallCommand("Update OTB-Applications ...","hg update default")

        # ---  HG update OTB-Data (ou OTB-Data)  ----------------------------------
        self.CallChangeDirectory("OTB-Data",self.GetOtbDataSourceDir() )
        self.CallCommand("Pull OTB-Data ...","hg pull")
        self.CallCommand("Update OTB-Data ...","hg update default")
        
        self.DisableUpdateCurrentSources()
    
    # =====================================================================================================================================
    # ===  Set/Get methods to configure the test process
    # =====================================================================================================================================
    # ---  Set/Get ItkVersion methods   -----------------------------------
    def SetItkVersion(self,itkVersion):
        self.__itkVersion__ = itkVersion
    def GetItkVersion(self):
        return self.__itkVersion__

    # ---  Set/Get Username/Pasword for svn base methods   -----------------------------------
    def SetSvnUsernamePassword(self,username, password):
        self.__svn_username__ = username
        self.__svn_password__ = password
    def GetSvnUsername(self):
        return self.__svn_username__
    def GetSvnPassword(self):
        return self.__svn_password__

    # ---  Set/Get FltkVersion methods   -----------------------------------
    def SetFltkVersion(self,fltkVersion):
        self.__fltkVersion__ = fltkVersion
    def GetFltkVersion(self):
        return self.__fltkVersion__

    # ---  Set/Get VtkVersion methods   -----------------------------------
    def SetVtkVersion(self,vtkVersion):
        self.__vtkVersion__ = vtkVersion
    def GetVtkVersion(self):
        return self.__vtkVersion__
       
    # ---  Disable/Enable UseVtk methods   -----------------------------------
    def DisableTestOTBApplicationsWithInstallOTB(self):
        self.__disableTestOTBApplicationsWithInstallOTB___ = True
    def EnableTestOTBApplicationsWithInstallOTB(self):
        self.__disableTestOTBApplicationsWithInstallOTB___ = False


    # ---  Disable/Enable Make Clean After CTest methods   -----------------------------------
    def DisableMakeCleanAfterCTest(self):
        self.__makeCleanAfterCTest__ = False
    def EnableMakeCleanAfterCTest(self):
        self.__makeCleanAfterCTest__ = True

    # ---  Disable/Enable Make Clean After CTest methods   -----------------------------------
    def DisableCleanTestingResultsAfterCTest(self):
        self.__cleanTestingResultsAfterCTest__ = False
    def EnableCleanTestingResultsAfterCTest(self):
        self.__cleanTestingResultsAfterCTest__ = True

    # ---  Disable/Enable UseVtk methods   -----------------------------------
    def DisableUseVtk(self):
        self.__disableUseVtk__ = True
    def EnableUseVtk(self):
        self.__disableUseVtk__ = False

    # ---  Disable/Enable BuildExamples methods   -----------------------------------
    def DisableBuildExamples(self):
        self.__disableBuildExamples__ = True
    def EnableBuildExamples(self):
        self.__disableBuildExamples__ = False
    
    
    
    def SetFullNightlyTesting(self):
        self.__configurationRunTesting__ = self.__full_nightly_testing__
    def SetFullContinuousTesting(self):
        self.__configurationRunTesting__ = self.__full_continuous_testing__
    def SetTuContinuousTesting(self):
        self.__configurationRunTesting__ = self.__tu_continuous_testing__

    # ---  Disable/Enable CTest (ex: only cmake generation ) methods   -----------------------------------
    def DisableCTest(self):
        self.__disableCTest__ = True
    def EnableCTest(self):
        self.__disableCTest__ = False
    def IsDisableCTest(self):
        return self.__disableCTest__
    def GetStringDisableCTest(self):
        if self.__disableCTest__ == True:
                return "True"
        else:
                return "False"

    # ---  Set/Get prefix buildname methods   -----------------------------------
    def SetPrefixBuildName(self,prefix_build_name):
        self.__prefix_build_name__ = prefix_build_name
    def GetPrefixBuildName(self):
        return self.__prefix_build_name__
    
    # ---  Set/Get distrib OS... methods   -----------------------------------
    def SetDistribName(self,distrib):
        self.__distrib_name__ = distrib
    def GetDistribName(self):
        return self.__distrib_name__

    # ---  Set/Get GEOTIFF_INCLUDE_DIRS methods   -----------------------------------
    def SetGeotiffIncludeDirs(self,geotiff_include_dirs):
        self.__geotiff_include_dirs__ = geotiff_include_dirs
    def GetGeotiffIncludeDirs(self):
        return self.__geotiff_include_dirs__ 

    # ---  Set/Get GEOTIFF_LIBRARY methods   -----------------------------------
    def SetGeotiffLibrary(self,geotiff_library):
        self.__geotiff_library__ = geotiff_library
    def GetGeotiffLibrary(self):
        return self.__geotiff_library__ 
    
    # ---  Set/Get TIFF_INCLUDE_DIRS methods   -----------------------------------
    def SetTiffIncludeDirs(self,tiff_include_dirs):
        self.__tiff_include_dirs__ = tiff_include_dirs
    def GetTiffIncludeDirs(self):
        return self.__tiff_include_dirs__ 

    # ---  Set/Get JPEG_INCLUDE_DIRS methods   -----------------------------------
    def SetJpegIncludeDirs(self,jpeg_include_dirs):
        self.__jpeg_include_dirs__ = jpeg_include_dirs
    def GetJpegIncludeDirs(self):
        return self.__jpeg_include_dirs__ 

    # ---  Set/Get GDAL_LIBRARY methods   -----------------------------------
    def SetGdalLibrary(self,gdal_library):
        self.__gdal_library__ = gdal_library
    def GetGdalLibrary(self):
        return self.__gdal_library__ 

    # ---  Disable/Enable Update Nightly sources methods   -----------------------------------
    def EnableUpdateNightlySources(self):
        self.__update_nightly_sources__ = True
    def DisableUpdateNightlySources(self):
        self.__update_nightly_sources__ = False
    def GetUpdateNightlySources(self):
        return self.__update_nightly_sources__

    # ---  Disable/Enable Update Current sources methods   -----------------------------------
    def EnableUpdateCurrentSources(self):
        self.__update_current_sources__ = True
    def DisableUpdateCurrentSources(self):
        self.__update_current_sources__ = False
    def GetUpdateCurrentSources(self):
        return self.__update_current_sources__
    
    # ---  deprecated Disable/Enable Update sources methods   -----------------------------------
    def EnableUpdateSources(self):
        self.PrintWarning("Deprecated 'EnableUpdateSources' function: Use 'EnableUpdateNightlySources' or 'EnableUpdateCurrentSources' functions to updates sources.") 
        self.EnableUpdateNightlySources()
        self.EnableUpdateCurrentSources()
    def DisableUpdateSources(self):
        self.PrintWarning("Deprecated 'DisableUpdateSources' function: Use 'DisableUpdateNightlySources' or 'DisableUpdateCurrentSources' functions to updates sources.") 
        self.DisableUpdateNightlySources()
        self.DisableUpdateCurrentSources()
    
    
    def GetStringUpdateSources(self):
        if self.__update_sources__ == True:
                return "True"
        else:
                return "False"

    # ---  Set/Get TestConfigurationDir methods   -----------------------------------
    def SetTestConfigurationDir(self,TestConfigurationDir):
        self.__testConfigurationDir__ = TestConfigurationDir
    def GetTestConfigurationDir(self):
        return self.__testConfigurationDir__

    # ===  Users methods   ===================================
        
    # ---  Generate Makefiles methods   -----------------------------------
    def EnableGenerateMakefiles(self):
        self.__genMakefiles__ = True
    def DisableGenerateMakefiles(self):
        self.__genMakefiles__ = False
    def GetGenerateMakefiles(self):
        return self.__genMakefiles__
    def GetStringGenerateMakefiles(self):
        if self.__genMakefiles__ == True:
                return "True"
        else:
                return "False"

    # ---  Make clean configuration methods   -----------------------------------
    def EnableMakeClean(self):
        self.__makeClean__ = True
    def DisableMakeClean(self):
        self.__makeClean__ = False
    def GetMakeClean(self):
        return self.__makeClean__
    def GetStringMakeClean(self):
        if self.__makeClean__ == True:
                return "True"
        else:
                return "False"
                
    def EnableGlUseAccel(self):
        self.__disableGlUseAccel__ = False
    def DisableGlUseAccel(self):
        self.__disableGlUseAccel__ = True


    def EnableUseOtbDataLargeInput(self):
        self.__enableUseOtbDataLargeInput__ = True
    def DisableUseOtbDataLargeInput(self):
        self.__enableUseOtbDataLargeInput__ = False
    def GetUseOtbDataLargeInput(self):
        return self.__enableUseOtbDataLargeInput__

    # ---  Set/Get RunDir methods   -----------------------------------
    def SetRunDir(self,homedir):
        save_rep = os.getcwd() 
        os.chdir(homedir)
        homedir = os.getcwd()
        os.chdir(save_rep)
        self.__homeBaseRunDir__ = homedir

    # ---  Set/Get HomeDir methods   -----------------------------------
    def SetOutilsDir(self,homedir):
        save_rep = os.getcwd() 
        os.chdir(homedir)
        homedir = os.getcwd()
        os.chdir(save_rep)
        self.__homeBaseDirOutils__ = homedir

    def InitOutilsDir(self):
        value = os.path.normpath(self.__homeBaseDirOutils__+"/"+self.__homeOutilsName__)
        self.CallCheckDirectoryExit(self.__homeOutilsName__,value)
        self.__homeDirOutils__ = value

    def GetHomeDirOutils(self):
        return self.__homeDirOutils__

    # ---  Set/Get HomeDir methods   -----------------------------------
#    def SetHomeDir(self,homedir):
#        self.__homeDir__ = os.path.abspath(homedir)
    def GetHomeDir(self):
        return self.__homeDir__

    # ---  Set/Get OtbSourceDir  GetOtbSourceName methods   -----------------------------------
    def GetOtbSourceName(self):
        return self.__homeOtbSourceName__

    def GetBaseSourcesDir(self):
        return self.__homeBaseSourcesDir__
    def GetOtbSourceDir(self):
        return self.__homeOtbSourceDir__
    def GetOtbApplicationsSourceDir(self):
        return self.__homeOtbApplicationsSourceDir__
    def GetOtbDataSourceDir(self):
        return self.__homeOtbDataSourceDir__
    def GetOtbDataLargeInputSourceDir(self):
        return self.__homeOtbDataLargeInputSourceDir__

    # --- HomeSourcesDir
    def SetSourcesDir(self,HomeSourcesDir):
        save_rep = os.getcwd() 
        os.chdir(HomeSourcesDir)
        HomeSourcesDir = os.getcwd()
        os.chdir(save_rep)
        self.__homeBaseSourcesDir__ = HomeSourcesDir

    def SetHomeSourcesName(self,HomeSourcesName):
        self.__homeSourcesName__=HomeSourcesName

    # --- Set OtbDataLargeInputDir 
    def SetOtbDataLargeInputDir(self,HomeDir):
        save_rep = os.getcwd() 
        os.chdir(HomeDir)
        HomeDir = os.getcwd()
        os.chdir(save_rep)
        self.__homeOtbDataLargeInputSourceDir__ = HomeDir

        
    def InitSourcesDir(self):
        # manip for cygwin : D: -> /cygdrive/d 
#        save_rep = os.getcwd() 
#        os.chdir(self.__homeBaseSourcesDir__)
#        HomeSourcesDir = os.getcwd()
#        os.chdir(save_rep)
        rep_base = os.path.normpath(self.__homeBaseSourcesDir__+"/"+self.__homeSourcesName__)
#        print "rep_base -> ",rep_base
        # Find OTB source dir
        value = os.path.normpath(rep_base+"/OTB")
        self.__homeOtbSourceDir__ = value
        self.CallCheckDirectoryExit("OTB dir",self.__homeOtbSourceDir__)
        
        # Find OTB-Applications source dir
        value = os.path.normpath(rep_base+"/OTB-Applications")
        self.__homeOtbApplicationsSourceDir__ = value
        self.CallCheckDirectoryExit("OTB-Applications dir",self.__homeOtbApplicationsSourceDir__)

        # Find OTB-Data source dir
        value = os.path.normpath(rep_base+"/OTB-Data")
        self.__homeOtbDataSourceDir__ = value
        self.CallCheckDirectoryExit("OTB-Data dir",self.__homeOtbDataSourceDir__)

        # Find OTB-Data-LargeInput source dir
#        value = os.path.normpath(rep_base+"/OTB-Data-LargeInput-HG")
#        if self.CallCheckDirectory("OTB-Data-LargeInput dir",value) != 0:
#                self.__homeOtbDataLargeInputSourceDir__ = value
#        else:
#                value = os.path.normpath(rep_base+"/OTB-Data-LargeInput")
#                if self.CallCheckDirectory("OTB-Data-LargeInput dir",value) != 0:
#                        self.__homeOtbDataLargeInputSourceDir__ = value
#                else:
#                        self.__homeOtbDataLargeInputSourceDir__ = "disable"
#                        self.PrintMsg( "-> OTB-Data-LargeInput disable !!")

        self.CallCheckDirectoryExit("OTB-Data-LargeInput dir",self.__homeOtbDataLargeInputSourceDir__)

        return

    # ---  Set/Get OtbDataSourceDir methods   -----------------------------------
    def GetOtbDataSourceName(self):
        return self.__homeOtbDataSourceName__

    # ---  Get/Init Visual Command methods   -----------------------------------
    def GetVisualCommand(self):
        return self.__visual_command__
    def InitSetVisualCommand(self):
        if self.GetTestConfigurationDir().find("visual7") != -1:
                self.__visual_command__ = self.__use_to_running_visual_7_command__
                mode = "visual7"
        elif self.GetTestConfigurationDir().find("visual8") != -1:
                self.__visual_command__ = self.__use_to_running_visual_8_command__
                mode = "visual8"
        elif self.GetTestConfigurationDir().find("visualExpress2008") != -1:
                self.__visual_command__ = self.__use_to_running_visual_express9_command__
                mode = "visual9"
        elif self.GetTestConfigurationDir().find("visualExpress2005") != -1:
                self.__visual_command__ = self.__use_to_running_visual_express2005_command__
                mode = "visualExpress2005"
        elif self.GetTestConfigurationDir().find("visual") != -1:
                if os.path.exists(self.__use_to_detect_visual_7_command__) != 0 :
                        self.__visual_command__ = self.__use_to_running_visual_7_command__
                if os.path.exists(self.__use_to_detect_visual_8_command__) != 0:
                        self.__visual_command__ = self.__use_to_running_visual_8_command__
                if os.path.exists(self.__use_to_detect_visual_express9_command__) != 0:
                        self.__visual_command__ = self.__use_to_running_visual_express9_command__
        #Check
        if self.GetTestConfigurationDir().find("visual") != -1:
                self.CallCheckDirectoryExit("Visual program",self.__visual_command__)



    # ===  Internals methods   ==================================
    def SetCrtFile(self,CrtFile):
        self.__crt_file__ = CrtFile
    def GetCrtFile(self):
        return self.__crt_file__
    
    # =====================================================================================================================================
    # ===  Generation of OTB makefiles (cmake process): BinComponent=OTB, OTB-Application or OTB-Applications-with-install-OTB
    # =====================================================================================================================================
    def GenerateMakefiles(self,BinComponent,NameComponent):
        HomeDir = self.GetHomeDir()
        HomeDirOutils=self.GetHomeDirOutils()
        mode = ""
        
        # ---  SVN update SrcComponent   ----------------------------------
#        self.CallChangeDirectory("otb source",self.GetOtbSourceDir() )
#        self.CallCommand("Update "+SrcComponent+"..."," svn update " + SrcComponent +" --username "+self.GetSvnUsername() + " --password "+self.GetSvnPassword())
#        self.CallCommand("Pull "+SrcComponent+"..."," hg pull " + SrcComponent )
#        self.CallCommand("Update "+SrcComponent+"..."," hg update " + SrcComponent )

        command_line = []
        command_line.append('cmake ')

        command_line.append( self.GetCmakePlatform())
        
        mode = self.GetMode()        
        build_type=self.GetBuildType()
        
        if self.GetTestConfigurationDir().find("shared") != -1:
                build_mode="shared"
        else:
                build_mode="static"

        # Sous Linux ou Unix, pas d'ambiguite platform : donc pas forcement linux dans le nom du repetoire  
        # A FAIRE
        
        #Init paths for externals lib
        gdal_lib = ""
        if mode == "":
                gdal_include_dir=os.path.normpath(HomeDirOutils + "/gdal/install/include")
                if self.GetTestConfigurationDir().find("visual") != -1:
                    gdal_lib=os.path.normpath(HomeDirOutils + "/gdal/install/lib/gdal.lib")
                    self.CallCheckFileExit("gdal library",gdal_lib)
                elif self.GetTestConfigurationDir().find("cygwin") != -1:
                    gdal_lib=os.path.normpath(HomeDirOutils + "/gdal/install/lib/libgdal.dll.a")
                    self.CallCheckFileExit("gdal library",gdal_lib)
                else:
                    gdal_lib=os.path.normpath(HomeDirOutils + "/gdal/install/lib/libgdal.so")
                    if self.CallCheckFile("gdal library",gdal_lib)  == 0:
                        gdal_lib=os.path.normpath(HomeDirOutils + "/gdal/install/lib/libgdal.a")
                        self.CallCheckFileExit("gdal library",gdal_lib)
                # Set Binaries FOR VISUAL and Debug (The .pch files are not installed, and generet WARNING)
                if self.GetTestConfigurationDir().find("visual") != -1 and self.GetTestConfigurationDir().find("debug") != -1:
                        itk_dir=os.path.normpath(HomeDirOutils + "/itk/binaries-" + build_mode +"-"+ build_type)
                else:
                        itk_dir=os.path.normpath(HomeDirOutils + "/itk/install-" + build_mode +"-"+ build_type + "/lib/InsightToolkit")
                fltk_dir=os.path.normpath(HomeDirOutils + "/fltk/binaries-" + build_mode +"-" + build_type +"-fltk-"+ self.GetFltkVersion())
                vtk_dir=os.path.normpath(HomeDirOutils + "/vtk/install-" + build_mode +"-"+ build_type + "-vtk-"+ self.GetVtkVersion() + "/lib/vtk-"+ self.GetVtkVersion())
        else:
                gdal_include_dir=os.path.normpath(HomeDirOutils + "/gdal/install-"+ mode+"/include")
                if self.GetTestConfigurationDir().find("visual") != -1:
                    gdal_lib=os.path.normpath(HomeDirOutils + "/gdal/install-"+ mode+"/lib/gdal.lib")
                    self.CallCheckFileExit("gdal library",gdal_lib)
                elif self.GetTestConfigurationDir().find("cygwin") != -1:
                    gdal_lib=os.path.normpath(HomeDirOutils + "/gdal/install-"+ mode+"/lib/libgdal.dll.a")
                    self.CallCheckFileExit("gdal library",gdal_lib)
                else:
                    gdal_lib=os.path.normpath(HomeDirOutils + "/gdal/install-"+ mode+"/lib/libgdal.so")
                    if self.CallCheckFile("gdal library",gdal_lib)  == 0:
                        gdal_lib=os.path.normpath(HomeDirOutils + "/gdal/install-"+ mode+"/lib/libgdal.a")
                        self.CallCheckFileExit("gdal library",gdal_lib)
                if self.GetTestConfigurationDir().find("visual") != -1 and self.GetTestConfigurationDir().find("debug") != -1:
                        itk_dir=os.path.normpath(HomeDirOutils + "/itk/binaries-" + mode + "-" + build_mode +"-"+ build_type +"-itk-"+ self.GetItkVersion())
                else:
                        itk_dir=os.path.normpath(HomeDirOutils + "/itk/install-" + mode + "-" + build_mode +"-"+ build_type +"-itk-"+ self.GetItkVersion() + "/lib/InsightToolkit")
                fltk_dir=os.path.normpath(HomeDirOutils + "/fltk/binaries-" + mode + "-" + build_mode +"-" + build_type +"-fltk-"+ self.GetFltkVersion() )
                vtk_dir=os.path.normpath(HomeDirOutils + "/vtk/install-" + mode + "-" + build_mode +"-"+ build_type +"-vtk-"+ self.GetVtkVersion() + "/lib/vtk-"+ self.GetVtkVersion())

        fltk_fluid_exe=""
        if self.GetTestConfigurationDir().find("visual") != -1:
                fltk_fluid_exe=os.path.normpath(fltk_dir+'/bin/'+build_type+'/fluid.exe')
        elif self.GetTestConfigurationDir().find("mingw") != -1:
                fltk_fluid_exe=os.path.normpath(fltk_dir+'/bin/fluid.exe')
        else:        
                fltk_fluid_exe=os.path.normpath(fltk_dir+'/bin/fluid')

        otb_install_standard=os.path.normpath(HomeDir+'/'+self.GetTestConfigurationDir()+'/install-standard')
        otb_install_with_install_OTB=os.path.normpath(HomeDir+'/'+self.GetTestConfigurationDir()+'/install-with-install-OTB')
        otb_binary_dir=os.path.normpath(HomeDir+'/'+self.GetTestConfigurationDir()+'/binaries/OTB')
        otb_lib_install_standard=os.path.normpath(HomeDir+'/'+self.GetTestConfigurationDir()+'/install-standard/lib/otb')
        

        self.CallCheckDirectoryExit("GDAL include",gdal_include_dir)
#        self.CallCheckDirectoryExit("GDAL lib",gdal_lib_dir)
        if self.GetTestConfigurationDir().find("fltk-ext") != -1:
                self.CallCheckDirectoryExit("FLTK",fltk_dir)
#dede                if os.path.isfile(fltk_fluid_exe):
#                self.CallCheckDirectoryExit("Fluid executable",fltk_fluid_exe)
        if self.GetTestConfigurationDir().find("itk-ext") != -1:
                self.CallCheckDirectoryExit("ITK",itk_dir)

        #Print Msg if parsing "itk-int" or "itk-ext" is failed
        if self.GetTestConfigurationDir().find("itk-int") == -1 & self.GetTestConfigurationDir().find("itk-ext") == -1 :
                self.PrintWarning("Parsing 'itk-int' or 'itk-ext' is not detected in '"+self.GetTestConfigurationDir()+"' configuration !! ITK Internal is default value.")
        if self.GetTestConfigurationDir().find("fltk-int") == -1 & self.GetTestConfigurationDir().find("fltk-ext") == -1 :
                self.PrintWarning("Parsing 'fltk-int' or 'fltk-ext' is not detected in '"+self.GetTestConfigurationDir()+"' configuration !! FLTK Internal is default value.")

        # For Visual, set CMAKE_CONFIGURATION_TYPES parameter        
        if self.GetTestConfigurationDir().find("visual") != -1:
                command_line.append(' -D "CMAKE_CONFIGURATION_TYPES:STRING='+self.GetCmakeBuildType()+'"  ')
        else:
                command_line.append(' -D "CMAKE_BUILD_TYPE:STRING='+self.GetCmakeBuildType()+'"  ')
                command_line.append(' -D "CMAKE_C_FLAGS_DEBUG:STRING=-g -Wall" ')
                command_line.append(' -D "CMAKE_CXX_FLAGS_DEBUG:STRING=-g -Wall" ')
                command_line.append(' -D "CMAKE_MODULE_LINKER_FLAGS_DEBUG:STRING=-Wall" ')
                command_line.append(' -D "CMAKE_EXE_LINKER_FLAGS_DEBUG:STRING=-Wall" ')


        command_line.append(' -D "BUILD_TESTING:BOOL=ON" ')

        build_name=self.GetBuildName()
        
        if BinComponent == "OTB":
        
                command_line.append(' -D "OTB_SHOW_ALL_MSG_DEBUG:BOOL=OFF" ')
                command_line.append(' -D "BUILD_DOXYGEN:BOOL=OFF" ')
                if self.__disableBuildExamples__ == True:
                        command_line.append(' -D "BUILD_EXAMPLES:BOOL=OFF" ')
                else:
                        command_line.append(' -D "BUILD_EXAMPLES:BOOL=ON" ')

                if self.GetTestConfigurationDir().find("shared") != -1:
                        command_line.append(' -D "BUILD_SHARED_LIBS:BOOL=ON" ')
                else:
                        command_line.append(' -D "BUILD_SHARED_LIBS:BOOL=OFF" ')

                command_line.append(' -D "CMAKE_INSTALL_PREFIX:PATH='+otb_install_standard+'"  ')

                command_line.append(' -D "GDAL_INCLUDE_DIRS:PATH='+gdal_include_dir+'"  ')
                if self.GetGdalLibrary() != "" :
                        command_line.append(' -D "GDAL_LIBRARY:FILEPATH='+self.GetGdalLibrary()+'" ')
                else:
                        command_line.append(' -D "GDAL_LIBRARY:FILEPATH='+gdal_lib+'" ')
                
                if self.GetTestConfigurationDir().find("fltk-ext") != -1:
                        command_line.append(' -D "OTB_USE_EXTERNAL_FLTK:BOOL=ON" ')
                        command_line.append(' -D "FLTK_DIR:PATH='+fltk_dir+'" ')
                        command_line.append(' -D "FLTK_FLUID_EXECUTABLE:FILEPATH='+fltk_fluid_exe+'" ' )
                else:
                        command_line.append(' -D "OTB_USE_EXTERNAL_FLTK:BOOL=OFF" ')
                        
                if self.GetTestConfigurationDir().find("itk-ext") != -1:
                        command_line.append(' -D "OTB_USE_EXTERNAL_ITK:BOOL=ON" ')
                        command_line.append(' -D "ITK_DIR:PATH='+itk_dir+'" ')
                else:
                        command_line.append(' -D "OTB_USE_EXTERNAL_ITK:BOOL=OFF" ')
                
                command_line.append(' -D "OTB_USE_JPEG2000:BOOL=ON" ')
                command_line.append(' -D "OTB_USE_PATENTED:BOOL=OFF" ')
                command_line.append(' -D "OTB_USE_VISU_GUI:BOOL=ON" ')
                
                if self.__disableGlUseAccel__ == True:
                        command_line.append(' -D "OTB_GL_USE_ACCEL:BOOL=OFF" ')
                else:
                        command_line.append(' -D "OTB_GL_USE_ACCEL:BOOL=ON" ')
                        
                if self.GetTestConfigurationDir().find("cygwin") != -1:
                        self.PrintWarning("For Cygwin, disable UUID cmake parameters in OTB generation makefiles process !!! UUID_INCLUDE_DIR and UUID_LIBRARY cmake variables are set to empty.")
                        command_line.append(' -D "UUID_INCLUDE_DIR:PATH=" ')
                        command_line.append(' -D "UUID_LIBRARY:FILEPATH=" ')
                        
                if self.GetTiffIncludeDirs() != "" :
                        command_line.append(' -D "TIFF_INCLUDE_DIRS:PATH='+self.GetTiffIncludeDirs()+'" ')
                if self.GetJpegIncludeDirs() != "" :
                        command_line.append(' -D "JPEG_INCLUDE_DIRS:PATH='+self.GetJpegIncludeDirs()+'" ')
                if self.GetGeotiffIncludeDirs() != "" :
                        command_line.append(' -D "GEOTIFF_INCLUDE_DIRS:PATH='+self.GetGeotiffIncludeDirs()+'" ')
                if self.GetGeotiffLibrary() != "" :
                        command_line.append(' -D "GEOTIFF_LIBRARY:FILEPATH='+self.GetGeotiffLibrary()+'" ')

                        
                
        if BinComponent == "OTB-Applications":
                command_line.append(' -D "OTB_DIR:PATH='+otb_binary_dir+'"  ')
                command_line.append(' -D "CMAKE_INSTALL_PREFIX:PATH='+otb_install_standard+'"  ')
                build_name='zApps-'+build_name

        if BinComponent == "OTB-Applications-with-install-OTB":
                command_line.append(' -D "OTB_DIR:PATH='+otb_lib_install_standard+'"  ')
                command_line.append(' -D "CMAKE_INSTALL_PREFIX:PATH='+otb_install_with_install_OTB+'"  ')
                build_name='zApps-'+build_name+'-WithInstallOTB'

        # Add VTK parameters
        if BinComponent.find("OTB-Applications") != -1:
                if self.__disableUseVtk__ == True:
                        command_line.append(' -D "OTB_USE_VTK:BOOL=OFF" ')
                else:
                        if self.CallCheckDirectory("VTK install",vtk_dir) == 0:
                                self.PrintWarning("TK was selected but the VTK library is not installed!!! Using VTK is disable (OTB_USE_VTK:BOOL=OFF)")
                                command_line.append(' -D "OTB_USE_VTK:BOOL=OFF" ')
                        else:
                                command_line.append(' -D "OTB_USE_VTK:BOOL=ON" ')
                                command_line.append(' -D "VTK_DIR:PATH='+vtk_dir+'" ')

        if self.GetTestConfigurationDir().find("visual") != -1:
                command_line.append(' -D "MAKECOMMAND:STRING='+self.GetVisualCommand() + ' '+NameComponent+'.sln /build '+self.GetCmakeBuildType() +' /project ALL_BUILD"')

        command_line.append(' -D "OTB_DATA_ROOT:PATH='+self.GetOtbDataSourceDir()+'" ')
        if self.GetUseOtbDataLargeInput() == False:
                command_line.append(' -D "OTB_DATA_USE_LARGEINPUT:BOOL=OFF" ')
        else:
                command_line.append(' -D "OTB_DATA_USE_LARGEINPUT:BOOL=ON" ')
                command_line.append(' -D "OTB_DATA_LARGEINPUT_ROOT:PATH='+self.GetOtbDataLargeInputSourceDir()+'" ')

        command_line.append(' -D "BUILDNAME:STRING='+build_name+'" ' )

        # Add sources dir
        if BinComponent.find("OTB-Applications") != -1:
                command_line.append(self.GetOtbApplicationsSourceDir())
        else:
                command_line.append(self.GetOtbSourceDir())
        
#        command_line.append(os.path.abspath(self.GetOtbSourceDir()+'/'+SrcComponent))
#        command_line.append("../../../sources/"+self.GetOtbSourceName()+"/"+SrcComponent)
#        command_line.append("..\\..\\..\\sources\\"+self.GetOtbSourceName()+"\\"+SrcComponent)

        cpt = 0
        self.PrintMsg("cmake configuration:")
        while cpt < len(command_line):
                self.PrintMsg(command_line[cpt])
                cpt = cpt + 1
        cmake_command_line=""
        cpt = 0
        while cpt < len(command_line):
                cmake_command_line = cmake_command_line + " " + command_line[cpt]
                cpt = cpt + 1
#        self.CallCommand(cpt,nb_commands,"Makefiles generation... (cmake)",cmake_command_line)
        self.CallChangeDirectory(BinComponent,HomeDir+'/'+self.GetTestConfigurationDir()+"/binaries/"+BinComponent)
        self.CallCommand(BinComponent +" generation",cmake_command_line)


    # =====================================================================================================================================
    # ===  Get mode (use for find and configure tools libraries): visual7, .., macosx, unix, linux or "empty"
    # =====================================================================================================================================
    def GetMode(self):
        mode = ""
        if self.GetTestConfigurationDir().find("visual7") != -1:
                mode = "visual7"
        elif self.GetTestConfigurationDir().find("visual8") != -1:
                mode = "visual8"
        elif self.GetTestConfigurationDir().find("visual9") != -1:
                mode = "visual9"
        elif self.GetTestConfigurationDir().find("visualExpress2008") != -1:
                mode = "visualExpress2008"		
        elif self.GetTestConfigurationDir().find("visualExpress2005") != -1:
                mode = "visualExpress2005"		
        elif self.GetTestConfigurationDir().find("visual") != -1:
                mode = "visual"
        elif self.GetTestConfigurationDir().find("mingw") != -1:
                mode = "mingw"
        elif self.GetTestConfigurationDir().find("cygwin") != -1:
                mode = "cygwin"
        elif self.GetTestConfigurationDir().find("macosx") != -1:
                mode = "macosx"
        elif self.GetTestConfigurationDir().find("linux") != -1:
                mode = "linux"
        elif self.GetTestConfigurationDir().find("unix") != -1:
                mode = "unix"
        return mode

    # =====================================================================================================================================
    # ===  Get Cmake build type: Release, DebugWall, RelWithDebInfo or MinSizeRel 
    # =====================================================================================================================================
    # Use for Build name
    def GetCmakeBuildType2(self):
        cmake_build_type=''
        if self.GetTestConfigurationDir().find("release") != -1:
                cmake_build_type='Release'
        elif self.GetTestConfigurationDir().find("debug") != -1:
                cmake_build_type='DebugWall'
        elif self.GetTestConfigurationDir().find("relwithdebinfo") != -1:
                cmake_build_type='RelWithDebInfo'
        elif self.GetTestConfigurationDir().find("minsizerel") != -1:
                cmake_build_type='MinSizeRel'
        return cmake_build_type

    # =====================================================================================================================================
    # ===  Get Cmake build type: Release, DebugWall, RelWithDebInfo or MinSizeRel 
    # =====================================================================================================================================
    def GetCmakeBuildType(self):
        cmake_build_type=''
        if self.GetTestConfigurationDir().find("release") != -1:
                cmake_build_type='Release'
        elif self.GetTestConfigurationDir().find("debug") != -1:
                cmake_build_type='Debug'
        elif self.GetTestConfigurationDir().find("relwithdebinfo") != -1:
                cmake_build_type='RelWithDebInfo'
        elif self.GetTestConfigurationDir().find("minsizerel") != -1:
                cmake_build_type='MinSizeRel'
        return cmake_build_type

    # =====================================================================================================================================
    # ===  Get Cmake build type: release, debug, relwithdebinfo or minsizerel 
    # =====================================================================================================================================
    def GetBuildType(self):
        build_type = ""
        if self.GetTestConfigurationDir().find("release") != -1:
                build_type="release"
        elif self.GetTestConfigurationDir().find("debug") != -1:
                build_type="debug"
        elif self.GetTestConfigurationDir().find("relwithdebinfo") != -1:
                build_type="relwithdebinfo"
        elif self.GetTestConfigurationDir().find("minsizerel") != -1:
                build_type="minsizerel"
        return build_type


    # =====================================================================================================================================
    # ===  Get Cmake platform compiler (only for WIN32): -G "Visual Studio 7 .NET 2003", etc... 
    # =====================================================================================================================================
    def GetCmakePlatform(self):
        cmake_command_line=''
        if self.GetTestConfigurationDir().find("visual7") != -1:
                cmake_command_line='-G "Visual Studio 7 .NET 2003" '
        elif self.GetTestConfigurationDir().find("visual8") != -1:
                cmake_command_line=' -G "Visual Studio 8 2005" '
        elif self.GetTestConfigurationDir().find("visualExpress2005") != -1:
                cmake_command_line=' -G "Visual Studio 8 2005" '
        elif self.GetTestConfigurationDir().find("visual9") != -1:
                cmake_command_line=' -G "Visual Studio 9 2008" '
        elif self.GetTestConfigurationDir().find("visualExpress2008") != -1:
                cmake_command_line=' -G "Visual Studio 9 2008" '
        elif self.GetTestConfigurationDir().find("mingw") != -1:
                cmake_command_line=' -G "MSYS Makefiles" '
#        if self.GetTestConfigurationDir().find("cygwin") != -1:
#        if self.GetTestConfigurationDir().find("macosx") != -1:
#        if self.GetTestConfigurationDir().find("linux") != -1:
#        if self.GetTestConfigurationDir().find("unix") != -1:
        return cmake_command_line
    
    # =====================================================================================================================================
    # ===  Get OTB build name for cmake genration
    # =====================================================================================================================================
    def GetBuildName(self):
        build_name=""
        # Prefix Buildname
        if self.GetPrefixBuildName() != "":
                build_name=self.GetPrefixBuildName()+'-'

	# Ditrib (ex: CentOS, RedHat, Ubuntu, XP, Vista, ...)
        if self.GetDistribName() != "":
                build_name=build_name+self.GetDistribName()+'-'
        else:
                if self.GetTestConfigurationDir().find("mingw") != -1:
                        build_name=build_name+'MinGW-Win32-'
                elif self.GetTestConfigurationDir().find("cygwin") != -1:
                        build_name=build_name+'Cygwin-Win32-'
                elif self.GetTestConfigurationDir().find("macosx") != -1:
                        build_name=build_name+'Darwin-OSX-'
                elif self.GetTestConfigurationDir().find("sun") != -1:
                        build_name=build_name+'Sun-'
                elif self.GetTestConfigurationDir().find("linux") != -1:
                        build_name=build_name+'Linux-'
                elif self.GetTestConfigurationDir().find("visual7") != -1:
                        build_name=build_name+'Visual7.1-Win32-'
                elif self.GetTestConfigurationDir().find("visual8") != -1:
                        build_name=build_name+'Visual8.0-Win32-'
                elif self.GetTestConfigurationDir().find("visual9") != -1:
                        build_name=build_name+'Visual9.0-Win32-'
                elif self.GetTestConfigurationDir().find("visualExpress2005") != -1:
                        build_name=build_name+'VisualExpress2005-Win32-'
                elif self.GetTestConfigurationDir().find("visualExpress2008") != -1:
                        build_name=build_name+'VisualExpress2008-Win32-'
                else:
                        #Sinon essaie de trouver la plaforme Hote
                        build_name=build_name+'Local-'
	
        # GCC Info
        if self.GetTestConfigurationDir().find("mingw") != -1:
                build_name=build_name+'GCC'+self.GetGCCVersion()+'-'
        elif self.GetTestConfigurationDir().find("cygwin") != -1:
                build_name=build_name+'GCC'+self.GetGCCVersion()+'-'
        elif self.GetTestConfigurationDir().find("macosx") != -1:
                build_name=build_name+'GCC'+self.GetGCCVersion()+'-'
        elif self.GetTestConfigurationDir().find("sun") != -1:
                build_name=build_name+'GCC'+self.GetGCCVersion()+'-'
        elif self.GetTestConfigurationDir().find("linux") != -1:
                build_name=build_name+'GCC'+self.GetGCCVersion()+'-'

	# 32/64bits info	
        if self.GetTestConfigurationDir().find("32bit") != -1:
               build_name=build_name+'32Bits-'
        elif self.GetTestConfigurationDir().find("64bit") != -1:
                build_name=build_name+'64Bits-'
	
        # CMake build info
        build_name=build_name+self.GetCmakeBuildType2()+'-'
        if self.GetTestConfigurationDir().find("shared") != -1:
                build_name=build_name+'Shared-'
        else:
                build_name=build_name+'Static-'
        # ITK Info
        if self.GetTestConfigurationDir().find("itk-ext") != -1:
                build_name=build_name+'ITK'+self.GetItkVersion()+'-External-'
        else:
                build_name=build_name+'ITK-Internal-'
        # FLTK Info
        if self.GetTestConfigurationDir().find("fltk-ext") != -1:
                build_name=build_name+'FLTK'+self.GetFltkVersion()+'-External'
        else:
                build_name=build_name+'FLTK-Internal'

        # DisableExamples
        if self.__disableBuildExamples__ == True:
                build_name=build_name+'-DisableExamples'
        else:
                build_name=build_name+'-EnableExamples'

        # Disable VTK
        if self.__disableUseVtk__ == True:
                build_name=build_name+'-DisableUseVtk'
        else:
                build_name=build_name+'-EnableUseVtk'

#        if len(build_name) > 64:
#                build_name=build_name[0:64]
#                self.PrintMsg("BuildName troncated 64 char :"+build_name)
        return build_name
        
    def GetGCCVersion(self):
        filename = self.GetHomeDir()+"/gcc-version.tmp"
        crtfile = open(filename,"w")
        retcode = subprocess.call("gcc --version", stdout=crtfile, shell=True)
        crtfile.close()
        crtfile = open(filename,"r")
        tab = crtfile.read()
        tab2 = tab.split(" ")
        crtfile.close()
        result = ""
        result = tab2[2]
        return result

    # =====================================================================================================================================
    # ===  Check (and install) FLTK library : generation of command line argument for cmake generation   ==================================
    # =====================================================================================================================================
    def CheckFltkInstallation(self):

        mode = self.GetMode()
        build_type=self.GetBuildType()

        command_line = []
        command_line.append('cmake ')

        command_line.append( self.GetCmakePlatform())
        
        if self.GetTestConfigurationDir().find("shared") != -1:
                build_mode="shared"
        else:
                build_mode="static"
                
        #Sous Linux ou Unix, pas d'ambiguite platform : donc pas forcement linux dans le nom du repetoire  
        # A FAIRE
        HomeDirOutils = self.GetHomeDirOutils()
        
        if mode == "":
                fltk_binary_dir=HomeDirOutils + "/fltk/binaries-" + build_mode +"-"+ build_type +"-fltk-"+ self.GetFltkVersion()
        else:
                fltk_binary_dir=HomeDirOutils + "/fltk/binaries-" + mode + "-" + build_mode +"-"+ build_type +"-fltk-"+ self.GetFltkVersion()
        
        # Check FLTK
        # ---------------------------
        if ( self.GetTestConfigurationDir().find("fltk-exter") != -1 ) and (self.CallCheckDirectory("FLTK Binary",fltk_binary_dir) == 0):
                self.PrintMsg(" => FLTK generation ...")
                fltk_source_dir=HomeDirOutils + "/fltk/sources/fltk-"+self.GetFltkVersion()
                self.CallCheckDirectoryExit("FLTK source dir",fltk_source_dir)
                # Clean directories
                self.CallRemoveDirectory("FLTK binaries",fltk_binary_dir)
                command_line = command_line
        
                # For Visual, set CMAKE_CONFIGURATION_TYPES parameter        
                if self.GetTestConfigurationDir().find("visual") != -1:
                        command_line.append(' -D "CMAKE_CONFIGURATION_TYPES:STRING='+self.GetCmakeBuildType()+'"  ')
                else:
                        command_line.append(' -D "CMAKE_BUILD_TYPE:STRING='+self.GetCmakeBuildType()+'"  ')
                        command_line.append(' -D "CMAKE_C_FLAGS_DEBUG:STRING=-g -Wall" ')
                        command_line.append(' -D "CMAKE_CXX_FLAGS_DEBUG:STRING=-g -Wall" ')

                command_line.append(' -D "BUILD_EXAMPLES:BOOL=OFF" ')
                command_line.append(' -D "BUILD_TESTING:BOOL=OFF" ')
        
                if self.GetTestConfigurationDir().find("shared") != -1:
                        command_line.append(' -D "BUILD_SHARED_LIBS:BOOL=ON" ')
                else:
                        command_line.append(' -D "BUILD_SHARED_LIBS:BOOL=OFF" ')

                if self.GetTestConfigurationDir().find("visual") != -1:
                        command_line.append(' -D "MAKECOMMAND:STRING='+self.GetVisualCommand() + ' FLTK.sln /build '+self.GetCmakeBuildType() +' /project ALL_BUILD"')
                command_line.append("../sources/fltk-"+self.GetFltkVersion())

                cpt = 0
                self.PrintMsg("FLTK cmake configuration:")
                while cpt < len(command_line):
                        self.PrintMsg(command_line[cpt])
                        cpt = cpt + 1
                cmake_command_line=""
                cpt = 0
                while cpt < len(command_line):
                        cmake_command_line = cmake_command_line + " " + command_line[cpt]
                        cpt = cpt + 1
                
                self.CallCreateDirectory("FLTK binaries",fltk_binary_dir)
                self.CallChangeDirectory("FLTK binaries",fltk_binary_dir)
                self.CallCommand("FLTK generation",cmake_command_line)
                if self.GetTestConfigurationDir().find("visual") != -1:
                        self.CallCommand("FLTK make", self.GetVisualCommand() + " FLTK.sln /build "+self.GetCmakeBuildType() +" /project ALL_BUILD")
                else:
                        self.CallCommand("FLTK make", "make")

                self.PrintMsg("FLTK library installed with success (on directory <"+fltk_binary_dir+">) !")


    # =====================================================================================================================================
    # ===  Check (and install) ITK library : generation of command line argument for cmake generation   ==================================
    # =====================================================================================================================================
    def CheckItkInstallation(self):

        mode = self.GetMode()
        build_type=self.GetBuildType()

        command_line = []
        command_line.append('cmake ')

        command_line.append( self.GetCmakePlatform())
        
        if self.GetTestConfigurationDir().find("shared") != -1:
                build_mode="shared"
        else:
                build_mode="static"
                
        #Sous Linux ou Unix, pas d'ambiguite platform : donc pas forcement linux dans le nom du repetoire  
        # A FAIRE
        HomeDirOutils = self.GetHomeDirOutils()
        
        if mode == "":
                itk_install_dir=HomeDirOutils + "/itk/install-" + build_mode +"-"+ build_type +"-itk-"+ self.GetItkVersion()
                itk_binary_dir=HomeDirOutils + "/itk/binaries-" + build_mode +"-"+ build_type +"-itk-"+ self.GetItkVersion()
        else:
                itk_install_dir=HomeDirOutils + "/itk/install-" + mode + "-" + build_mode +"-"+ build_type +"-itk-"+ self.GetItkVersion()
                itk_binary_dir=HomeDirOutils + "/itk/binaries-" + mode + "-" + build_mode +"-"+ build_type +"-itk-"+ self.GetItkVersion()
        
        if ( self.CallCheckDirectory("ITK install",itk_install_dir) == 0 ):
                self.PrintMsg("ITK generation ........")
                #Init paths for externals lib
                itk_source_dir=HomeDirOutils + "/itk/sources/InsightToolkit-"+self.GetItkVersion()
                self.CallCheckDirectoryExit("ITK source dir",itk_source_dir)
                # Clean directories
                self.CallRemoveDirectory("ITK binaries",itk_binary_dir)
                self.CallRemoveDirectory("ITK install",itk_install_dir)
                command_line = command_line
        
                # For Visual, set CMAKE_CONFIGURATION_TYPES parameter        
                if self.GetTestConfigurationDir().find("visual") != -1:
                        command_line.append(' -D "CMAKE_CONFIGURATION_TYPES:STRING='+self.GetCmakeBuildType()+'"  ')
                else:
                        command_line.append(' -D "CMAKE_BUILD_TYPE:STRING='+self.GetCmakeBuildType()+'"  ')
                        command_line.append(' -D "CMAKE_C_FLAGS_DEBUG:STRING=-g -Wall" ')
                        command_line.append(' -D "CMAKE_CXX_FLAGS_DEBUG:STRING=-g -Wall" ')
       
#                command_line.append(' -D "BUILD_DOXYGEN:BOOL=OFF" ')
                command_line.append(' -D "BUILD_EXAMPLES:BOOL=OFF" ')
                command_line.append(' -D "BUILD_TESTING:BOOL=OFF" ')
        
                if self.GetTestConfigurationDir().find("shared") != -1:
                        command_line.append(' -D "BUILD_SHARED_LIBS:BOOL=ON" ')
                else:
                        command_line.append(' -D "BUILD_SHARED_LIBS:BOOL=OFF" ')


                command_line.append(' -D "CMAKE_INSTALL_PREFIX:PATH='+itk_install_dir+'"  ')

                if self.GetTestConfigurationDir().find("cygwin") != -1:
                        self.PrintWarning("For Cygwin, disable UUID cmake parameters in ITK generation makefiles process !!! UUID_INCLUDE_DIR and UUID_LIBRARY cmake variables are set to empty.")
                        command_line.append(' -D "UUID_INCLUDE_DIR:PATH=" ')
                        command_line.append(' -D "UUID_LIBRARY:FILEPATH=" ')

                if self.GetTestConfigurationDir().find("visual") != -1:
                        command_line.append(' -D "MAKECOMMAND:STRING='+self.GetVisualCommand() + ' ITK.sln /build '+self.GetCmakeBuildType() +' /project ALL_BUILD"')

#                command_line.append(itk_source_dir)
                command_line.append("../sources/InsightToolkit-"+self.GetItkVersion())

                cpt = 0
                self.PrintMsg("ITK cmake configuration:")
                while cpt < len(command_line):
                        self.PrintMsg(command_line[cpt])
                        cpt = cpt + 1
                cmake_command_line=""
                cpt = 0
                while cpt < len(command_line):
                        cmake_command_line = cmake_command_line + " " + command_line[cpt]
                        cpt = cpt + 1
                
                self.CallCreateDirectory("ITK binaries",itk_binary_dir)
                self.CallChangeDirectory("ITK binaries",itk_binary_dir)
                self.CallCommand("ITK generation",cmake_command_line)
                
                if self.GetTestConfigurationDir().find("visual") != -1:
                        self.CallCommand("ITK make", self.GetVisualCommand() + " ITK.sln /build "+self.GetCmakeBuildType() +" /project ALL_BUILD")
                        self.CallCommand("ITK make intall", self.GetVisualCommand() + " ITK.sln /build "+self.GetCmakeBuildType() +" /project INSTALL")
                else:
                        self.CallCommand("ITK make", "make")
                        self.CallCommand("ITK make intall", "make install")
#                self.CallRemoveDirectory("ITK binaries",itk_binary_dir)
                self.PrintMsg("ITK library installed with success (on directory <"+itk_install_dir+">) !")

    # =====================================================================================================================================
    # ===  Check (and install) VTK library : generation of command line argument for cmake generation   ==================================
    # =====================================================================================================================================
    def CheckVtkInstallation(self):

        mode = self.GetMode()
        build_type=self.GetBuildType()

        command_line = []
        command_line.append('cmake ')

        command_line.append( self.GetCmakePlatform())
        
        if self.GetTestConfigurationDir().find("shared") != -1:
                build_mode="shared"
        else:
                build_mode="static"
                
        #Sous Linux ou Unix, pas d'ambiguite platform : donc pas forcement linux dans le nom du repetoire  
        # A FAIRE
        HomeDirOutils = self.GetHomeDirOutils()
        
        if mode == "":
                vtk_install_dir=HomeDirOutils + "/vtk/install-" + build_mode +"-"+ build_type +"-vtk-"+ self.GetVtkVersion()
                vtk_binary_dir=HomeDirOutils + "/vtk/binaries-" + build_mode +"-"+ build_type +"-vtk-"+ self.GetVtkVersion()
        else:
                vtk_install_dir=HomeDirOutils + "/vtk/install-" + mode + "-" + build_mode +"-"+ build_type +"-vtk-"+ self.GetVtkVersion()
                vtk_binary_dir=HomeDirOutils + "/vtk/binaries-" + mode + "-" + build_mode +"-"+ build_type +"-vtk-"+ self.GetVtkVersion()
        
        if ( self.CallCheckDirectory("VTK install",vtk_install_dir) == 0 ):
                self.PrintMsg("VTK generation ........")
                #Init paths for externals lib
                vtk_source_dir=HomeDirOutils + "/vtk/sources/VTK"     #-"+self.GetVtkVersion()
                self.CallCheckDirectoryExit("VTK source dir",vtk_source_dir)
                # Clean directories
                self.CallRemoveDirectory("VTK binaries",vtk_binary_dir)
                self.CallRemoveDirectory("VTK install",vtk_install_dir)
                command_line = command_line
        
                # For Visual, set CMAKE_CONFIGURATION_TYPES parameter        
                if self.GetTestConfigurationDir().find("visual") != -1:
                        command_line.append(' -D "CMAKE_CONFIGURATION_TYPES:STRING='+self.GetCmakeBuildType()+'"  ')
                else:
                        command_line.append(' -D "CMAKE_BUILD_TYPE:STRING='+self.GetCmakeBuildType()+'"  ')
                        command_line.append(' -D "CMAKE_C_FLAGS_DEBUG:STRING=-g -Wall" ')
                        command_line.append(' -D "CMAKE_CXX_FLAGS_DEBUG:STRING=-g -Wall" ')
       
#                command_line.append(' -D "BUILD_DOXYGEN:BOOL=OFF" ')
                command_line.append(' -D "BUILD_EXAMPLES:BOOL=OFF" ')
                command_line.append(' -D "VTK_WRAP_JAVA:BOOL=OFF" ')
                command_line.append(' -D "VTK_WRAP_PYTHON:BOOL=OFF" ')
                command_line.append(' -D "VTK_WRAP_TCL:BOOL=OFF" ')
        
                if self.GetTestConfigurationDir().find("shared") != -1:
                        command_line.append(' -D "BUILD_SHARED_LIBS:BOOL=ON" ')
                else:
                        command_line.append(' -D "BUILD_SHARED_LIBS:BOOL=OFF" ')


                command_line.append(' -D "CMAKE_INSTALL_PREFIX:PATH='+vtk_install_dir+'"  ')

                if self.GetTestConfigurationDir().find("visual") != -1:
                        command_line.append(' -D "MAKECOMMAND:STRING='+self.GetVisualCommand() + ' VTK.sln /build '+self.GetCmakeBuildType() +' /project ALL_BUILD"')
#                command_line.append(vtk_source_dir)
                command_line.append("../sources/VTK")

                cpt = 0
                self.PrintMsg("VTK cmake configuration:")
                while cpt < len(command_line):
                        self.PrintMsg(command_line[cpt])
                        cpt = cpt + 1
                cmake_command_line=""
                cpt = 0
                while cpt < len(command_line):
                        cmake_command_line = cmake_command_line + " " + command_line[cpt]
                        cpt = cpt + 1
                
                self.CallCreateDirectory("VTK binaries",vtk_binary_dir)
                self.CallChangeDirectory("VTK binaries",vtk_binary_dir)
                self.CallCommand("VTK generation",cmake_command_line)
                
                if self.GetTestConfigurationDir().find("visual") != -1:
                        self.CallCommand("VTK make", self.GetVisualCommand() + " VTK.sln /build "+self.GetCmakeBuildType() +" /project ALL_BUILD")
                        self.CallCommand("VTK make intall", self.GetVisualCommand() + " VTK.sln /build "+self.GetCmakeBuildType() +" /project INSTALL")
                else:
                        self.CallCommand("VTK make", "make")
                        self.CallCommand("VTK make intall", "make install")
#                self.CallRemoveDirectory("VTK binaries",vtk_binary_dir)
                self.PrintMsg("VTK library installed with success (on directory <"+vtk_install_dir+">) !")



    def FindTemporayFileName(self):
#        filename=os.tmpfile
#        filename = os.getcwd() + "/otb-internal-otb-auto.sh"
        filename = "otb-internal-otb-auto.sh"
        return filename

    def FindCrtFileName(self,TestConfigurationDir):
        home_dir = os.getcwd()
        thedate = date.today().isoformat()
        
        if os.path.exists(home_dir+"/crt") == 0:
                os.mkdir(home_dir+"/crt")
        crt_file = home_dir + "/crt/"+TestConfigurationDir+"-"+thedate+".log"
        return  crt_file       
    
    def PrintWarning(self,msg):
        self.PrintMsg("#############   WARNING: "+msg)
    def PrintMsg(self,msg):
        self.AddMsgToCDLAndCrtFile("  "+msg)
    def PrintTitle(self,msg):
        command =       "\n====================================\n"
        command = command+"=====  "+msg+ "\n"
        command = command+"====================================\n"
        self.AddMsgToCDLAndCrtFile(command)

    # ===  Internals methods   ==================================
    def CallGetVersion(self,source_dir):
        filename = "otb.tmp"
        crtfile = open(filename,"w")
        save_rep = os.getcwd() 
        os.chdir(source_dir)
        value = subprocess.call("hg tip", shell=True, stdout=crtfile)
        crtfile.close()
        os.chdir(save_rep)
        crtfile2 = open(filename,"r")
        value2 = crtfile2.readline()
        crtfile2.close()
        value3 = value2.split(" ")
        
        return value3[3][0:16]


    def CallCommand(self,comment,command):
        __command = "  Call "+comment+" -> subprocess.call("+command+", shell=True) ..."
        self.AddMsgToCDLAndCrtFile(__command)
        try:
                #os.execl(commandLineExecuted, self.__commanLineArgument__)
#                os.system(command)
#                p = Popen('"'+command+'"', shell=False)
#                sts = os.waitpid(p.pid, 0)
#                crtfile = open(self.GetCrtFile(),"a")

                retcode = subprocess.call(command, shell=True)
		#, env="http_proxy=http://feuvriert:montdor25-@proxy-HTTP1.cnes.fr:8050")
#                retcode = subprocess.call(command, shell=True, stdout=crtfile, stderr=crtfile)
#                retcode = subprocess.check_call(command, shell=True)
#                crtfile.close()
                if retcode < 0:
                        print >>sys.stderr, "Child was terminated by signal", -retcode
                        self.AddMsgToCDLAndCrtFile( __command+"  KO")
                else:
                        print >>sys.stderr, "Child returned", retcode
                        self.AddMsgToCDLAndCrtFile( __command+"  OK")
        except OSError, e:
                print >>sys.stderr, "Execution failed:", e
#        except:
                self.AddMsgToCDLAndCrtFile("  ERROR: error to execute following process: "+ comment+"  subprocess.call("+command+", shell = True).")

    def CallRemoveDirectory(self,comment,directory):
        directory = os.path.normpath(directory)
        command = "  Remove "+comment+" directory ("+directory+") ..."
        self.AddMsgToCDLAndCrtFile(command)
        try:
                if os.path.exists(directory):
                        self.RemoveDirectories(directory)
                self.AddMsgToCDLAndCrtFile(command+"  OK")
        except:
                self.AddMsgToCDLAndCrtFile("  ERROR: One error to execute following process: RemoveDirectories "+directory)
                
    def RemoveDirectories(self,top):
        for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                        try:
                                os.remove(os.path.join(root,name))
                        except:
                                self.PrintMsg("Error removing file "+name+" in directory "+root)
                for name in dirs:
                        try:
                                os.rmdir(os.path.join(root,name))
                        except:
                                self.PrintMsg("Error removing directory "+name+" in directory "+root)
        if os.path.exists(top):
                os.rmdir(top)
        

#        if self.CallCheckDirectory("OTB-Data-LargeInput dir",value) != 0:
#                self.__homeOtbDataLargeInputSourceDir__ = value
#        else:
#                value = os.path.normpath(rep_base+"/OTB-Data-LargeInput")
#                if self.CallCheckDirectory("OTB-Data-LargeInput dir",value) != 0:
#                        self.__homeOtbDataLargeInputSourceDir__ = value
#                else:
#                        self.__homeOtbDataLargeInputSourceDir__ = "disable"
#                        self.PrintMsg( "-> OTB-Data-LargeInput disable !!")

        self.CallCheckDirectoryExit("OTB-Data-LargeInput dir",self.__homeOtbDataLargeInputSourceDir__)

    def CallCheckFileExit(self,comment,directory):
        if self.CallCheckFile(comment,directory) == 0:
                exit(1)
    def CallCheckFile(self,comment,directory):
        if os.path.exists(directory) == 0:
                self.AddMsgToCDLAndCrtFile("  Check "+comment+" file ("+directory+") ...  KO !")
        else:
                self.AddMsgToCDLAndCrtFile("  Check "+comment+" file ("+directory+") ...  OK")
        return os.path.exists(directory)



    # Exit if don't exist !!
    def CallCheckDirectoryExit(self,comment,directory):
        if self.CallCheckDirectory(comment,directory) == 0:
                exit(1)
    def CallCheckDirectory(self,comment,directory):
        if os.path.exists(directory) == 0:
                self.AddMsgToCDLAndCrtFile("  Check "+comment+" directory ("+directory+") ...  KO !")
        else:
                self.AddMsgToCDLAndCrtFile("  Check "+comment+" directory ("+directory+") ...  OK")
        return os.path.exists(directory)

    def CallCreateDirectory(self,comment,directory):
        self.AddMsgToCDLAndCrtFile("  "+comment+" -> os.makedirs("+directory+")")
        try:
                if os.path.exists(directory) == 0:
                        os.makedirs(directory)
        except:
                self.AddMsgToCDLAndCrtFile("  ERROR: One error to execute following process: os.makedirs("+directory+").")
                exit(1)
    def CallCreateDirectory(self,comment,directory):
        command = "  Create "+comment+" directory -> os.makedirs("+directory+")"
        self.AddMsgToCDLAndCrtFile(command)
        try:
                if os.path.exists(directory) == 0:
                        os.makedirs(directory)
                self.AddMsgToCDLAndCrtFile(command+"  OK")
        except:
                self.AddMsgToCDLAndCrtFile("  ERROR: One error to execute following process: os.makedirs("+directory+").")
                exit(1)

    def CallChangeDirectory(self,comment,directory):
        directory = os.path.normpath(directory)
        self.AddMsgToCDLAndCrtFile("  Change current directory to "+comment+" directory ("+directory+")  ...")
        try:
                os.chdir(directory)
                self.AddMsgToCDLAndCrtFile("  The current directory is <"+os.getcwd()+">")
        except:
                self.AddMsgToCDLAndCrtFile("  ERROR: One error to execute following process: os.chdir("+directory+").")
                exit(1)

    def AddMsgToCDLAndCrtFile(self,line):
        date = datetime.now().isoformat(' ')
        print date+' '+line
        sys.stdout.flush()
        crtfile = open(self.GetCrtFile(),"a")
        crtfile.write(date+' '+line + '\n')
        crtfile.close()
        

###################################################################################################################""

# 1. Parameters for HOST PLATFORM:             otb.py "visual-static-release-itk-internal_fltk-internal" (len(sys.argv) = 2)
# 2. Parameters for SYSTEM PLATFORM TESTED:    otb.py "visual-static-release-itk-internal_fltk-internal" "Experimental" "True/False (MakeClean)" "True/False (GenerateMakefiles)" "True/False (DisableCTest)" "True/False (UpdateSources)" (len(sys.argv) = 7)

#### 2. Parameters for SYSTEM PLATFORM TESTED:    otb.py "visual-static-release-itk-internal_fltk-internal" "local_system" (len(sys.argv) = 3)
if __name__ == "__main__":

        print "otbhg.py Main function called ..."

        #=============================================================================================
        # Processing configuration level 2.
        if len(sys.argv) == 7:
                print "Run for ", sys.argv[1]
                x=TestProcessing()
                testConfigurationDir = sys.argv[1]
                
#                if sys.argv[2] == "Experimental":
#                        x.SetExperimental()
#                if sys.argv[2] == "Nightly":
#                        x.SetNightly()
#                if sys.argv[2] == "Continuous":
#                        x.SetContinuous()

                if sys.argv[3] == "True":
                        x.EnableMakeClean()
                else:
                        x.DisableMakeClean()
                if sys.argv[4] == "True":
                        x.EnableGenerateMakefiles()
                else:
                        x.DisableGenerateMakefiles()
                if sys.argv[5] == "True":
                        x.DisableCTest()
                else:
                        x.EnableCTest()
                if sys.argv[6] == "True":
                        x.EnableUpdateSources()
                else:
                        x.DisableUpdateSources()

                x.Run(testConfigurationDir)


