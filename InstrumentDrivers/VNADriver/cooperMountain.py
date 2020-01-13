# -*- coding: utf-8 -*- 
'''
Created on 2015.10.14

@author: Penghan Xie
'''

from .VectorNetworkAnalyzer import VNA
import pyvisa
import re,string,os
import time

class R60(VNA):
    '''
    R&S矢量网络分析仪底层驱动，包括ZVA,ZVB,ZVT系列
    '''
    def __init__(self,Addr):
        VNA.__init__(self,Addr)
        self.instr.term_chars  = '\n' 
        vpp43.set_attribute(self.instr.vi, VI_ATTR_SUPPRESS_END_EN, VI_FALSE)
        
    def SetStartFreq(self,channel,StartFreq):
        '''
        起始频率，单位Hz
        '''
#         cmd='SENS:FREQ:STAR '+str(StartFreq)
        cmd='SENS'+str(channel)+':FREQ:STAR '+str(StartFreq)
        self.Write(cmd)
        
    def GetStartFreq(self):  
        cmd='SENS:FREQ:STAR?'
        resultstring= self.Ask(cmd)
        return self.GetReturnNumberFromString(resultstring)    
    
    def SetStopFreq(self,channel,StopFreq):    
        '''
        截止频率
        '''
#         cmd='SENS:FREQ:STOP '+str(StopFreq)
        cmd='SENS'+str(channel)+':FREQ:STOP '+str(StopFreq)
        self.Write(cmd)
        
    def GetStopFreq(self):  
        cmd='SENS:FREQ:STOP?'
        resultstring= self.Ask(cmd)
        return self.GetReturnNumberFromString(resultstring)
        
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
        cmd='SENS:FREQ:CENT '+str(Freq)
        self.Write(cmd)
    
    def SetTracePoint(self,channel,points):
        cmd='SENS'+str(channel)+':SWE:POIN '+ str(points)
        cmd=cmd+'\n'
        self.Write(cmd)
           
    def GetCentreFreq(self):  
        cmd='SENS:FREQ:CENT?'
        resultstring= self.Ask(cmd)
        return self.GetReturnNumberFromString(resultstring)
    
    def SetIFBW(self,channel,IFBW):
        '''
        中频带宽IFBW
        '''
#         cmd='SENS:BWID '+str(IFBW)
        cmd='SENS'+str(channel)+':BWID '+str(IFBW)
        self.Write(cmd)    
    
    def GetIFBW(self):  
        cmd='SENS:BWID?'
        resultstring= self.Ask(cmd)
        return self.GetReturnNumberFromString(resultstring) 
    
    def SetMeasFormat(self,channel,format):
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
#         cmd='CALC:FORM '+ str(format)
        cmd='CALC'+str(channel)+':FORM '+ str(format)
        self.Write(cmd)
    def SelectMeas_channel1(self,TraceName):
        TraceName=str(TraceName)
        if TraceName.find('1')>=0:
            cmd='CALCulate1:PARameter1:SELect'
        elif TraceName.find('2')>=0:
            cmd='CALCulate1:PARameter2:SELect'
        elif TraceName.find('3')>=0:
            cmd='CALCulate1:PARameter3:SELect'
        elif TraceName.find('4')>=0:
            cmd='CALCulate1:PARameter4:SELect'
        cmd=cmd+"\n"
        self.Write(cmd)
        
    def SelectMeas_channel2(self,TraceName):
        TraceName=str(TraceName)
        if TraceName.find('1')>=0:
            cmd='CALCulate2:PARameter1:SELect'
        elif TraceName.find('2')>=0:
            cmd='CALCulate2:PARameter2:SELect'
        elif TraceName.find('3')>=0:
            cmd='CALCulate2:PARameter3:SELect'
        elif TraceName.find('4')>=0:
            cmd='CALCulate2:PARameter4:SELect'
        cmd=cmd+"\n"
        self.Write(cmd)
        
    def get_limit_result(self,channel):
#         cmd='CALCulate2:LIMit:FAIL?'
        cmd='CALCulate'+str(channel)+':LIMit:FAIL?'
        cmd=cmd+'\n'
        temp=self.Ask(cmd)
        if int(temp)>0:
            return False
        else:
            return True  
    def get_limit_result_channel1(self):
        cmd='CALCulate1:LIMit:FAIL?'
        cmd=cmd+'\n'
        temp=self.Ask(cmd)
        if int(temp)>0:
            return False
        else:
            return True
        
    def get_limit_result_channel2(self):
        cmd='CALCulate2:LIMit:FAIL?'
        cmd=cmd+'\n'
        temp=self.Ask(cmd)
        if int(temp)>0:
            return False
        else:
            return True
    def get_marker_value(self,channel,marker):
