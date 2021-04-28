#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  appli.py
#  
#  Copyright 2021 William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  ### Press Run to watch it working 

import seaborn as sns;
from ipywidgets import interact,interactive,fixed;
import ipywidgets as widgets;
from IPython import display;
from IPython.core.display import display,HTML;
import pandas as pd;


#Constants
defSep="10px ";defHeight="50px";
ALL="                     ___ALL___ ";
auto="auto ";
yearBase=1900;
mpgToKMPL=0.4251;
lbsToKG=0.453592;

style = """
<style>
div.output_area {
	overflow-y: scroll;
}
div.output_area img {
	max-width: unset;
	max-height:20em;
}
    .widget-label { min-width: 20ex !important; }
</style>
""";



def contentWidget():
	"""
		Create a container to data frame presentation
	"""
	return(widgets.Output(layout=widgets.Layout(width='100%',
		height='auto',max_height='1000px',
		overflow='hidden scroll',)));

def boxWidget():
	global row0,row1,row2,row3,rowBottom,Content;
	return(widgets.VBox(children=(row0,row1,row2,row3,row4,rowBottom,Content)));

def resetHandler(obj):
	"""
		When button Reset is pressed, it will restart filters and
		combo-boxes
	"""
	global drops,box,Content,df;
	for f in drops:
		f.value=ALL;
	
	#Eliminate content
	Content.close();
	#Create new empty content
	Content=contentWidget();
	#take clean data from arrange
	df=pd.DataFrame(data=arrange);
	
	with Content:
		display(df);#display dataFrame
	
	box.close();
	box=boxWidget();
	display(box);

def filterHandler(obj):
	global drops,box,Content,df;
	
	#Eliminate content
	Content.close();
	#Create new empty content
	Content=contentWidget();
	
	#get chosen options
	origin=dropdown_Origins.value;
	company=dropdown_Companies.value;
	year=dropdown_Years.value;
	model=dropdown_Models.value;
	
	#filter data
	df=pd.DataFrame(data=arrange);
	if (origin!=ALL):
		df=pd.DataFrame(df[df['Origin']==origin]);
	if (company!=ALL):
		df=pd.DataFrame(df[df['Company']==company]);
	if (year!=ALL):
		df=pd.DataFrame(df[df['Year']==year]);
	if (model!=ALL):
		df=pd.DataFrame(df[df['Model']==model]);
	
	#show dataframe
	with Content:
		display(df);
	#delete previous output
	box.close();
	#regenerate display
	box=boxWidget();
	display(box);
	

#Load data from seaborn predefined data
data=sns.load_dataset("mpg");

### Processing data to present it

#convert miles per gallon to Kilometers per litre
data["Km_per_litre"]=data["mpg"]*mpgToKMPL; #constant to convert

#take companies' names to uppercase
data["company"]=[f.split(" ")[0].upper() for f in data["name"] ];
data["Company"]=[ (f if f!="TOYOUTA" else "TOYOTA") for f in data["company"] ];

#also model, and take company name as model when it is empty
data["Model"]=[" ".join(f.split(" ")[1:]).upper() for f in data["name"]];
data["Model"]=[ 
					(
						str(data["Model"][n]).upper()
						if len(str(data["Model"][n]).strip())!=0 
						else str(data["Company"][n]).upper()
						) for n in range(0,len(data["Model"])) ];

#acceleration to international measures
data["From_0_to_96km_per_h_in_secs"]=data["acceleration"];# 0-96km in n seconds

#year with 4 digits
data["Year"]=[str(f+yearBase) for f in data["model_year"]];#to 4-digit year
#origin to uppercase
data["From"]=[ str(f).upper() for f in data["origin"]];
data["Origin"]=data["From"];
#just change name
data["Power"]=data["horsepower"];
#capitalize title and commonwealth writting style
data["Cylindres"]=data["cylinders"];
#convert weight to international measures
data["Weight_Kg"]=data["weight"]*lbsToKG;
data["Weight"]=data["Weight_Kg"];
#just rename 
data["Displacement_mm"]=data["displacement"];

