#jgr2722

#!/usr/bin/python
import json
import xmltodict
import logging
import flask
from flask import Flask

app = Flask(__name__)

@app.route('/download-data', methods=['POST'])
def download_data(iss = 'ISS.OEM_J2K_EPH.xml', sightings = 'XMLsightingData_citiesUSA02.xml'):
    """
    Here is where the ISS positional and sighting data is loaded into global variables used later in the flask program.
    Each XML file is converted into a dictionary using xmltodict, and are saved into the variables iss_data and sighting_data.

    return (string):
        Returns if the file uploading process was completed or if an error occured when running the route.
    """
    try:
        global iss_data, sighting_data
        with open(iss, 'r') as f:
            dat = xmltodict.parse(f.read())
        iss_data = dat['ndm']['oem']['body']['segment']['data']['stateVector']
    except FileNotFoundError as a:
        logging.error(a)
        return ("The ISS positional data was not found\n")
    
    try:
        with open(sightings, 'r') as f:
            dat = xmltodict.parse(f.read())
        sighting_data = dat['visible_passes']['visible_pass']
    except FileNotFoundError as a:
        logging.error(a)
        return ("The ISS sighting data was not found\n")
    return ('Data Successfully Downloaded\n')


@app.route('/', methods=['GET'])
def hello_world():
    """
    Here is the default route, which returns infomation needed to run the flask app properly.

    return (string):
        Returns instructions on how to run the flask app properly.
    """
    return """\nProgram successfully ran, but no input route was selected.\n
This program contains two data sets, one that depicts where the International Space Station is located around the world, and data of the ISS being visible in a certain region of the United States.\n\n
To access this information, follow the steps below:\n

1. Load the data using the terminal command:  curl localhost:5023/download-data -X POST\n

(Now use any one of these commands based on the information you want to access)
2. Access epoch data:  curl localhost:5023/epochs\n
3. Access specific epoch data:  curl localhost:5023/epochs/<epoch>\n
4. Access country data:  curl localhost:5023/countries\n
5. Access specific country data:  curl localhost:5023/country/<country>\n
6. Access regions in specifc country data:  curl localhost:5023/country/<country>/regions\n
7. Access specific regional data:  curl localhost:5023/country/<country>/regions/<region>\n
8. Access city data in region:  curl localhost:5023/country/<country>/regions/<region>/cities\n
9. Access city data:  curl localhost:5023/country/<country>/regions/<region>/cities/<city>\n
Each of these routes will return a dictionary of data, and displayed in the terminal.\n"""

@app.route('/epochs', methods=['GET'])
def epochs():
    """
    This route returns all of the epoch data in the ISS position xml file. Each key in the dictionary iss_data
    is checked for its EPOCH data, and all of these are added to a dictionary.
    The function returns this data dictionary to the terminal.

    return (dictionary):
        Returns a dictionary of EPOCH values found in the ISS data.
    """
    try:
        eDict = {}
        a=0
        for i in iss_data:
            eDict['EPOCH '+str(a)]=(i.get('EPOCH'))
            a=a+1
    except NameError as a:
        logging.error(a)
        return("Data variables not defined\n")
    return eDict

@app.route('/epochs/<epoch>', methods=['GET'])
def epochData(epoch):
    """
    This route finds a specific EPOCH in iss_data and adds all of the data at that epoch to a dictionary.
    It finds the X position, Y position, Z position, and dot units for all.

    return (dictionary):
        Contains a dictionary of lists. A list is created in case of repeated epoch values being found, and the function
        would return all of them. 
    """
    try:
        Ldicts=[]
        for i in iss_data:
            if ((i.get('EPOCH')) == ("%s" % (epoch))):      
                eDatDict={"X Units(km)":(i.get('X').get('#text')),"Y Units(km)":(i.get('Y').get('#text')),"Z Units(km)":(i.get('Z').get('#text')),"X_Dot Units(km/s)":(i.get('X_DOT').get('#text')),"Y_Dot Units(km/s)":(i.get('Y_DOT').get('#text')),"Z_Dot Units(km/s)":(i.get('Z_DOT').get('#text'))}
                Ldicts.append(eDatDict)   
        fDict={i.get('EPOCH'): Ldicts}
    except NameError as a:
        logging.error(a)
        return("Data variables not defined\n")
    return fDict

@app.route('/countries', methods=['GET'])
def countries():
    """
    This route finds all of the countries present in sighting_data. Two lists are created,
    one to append all countries in the dictionary sighting_data, and anoter to append unique countries.
    The unique countries are then returned.

    return (dictionary):
        Returns a dictionary of a list, containing each unique country found in the data set.
    """
    try:
        Ldicts=[]
        LdictF=[]
        for i in sighting_data:
            Ldicts.append(i.get('country'))
            for a in Ldicts:
                if a not in LdictF:
                    LdictF.append(a)
        fDict={"Countries": LdictF}
    except NameError as a:
        logging.error(a)
        return("Data variables not defined\n")
    return (fDict)