#         cmd='CALCulate1:MARKer'+str(marker)+':Y?\n'
        cmd='CALCulate'+str(channel)+':MARKer'+str(marker)+':Y?\n'
        temp=self.Ask(cmd)
        temp=temp.split(',')
        return string.atof(temp[0])   
        
    def get_marker_value_channel1(self,marker):
        cmd='CALCulate1:MARKer'+str(marker)+':Y?\n'
        temp=self.Ask(cmd)
        temp=temp.split(',')
        return string.atof(temp[0])
        
    def get_marker_value_channel2(self,marker):
        cmd='CALCulate2:MARKer'+str(marker)+':Y?\n'
        temp=self.Ask(cmd)
        temp=temp.split(',')
        return string.atof(temp[0])
    def continuous_sweep(self):
        cmd='TRIGger:SOUR INT\n'
        self.Write(cmd)
        cmd='TRIGger:SINGle\n'
    def single_sweep(self):
        self.Write('TRIGger:SOUR BUS\n')
        self.Write('TRIGger:SINGle\n')
        self.Write('INIT:IMM\n')
        while True:
            time.sleep(0.05)
            tmp=self.Ask('*OPC?\n')
            if tmp=='1':
                break
        
    def LoadState(self,filename):
        cmd='MMEM:LOAD ' + "'"+filename+"'"+'\n'
        self.Write(cmd)
        time.sleep(0.05)
        
    def StoreState(self,filename):
        cmd='MMEMory:STORe ' + "'"+filename+"'"+'\n'
        self.Write(cmd)
        time.sleep(0.05)
        
    def GetTraceData(self,channel):
        cmd='CALC'+str(channel)+':DATA:FDAT?\n'
        temp=self.Ask(cmd)
        result=temp.split(',')
        return result[::2]
    
    def set_marker_search_range(self,channel,start,stop):
#         CALC:MARK:FUNC:DOM
        cmd='CALC'+str(channel)+':MARK:FUNC:DOM ON\n'
        self.Write(cmd)
#         CALC:MARK:FUNC:DOM:STAR
        cmd='CALC'+str(channel)+':MARK:FUNC:DOM:STAR '+str(start)+'\n'
        self.Write(cmd)
        cmd='CALC'+str(channel)+':MARK:FUNC:DOM:STOP '+str(stop)+'\n'
        self.Write(cmd)
        
    def left_target_search(self,channel,marker,value):
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:TYPE LTARget\n'
        self.Write(cmd)
        cmd='CALC'+str(channel)+':MARK'+str(marker)+' ON'
        self.Write(cmd)
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:TARGet '+str(value)+ '\n'
        self.Write(cmd)
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:EXEC'
        self.Write(cmd)
        
    def right_target_search(self,channel,marker,value):
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:TYPE RTARget\n'
        self.Write(cmd)
        
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:TARGet '+str(value)+ '\n'
        self.Write(cmd)
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:EXEC'
        self.Write(cmd)
        
    def max_search(self,channel,marker):
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:TYPE MAXimum\n'
        self.Write(cmd)
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:EXEC'
        self.Write(cmd)   
        
    def minimus_search(self,channel,marker):
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:TYPE MINimum\n'
        self.Write(cmd)
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':FUNC:EXEC'
        self.Write(cmd)

    def set_marker_freq(self,channel,marker,freq):
        cmd='CALC'+str(channel)+':MARK'+str(marker)+' ON'
        self.Write(cmd)
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':X '+str(freq)
        self.Write(cmd)
        
    def get_marker_freq(self,channel,marker):
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':X?'
        return self.AskForNumber(cmd)
    
    def get_marker_power(self,channel,marker):
        cmd='CALC'+str(channel)+':MARK'+str(marker)+':Y?'
        tmp= self.Ask(cmd)
        tmp=tmp.split(',')
        return string.atof(tmp[0])
    
    def set_marker_off(self,channel,marker):
        cmd='CALC'+str(channel)+':MARK'+str(marker)+' OFF'
        self.Write(cmd)
        
    def get_trace_data(self,channel):
        cmd='CALC'+str(channel)+':DATA:FDAT?\n'
        Temp=self.Ask(cmd)
        y=Temp.split(',')
        return y[0:len(y):2]
# from pyvisa.visa import *       
# vna=R60('TCPIP0::127.0.0.1::5025::SOCKET')
# vna.set_marker_search_range(8, 3.4e9, 3.7e9)
# vna.left_target_search(8, 1, -14.5)
# vna.right_target_search(8, 2, -14.5)
# vna.instr.term_chars  = '\n' 
# vpp43.set_attribute(vna.instr.vi, VI_ATTR_SUPPRESS_END_EN, VI_FALSE)
# temp=vna.Ask('CALC:DATA:FDAT?\n')
# result=temp.split(',')
# print result[::2]
# print len(temp)
# print temp
# vna.LoadState('ch2')
# vna.StoreState('ch4')
# vna.LoadState('ch1')
# time.sleep(1)
# vna.LoadState('ch2')
# time.sleep(1)
# vna.LoadState('ch3')
# time.sleep(1)
# vna.LoadState('ch4')
# vna.single_sweep()
# for i in range(8):
#     if i<4:
#         tracename='i+1'
#         vna.SelectMeas_channel1(tracename)
#         marker1[i]=vna.get_marker_value_channel1(1)
#         marker2[i]=vna.get_marker_value_channel1(2)
#         pass_status[i]=vna.get_limit_result_channel1()
#     else:
#         tracename='i-3'
#         vna.SelectMeas_channel2(tracename)
#         marker1[i]=vna.get_marker_value_channel2(1)
#         marker2[i]=vna.get_marker_value_channel2(2)
#         pass_status[i]=vna.get_limit_result_channel2()
#          
# print marker1,marker2,pass_status
        