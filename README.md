Program where users can record hikes they've been on, as well as get hike suggestions and view their cumulative hiking stats. Designed to demonstrate the concept of microservices 
(vs as a monolith) interacting with a main program via ZeroMQ sockets. Each main function of the application (detailed below) are running in their own process. The
main program  interacts with these processes programatically vs direct function calls.

Add Hike- users can add either a pre-entered hike or enter the hike's name, distance and elevation gain
Hike Log- users can see the list of all hikes they've entered
Hike Finder- users can receive a suggested hike based on the stats of the hikes in their hike log
View Stats- users can view the number of hikes they've been on, and the cumulative distance and mileage. Users can swap between Imperial and Metric units of measurement
Wishlist- users can add hikes they'd like to go on to their wishlist.
Help- users can choose from a variety of help topics and receive information about that subject.

In its current implementation, the program runs on Localhost and does not store data between runs on the program.

To run: 
5 terminal windows will be needed for each process.

1. From the project's directory, run the command 'flask --app board run --debug' This starts the app. It should be visible on localhost:5000/PORT_NUMBER.
2. python wishlist_service.py
3. python unit_converter.py
4. python suggestion_service.py
5. python help_service.py

Code Citation: suggestion_service.py was authored by Seth Mackovjak (sethm08) as part of a class assignment
