
# BUILD THE REST API USING HISTORICAL WEATHER DATA WITH PYTHON


#---------------------------------------------------
# Import the libraries 
#---------------------------------------------------

from flask import Flask, render_template
import pandas as pd 

#---------------------------------------------------
# Define app with "__name__"
#---------------------------------------------------

app = Flask("__name__")

#---------------------------------------------------
# Define the Global for stations
#---------------------------------------------------

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']]

#---------------------------------------------------
# Define the rendering
#---------------------------------------------------

#Define function to render home page (title and instruction for user)
@app.route("/")
def home(): 
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")

#Define function for getting dictionary of data (temperature, date, and stations)
def about(station, date): 
    
    #Get the input from different files 
    filename = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'
    
    #Skip the rows and parse the date
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    
    #Rename the columns
    df.rename(columns=lambda x: x.replace(' ', ''), inplace=True)
    
    #Get the temperature date
    temperature = df[df['DATE'] == date]['TG'].squeeze()/10

    return {"station" : station,
            "date": date,
            "temperature" :temperature}
    
    
#Define function to get all data based on the stations number 
@app.route("/api/v1/<station>")
def all_data(station): 
    
    #Get the input from different files 
    filename = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'
    
    #Skip the rows and parse the date
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    
    #Rename the columns
    df.rename(columns=lambda x: x.replace(' ', ''), inplace=True)
    
    #Change to dictionary and each row represent in each dictionary 
    result =df.to_dict(orient='records')
    
    return result
    

#Define yearly
@app.route("/api/v1/yearly/<station>/<year>")
def yearly (station, year):
    #Get the input from different files 
    filename = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'
    
    #Skip the rows and parse the date
    df = pd.read_csv(filename, skiprows=20)
    
    #Rename the columns
    df.rename(columns=lambda x: x.replace(' ', ''), inplace=True)
    
    #Change data type
    df['DATE'] = df['DATE'].astype(str)
    
    #Result 
    result = df[df['DATE'].str.startswith(str(year))].to_dict(orient='records')

    return result



#---------------------------------------------------
# Run the app
#---------------------------------------------------
 
if __name__ == "__main__": 
    app.run(debug=True)