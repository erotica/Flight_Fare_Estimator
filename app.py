import streamlit as st
import datetime
from PIL import Image

import pickle
import pandas as pd
import numpy as np
import logging as lg

import inform

# creating a log file
lg.basicConfig(filename="minihac2022scraperlog.log", level = lg.DEBUG, format = '%(levelname)s %(name)s %(asctime)s %(message)s')

# Load the model
lg.info("Loading pickled model")
pickled_file = open("ModelFlight.pkl", "rb")
model = pickle.load(pickled_file)

try:
    tab1, tab2 = st.tabs(["📉 Fare Estimator", "👩🏾‍🔬 About"])
    data = np.random.randn(10, 1)

    tab1.title(inform.Title)

    tab1.subheader(inform.Appinfo)

    lg.info("taking inputs from user")
    c1,c2 = tab1.columns(2)
    source= c1.selectbox("From",["Delhi", "Kolkata", "Banglore", "Mumbai", "Chennai"])
    destination= c2.selectbox("To",["New Delhi","Delhi", "Banglore", "Hyderabad", "Kolkata", "Cochin"])


    dep_date= c1.date_input("Departure date")
    arr_date= c2.date_input("Arrival date",help='Select same or later date')


    dep_time= c1.slider("Departure time",value = (datetime.time()),step= datetime.timedelta(minutes = 5))
    arr_time= c2.slider("Arrival time",value = (datetime.time()),step= datetime.timedelta(minutes = 5))

    # nstops= c1.selectbox("Number of Stops",[0, 1, 2, 3, 4])
    nstops=c1.slider("Number of Stops", 1, 4, value = 0,step= 1)
    airline = c2.selectbox("Select Airline",["Jet Airways", "Multiple carriers", "Air India", "Multiple carriers", "SpiceJet","GoAir","IndiGo", "Vistara", "Multiple carriers Premium economy", "Air Asia", "Vistara Premium economy"])

    # warning for certain conditions
    if source == destination:
        tab1.error("Arrival and Destination Cannot be Same.")
        lg.info("Arrival and Destination Cannot be Same. Asking user to change")
    if dep_date > arr_date:
        tab1.error("Please Select Correct Arrival Date, It Must be Greater than Departure Date.")
        lg.info("Error in arrival date, must be greater than departure date. Asking user to change")


    if tab1.button("Show Fare . . . . . . .     🛩️"):
        Total_Stops= pd.DataFrame([nstops])[0][0]
        # print(Total_Stops)
        Journey_Date= int(pd.to_datetime(dep_date, format="%Y-%m-%d").day)
        Journey_Month= int(pd.to_datetime(dep_date, format="%Y-%m-%d").month)
        Dep_Hour= int(pd.to_datetime(dep_time, format="%H:%M:%S").hour)
        Dep_Min= int(pd.to_datetime(dep_time, format="%H:%M:%S").minute)
        Arr_Hour= int(pd.to_datetime(arr_time, format="%H:%M:%S").hour)
        Arr_Min= int(pd.to_datetime(arr_time, format="%H:%M:%S").minute)

        Dep_time= "-".join(([dep_date.isoformat(), dep_time.isoformat()]))
        Dep_time = pd.to_datetime(Dep_time, format="%Y-%m-%d-%H:%M:%S")
        Arr_time= "-".join(([arr_date.isoformat(), arr_time.isoformat()]))
        Arr_time = pd.to_datetime(Arr_time, format="%Y-%m-%d-%H:%M:%S")
        Duration_in_mins= int((Dep_time-Arr_time).total_seconds()/60)

        Airline_one_hot = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], columns=["Airline_Air India", "Airline_GoAir", "Airline_IndiGo", "Airline_Jet Airways", "Airline_Jet Airways Business", "Airline_Multiple carriers", "Airline_Multiple carriers Premium economy", "Airline_SpiceJet", "Airline_Trujet", "Airline_Vistara", "Airline_Vistara Premium economy"])
        selected_airline = "_".join(("Airline", airline))
        if airline != "Air Asia":
            Airline_one_hot[selected_airline][0] = 1

        Source_one_hot = pd.DataFrame([[0, 0, 0, 0, 0]], columns=["Source_Banglore", "Source_Chennai", "Source_Delhi", "Source_Kolkata", "Source_Mumbai"])
        selected_source= "_".join(("Source", source))
        if source != "Banglore":
            Source_one_hot[selected_source][0] = 1

        Destination_one_hot = pd.DataFrame([[0, 0, 0, 0, 0, 0]], columns=[ "Destination_Banglore", "Destination_Cochin", "Destination_Delhi", "Destination_Hyderabad", "Destination_Kolkata", "Destination_New Delhi"])
        selected_destination = "_".join(("Destination", destination))
        if destination != "Banglore":
            Destination_one_hot[selected_destination][0] = 1

        weekday = pd.to_datetime(dep_date, format="%Y-%m-%d").day_name()    

        Weekday_one_hot = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]], columns=["Journey_Day_Friday", "Journey_Day_Monday", "Journey_Day_Saturday", "Journey_Day_Sunday", "Journey_Day_Thursday", "Journey_Day_Tuesday", "Journey_Day_Wednesday"])
        selected_weekday = "_".join(("Journey_Day", weekday))
        # if weekday != "Friday":
        Weekday_one_hot[selected_weekday][0] = 1

        df = pd.DataFrame([[Total_Stops, Journey_Date, Journey_Month,  Dep_Hour, Dep_Min, Arr_Hour, Arr_Min, Duration_in_mins]], columns=["Total_Stops", "Journey_Date", "Journey_Month", "Dep_Hour", "Dep_Min", "Arr_Hour", "Arr_Min", "Duration_in_mins"])

        X = pd.concat([df, Airline_one_hot, Source_one_hot, Destination_one_hot, Weekday_one_hot], axis=1)
        lg.info("Predicting the fare")
        predicted_fare = model.predict(X)    
        

        tab1.subheader(f"{inform.DisplayMsg}**{inform.RupeesSymbol}{int(round(predicted_fare[0],0))}/-**")
        lg.info(f"{inform.DisplayMsg}{inform.RupeesSymbol}{int(round(predicted_fare[0],0))}/-")
    else:
        tab1.write(inform.PageInstruction)

    tab2.title("About")
    tab2.subheader("Shubham Shaah")


    c2_1,c2_2 = tab2.columns([6,1])
    image = Image.open('Shubham.jpeg')

    c2_2.image(image, caption='Shaah_i', width=150)
    c2_1.text(inform.About_Shubham)

    
    tab2.markdown("[![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/Shaah-i)")
    tab2.markdown("[![Linkedin](https://badgen.net/badge/icon/LinkedIn?icon=in&label=in)](https://www.linkedin.com/in/shubham-shaah/)")
    # tab2.markdown("[![Hire Shubham!](https://badgen.net/badge/icon/Hire_Shubham!?&label)](mailto:shubbh9@gmail.com)")

    import webbrowser
    if tab2.button("Hire Shubham!"):
        lg.info("User wants to hire you")
        webbrowser.open_new_tab("mailto:shubbh9@gmail.com")

except Exception as e:
    lg.exception(f"something went wrong: {e}")