jgr2722
# **Global Positioning Analysis and Flask Programming**

## **Purpose**
For this problem, we need to analyze ISS data from a xml file and analyze it within a flask web application. Additionally, the entire contents of the program was containerized into a *Docker* image, allowing the program to be run from a terminal window, and a *Makefile* was also created to both create the flask program and run the web application. These challenges are useful skills to learn, because it gets us familiar with using the Docker imaging system, analyzing larger/different types of data sets and familiarizes us with flask web applications.

## **Repository Contents**
In this repository, *(midterm332-JGR2722)*, one program, two .xml data files, a Dockerfile and a Makefile are included along with this README file. The program, **app.py**, is used to create the flask server and analyze the .xml data. The server is initialized, and users can ask for specific data sets, such as the countries in the data set, cities, positioning data and others. These functions use the two data sets, **ISS.OEM_J2K_EPH.xml** and **XMLsightingData_citiesUSA02.xml**. The *ISS* file contains the time and location of the International Space Station, and the *Sighting Data* file contains data of sightings in a certain region of the United States. (Documentation at the end)

The data can be downloaded [here](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq)(under Public Distribution File and the desired XML file), and the data sets were then copied into this repository. This data is then saved to global variables *iss* and *sightings* in the flask *app.py* program using a **POST** function, */download-data*. After running this route, all other **GET** functions can be accessed by the routes described in the default **/** route. Some function examples are **/epochs**,**/countries**,**/epochs/(epoch)**,**/country/(country)/regions/(region)/cities/(city)**, etc. (These functions will be explored below)

 After the program was completed, the necessary files and programs were containerized in a *Docker* image for easy distribution, and a *Makefile* was created to build this image and run all the necessary code to initialize the flask server.

## **Running the files**

Once you are in the correct repository, the first step is to run the **Makefile**. This can be done by simply typing
```ruby
make all
```
This runs the path **all** in the make file, which includes *build and run*. 

**Remember to include your own docker name in the Makefile, so that the docker container is created under your own username.**

**[For reference, ${NAME} means that your own docker username is used for the command. This should be done automatically if you replaced the NAME variable with your docker username.]**

```ruby
build:
	docker image build -t ${NAME}/app:1.0 .
```
```ruby
run:
	docker run --name "ISS-Data-Analysis" -d -p 5023:5000 ${NAME}/app:1.0
```
The makefile removes a few manual steps to run and access the Dockerfile, but steps to properly run the dockerfile will be outlined below (*Dockerfile manual Building and running located below*).

The first path, *build*, creates the docker image **app.py**. The second, *run*, initializes the docker image and starts the flask server.

**Example Output:**
```ruby
 ...
 => => exporting layers                                                                                                                           0.0s
 => => writing image sha256:31d055481be49fd8fe650935af52027bfddbbe03570518e4eb3d28348f4a8a4c                                                      0.0s
 => => naming to docker.io/jwallee/app:1.0                                                                                                        0.0s
docker run --name "ISS-Data-Analysis" -d -p 5023:5000 jwallee/app:1.0
15a5d94b9f9111a0e18aa7c584e73b49033a4743f99a285686b3c61eb2198683
```

With the flask server active within the docker image, all it takes is to access the functions present in the file using a *curl* function. The first step would be to go to the terminal and run:
```ruby
curl localhost:5023/
```
This command returns a long string detailing what functions can be used and what steps that need to be taken in order to properly run the program.

**Example output:**
```
Program succesfully ran, but no input route was selected.

This program contains two data sets, one that depicts where the International Space Station is located around the world, and data of the ISS being visible in a certain region of the United States.


To access this information, follow the steps below:


1. Load the data using the terminal command:  curl localhost:5023/download-data -X POST


(Now use any one of these commands based on the information you want to access)
2. Access epoch data:  curl localhost:5023/epochs

3. Access specific epoch data:  curl localhost:5023/epochs/<epoch>
...etc.
```
## **Initialization**
As the instructions say, the first command that **must** be run is what loads the data into the flask program. Try it now:

**Command:**
```ruby
curl localhost:5023/download-data -X POST
```
---
**Output:**
```ruby
Data Successfully Downloaded
```

If the output matches the one seen above, that means that the data was successfully loaded into the flask app! Now you can choose what data you would like to access from the routes listed before.

## **Functions/Routes**

Let's look at some example routes you can now access. Let's try the first one:
```ruby
curl localhost:5023/epochs
```
This route calls upon the function **epochs()** as seen below:
```ruby
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
```
As the function description says, this route goes through every dictionary in **iss_data** and adds all *EPOCH* values to a dictionary. This dictionary is returned to the terminal.

**Example Output**
```
...
  "EPOCH 991": "2022-045T06:04:00.000Z", 
  "EPOCH 992": "2022-045T06:08:00.000Z", 
  "EPOCH 993": "2022-045T06:12:00.000Z", 
  "EPOCH 994": "2022-045T06:16:00.000Z", 
  "EPOCH 995": "2022-045T06:20:00.000Z", 
  "EPOCH 996": "2022-045T06:24:00.000Z", 
  "EPOCH 997": "2022-045T06:28:00.000Z", 
  "EPOCH 998": "2022-045T06:32:00.000Z", 
  "EPOCH 999": "2022-045T06:36:00.000Z"
}
```
Next we'll look at another example route that can be accessed:
```ruby
curl localhost:5023/country/<country>/regions/<region>/cities/<city>
```
This route calls upon the function **countryRegionCityData()** as seen below:
```ruby
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
```
As this function description says, it finds all city data within a specified country, region and city. It creates a dictionary with all of the found data and returns this list of dictionaries to the terminal.

