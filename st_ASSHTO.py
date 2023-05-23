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
import base64





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


# Create an empty dataframe
df = pd.DataFrame({'Period[s]': x})

# Iterate over SiteClass
for k in SiteClass:
    # Create dataframe df_k for the current SiteClass
    df_k = pd.DataFrame({'Period[s]': x,
                         "C_sm"+"-"+str(k): RS.ASSHTO(x, PGA=PGA, S_S=S_S, S_1=S_1, SiteClass=k)})

    # Merge df and df_k on the "Period" column
    df = pd.merge(df, df_k, on="Period[s]")

# Round all float columns to four decimal places
df = df.round(4)

# Display the merged dataframe
st.write(df)

# Create a button for downloading the dataframe as CSV
def download_csv():

    # Convert the rounded dataframe to CSV
    csv = df.to_csv(index=False, float_format='%.4f')
    
    # Encode and create the download link
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ASSHTO_SOFISTIK.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

download_csv()


text = '\n'.join([
     "+PROG SOFILOAD",'\n',
     "HEAD 'Definition of response spectrum'",'\n',
     "UNIT 5 $ units: sections in mm, geometry+loads in m",'\n',
     "",
     "lc no 101 type none titl 'Sa(T)-SOIL C'",'\n',
     "resp type user mod 5[%] ag 10",'\n',
     "ACCE DIR AX 1",'\n',
     "FUNC   "
 ])


# Concatenate the existing text and the DataFrame
combined_text = text + '\n\n' + df.to_string(index=False, col_space=3)+ '\n\n'+ "END"




def download_text():
    # Create a BytesIO object and write the combined text to it
    text_bytes = combined_text.encode('utf-8')
    buffer = BytesIO()
    buffer.write(text_bytes)
    buffer.seek(0)

    # Create the download link
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="combined_text.txt">Download Text</a>'
    st.markdown(href, unsafe_allow_html=True)

download_text()
