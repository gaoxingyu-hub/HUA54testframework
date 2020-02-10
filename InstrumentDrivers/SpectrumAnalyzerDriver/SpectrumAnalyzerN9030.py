# -*- coding: utf-8 -*- 
'''
Created on 2015年5月14日

@author: SYH
'''
import SpectrumAnalyzer

class SpectrumAnalyzerN9030A(SpectrumAnalyzer.SpectrumAnalyzer):
    '''
    classdocs
    '''
    def __init__(self,Addr):
        SpectrumAnalyzer.SpectrumAnalyzer.__init__(self,Addr)

    