@app.route('/country/<country>', methods=['GET'])
def countryData(country):
    """
    This route finds all of the data linked to a specific country. This is achieved by matching the country string name to the input name.
    The data is then added to a dictionary, which is then added to a list containing all of the information reported under a specific country.

    return (dictionary):
        Returns the list of dictionaries containing the data associated with a specific country.
    """
    try:
        Ldicts=[]
        for i in sighting_data:
            if ((i.get('country')) == ("%s" % (country))):
                cDatDict={"Region":(i.get('region')),"City":(i.get('city')),"Spacecraft":(i.get('spacecraft')),"Sighting Date":(i.get('sighting_date')),"Duration(minutes)":(i.get('duration_minutes')),"Maximum Elevation":(i.get('max_elevation')),"Entering Location":(i.get('enters')),"Exiting Location":(i.get('exits')),"UTC Offset":(i.get('utc_offset')),"UTC Time":(i.get('utc_time')),"UTC Date":(i.get('utc_date'))}
                Ldicts.append(cDatDict)
        fDict={"%s Data"%(country): Ldicts}
    except NameError as a:
        logging.error(a)
        return("Data variables not defined\n")
    return (fDict)

@app.route('/country/<country>/regions', methods=['GET'])
def countryRegion(country):
    """
    This route finds all of the regions within a certain country. This is achieved the same way as befroe,
    where every region is appended to a list, and then the unique regions are added to a final list.

    retun (dictionary):
        Returns a dictionary of list containing every unique region in a country.
    """
    try:
        Ldicts=[]
        LdictF=[]
        for i in sighting_data:
            if ((i.get('country')) == ("%s" % (country))):
                Ldicts.append(i.get('region'))
                for a in Ldicts:
                    if a not in LdictF:
                        LdictF.append(a)
        fDict={"%s Regions"%(country): LdictF}
    except NameError as a:
        logging.error(a)
        return("Data variables not defined\n")
    return (fDict)

@app.route('/country/<country>/regions/<region>', methods=['GET'])
def countryRegionData(country, region):
    """
    This route finds the collected data within a specific region. The input country and region are used to check the data sets and 
    match them to contain the desired location.
    The data is then added to a dictionary, and that dictionary is added to a list.

    retun (dictionary):
        Returns a dictionary containing a list of dictionary data sets for the specific region entered.
    """
    try:
        Ldicts=[]
        for i in sighting_data:
            if ((i.get('country')) == ("%s" % (country))):
                if ((i.get('region'))==("%s" % (region))):
                    cDatDict={"City":(i.get('city')),"Spacecraft":(i.get('spacecraft')),"Sighting Date":(i.get('sighting_date')),"Duration(minutes)":(i.get('duration_minutes')),"Maximum Elevation":(i.get('max_elevation')),"Entering Location":(i.get('enters')),"Exiting Location":(i.get('exits')),"UTC Offset":(i.get('utc_offset')),"UTC Time":(i.get('utc_time')),"UTC Date":(i.get('utc_date'))}
                    Ldicts.append(cDatDict)
        fDict={"%s %s Data" % (country,region): Ldicts}
    except NameError as a:
        logging.error(a)
        return("Data variables not defined\n")
    return (fDict)

@app.route('/country/<country>/regions/<region>/cities', methods=['GET'])
def countryRegionCity(country, region):
    """
    This route finds the cities found within a specific region entered. If the data matches the entered country and region, all city names
    are gathered and added to a list, and the unique cities are added to a final list.

    return (dictionary):
        Returns a dictionary with a list of cities found in the specific region entered.
    """
    try:
        Ldicts=[]
        LdictsF=[]
        for i in sighting_data:
            if ((i.get('country')) == ("%s" % (country))):
                if ((i.get('region'))==("%s" % (region))):
                    Ldicts.append(i.get('city'))
                    for a in Ldicts:
                        if a not in LdictsF:
                            LdictsF.append(a)
        fDict={"%s %s Cities" % (country,region): LdictsF}
    except NameError as a:
        logging.error(a)
        return("Data variables not defined\n")
    return (fDict)

@app.route('/country/<country>/regions/<region>/cities/<city>', methods=['GET'])
def countryRegionCityData(country, region, city):
    """
    This route finds all the data associated with a specific city. The function checks to see if the country, region and city match any 
    of the data sets, and takes the data of those that match and adds it to a dictionary. This dictionary is then appended to a list.

    return (dictionary):
        Returns a dictionary containing a list of all of the information within the city specified.
    """
    try:
        Ldicts=[]
        for i in sighting_data:
            if ((i.get('country')) == ("%s" % (country))):
                if ((i.get('region'))==("%s" % (region))):
                    if ((i.get('city'))==("%s" % (city))):
                        cityDatDict={"Spacecraft":(i.get('spacecraft')),"Sighting Date":(i.get('sighting_date')),"Duration(minutes)":(i.get('duration_minutes')),"Maximum Elevation":(i.get('max_elevation')),"Entering Location":(i.get('enters')),"Exiting Location":(i.get('exits')),"UTC Offset":(i.get('utc_offset')),"UTC Time":(i.get('utc_time')),"UTC Date":(i.get('utc_date'))}
                        Ldicts.append(cityDatDict)
        fDict={"%s %s %s Data" % (country,region,city): Ldicts}
    except NameError as a:
        logging.error(a)
        return("Data variables not defined\n")
    return (fDict)


# the next statement should usually appear at the bottom of a flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')