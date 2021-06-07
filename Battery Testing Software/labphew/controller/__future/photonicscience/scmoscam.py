# -*- coding: utf-8 -*-
"""
    UUTrack.Controller.devices.PhotonicScience.scmoscam.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    A wrapper class originally written by Perceval Guillou,
    perceval@photonic-science.com in Py2 and has been tested successfully with
    scmoscontrol.dll SCMOS Pleora (GEV) control dll (x86 )v5.6.0.0 (date modified 10/2/2013)
    
    SaFa @nanoLINX has adapted the wrapper class for a camera control program.
    
    v1.0, 24 feb. 2015

    .. sectionauthor:: SaFa <S.Faez@uu.nl>

"""

import ctypes as C
import os
import sys
from sys import platform
if platform == "linux" or platform == "linux2":
    pass
elif platform == "darwin":
    pass
elif platform == "win32":
    from _ctypes import LoadLibrary, FreeLibrary

import numpy

NUMPY_MODES = {"L":numpy.uint8, "I;16":numpy.uint16}
class GEVSCMOS:
    def __init__(self, cwd_path, name):
        self.cwd_path = cwd_path #working directory
        self.name = name #Camera name = folder where DLL and settings are stored
        self.setup_file = "%s\\%s\\PSL_camera_files\\ps_setup.dat"%(cwd_path,name)
        self.dll_name = self.GetDLL()
        self.dll = None
        self.LoadCamDLL()
        self.ResetOptions()

    def __str__(self):
        msg = "Camera setting located in %s"%(self.setup_file)
        return msg

    def GetDLL(self):
        FileList = os.listdir('%s\\%s'%(self.cwd_path,self.name))
        count = 0
        for file in FileList:
            if file[-4:] == ".dll":
                dll_name = file
                count+=1

        if count == 0:
            msg = "Check in '%s'\n!!!CAMERA CONTROL DLL NOT FOUND!!!"%self.cwd_path
            print (msg)
            return ""

        elif count > 1:
            msg = "Check in '%s'\n!!!ONLY ONE DLL FILE MUST EXIST IN THE CAMERA FOLDER!!!"%self.cwd_path
            print (msg)
            return ""
        else:
            return dll_name

    def LoadCamDLL(self):
        self.libHandle = LoadLibrary('%s\\%s\\%s'%(self.cwd_path,self.name,self.dll_name))
        #self.libHandle = C.windll.kernel32.LoadLibraryA('%s\\%s\\%s'%(self.cwd_path,self.name,self.dll_name))
        self.dll = C.CDLL(None, handle=self.libHandle)  #cdecl
        #self.dll = C.WinDLL(None, handle=self.libHandle)  #stdcall
        #self.dll = C.CDLL('%s\\%s\\%s'%(self.cwd_path,self.name,self.dll_name))
        self.InitFunctions()

    def UnloadCamDLL(self):
        del self.dll
        self.dll = None
        FreeLibrary(self.libHandle)
        #C.windll.kernel32.FreeLibrary(self.libHandle)

    def ResetOptions(self):
        self.mode = "I;16"
        self.size = (0,0)
        self.sizemax = (1919,1079)
        self.state = 0
        self.abort_flag = False
        self.remapping = False
        self.smooth = False
        self.clip = True
        self.SubArea = (0,0,0,0)
        self.SoftBin = (1,1)
        self.gainmode = 0
        self.expous = 100000
        self.FlatAverage = 10
        self.GlobalRemap = False
        self.tempread = True

        #self.is2tap = False

        # 0 = gain mode 1 - 16 bit
        # 1 = gain mode 2 - 16 bit
        # 2 = gain mode 10 - 16 bit
        # 3 = gain mode 30 - 16 bit
        # 4 = combined (1 and 30) in software - 24 => Demangle => 16 bit
        # 5 = combined in hardware - 16 bit
        # 6 = gain mode 1 - 8 bit
        # 7 = gain mode 2 - 8 bit
        # 8 = gain mode 10 - 8 bit
        # 9 = gain mode 30 - 8 bit
        # 10= combined in hardware - 8bit

        if self.IsInCamCor():
            if self.Has8bitGainModes():
                gainmodes = ['gain1','gain2','gain10','gain30','gain1+30_Hardware','gain1_8b','gain2_8b','gain10_8b','gain30_8b','gain1+30_8b']
            else:
                gainmodes = ['gain1','gain2','gain10','gain30','gain1+30_Hardware']
        else:
            if self.Has8bitGainModes():
                gainmodes = ['gain1','gain2','gain10','gain30','gain1+30','gain1_8b','gain2_8b','gain10_8b','gain30_8b']
            else:
                gainmodes = ['gain1','gain2','gain10','gain30','gain1+30']

        if self.HasClockSpeedLimit():
            clockspeedmodes = ['50MHz']
        else:
            clockspeedmodes = ['50MHz','100MHz'] #,'200MHz'

        #self.flipdata = self.IsFlipped()

        self.Options = {
        'TriggerMode'       :['FreeRunning','Software',
                              'Hardware_Falling','Hardware_Rising'],
        'ClockSpeedMode'     :clockspeedmodes,
        'GainMode'           :gainmodes,
        'PowerSavingMode'    :['PowerOn','PowerOff','CoolingOff'],
        #'VideoGain'          :[0,100],
        'IntensifierGain'    :[1,100],
        #'ChipGain'           :[1,100],
        'SoftBin'            :[(1,1),(1040,1040)],
        'SubArea'            :[(0,0,0,0)],
        'Exposure'           :[(100,'Millisec'),(4294967,['Microsec','Millisec','Second'])],
        'Temperature'        :[0,0],
        'Offset'             :[1],
        'BrightPixel'        :[1],
        'FlatField'          :[0],
        'MakeFlat'           :[None],
        'FlatAverage'        :[10,1000],
        'Remapping'          :[0],
        'Smooth'             :[0],
        'Clip'               :[0],
        'Sharpening'         :[0],
        'AutoLevel'          :[0],
        'ALC_maxexp'         :[1000,65535],
        'ALC_win'            :[(0,0,1919,1079)],
        'BestFit'            :[0],
        'BF_Peek'            :[1000,65535],
        'IF_delay'           :[0,65535],
        'BinningFilter'      :[0],
        'AutoBinning'        :[0],
        'Gamma'              :[0],
        'GammaPeak'          :[0,100],
        'GammaBright'        :[0,100],
        #'FlickerMode'        :['Off','50MHz','60MHz'],
        }

    def InitFunctions(self):
        #Buffer
        self.dll.PSL_VHR_get_image_pointer.restype = C.POINTER(C.c_char) #ushort
        self.dll.PSL_VHR_demangle_rgb24_into_16bit_image.restype = C.POINTER(C.c_char) #ushort
        self.dll.PSL_VHR_remap_image.restype = C.POINTER(C.c_char) #ushort
        self.dll.PSL_VHR_get_pointer_to_safebufferA.restype = C.POINTER(C.c_char) #ushort
        self.dll.PSL_VHR_get_pointer_to_safebufferB.restype = C.POINTER(C.c_char) #ushort
        self.dll.PSL_VHR_get_pointer_to_safebufferC.restype = C.POINTER(C.c_char) #ushort
        #Bool
        self.dll.PSL_VHR_Open.restype = C.c_bool
        self.dll.PSL_VHR_open_map.restype = C.c_bool
        self.dll.PSL_VHR_Close.restype = C.c_bool
        self.dll.PSL_VHR_set_gain_mode.restype = C.c_bool
        self.dll.PSL_VHR_set_speed.restype = C.c_bool
        self.dll.PSL_VHR_set_video_gain.restype = C.c_bool
        self.dll.PSL_VHR_set_chip_gain.restype = C.c_bool
        self.dll.PSL_VHR_set_exposure.restype = C.c_bool
        self.dll.PSL_VHR_set_trigger_mode.restype = C.c_bool
        self.dll.PSL_VHR_set_sub_area_coordinates.restype = C.c_bool
        self.dll.PSL_VHR_enable_offset_subtraction.restype = C.c_bool
        self.dll.PSL_VHR_enable_bright_pixel_correction.restype = C.c_bool
        self.dll.PSL_VHR_enable_flat_field_correction.restype = C.c_bool
        self.dll.PSL_VHR_Snap_and_return.restype = C.c_bool
        self.dll.PSL_VHR_Get_snap_status.restype = C.c_bool
        self.dll.PSL_VHR_abort_snap.restype = C.c_bool
        self.dll.PSL_VHR_apply_post_snap_processing.restype = C.c_bool
        self.dll.PSL_VHR_enable_gamma.restype = C.c_bool
        self.dll.PSL_VHR_set_gamma_gain_bright.restype = C.c_bool
        self.dll.PSL_VHR_set_gamma_gain_brightness.restype = C.c_bool
        #self.dll.PSL_VHR_set_flicker_mode.restype = C.c_bool

    def IsInCamCor(self):
        isincamcor = 0
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option.lower() in ["onboardcorrectionssupported","incameracorrections"]:
                    isincamcor = int(value)
                    break

        except:
            pass

        return bool(isincamcor)

    def IsFlipped(self):
        isflip = 0
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option.lower() in ["swflipimage"]:
                    isflip = int(value)
                    break

        except:
            pass

        return bool(isflip)

    def GetRemapSize(self):
        remapsize = None
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            Nx,Ny = (0,0)
            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option in ["Submapwidth","submapwidth"]:
                    Nx = int(value)
                if option in ["Submapheight","submapheight"]:
                    Ny = int(value)
                    break

            remapsize = Nx,Ny

        except:
            pass

        #print "remap size is (%s,%s)"%remapsize

        return remapsize

    def HasIntensifier(self):
        intensifier_value = 1
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option in ["intensifiergaincanbeset","IntensifierGainCanBeSet","HasIntensifier","hasintensifier"]:
                    intensifier_value = int(value)
                    break

        except:
            pass

        return bool(intensifier_value)

    def HasTemperature(self):
        tempset = None
        tempread = None
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option in ["TemperatureCanBeSet","temperaturecanbeset"]:
                    tempset = int(value)
                if option in ["TemperatureCanBeRead","temperaturecanberead"]:
                    tempread = int(value)

            if tempset==1:
                return [-30,50]
            elif tempset==0:
                return [0,0]
            elif tempread==1:
                return [0,0]
            elif tempread==0:
                return None
            else:
                return [-30,50]

        except:
            return [-30,50]

    def HasHPMapping(self):
        use_hpm_remap = 0
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option in ["viewer_use_hp_mapping"]:
                    use_hpm_remap = int(value)
                    break

        except:
            print ("HasHPMapping: %s: %s"%(sys.exc_info()[0],sys.exc_info()[1]))

        return bool(use_hpm_remap)

    def HasBinning(self):
        use_binning = 1
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option in ["binning_supported"]:
                    use_binning = int(value)
                    break

        except:
            print ("HasBinning: %s: %s"%(sys.exc_info()[0],sys.exc_info()[1]))

        return bool(use_binning)

    def HasClockSpeedLimit(self):
        clockspeedlimit = 0
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option.lower() in ["hasclockspeedlimit","clockspeedlimit"]:
                    clockspeedlimit = int(value)
                    break

        except:
            pass

        return bool(clockspeedlimit)

    def Has8bitGainModes(self):
        has8bit = 1
        try:
            fich = open(self.setup_file,'r')
            lines = fich.readlines()
            fich.close()

            for line in lines:
                (option,sep,value) = line.strip().partition('=')
                if option.lower() in ["remove_8bit_gainmodes"]:
                    if int(value)==0:
                        has8bit = 1
                    else:
                        has8bit = 0
                    break

        except:
            pass

        return bool(has8bit)

    #------ CAMERA PROPERTIES ---------------------------------
    def GetName(self):
        return self.name

    def GetDLLName(self):
        return self.dll_name

    def GetMode(self):
        return self.mode

    def GetState(self):
        return self.state

    def GetPedestal(self):
        return self.pedestal

    def GetOptions(self):
        return self.Options.keys()

    def GetSize(self):
        return self.size

    def GetSizeMax(self):
        return self.sizemax

    def UpdateSizeMax(self):
        Nx = self.dll.PSL_VHR_get_maximum_width()
        Ny = self.dll.PSL_VHR_get_maximum_height()
        self.sizemax = (Nx,Ny)
        return self.sizemax

    def UpdateSize(self):
        Nx = self.dll.PSL_VHR_get_width()
        Ny = self.dll.PSL_VHR_get_height()
        self.size = (Nx,Ny)

    #----- Specificities -----------------------------------------------------------------
    def SelectIportDevice(self):
        path = "%s\\%s\\IPconf.dat"%(self.cwd_path,self.name)
        if os.path.exists(path):
            self.IP_add = ""
            self.mac_add = ""
            self.IsIport = True
            fich = open(path,'r')
            lines = fich.readlines()
            fich.close()
            for line in lines:
                (option, sep, value) = line.strip().partition('=')
                if option == "MAC":
                    self.mac_add = value
                elif option == "IP":
                    self.IP_add = value

            if self.mac_add=="" or self.IP_add=="":
                self.dll.PSL_VHR_select_IPORT_device("","")
            else:
                self.dll.PSL_VHR_select_IPORT_device(self.mac_add,"[%s]"%self.IP_add)

            return True
        else:
            self.IsIport = False
            return False

    #-------- CAMERA STANTARD FUNCTIONS ------------------
    def Open(self):
        path = "%s\\%s\\PSL_camera_files"%(self.cwd_path,self.name)
        self.SelectIportDevice()

        if self.dll.PSL_VHR_Open(str(path)) :
            if not self.OpenMap():
                #del self.Options['Remapping']
                pass

            if not self.IsIntensifier():
                del self.Options['IntensifierGain']

            Temp = self.HasTemperature()
            if Temp==None:
                self.tempread = False
            else:
                self.tempread = True

            (Nx,Ny) = self.UpdateSizeMax()
            self.Options["SubArea"][0] = (0,0,Nx-1,Ny-1)
            self.Options["ALC_win"][0] = (0,0,Nx-1,Ny-1)
            self.SetSubArea(0,0,Nx-1,Ny-1)
            self.UpdateSize()
            return 0

        else:
            return 1

    def Close(self):
        self.dll.PSL_VHR_Close()
        self.UnloadCamDLL()

    def SetSubArea(self,left,top,right,bottom):
        self.SubArea = (left,top,right,bottom)
        rep = self.dll.PSL_VHR_set_sub_area_coordinates(left,right,top,bottom)
        self.UpdateSize()
        return rep

    def SetSoftBin(self,Sx,Sy):
        self.SoftBin = (Sx,Sy)

    def SetExposure(self, expo, unit):
        if unit=="Second":
            self.expous = expo*1000000
        elif unit=="Millisec":
            self.expous = expo*1000
        elif unit=="Microsec":
            self.expous = expo

        ans = self.dll.PSL_VHR_set_exposure(self.expous)

        #print "SetExposure ",self.name,expo,unit,self.expous,type(self.expous),ans

        return ans

    def SetTrigger(self,mode):
        if mode == "FreeRunning":
            return self.dll.PSL_VHR_set_trigger_mode(0)
        elif mode == "Software":
            return self.dll.PSL_VHR_set_trigger_mode(1)
        elif mode == "Hardware_Falling":
            return self.dll.PSL_VHR_set_trigger_mode(2)
        elif mode == "Hardware_Rising":
            return self.dll.PSL_VHR_set_trigger_mode(6)
        elif mode == "Pipeline_Master":
            return self.dll.PSL_VHR_set_trigger_mode(16)
        elif mode == "Pipeline_Slave":
            return self.dll.PSL_VHR_set_trigger_mode(18)
        else:
            return "Trigger mode not valid"

    def SetGainMode(self, mode):
        # 0 = gain mode 1 - 16 bit
        # 1 = gain mode 2 - 16 bit
        # 2 = gain mode 10 - 16 bit
        # 3 = gain mode 30 - 16 bit
        # 4 = combined (1 and 30) in software - 24 => Demangle => 16 bit
        # 5 = combined in hardware - 16 bit
        # 6 = gain mode 1 - 8 bit
        # 7 = gain mode 2 - 8 bit
        # 8 = gain mode 10 - 8 bit
        # 9 = gain mode 30 - 8 bit
        # 10= combined in hardware - 8bit

        if mode == 'gain1':
            self.gainmode = 0
            rep  = self.dll.PSL_VHR_set_gain_mode(0)
        elif mode == 'gain2':
            self.gainmode = 1
            rep  = self.dll.PSL_VHR_set_gain_mode(1)
        elif mode == 'gain10':
            self.gainmode = 2
            rep  = self.dll.PSL_VHR_set_gain_mode(2)
        elif mode == 'gain30':
            self.gainmode = 3
            rep  = self.dll.PSL_VHR_set_gain_mode(3)
        elif mode == 'gain1+30':
            self.gainmode = 4
            rep  = self.dll.PSL_VHR_set_gain_mode(4)
        elif mode == 'gain1+30_Hardware':
            self.gainmode = 5
            rep  = self.dll.PSL_VHR_set_gain_mode(5)
        elif mode == 'gain1_8b':
            self.gainmode = 6
            rep  = self.dll.PSL_VHR_set_gain_mode(6)
        elif mode == 'gain2_8b':
            self.gainmode = 7
            rep  = self.dll.PSL_VHR_set_gain_mode(7)
        elif mode == 'gain10_8b':
            self.gainmode = 8
            rep  = self.dll.PSL_VHR_set_gain_mode(8)
        elif mode == 'gain30_8b':
            self.gainmode = 9
            rep  = self.dll.PSL_VHR_set_gain_mode(9)
        elif mode == 'gain1+30_8b':
            self.gainmode = 10
            rep  = self.dll.PSL_VHR_set_gain_mode(10)
        else:
            rep  = "Gain mode not valid"

        if self.gainmode in [0,1,2,3,4,5]:
            self.mode = "I;16"
        elif self.gainmode in [6,7,8,9,10]:
            self.mode = "L"

        self.UpdateSize()

        return rep

    def SetVideoGain(self, gain):
        return self.dll.PSL_VHR_set_video_gain(gain)

    def SetChipGain(self, gain):
        return self.dll.PSL_VHR_set_chip_gain(gain)

    def IsIntensifier(self):
        return self.HasIntensifier()

    def SetIntensifierGain(self, gain): #SetChipGain
        return self.dll.PSL_VHR_set_chip_gain(gain)

    def SetClockSpeed(self, mode):
        if mode == '200MHz':
            return self.dll.PSL_VHR_set_speed(2)
        elif mode == '100MHz':
            return self.dll.PSL_VHR_set_speed(1)
        elif mode == '50MHz':
            return self.dll.PSL_VHR_set_speed(0)
        else:
            return False

    def GetTemperature(self):
        try:
            if self.tempread:
                return self.dll.PSL_VHR_read_CCD_temperature()
            else:
                return None
        except:
            return None

    def SetTemperature(self,temp):
        return False

    def SetPowerSavingMode(self,mode):
        try:
            if mode=='PowerOn':
                return self.dll.PSL_VHR_set_power_saving_mode(1)
            elif mode=='PowerOff':
                return self.dll.PSL_VHR_set_power_saving_mode(0)
            elif mode=='CoolingOff':
                return self.dll.PSL_VHR_set_power_saving_mode(2)
        except:
            print ("Cannot apply PowerSavingMode %s"%mode)

    #-------- IMAGE ACQUISITION--------------------------------
    def Snap(self):
        self.state = 1
        self.abort_flag = False
        rep = self.dll.PSL_VHR_Snap_and_return()
        while not self.dll.PSL_VHR_Get_snap_status():
            pass
        self.state = 0
        return rep

    def SnapAndReturn(self):
        self.abort_flag = False
        rep = self.dll.PSL_VHR_Snap_and_return()
        return rep

    def GetStatus(self):
        return self.dll.PSL_VHR_Get_snap_status()

    def AbortSnap(self):
        self.abort_flag = True
        self.state = 0
        return self.dll.PSL_VHR_abort_snap()

    def GetImagePointer(self):
        imp = self.dll.PSL_VHR_get_image_pointer()
        self.dll.PSL_VHR_transfer_to_safebufferC(imp)
        return self.dll.PSL_VHR_get_pointer_to_safebufferC()

    def GetRawImage(self):
        imp = self.GetImagePointer()
        (Nx,Ny) = self.GetSize()

        if self.gainmode in [0,1,2,3]:
            depth = 2
        elif self.gainmode == 4 :
            depth = 3
        else:
            depth = 1

        return ((Nx,Ny),imp[0:depth*Nx*Ny])

    def GetImage(self,imp=None):
        if imp==None:
            imp = self.GetImagePointer()

        (Nx,Ny) = self.GetSize()

        if self.gainmode in [0,1,2,3]:
            self.dll.PSL_VHR_apply_post_snap_processing(imp)
            depth = 2
        elif self.gainmode == 4 :
            (Nx,Ny),imp = self.Demangle(imp,Nx,Ny)
            depth = 2
        elif self.gainmode == 5 :
            self.dll.PSL_VHR_apply_post_snap_processing(imp)
            depth = 2
        elif self.gainmode in [6,7,8,9,10]:
            depth = 1


        if self.remapping and not self.GlobalRemap:
            (Nx,Ny),imp = self.Remap(imp,Nx,Ny)

        if self.SoftBin!=(1,1):
            Nx,Ny = self.SoftBinImage(imp,Nx,Ny)


        return ((Nx,Ny),imp[0:depth*Nx*Ny])

    #-------- CAMERA CORRECTION FUNCTIONS -------------

    def SoftBinImage(self, image_pointer, Nx, Ny):
        newX = C.c_int(Nx)
        newY = C.c_int(Ny)
        Sx,Sy = self.SoftBin
        if self.gainmode in [6,7,8,9,10]:
            self.dll.PSL_VHR_software_bin_8bit_image(image_pointer,C.byref(newX),C.byref(newY),Sx,Sy)
        else:
            self.dll.PSL_VHR_software_bin_image(image_pointer,C.byref(newX),C.byref(newY),Sx,Sy)

        Nx,Ny = newX.value,newY.value
        return (Nx,Ny)

    def OpenMap(self, file_name="distortion.map"):
        return self.dll.PSL_VHR_open_map(file_name)

    def Remap(self, image_pointer, Nx, Ny):
        newX = C.c_int(Nx)
        newY = C.c_int(Ny)

        #if self.is2tap:
        #    imp = self.dll.PSL_VHR_remap_double_image(image_pointer,C.byref(newX),C.byref(newY),self.smooth, self.clip)
        #else:
        imp = self.dll.PSL_VHR_remap_image(image_pointer,C.byref(newX),C.byref(newY),self.smooth, self.clip)


        return ((newX.value,newY.value),imp)

    def Demangle(self, image_pointer, Nx, Ny):
        newX = C.c_int(Nx)
        newY = C.c_int(Ny)
        imp = self.dll.PSL_VHR_demangle_rgb24_into_16bit_image(image_pointer,C.byref(newX),C.byref(newY))
        return ((newX.value,newY.value),imp)

    def EnableRemapping(self,enable):
        self.remapping = enable
        return True

    def EnableSmooth(self,enable):
        self.smooth = bool(enable)
        return True

    def EnableClip(self,enable):
        self.clip = bool(enable)
        return True

    def EnableOffset(self, enable):
        return self.dll.PSL_VHR_enable_offset_subtraction(enable)

    def EnableBrightPixel(self, enable):
        return self.dll.PSL_VHR_enable_bright_pixel_correction(enable)

    def EnableFlatField(self, enable):
        return self.dll.PSL_VHR_enable_flat_field_correction(enable)

    def MakeFlatField(self):
        try:
            if self.dll.PSL_VHR_generate_flat_field_image(self.FlatAverage):
                return True
            else:
                return False
        except:
            return False

    def SetFlatAverage(self,average_number):
        self.FlatAverage = average_number
        return True

    def EnableStreaming(self,enable):
        self.dll.PSL_VHR_enable_image_streaming(C.c_bool(enable))
        #print "Streaming",enable,self
        return True

    def InitSequence(self,imnum):
        self.SeqLen = imnum
        self.dll.PSL_VHR_initialise_sequence_storage(C.c_uint(self.SeqLen))

    def SnapSequence(self):
        self.dll.PSL_VHR_snap_sequence(C.c_uint(self.SeqLen))

    def GetSequencePointer(self,id):
        self.PSL_VHR_get_sequence_image_pointer(C.byref(self.safe),C.c_uint(id))
        return self.safe

    def FreeSequence(self):
        self.dll.PSL_VHR_free_sequence_storage()

    def SaveSequence(self):
        self.dll.PSL_VHR_save_sequence_as_multiple_flf_files(C.c_uint(self.SeqLen))

    def EnableSharpening(self, enable):
        self.dll.PSL_VHR_enable_sharpening(enable)
        return True

    def EnableAutoLevel(self, enable):
        self.dll.PSL_VHR_enable_ALC(enable)
        return True

    def SetALCMaxExp(self,maxexp):
        self.dll.PSL_VHR_set_ALC_max_exp(maxexp)
        return True

    def SetALCWin(self,l,t,r,b):
        self.dll.PSL_VHR_set_ALC_window_coords(l,t,r,b)
        return True

    def EnableBestFit(self, enable):
        self.dll.PSL_VHR_enable_bestfit(enable)
        return True

    def SetBFPeek(self,peek):
        self.dll.PSL_VHR_set_bestfit_peek(peek)
        return True

    def SetIFDelay(self,delay):
        self.dll.PSL_VHR_set_delay_between_images(delay)
        return True

    def EnableBinningFilter(self, enable):
        try:
            self.dll.PSL_VHR_enable_binning_filter(enable)
            return True
        except:
            return False

    def AutoBinningFilter(self, enable):
        try:
            self.dll.PSL_VHR_enable_auto_binning_filter(enable)
            return True
        except:
            return False

    def EnableGamma(self, enable):
        return self.dll.PSL_VHR_enable_gamma(enable)

    def SetGammaPeak(self,value):
        return self.dll.PSL_VHR_set_gamma_gain_bright(value)

    def SetGammaBright(self,value):
        return self.dll.PSL_VHR_set_gamma_gain_brightness(value)

    def SetFlickerMode(self,value):
        if value=="Off":
            return self.dll.PSL_VHR_set_flicker_mode(0)
        elif value=="50MHz":
            return self.dll.PSL_VHR_set_flicker_mode(1)
        elif value=="60MHz":
            return self.dll.PSL_VHR_set_flicker_mode(2)




