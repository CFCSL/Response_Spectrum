#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:53:20 2023

@author: namnguyen
"""
import pandas as pd
import streamlit as st
import Response_Spectrum as RS
import help_functions as hf
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


hf.download_csv(df)




# =============================================================================
# 
# # Concatenate the existing text and the DataFrame
# combined_text = text + '\n\n' + df.to_string(index=False, col_space=3)+ '\n\n'+ "END"
# 
# 
# 
# =============================================================================
















