# -*- coding: utf-8 -*- 
'''
Created on 2018.8.14

@author: xiaowei.xu
'''


from .VectorNetworkAnalyzer import VNA
import re,string
import time

# class S2VNA(PyVisaInstr.pyVisaInstr):
class S2VNA_SCPI(VNA):
    '''
    copper mountain 系列频谱分析仪
    '''

    def __init__(self,Addr):
        VNA.__init__(self,Addr)

     
#     def __init__(self,Addr):
#         '''
#                         初始化示波器，根据给定的地址进行初始化，并获得操作句柄
#         '''
#         PyVisaInstr.pyVisaInstr.__init__(self, Addr)
#         self.VNA=self.instr     
    
    
    def GetRawData(self):
        Data = self.app.SCPI.SENSe(1).DATA.RAWData("S11")
#         cmd='SENSe1:DATA:RAWData? S11\n'
#         Data = self.Ask(cmd)
        return Data
    def GetIDN(self):
#         return self.Ask('*IDN?\n')
        return self.Ask('*IDN?')
      
    def SetStartFreq(self,StartFreq):
        '''
        起始频率，单位Hz
        '''
        self.app.SCPI.SENSe.FREQuency.STARt = StartFreq
        
    def GetStartFreq(self):  
        mval = self.app.SCPI.SENSe.FREQuency.STARt  
        return mval 
    
    def SetStopFreq(self,StopFreq):    
        '''
        截止频率
        '''
        self.app.SCPI.SENSe.FREQuency.STOP = StopFreq
        
    def GetStopFreq(self):  
        mval = self.app.SCPI.SENSe.FREQuency.STOP  
        return mval
        
    def SetSpan(self,Span):    
        '''
        频率范围，扫频有两种描述方式：
    1. 起始频率和截止频率；
    2. 中心频率和频率范围
        '''
        cmd='SENS:FREQ:SPAN '+str(Span)
        self.Write(cmd)
        
    def GetSpan(self):  
        cmd='SENS:FREQ:SPAN?'
        resultstring= self.Ask(cmd)
        return self.GetReturnNumberFromString(resultstring)
    
    def SetCentreFreq(self,Freq):
        self.app.SCPI.SENSe.FREQuency.CENTer = Freq
        
    def GetCentreFreq(self):  
        Value = self.app.SCPI.SENSe.FREQuency.CENTer
        return Value
    
    def SetIFBW(self,IFBW):
        '''
        中频带宽IFBW
        '''
        cmd='SENS:BWID '+str(IFBW)
        self.Write(cmd)    
    
    def GetIFBW(self):  
        cmd='SENS:BWID?'
        resultstring= self.Ask(cmd)
        return self.GetReturnNumberFromString(resultstring) 
    
    def SetAverageStatus(self,Status):
        cmd='SENS:AVER '+ str(Status)
        self.Write(cmd)    
    
    def GetAverageStatus(self):
        cmd='SENS:AVER?'
        resultstring= self.Ask(cmd)
        return self.GetReturnNumberFromString(resultstring)>0
    
    def SetAverageTimes(self,times):
        
        cmd='SENS:AVER:COUN '+ str(times)
        self.Write(cmd)
    
    def setSweepTime(self,SweepTime):
        cmd='SENSe:SWEep:TIME '+ str(SweepTime) 
        self.Write(cmd)
        
    def SweepTimeAuto(self,status):
        cmd='SENSe:SWEep:TIME:AUTO '+status 
        self.Write(cmd)
        
    def SetOutputPower(self,dBm):
        '''
        设置矢网源功率输出大小
        '''
        cmd='SOUR:POW '+ str(dBm)
        self.Write(cmd)
            
    def SetTracePoint(self,point):   
        '''
        设置扫描点数
        '''
        cmd='SENS:SWE:POIN '+ str(point)
        self.Write(cmd)
        
    def DeletAllMeas(self):
        cmd='CALC:PAR:DEL:ALL'
        self.Write(cmd) 
        
    def CreateMeas(self,TraceName,MeasType):
        cmd='CALC:PAR:SDEF '+"'"+TraceName+"'"+','+"'"+MeasType+"'"
        self.Write(cmd) 
        
    def DisplayMeas(self,TraceName):  
        cmd = 'DISP:WIND:TRACE:FEED '+"'"+TraceName+"'" 
        self.Write(cmd)
        
    def SelectMeas(self,TraceName):
        if TraceName.find('1')>=0:
            cmd='CALCulate1:PARameter1:SELect'
        elif TraceName.find('2')>=0:
            cmd='CALCulate1:PARameter2:SELect'
        elif TraceName.find('3')>=0:
            cmd='CALCulate1:PARameter3:SELect'
        elif TraceName.find('4')>=0:
            cmd='CALCulate1:PARameter4:SELect'
        self.Write(cmd)
    def DataFormat(self):
        self.Write('FORMat ASCII')    
        
    def GetTraceData(self,DataFormat):
        cmd='CALC:DATA? '+str(DataFormat)
        time.sleep(1)
        Temp=self.Ask(cmd)
        #TraceData=Temp.Spilt('')
        return Temp.split(',')
    
    def MeasQ_F_Loss(self):
        self.Write('CALC:MARK:FUNC:BWID:MODE BPAS')   
        self.Write('CALC:MARK:FUNC:BWID:GMC OFF')   
        self.Write('CALC:MARK:FUNC:BWID:GMC OFF')   
        self.Write('CALC:MARK:FUNC:EXEC BFIL')
        self.Write('CALC:MARK:SEAR:BFIL:RES ON')
        self.Write('CALC:MARK:BWID 3')
        Temp=self.Ask('CALC:MARK:BWID?')
        return Temp.split(',')
    
    def MarkerSearchLeft(self):
        '''
        This command is the ZVR-compatible equivalent of
        CALCulate<Chn>:MARKer<Mk>:FUNCtion:EXECute LPEak
        '''
        cmd='CALCulate:MARKer:SEARch:LEFT'
        self.Write(cmd)
        
    def MarkerSearchRight(self):
        '''
        This command is the ZVR-compatible equivalent of
        CALCulate<Chn>:MARKer<Mk>:FUNCtion:EXECute RPEak
        '''
        cmd='CALCulate:MARKer:SEARch:RIGHt'
        self.Write(cmd)
        
    def SetMarker(self,MarkerNO,status):
        cmd='CALC:MARK'+str(MarkerNO)+''+str(status)
        self.Write(cmd)
            

    def DefineMarkerXValue(self,markerno,X):
        cmd='CALC:MARK'+str(markerno)+':X '+str(X)
        self.Write(cmd)    
        
    def GetXValueofMarker(self,markerno):
        cmd='CALC:MARK'+str(markerno)+':X?'
        return float(self.Ask(cmd))
    
    def GetMarkerValue(self,markerno):
        cmd='CALC:MARK'+str(markerno)+':Y?'
        mtemp = self.Ask(cmd).strip(',').split(',')
        return float(mtemp[0])
