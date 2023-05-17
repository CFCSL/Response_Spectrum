#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:53:20 2023

@author: namnguyen
"""
import pandas as pd
import streamlit as st
import Response_Spectrum as RS
import numpy as np
import matplotlib.pyplot as plt
import zipfile
from io import BytesIO



st.write('**Direction:**')
Dir=st.radio("Select Direction:", ("Horizontal", "Vertical"))


st.write("**Response Spectrum:**")
RS_Type=st.radio("Response Spectrum Type",("Type 1", "Type 2"))


st.write("Ground Type: ")
options=["A","B","C","D","E"]
GroundType=st.multiselect("Select options:", options)


st.write("Period T(s)")

st.write("select the range of T(s) to plot:")

T_max=st.number_input("T_max(s)", value= 10., min_value=1., step=1., format="%.3f")
x = np.linspace(0.01,T_max , 200)


# Create the plot
fig, ax = plt.subplots()
for k in GroundType:
    ax.plot(x, RS.EC8(x, GroundType=k, Dir='Horizontal', RS_Type=2), label=k)
    ax.legend()
    ax.set_title(Dir)
    
# Set the x-axis and y-axis labels
ax.set_xlabel('T(s)')
ax.set_ylabel('$S_e/a_g$')

# Display the plot in Streamlit
st.pyplot(fig)

# Create an empty list to store the file paths
file_paths = []

## Export the RS to csv in Abaqus input format¶
#A=pd.DataFrame({'Amplitude':seismic.EC8(x,GroundType='A',Dir='Horizontal',RS_Type=1)*9.81,'Frequency':(1/x),'Damping':0})


for k in GroundType:
        df=pd.DataFrame({'Amplitude':RS.EC8(x,GroundType=k,Dir=Dir,RS_Type=1)*9.81,'Frequency':(1/x),'Damping':0})
        df=df.drop('Damping', axis=1)
        df=df.sort_values(by=['Frequency']).round(5)
        st.write("Ground type ", k)
        file_path = 'RS_EC8' + '_' + str(k) + '_' + str(Dir) + '.csv'
        df.to_csv(file_path, index=False, header=False)
        st.write(df)
        file_paths.append(file_path)
# Create a zip file in memory
zip_file = BytesIO()
with zipfile.ZipFile(zip_file, 'w') as zipf:
    for file_path in file_paths:
        zipf.write(file_path)

# Download the zip file
zip_file.seek(0)
st.download_button(label='Download CSV Files as ZIP', data=zip_file, file_name='files.zip')