arrange=data[
				[
					"Origin",
					"Company",
					"Model",
					"Year",
					"Cylindres",
					"Weight",
					"Power",
					"From_0_to_96km_per_h_in_secs",
					"Km_per_litre",
					"Displacement_mm"
					]];


#Filter categories to make the drop downs' widgets, and add ALL option
 
origins=[ALL]+[f.upper() for f in list(set(arrange["Origin"]))];
origins.sort();

companies=[ALL]+[f.upper() for f in list(set(arrange["Company"]))];
companies.sort();

years=[str(f) for f in list(set(data["Year"]))];
years.sort();
years=[ALL]+years;

models=[ALL]+[str(f) for f in list(set(data["Model"]))];
models.sort();






#### LAYOUT


#row0
labSelect=widgets.Label("Select your criteria and press Search or Reset",align="center");
labSelect.layout.margin=defSep+auto+defSep+"100px ";
labSelect.layout.height=defHeight;
labSelect.layout.width="75%";
row0=widgets.HBox(children=(labSelect,),layout=widgets.Layout(margin="0 0 0 22px"));

#row1
labOrigins=widgets.Label("Origin:");
labOrigins.layout.width="150px";
dropdown_Origins=widgets.Dropdown(options=origins);
row1=widgets.HBox(children=tuple([labOrigins,dropdown_Origins]),layout=widgets.Layout(margin="0 0 0 22px"));

#row2
labCompanies=widgets.Label("Company:");
labCompanies.layout.width="150px";

dropdown_Companies=widgets.Dropdown(options=companies);
row2=widgets.HBox(children=tuple([labCompanies,dropdown_Companies]),layout=widgets.Layout(margin="0 0 0 22px"));

#row3
labYears=widgets.Label("Year:");
labYears.layout.width="150px";
dropdown_Years=widgets.Dropdown(options=years);
row3=widgets.HBox(children=tuple([labYears,dropdown_Years]),layout=widgets.Layout(margin="0 0 0 22px"));


#row4
labModels=widgets.Label("Model:");
labModels.layout.width="150px";

dropdown_Models=widgets.Dropdown(options=models);
row4=widgets.HBox(children=tuple([labModels,dropdown_Models]),layout=widgets.Layout(margin="0 0 0 22px"));

#rowBottom

butSearch=widgets.Button(description="Search",button_style="success");#info,success, warning, danger
butSearch.layout.margin=defSep+auto+defSep+auto;
butSearch.layout.height=defHeight;
butSearch.layout.width="33%";

butReset=widgets.Button(description="Reset",button_style="warning");#success, warning, danger
butReset.layout.margin=defSep+auto+defSep+auto;
butReset.layout.height=defHeight;
butReset.layout.width="33%";
rowBottom=widgets.HBox(children=tuple([butSearch,butReset]),layout=widgets.Layout(margin="0 0 0 22px"));


#List of dropdows to reset it later
drops=[dropdown_Origins,dropdown_Companies,dropdown_Years,dropdown_Models];

#set drops height
for f in drops:
    f.layout.height=defHeight;


#Set events onClick to buttons
butSearch.on_click(filterHandler);
butReset.on_click(resetHandler);

#Allow to show all the rows of a dataFrame
pd.set_option("display.max_rows", None);
#set dataFrame df
df=pd.DataFrame(data=arrange);

#add style to the page, with scroll allowed on y, without max-width
HTML(style);

#Create a container to the Content
Content=contentWidget();

with Content:
	display(df[df["Origin"]=="CANADA"]);#There is no data with CANADA 
	#origin, so it will show only dataframe's header

#create box with the rows
box=boxWidget();

#show it
display(box);


### Press Run to watch it working 
