#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:20:10 2023

@author: namnguyen
"""
import pandas as pd
import streamlit as st
import Response_Spectrum as RS
import numpy as np
import matplotlib.pyplot  as plt
import zipfile
from io import BytesIO





st.write("**Peak Ground Acceleration:**")
PGA=st.number_input("PGA",value= 0.1, min_value=0.0, step=0.05, format="%.3f")

st.write("**Short-Period Range of Spectrum Acceleration:**")
S_S=st.number_input("$S_S$",value= 0.25, min_value=0.0, step=0.05, format="%.3f")

st.write("**Long-Period Range of Spectrum Acceleration:**")
S_1=st.number_input("$S_1$",value= 0.1, min_value=0.0, step=0.05, format="%.3f")



st.write("Site Class: ")
options=["A","B","C","D","E"]
default_options = options  # Set all options as default
SiteClass=st.multiselect("Select options:", options, default=default_options)


st.write("Period T(s)")

st.write("select the range of T(s) to plot:")

T_max=st.number_input("T_max(s)", value= 10., min_value=1., step=1., format="%.3f")
x = np.linspace(0.01,T_max , 200)


# Create the plot
fig, ax = plt.subplots()
for k in SiteClass:

    ax.plot(x, RS.ASSHTO(x, PGA=PGA, S_S=S_S, S_1=S_1, SiteClass=k), label=k)

    ax.legend()
    #ax.set_title("Design Response Spectrum"+ "PGA=",PGA, + "$S_S$=", S_S, + "$S_1$=", S_1, + "Site Class=", SiteClass)
    ax.set_title("Design Response Spectrum PGA={}, $S_S$={}, $S_1$={}, Site Class={}".format(PGA, S_S, S_1, SiteClass))
    
# Set the x-axis and y-axis labels
ax.set_xlabel('T(s)')
ax.set_ylabel('$C_{sm}$')

# Display the plot in Streamlit
st.pyplot(fig)

# Create an empty list to store the file paths
file_paths = []

for k in SiteClass:
        df=pd.DataFrame({'C_sm':RS.ASSHTO(x, PGA=PGA, S_S=S_S, S_1=S_1, SiteClass=k),'Period':(x)})
        df=df.sort_values(by=['Period']).round(5)
        st.write("Siite Class", k)
        file_path = 'RS_ASSHTO' + '_' + str(k) + '.csv'
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

