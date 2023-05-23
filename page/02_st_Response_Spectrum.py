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
import matplotlib.pyplot  as plt
import zipfile
from io import BytesIO
import base64



st.write('**Direction:**')
Dir=st.radio("Select Direction:", ("Horizontal", "Vertical"))


st.write("**Response Spectrum:**")
RS_Type = st.radio("Response Spectrum Type", ["Type 1", "Type 2"], index=0)
RS_Type_value = 1 if RS_Type == "Type 1" else 2


st.write("Ground Type: ")
options=["A","B","C","D","E"]
default_options = options  # Set all options as default
GroundType=st.multiselect("Select options:", options, default=default_options)

a_g=st.number_input("a_g [$m/s^2$]", value= 0.5, min_value=0.0, step=0.1, format="%.3f")

st.write("Period T(s)")

st.write("select the range of T(s) to plot:")

T_max=st.number_input("T_max(s)", value= 10., min_value=1., step=1., format="%.3f")
x = np.linspace(0.01,T_max , 200)

# Create the plot
fig, ax = plt.subplots()
for k in GroundType:

    ax.plot(x, 1/a_g*RS.EC8(x, GroundType=k, Dir=Dir, RS_Type=RS_Type_value), label=k)

    ax.legend()
    ax.set_title(Dir)
    
# Set the x-axis and y-axis labels
ax.set_xlabel('T(s)')
ax.set_ylabel('$S_e/a_g$')

# Display the plot in Streamlit
st.pyplot(fig)



# Create an empty dataframe
df = pd.DataFrame({'Frequency[1/s]': (1/x)})


#%%

for k in GroundType:
	df_k=pd.DataFrame({'Frequency[1/s]':(1/x),'Amplitude'+" "+str(k):RS.EC8(x,GroundType=k,Dir=Dir,RS_Type=RS_Type_value)*9.81})
	
	# Merge df and df_k on the "Frequency[1/s]" column
	df = pd.merge(df, df_k, on="Frequency[1/s]")
	
# Round all float columns to three decimal places
df=df.round(3)
st.write(df)

def download_csv():

    # Convert the rounded dataframe to CSV
    csv = df.to_csv(index=False, float_format='%.3f')
    
    # Encode and create the download link
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="RS_E8.csv">Download CSV</a>'
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
    href = f'<a href="data:text/plain;base64,{b64}" download="RS_E8_SOFISTIK.txt">Download Text</a>'
    st.markdown(href, unsafe_allow_html=True)

download_text()


