if __name__ == '__main__':


    from PIL import Image
    import numpy
    NUMPY_MODES = {"L":numpy.uint8, "I;16":numpy.uint16}

    def PILfromArray(newarr,mode='I;16'):
        return Image.fromarray(newarr,mode)

    def arrayFromBuffer(data, size, mode='I;16'):
        w,h = size
        return numpy.frombuffer(data,NUMPY_MODES[mode]).reshape((h,w))

    cam = GEVSCMOS("", "SCMOS")

    cam.Open()

    #======= Init camera setup
    cam.SetClockSpeed('50MHz')
    cam.SetGainMode("gain1")
    cam.SetTrigger("FreeRunning")
    cam.EnableAutoLevel(0)
    cam.SetExposure(2,"Millisec")

    #======= Acquire Image
    cam.Snap()
    #cam.Snap()
    size,data = cam.GetImage()
    mode = cam.GetMode()

    #====== Buffer to Numpy array
    arry = arrayFromBuffer(data,size)
    arry8 = arry*(255/65535.)
    arry8 = arry8.astype(numpy.uint8)

    #======== Array to PIL Image
    pil16 = PILfromArray(arry,mode)  #16bit image
    pil8 =  PILfromArray(arry8,'L')  #8bit image
    #save the images
    #pil16.save("test16.tiff")
    pil8.show()
    pil8.save("test8.tiff")

    cam.Close()