#         val =self.app.SCPI.CALCulate(1).SELected.MARKer(markerno).Y
#         return val[0]
        
    def SetMeasFormat(self,format):
        '''
        设置矢网的测量格式：
        MLINear,
        MLOGarithmic,
        PHASe,
        IMAGinary,
        REAL,
        POLar,
        SMITh,
        SWR,
        GDELay
        '''
        cmd='CALC:FORM '+ str(format)
        self.Write(cmd)

        
    def Port1OpenCal(self):
        self.Write(':SENSe1:CORRection:COLLect:ACQuire:SELected OPEN, 1')
        
    def Port2OpenCal(self):
        self.Write(':SENSe1:CORRection:COLLect:ACQuire:SELected OPEN, 2')
        
    def Port1ShortCal(self):
        self.Write(':SENSe1:CORRection:COLLect:ACQuire:SELected SHORT, 1')
        
    def Port2ShortCal(self):
        self.Write(':SENSe1:CORRection:COLLect:ACQuire:SELected SHORT, 2')
        
    def Port1MathchCal(self):
        self.Write(':SENSe1:CORRection:COLLect:ACQuire:SELected MATCH, 1')   
        
    def Port2MathchCal(self):
        self.Write(':SENSe1:CORRection:COLLect:ACQuire:SELected MATCH, 2')    
        
    def Port1Reflect(self):
        self.Write(':SENSe1:CORRection:COLLect:ACQuire:SELected REFL, 1')
        
    def Port2Reflect(self):
        self.Write(':SENSe1:CORRection:COLLect:ACQuire:SELected REFL, 2')
        
    def LineCal(self):
        cmd=':SENSe1:CORRection:COLLect:ACQuire:SELected LINE1, 1,2'
        self.Write(cmd)
    
    def ApplyCal(self):
        self.Write(':SENSe1:CORRection:COLLect:SAVE:SELected')
        
    def StoreCalResult(self,filename):
        cmd=':MMEMORY:STORE:CORRection 1, '+"'"+filename+'.cal'+"'"
        self.Write(cmd)
           
    def LoadCalResult(self,filename):
        cmd=':MMEMORY:LOAD:CORRection 1, '+"'"+filename+'.cal'+"'"
        self.Write(cmd)
        
    def LoadState(self,filename):
        cmd="MMEM:LOAD:STAT 'State01'"
        self.Write(cmd)
        
     

######### SCPI指令
# mVNA= S2VNA('TCPIP0::127.0.0.1::5025::SOCKET')
# vpp43.set_attribute(mVNA.instr.vi, VI_ATTR_SUPPRESS_END_EN, VI_FALSE)
# vpp43.set_attribute(mVNA.instr.vi, VI_ATTR_SEND_END_EN, VI_FALSE)

######### DCOM指令
# mVNA = S2VNA()
# # mVNA.app.SCPI.system.preset()
# # mVNA.app.SCPI.MMEMory.LOAD.STATe = 'State01'
# # mVNA.SelectMeas('Tr3')
# # mVNA.SetMarker(1,'ON')
# # mVNA.DefineMarkerXValue(1,1500*1e6)
# # 
# start = time.clock()
# for i in range(100):
#     record=mVNA.GetRawData()
# #     record = mVNA.GetMarkerValue(1)
# end = time.clock()
#  
# print end-start
# print record

# print record
# 