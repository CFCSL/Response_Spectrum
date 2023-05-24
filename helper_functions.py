#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 12:58:48 2023

@author: namnguyen
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os,re
import base64
from io import BytesIO


#%% Download CSV

def download_csv(df):

    data_csv = df.to_csv(index=False, float_format='%.4f')
    
    # Encode and create the download link
    b64 = base64.b64encode(data_csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="RS_ASSHTO.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)


# Download Sofistik
def download_sofistik(list_df):
    text = '\n'.join([
        "+PROG SOFILOAD",
        "HEAD 'Definition of response spectrum'",
        "UNIT 5 $ units: sections in mm, geometry+loads in m"
    ])
    local_text = ""
    for i, df in enumerate(list_df, 1):
        data_csv = df.to_csv(index=False, float_format='%.4f')
        local_text += '\n'.join([
            "lc no" + str(i+1) + "type none titl 'Sa(T)-SOIL '" + str(df.columns[1]),
            "resp type user mod 5[%] ag 10",
            "ACCE DIR AX 1",
            "FUNC   T   F",
            data_csv
        ])
    
    # Concatenate the existing text and the DataFrame
    combined_text = text + '\n' + local_text + '\n' + "END"
    
    # Create a BytesIO object and write the combined text to it
    text_bytes = combined_text.encode('utf-8')
    buffer = BytesIO()
    buffer.write(text_bytes)
    buffer.seek(0)
    
    # Create the download link
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="RS_SOFISTIK.txt">Download Text</a>'
    
    return href




# =============================================================================
# def download_sofistik(list_df):
#     text = '\n'.join([
#         "+PROG SOFILOAD",
#         "HEAD 'Definition of response spectrum'",
#         "UNIT 5 $ units: sections in mm, geometry+loads in m"
#     ])
#     local_text = ""
#     for i, df in enumerate(list_df, 1):
#         data_csv = df.to_csv(index=False, float_format='%.4f')
#         local_text += '\n'.join([
#             "lc no" + str(i+1) + "type none titl 'Sa(T)-SOIL '" + str(df.columns[1]),
#             "resp type user mod 5[%] ag 10",
#             "ACCE DIR AX 1",
#             "FUNC   T   F",
#             data_csv
#         ])
#     
#     # Concatenate the existing text and the DataFrame
#     combined_text = text + '\n' + local_text + '\n' + "END"
#     
#     # Create a BytesIO object and write the combined text to it
#     text_bytes = combined_text.encode('utf-8')
#     buffer = BytesIO()
#     buffer.write(text_bytes)
#     buffer.seek(0)
#     
#     # Create the download link
#     b64 = base64.b64encode(buffer.read()).decode()
#     href = f'<a href="data:text/plain;base64,{b64}" download="RS_SOFISTIK.txt">Download Text</a>'
#     st.markdown(href, unsafe_allow_html=True)
# 
# 
# 
# =============================================================================






