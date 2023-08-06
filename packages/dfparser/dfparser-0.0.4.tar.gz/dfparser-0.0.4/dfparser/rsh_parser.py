#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:06:51 2017

Parser for Troitsk Rsh data files

data file description: 
    https://drive.google.com/open?id=0B0Ux_fvsLMdAOXUwSVRKanNORnc

@author: chernov
"""

import struct
from datetime import datetime

import numpy as np


class RshPackage():
    
    def __init__(self, filename):
        self.file = open(filename, "rb+")
        self.file.seek(0)
        
        self.text_header = self.file.read(5120).decode("cp1251").rstrip('\0')

        header = self.file.read(2048)
        
        self.params = self.__parse_header(header)
        
    def get_event(self, num):
        if num < 0 or num >= self.params["events_num"]:
            raise IndexError("Index out of range [0:%s]"%
                             (self.params["events_num"]))
            
        ch_num = self.params['ch_num']
        ev_size = self.params['event_size']
        
        event = {}
            
        self.file.seek(7168 + num*(96 + 2*ch_num*ev_size))
        
        event["text_hdr"] = self.file.read(64)
        event["ev_num"] = struct.unpack('I', self.file.read(4))[0]
        self.file.read(4)
        
        start_time = struct.unpack('Q', self.file.read(8))[0]
        event["start_time"] = datetime.fromtimestamp(start_time)
        
        self.file.read(16)
        
        event_data = self.file.read(2*ev_size*ch_num)
        
        event["data"] = np.fromstring(event_data, np.short)
                    
        return event

    def update_event_data(self, num, data):
        if num < 0 or num >= self.params["events_num"]:
            raise IndexError("Index out of range [0:%s]"%
                             (self.params["events_num"]))
            
        if type(data) != np.ndarray:
            raise TypeError("data should be np.ndarray")
            
        if data.dtype != np.short:
            raise TypeError("data array dtype should be dtype('int16')")
            
        ch_num = self.params['ch_num']
        ev_size = self.params['event_size']
            
        if data.shape != (ch_num*ev_size,):
            raise Exception("data should contain same number of elements "\
                            "(%s)"%(ch_num*ev_size))
        
        self.file.seek(7168 + num*(96 + 2*ch_num*ev_size) + 96)
        self.file.write(data.tostring())
        self.file.flush()

    def __parse_header(self, header):
        """
          @header - binary header (2048 bytes)
          
        """
        params = {}
        
        params["text_header_size"] = struct.unpack('I', header[0:4])[0] #check

        params["events_num"] = struct.unpack('I', header[8:12])[0]
        
        start_time = struct.unpack('Q', header[16:24])[0]
        params["start_time"] = datetime.fromtimestamp(start_time)
        end_time = struct.unpack('Q', header[24:32])[0]
        params["end_time"] = datetime.fromtimestamp(end_time)
        
        params["datapath"] = header[32: 32 + 255].rstrip(b'\0')
        
        #acquisition max frames
        params["max_events"] = struct.unpack('I', header[288:292])[0]
        
        #acquisition max time in msec
        params["max_time"] = struct.unpack('I', header[292:296])[0]
        
        params["events_per_file"] = struct.unpack('I', header[296:300])[0]
        
        
        params["max_wait_time"] = struct.unpack('I', header[300:304])[0]
        
        params["syncho_channel"] = struct.unpack('I', header[304:308])[0]
        
        params["threshold"] = struct.unpack('d', header[312:320])[0]
        
        params["sync_params"] = header[320:336] #convert
        params["sync_params_num"] = struct.unpack('I', header[336:340])[0]
        
        params["freq"] = struct.unpack('d', header[344:352])[0]
        params["pre_history_size"] = struct.unpack('I', header[352:356])[0]
        
        params["events_in_pack"] = struct.unpack('I', header[356:360])[0]
        
        params["event_size"] = struct.unpack('I', header[360:364])[0]
        
        params["hyst_level"] = struct.unpack('I', header[364:368])[0]
        
        params["ch_num"] = struct.unpack('I', header[368:372])[0]
        
        ch_params = []
        
        for i in range(4):
            ch_data = header[372 + 56*i: 372 + 56*(i+1)]
            ch_param = {}
            ch_param["params"] = ch_data[4:36] #convert
            ch_param["param_num"] = struct.unpack('I', ch_data[36:40])[0]
            ch_param["adjustment"] = struct.unpack('d', ch_data[44:52])[0]
            ch_param["gain"] = struct.unpack('I', ch_data[52:56])[0]
            ch_params.append(ch_param)
            
        params["ch_params"] = ch_params
            
            
        sync_params = {}
        
        sync_params["params"] = header[600:632] #convert
        sync_params["param_num"] = struct.unpack('I', header[632:636])[0]
        sync_params["gain"] = struct.unpack('I', header[636:640])[0]
        
        params["sync_params"] = sync_params
        
        params["err_lang"] = struct.unpack('I', header[640:644])[0]
        params["board_name"] = header[644: 644 + 255].rstrip(b'\0')
        
        params["board_id"] = struct.unpack('I', header[900: 904])[0]
        
        return params

