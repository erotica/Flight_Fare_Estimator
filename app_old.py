# from calendar import weekday
# from ntpath import join
import streamlit as st
import datetime
# import time
# import sklearn
import pickle
import pandas as pd

# Load the model
pickled_file = open("ModelFlight.pkl", "rb")
model = pickle.load(pickled_file)

st.title(" ✈ Flight Fare Estimator")

st.subheader("Get to know your flight fare for travel with help of Machine Learning")

c1,c2 = st.columns(2)
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
    st.error("Arrival and Destination Cannot be Same.")
if dep_date > arr_date:
    st.error("Please Select Correct Arrival Date, It Must be Greater than Departure Date.")


if st.button("Show Fare . . . . . . .     🛩️"):
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
    predicted_fare = model.predict(X)    
    

    st.subheader("Estimated fare for your Journey is: **RS.{}**".format(int(round(predicted_fare[0],0))))
else:
    st.write("Click to estimate the fare for your trip.")
