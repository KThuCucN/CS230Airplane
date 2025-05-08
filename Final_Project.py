'''
Katherine Nguyen did this YIPPEEEE!
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
import streamlit as st
from streamlit import session_state

#initalization
DATA="airports.csv"
R_File=pd.read_csv(DATA,index_col="id")
R_File=R_File.sort_values(['ident','name']) # [DA2] Sorted data based by indentity ID and then name
R_File.dropna(inplace=True) #[DA1] Cleaning the Data
R_File=R_File.drop(columns=["local_code"]) #[DA7]
#This is a silly little prank, please don't be mad :)
check=st.checkbox("I agree to give Katherine ThuCuc Nguyen an A")
if check:
    st.success("Thank you! Enjoy the website!")
else:
    st.warning("Please check box to proceed!")
    st.stop()

#title
st.title("New England AirPorts 🛫✈️")
st.subheader("Locations: MA | CT | RI | NH | VT | ME")
st.image("Python_Airplane.jpg")
click=st.button("Click Me!") #WIDGET ALERT
if click:
    st.write("What sound do airplanes make?")
    st.audio("airplane-sound-67522.mp3")

#Points
lat=list(R_File["latitude_deg"])
long=list(R_File["longitude_deg"])
points=pd.DataFrame({"latitude":lat,"longitude":long}) #[PY5]
points["latitude"] = pd.to_numeric(points["latitude"], errors="coerce")
points["longitude"] = pd.to_numeric(points["longitude"], errors="coerce")
place=st.select_slider("Pick a range", ["First","Second","Third"])#[ST2]
if place=="First":
    points=pd.DataFrame({"latitude":[36.075833],"longitude":[10.438611]})
elif place=="Second":
    points=pd.DataFrame({"latitude":[42.379902],"longitude":[13.3092]})
elif place=="Third":
    points=pd.DataFrame({"latitude":[38.9972],"longitude":[17.0802]})
mock_points = pd.DataFrame({
    "latitude": [42.3601, 42.3744, 42.3656],
    "longitude": [-71.0589, -71.0665, -71.0627]
})
#[MAP]
st.subheader("🎀🎀🎀🎀🎀🎀 Teleport to the point 🎀🎀🎀🎀🎀🎀")
scale=st.slider("Zoom Scale", 0, 20,value=10)

layer = pdk.Layer("ScatterplotLayer",data=points,get_position=["longitude", "latitude"],get_fill_color=[255, 192, 203],get_radius=2000)

deck = pdk.Deck(layers=[layer], initial_view_state=pdk.ViewState(latitude=points["latitude"].mean(),longitude=points["longitude"].mean(),zoom=scale,map_style = 'mapbox://styles/mapbox/satellite-v9'))

st.pydeck_chart(deck)

#[VIz1] Pie Chart
Type_Port=["small_airport","medium_airport","large_airport"]
n=len(R_File) #sample size

st.subheader("🎀🎀🎀🎀🎀🎀 Types of Ports 🎀🎀🎀🎀🎀🎀")
value_counts=R_File["type"].value_counts()
Pie_Size=value_counts/n
Fig1,Ax=plt.subplots(figsize=(8,6))
Ax.pie(Pie_Size,labels=value_counts.index,autopct="%1.1f%%",pctdistance=.75, labeldistance=1.10)
st.pyplot(Fig1)

#Table
st.subheader("🎀🎀🎀🎀🎀 General Information 🎀🎀🎀🎀🎀")
selected=st.multiselect("Type", Type_Port) #[ST1] Multiselect
#[DA4]
if selected:
    filtered_data=R_File[R_File["type"].isin(selected)]
    st.dataframe(filtered_data)
else:
    st.dataframe(R_File)



#Feedback/ WIDGET???
st.write("Did you like this website?")
thumb=st.feedback("thumbs") #[ST3]
if thumb:
    feedback = st.text_input("What was your favorite part?")
    if feedback:
        st.write("Thank you for letting me know!")
elif thumb == 0: #binary code: 1 is thumbs up 0 is thumbs down
    st.warning("What do you mean you dislike my app? No")


#[ST4]sidebar section
def minmax(dataframe):
    return min(dataframe), max(dataframe) #[PY2]
st.sidebar.header("🌟 Elevation Time! ✨")
st.sidebar.subheader("Fun Message")
st.sidebar.write("01010011 01000111 01010110 01110011 01100010 01000111 00111000 01100111 01010110 00110010 00111001 01111001 01100010 01000111 01010001 00111101")
Extreme_Direction = st.sidebar.radio("Would you like to see the minimum or maximum of elevation (ft)?", ["Min", "Max","Avg"])
minmax(R_File["elevation_ft"])
if Extreme_Direction=="Min": #[DA3]
    lowest=min(R_File["elevation_ft"])
    lowest_position = R_File.loc[R_File["elevation_ft"] == lowest]
    who=",".join(lowest_position["name"])
    st.sidebar.write(f"The {Extreme_Direction.lower()} is {lowest} feet by {who}")
elif Extreme_Direction=="Max":
    highest=max(R_File["elevation_ft"])
    highest_position= R_File.loc[R_File["elevation_ft"] == highest]
    who=",".join(highest_position["name"])
    st.sidebar.write(f"The {Extreme_Direction.lower()} is {highest} feet by {who}")
elif Extreme_Direction=="Avg": #[DA9]
    st.sidebar.write(f"The {Extreme_Direction.lower()} is {sum([x for x in R_File['elevation_ft']]) / len([x for x in R_File['elevation_ft']]):.2f} feet") #[PY4] List Comphrension
st.sidebar.write("🎀🎀🎀🎀🎀 Graphs 🎀🎀🎀🎀🎀") #boarder lol
#[VIz2] Bar Graph
#geting the height
elevation_interval={"0-1700":0,"1701-3400":0,"3401-5100":0,"5101-6800":0,"6801-8500":0}
count_elevation={}
for x in R_File["elevation_ft"]:
    if 0 < x < 1700:
        elevation_interval["0-1700"]+=1
    elif 1071<x<3400:
        elevation_interval["1701-3400"]+=1
    elif 3401<x<5100:
        elevation_interval["3401-5100"] += 1
    elif 5101<x<6800:
        elevation_interval["5101-6800"] += 1
    else:
        elevation_interval["6801-8500"] += 1
Elevation_Distrabution=list(elevation_interval.values())
Elevation_Keys=list(elevation_interval.keys())

Fig2, Ax2 = plt.subplots(figsize = (20,10)) #[PY1]
Ax2.barh(Elevation_Keys, Elevation_Distrabution, color =["pink", "green", "yellow","purple","blue"])
plt.title("Elevation Distrabution")
plt.xlabel('Elevation')
plt.ylabel('Height in FT')
st.sidebar.subheader("Elevation Distrabution ")
st.sidebar.pyplot(Fig2)


#[VIz3] SCATTERPLOT
st.sidebar.subheader("\nLatitude and Elevation")
x=R_File["latitude_deg"]
y=R_File["elevation_ft"]
Fig3, Ax3 = plt.subplots()
Ax3.plot(x, y, '*', label="Elevation Data",color="purple")
slope,y_int = np.polyfit(x, y, 1)
Ax3.plot(x, slope*x+y_int, label="Trend Line", color="pink")
st.sidebar.pyplot(Fig3)

st.sidebar.write("🎀🎀🎀🎀 Additional Fun 🎀🎀🎀🎀")


#SELFIEEEE! it's cool.. I think Extra code that wasn't taught in class
#Learnt from youtube video
picture=st.sidebar.camera_input("Snap A Memory!📸✨") #Technically a widget
if picture:
    st.balloons()
    st.sidebar.write("Nice Shot!")
    st.sidebar.image(picture)
    session_state['hehehe']=picture
    jp=st.session_state['hehehe'].name
    with open(jp,"wb") as imageFile:
        imageFile.write(session_state['hehehe'].getbuffer())
    st.sidebar.download_button("Download Image",data=session_state['hehehe'],file_name=jp)