**Example Input**
```ruby
curl localhost:5023/country/United_States/regions/Florida/cities/New_Smyrna_Beach
```
**Example Output**
```
    ... 
    {
      "Duration(minutes)": "2", 
      "Entering Location": "10 above NW", 
      "Exiting Location": "10 above NNW", 
      "Maximum Elevation": "11", 
      "Sighting Date": "Sun Feb 20/06:27 AM", 
      "Spacecraft": "ISS", 
      "UTC Date": "Feb 20, 2022", 
      "UTC Offset": "-5.0", 
      "UTC Time": "11:27"
    }, 
    {
      "Duration(minutes)": "1", 
      "Entering Location": "17 above NNW", 
      "Exiting Location": "10 above N", 
      "Maximum Elevation": "17", 
      "Sighting Date": "Mon Feb 21/05:41 AM", 
      "Spacecraft": "ISS", 
      "UTC Date": "Feb 21, 2022", 
      "UTC Offset": "-5.0", 
      "UTC Time": "10:41"
    }
  ]
}
```
## **Logging**
Additionally, we can see that each of the programs have a logging component. This is to check and see that the data variables run properly, and any errors can be checked via:
```
docker logs ISS-Data-Analysis
```

## **Manually Setting up the Dockerfile**
In order to easily run this program on any system, a *Dockerfile* was set up to containerize this program. This process was streamlined via the **Makefile**, but outlined below is how to manually run the dockerfile. First, the file **Dockerfile** was set up to load all needed files, inputs and libraries needed to run the program. The dockerfile was set up like this:
```ruby
FROM python:3

RUN apt-get update

WORKDIR /app

RUN pip install pytest==7.0.0

RUN pip install xmltodict==0.12.0

RUN pip install Flask==2.0.3

RUN pip install flask

ADD app.py /app

ADD test_app.py /app

ADD ISS.OEM_J2K_EPH.xml /app

ADD XMLsightingData_citiesUSA02.xml /app

CMD python3 app.py
```
This dockerfile includes **python3** (the coding language used), **pytest** (python program testing tool), **Flask** and **flask** (a Microservice hosting platform) and **xmltodict** (module to convert xml files to dictionaries). Additionally, the programs **app.py** and **test_app.py** and the data sets **ISS.OEM_J2K_EPH.xml** and **XMLsightingData_citiesUSA02.xml** are copied over to the app directory so that the *Dockerfile* can access the programs and files needed.

## **Building the Dockerfile Image**

The next step was to build the *Dockerfile* image. This was done by executing this command:
```ruby
docker image build -t ${NAME}/app:1.0 .
```
This command executes all of the initialization statements in the *Dockerfile* and uploads the image to the Docker Hub.

## **Pulling the Dockerfile Image**

In order to run the *Dockerfile*, the dockerfile image must first be pulled from the Dockerfile Hub. This can be achieved by entering the command:
```ruby
docker pull ${NAME}/app:1.0
```
This pulls the image you just created from the Docker Hub and downloads it to your local device.

You can also download a **pre-containerized image** created by myself by running the command:
```ruby
docker pull jwallee/app:1.0
```

## **Running the Image**

**Now you're ready to run the image!**

With the Image pulled, you can now run the command:
```ruby
docker run --name "ISS-Data-Analysis" -d -p 5023:5000 ${NAME}/app:1.0
```
**NOTE: Make sure the [username] matches the Image downloaded.**

The image should run as expected now.

**Example Command and Output**
```ruby
% docker run --name "ISS-Data-Analysis" -d -p 5023:5000 jwallee/app:1.0

a437973e015cd99e1b5579a292adf0f0409c983c83eef83231fed3ba3cce446f
```
The image is now up and running!

# **If an error appears that says that a container is already active, follow the steps below**
```ruby
docker container stop ISS-Data-Analysis
```
```ruby
docker container rm ISS-Data-Analysis
```
**The container should now be stopped and removed, and the docker run command can now be used again.**

## **Running Tests**

Now with the program successfully running, we can run the pytest file connected in the docker image.

The test file **test_app.py** can be ran by executing the command:

```ruby
python3.10 -m pytest
```
*This is the newest version of python 3.10, but you can use what version you have on your system.*

**Output:**
```ruby
================================================================= test session starts =================================================================
platform darwin -- Python 3.10.2, pytest-7.1.1, pluggy-1.0.0
rootdir: /Users/<Username>/Documents/GitHub/midterm332-jgr2722
collected 10 items                                                                                                                                    

test_app.py ..........                                                                                                                          [100%]

================================================================= 10 passed in 2.21s ==================================================================
```
This result means that the file **test_app.py** ran successfully!

## **Dataset Documentation**
The data used in this program was gathered from [NASA's Open Data Portal](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq).

**Data Description:** *"This data represents the best estimated real-time trajectory and local sightings opportunities for the International Space Station (ISS) as generated by the Trajectory Operations and Planning (TOPO) flight controllers at Johnson Space Center."*

**Publisher:** *TOPO*

**Contact Name:** *Scott Goodwin*

**Contact Email:** *scott.goodwin@nasa.gov*

**Public Access Level:** *public*

**Issued:** *2022-02-13*

**License:** *http://www.usa.gov/publicdomain/label/1.0/*