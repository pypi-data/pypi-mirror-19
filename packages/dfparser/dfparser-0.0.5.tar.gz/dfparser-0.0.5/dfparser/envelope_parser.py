#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 20:54:46 2016

@author: chernov
"""

import os
import sys
import re
import json
import struct
import time

cur_dir = os.path.dirname(os.path.realpath(__file__))
if not cur_dir in sys.path: sys.path.append(cur_dir)
del cur_dir

from type_codes import meta_types, header_types
        
def create_message(json_meta: dict, data: bytearray=b'',
                   data_type: "binary_types"=0) -> bytearray:
    """
     Create message, containing meta and data in df-envelope format
     @json_meta - metadata
     @data - binary data
     @return - message as bytearray
     
    """
    __check_data(data)
    
    header = __create_machine_header(json_meta, data, data_type)
    meta = __prepare_meta(json_meta)
    
    return header + meta + data
    
    
def parse_from_file(filename: str, nodata: bool=False) \
    -> [dict, dict, bytearray]:
    """
     Parse df message from file
     @filename - path to file
     @nodata - do not load data
     @return - [binary header, metadata, binary data]
     
    """
    
    header = None
    with open(filename, "rb") as file:
        header = read_machine_header(file.read(30))
        meta_raw = file.read(header['meta_len'])
        meta = __parse_meta(meta_raw, header)
        data = b''
        if not nodata:
            data = file.read(header['data_len'])
        return header, meta, data 
    
    
def parse_message(message: bytearray, nodata: bool=False) \
    -> [dict, dict, bytearray]:
    """
     Parse df message from bytearray
     @message - message data
     @nodata - do not load data
     @return - [binary header, metadata, binary data]
     
    """
    
    header = read_machine_header(message)
    meta_raw = message[30:30 + header['meta_len']]
    meta = __parse_meta(meta_raw, header)
    data_start = 30 + header['meta_len']
    data = b''
    if not nodata:
        data = message[data_start:data_start + header['data_len']]
    return header, meta, data

    
def read_machine_header(data: bytearray) -> dict:
    """
     Parse binary header
     @data - bytearray, contains binary header
     @return - parsed binary header
    """
    
    header = dict()
    header['type'] = struct.unpack('>I', data[2:6])[0]
    header['time'] = struct.unpack('>I', data[6:10])[0]
    header['meta_type'] = struct.unpack('>I', data[10:14])[0]
    header['meta_len'] = struct.unpack('>I', data[14:18])[0]
    header['data_type'] = struct.unpack('>I', data[18:22])[0]
    header['data_len'] = struct.unpack('>I', data[22:26])[0]
    
    return header
    
    
def get_messages_from_stream(data: bytearray) \
    -> [[{dict, dict, bytearray}], bytearray]:
    """
      Extract complete messages from stream and cut out them from stream
      @data - stream binary data
      @return - [list of messages, choped stream data]
      
    """
    messages = []
    iterator = get_messages_from_stream.header_re.finditer(data)
    last_pos = 0
    for match in iterator:
        pos = match.span()[0]

        header = read_machine_header(data[pos:])
        cur_last_pos = pos + 30 + header['meta_len'] + header['data_len']

        if cur_last_pos > len(data):
            break
        
        header, meta, bin_data = parse_message(data[pos:])
        messages.append({'header': header, 'meta': meta, 'data': bin_data})
        
        last_pos = cur_last_pos
        
    data = data[last_pos:]
    return messages, data
        
get_messages_from_stream.header_re = re.compile(b"#!.{24}!#", re.DOTALL)
    

def __parse_meta(meta_raw, header):
    if header["meta_type"] == meta_types["JSON_METATYPE"]:
        return json.loads(meta_raw.decode())
    else:
        err = "Parsing meta type %s not implemented"%(bin(header["meta_type"]))
        raise NotImplementedError(err)
        
    
def __prepare_meta(json_meta):
    if type(json_meta) is dict:
        json_meta = json.dumps(json_meta).encode()
        json_meta += b'\r\n\r\n'
    elif not type(json_meta) is str:
        raise ValueError("Input meta should be dict or str")
    return json_meta


def __check_data(data):
    if not type(data) is bytes:
        raise ValueError("Input data should have bytes type")
        

def __create_machine_header(json_meta: dict, data: bytearray=b'',
                            data_type: "binary_types"=0) -> bytearray:
    
    json_meta = __prepare_meta(json_meta)
    __check_data(data)
    
    binary_header = b'#!'
    
    #binary header type
    binary_header += struct.pack('>I', header_types["DEFAULT"])
    millis = int(round(time.time() * 1000))
    #current time
    binary_header += struct.pack('>Q', millis)[4:]
    #meta type
    binary_header += struct.pack('>I', meta_types["JSON_METATYPE"])
    #meta length
    binary_header += struct.pack('>I', len(json_meta))
    #data type
    binary_header += struct.pack('>I', data_type)
    #data length
    binary_header += struct.pack('>I', len(data))
    
    binary_header += b'!#\r\n'
    
    return binary_header

