# Brevet time calculator service

Simple listing service for data stored in MongoDB database, built upon on a previous project.  

## Functionality that have been added

* Designed RESTful service to expose what is stored in MongoDB. The following three basic APIs are implemented:
    * `http://<host:port>/listAll`  returns all open and close times in the database
    * `http://<host:port>/listOpenOnly` returns open times only
    * `http://<host:port>/listCloseOnly` returns close times only

* Designed two different representations: one in csv and one in json. JSON is default representation. 
    * `http://<host:port>/listAll/csv` returns all open and close times in CSV format
    * `http://<host:port>/listOpenOnly/csv` returns open times only in CSV format
    * `http://<host:port>/listCloseOnly/csv` returns close times only in CSV format

    * `http://<host:port>/listAll/json` returns all open and close times in JSON format
    * `http://<host:port>/listOpenOnly/json` returns open times only in JSON format
    * `http://<host:port>/listCloseOnly/json` returns close times only in JSON format

* Designed a query parameter to get top "k" open and close times.
    * `http://<host:port>/listOpenOnly/csv?top=3` returns top 3 open times only (in ascending order) in CSV format 
    * `http://<host:port>/listOpenOnly/json?top=5` returns top 5 open times only (in ascending order) in JSON format
    * `http://<host:port>/listCloseOnly/csv?top=6` returns top 6 close times only (in ascending order) in CSV format
    * `http://<host:port>/listCloseOnly/json?top=4` returns top 4 close times only (in ascending order) in JSON format
   
* A consumer program has been made to use the service that have been exposed.
* Note that the data samples are there just for reference and is not exactly what is returned.


# Installation and Usage Documentation
1. To begin with, make sure to download docker for your machine [Mac](https://docs.docker.com/docker-for-mac/install/) or [Windows](https://docs.docker.com/docker-for-windows/install/#download-docker-for-windows) and follow the instructions provided in these links.
2. To install, download or clone this repo with `git clone https://Abduarraheem@bitbucket.org/Abduarraheem/proj6-rest.git`  
3. After installing docker and downloading the repo, navigate to the DockerRestAPI directory of the repo and build the flask app using  
`docker-compose build`  
`docker-compose up`
4. Launch `http://localhost:5100/` using a web browser and check out the brevet time calculator.  
`docker-compose down`  

# Submit and Display
There are two buttons one which is submit, which saves the entries of the table to the database, display which displays the entries save in database. Do note that if you attempt to save the table while it is empty an error message will appear notfiying you that there must be some entries in the table, if you try to display while the database is empty an error message will appear, do note that for the display error message or the table, they may take some time to appear if the database is not fully loaded.   
# Specification of the brevet controle time and calculation rules.
The algorithm for calculating controle times is based of the [ACP Brevet Control Times Calculator](https://rusa.org/pages/acp-brevet-control-times-calculator).

The table below gives the minimum and maximum speeds for ACP brevets.

| Control location (km) | Minimum Speed (km/hr) | Maximum Speed (km/hr) | 
| ----------- | ----------- | ----------- |
| 0 - 200     | 15       	| 34
| 200 - 400   | 15       	| 32
| 400 - 600   | 15       	| 30
| 600 - 1000  | 11.428     	| 28
| 1000 - 1300 | 13.333      | 26 


## Rules 
The time limit for every brevet is dependant on the distance, hence the time limit for 200 km brevet is 13 hours 30 minutes, 300 km brevet is 20 hours, 
400 km brevet is 27 hours, 600 km brevet is 40 hours, 1000 km is 75 hours.  
Another thing that is worth noting is that in this implementation of the brevet time calulator we omit the French oddity and controle points in 1000km brevets are allowed, 
control points that are 20% beyond the brevet location are considered invalid and you will be required to provide the correct control location.   
These rules are based of the project specifications and the rules provided [here](https://rusa.org/pages/rulesForRiders). Do note that the French oddity is not accounted for.  
  
The calculator changes the units of miles to kilometers and shortens the outcome to the closest kilometer prior to being utilized in calculation.  
To calculate the opening times and closing times we use the table provided.  
For example consider a 200km brevet with controls every 50km with the finsh being at 205km.  
## Opening Time
The controls locations are every 50kms (500, 100 and 150) is in between the range of 0-200 meaning that we will use the maximum speed of 34km/hr.  
50/34 = 1H28  
100/34 = 2H56  
150/34 = 4H25  
200/34 = 5H53  
Even though the final destination was longer (205km) we still use the distance of 200km in our calculation.  
## Closing Time
The minimum speed used here is 15km/hr.  
50/15 = 3H20  
100/15 = 6H40  
150/15 = 10H00  
200/15 = 13H30  
Using the rules the time limit for the 200km brevet is 13H30, despite the fact that by the calculation, 200/15 = 13H20. Once again even though or final destination is slightly longer than 200km is irrelevant.  

Here is another example to clear some common misunderstanding when we have a 600km brevet.  
Suppose that there are controls every 100 km with the overall distance being 650km.
One thing that confuses people is what rows of tables are going to be used is it the 400-600 or 600-1000.  
We use the first three rows of the table meaning that for controls in the range of 0-200 km we use the first row and the second row for controls at 200-400 and the third row for control at 400-600 km.  
## Opening Time
For the control at 200 we have 200/34 = 5H53, for control at 300, 200/34 + 100/32 = 9H and for control at 500, 200/34 + 200/32 + 100/30 = 15H28.
## Closing Time
Since the minimum speed for the first 600km is 15 km/hr. So the control at 300 will have a closing time of 300/15 = 20H and a control at 500 has a closing time of 500/15 = 33H20.  
And the overall time limit is 600/15 40H00. Once again the fact that the final control point is slight longer than 600km is irrelevant.   

If there are any questions feel free to contact me at elfandi.a23@gmail.com.
