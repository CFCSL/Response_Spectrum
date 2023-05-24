import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets



def EC8(T,ag=0.5,GroundType='A',Eta=1,Dir='Horizontal',RS_Type=1):
	#Turn it into Array:
	T=np.atleast_1d(T)
	T=T.astype('float64')
	Ground={1:{},2:{}}
	#Ground[RS_Type][GroundType]=[S,TB,TC,TD]
	#Type 1
	Ground[1]['A']=[1.0, 0.15,0.4,2.0]
	Ground[1]['B']=[1.2, 0.15,0.5,2.0]
	Ground[1]['C']=[1.15,0.20,0.6,2.0]
	Ground[1]['D']=[1.35,0.20,0.8,2.0]
	Ground[1]['E']=[1.4, 0.15,0.5,2.0]
	#Type 2
	Ground[2]['A']=[1.0, 0.05,0.25,1.2]
	Ground[2]['B']=[1.35,0.05,0.25,1.2]
	Ground[2]['C']=[1.5, 0.10,0.25,1.2]
	Ground[2]['D']=[1.8, 0.10,0.30,1.2]
	Ground[2]['E']=[1.6, 0.05,0.25,1.2]
	# Dir= Vartical:
	Ground[1]['Vertical']=[0.90,1.0, 0.05,0.15,1.0]
	Ground[2]['Vertical']=[0.45,1.0, 0.05,0.15,1.0]
	if Dir=='Horizontal':
		S,TB,TC,TD=Ground[RS_Type][GroundType]
		aa=ag
		_dir_coeff=2.5
	elif Dir=='Vertical':
		avg_ratio,S,TB,TC,TD=Ground[RS_Type][Dir]
		aa=ag*avg_ratio
		_dir_coeff=3.0
	else:
		print('Error: set dir=Vertical or Horizontal')
	condList=[(0<=T)&(T<TB),(TB<=T)&(T<=TC),(TC<T)&(T<=TD),TD<T]
	funcList=[lambda T: aa*S*(1+(T/TB)*(Eta*_dir_coeff-1)),lambda T: aa*S*Eta*_dir_coeff,lambda T: aa*S*Eta*_dir_coeff*(TC/T),lambda T: aa*S*Eta*_dir_coeff*((TC*T)/T**2)]
	Amp=np.piecewise(T, condList, funcList)
	return Amp


## Eurocode Elastic Design Spectrum (Type 1):

x = np.linspace(0, 10, 200)
plt.plot(x,EC8(x,GroundType='A',Dir='Horizontal',RS_Type=1),label='A')
plt.plot(x,EC8(x,GroundType='B',Dir='Horizontal',RS_Type=1),label='B')
plt.plot(x,EC8(x,GroundType='C',Dir='Horizontal',RS_Type=1),label='C')
plt.plot(x,EC8(x,GroundType='D',Dir='Horizontal',RS_Type=1),label='D')
plt.plot(x,EC8(x,GroundType='E',Dir='Horizontal',RS_Type=1),label='E')
plt.legend()
plt.show()


## Eurocode Elastic Design Spectrum (Type 2):

x = np.linspace(0.01, 10, 200)
plt.plot(x,EC8(x,GroundType='A',Dir='Horizontal',RS_Type=2),label='A')
plt.plot(x,EC8(x,GroundType='B',Dir='Horizontal',RS_Type=2),label='B')
plt.plot(x,EC8(x,GroundType='C',Dir='Horizontal',RS_Type=2),label='C')
plt.plot(x,EC8(x,GroundType='D',Dir='Horizontal',RS_Type=2),label='D')
plt.plot(x,EC8(x,GroundType='E',Dir='Horizontal',RS_Type=2),label='E')
plt.legend()
plt.show()

## Eurocode Elastic Design Spectrum (Type 1 & 2 -Vertical):
## Vertical is similar for all Soil types
x = np.linspace(0, 10, 200)
plt.plot(x,EC8(x,GroundType='A',Dir='Vertical',RS_Type=1),label='Type 1')
plt.plot(x,EC8(x,GroundType='A',Dir='Vertical',RS_Type=2),label='Type 2')
plt.legend()
plt.show()


## Export the RS to csv in Abaqus input format¶
A=pd.DataFrame({'Amplitude':EC8(x,GroundType='A',Dir='Horizontal',RS_Type=1)*9.81,'Frequency':(1/x),'Damping':0})
A=A.sort_values(by=['Frequency']).round(5)
A.to_csv('RS_EC8_A_Horizontal.inp',index=False,header=False)