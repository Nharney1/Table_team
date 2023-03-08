# Table_team Senior Design Repository for Team #14

## VISION - Visually Impaired Spatially Interactive Orientation Network 

<p align="justify">
Senior design is at the core of all engineering students' journey through university. When the team pondered what our project's focus should be, we knew one thing: we wanted to make something that could be the spark for future innovation to help others.
</p>

<p align="justify">
The Visually Impaired Spatial Interactive Orientation Network (VISION) is our effort toward this mission. VISION focuses on giving individuals with visual impairments a way to experience the world through playing billiards. With the use of audio arrays, a plethora of sensors,  computer vision (CV), artificial intelligence (AI), and dedicated engineering students, VISION will be able to navigate a user from any given starting point to a calculated shooting location within a game of billiards! This project will open the door for future innovation within this field, and allows for the visually impaired to be able to enjoy billiards in the same way able-bodied individuals can today! VISION is a joint project and works with SCRATCH (team #17) to provide the full user experience!
</p>

<p align="justify">
The VISION team is eager to get to work on the design and implement a truly revolutionary system that will hopefully start a trend toward inclusivity for the visually impaired community! VISION's development is well underway, and we plan to have the project complete by the end of April 2023 for the Senior Design showcase at UCF!
</p>

## VISION Team Members

### Alexander Parady
<p align="justify">
My focus within the project is centered on the navigation system, audio interface, PCB design, and power distribution of the project. 
</p>

### Aaron Crawford
<p align="justify">
Put some cool AI stuff here! 
</p>

### Arsene Tatke
<p align="justify">
My focus within the project is the user localization system. The system was achieved by using 3 Estimote UWB beacons from the company of the same name together with an app designed from the ground-up using Swift and XCode. The beacons allows for an accuracy in the realm of centimeters crucial for determining the user's position at all times around the pool table. The IOS App designed is configured to record distances to the beacons, averaging out over a defined x amounts of seconds and send the distances via MQTT to an online server. From there, a python code is used on the Jetson to pull the data from the online server. Said code also performs 2D or 3D trilateration based on the predefined positions of the beacons on the pool table, and the distances from user to individual beacons to return x,y position of the user in our choosen coordinate system. Code repeats as needed and information is sent to the user guidance system to direct and correct the user to the ideal position for a shot.
</p>

### Noah Harney
<p align="justify">
My focus within the project is the computer vision system, networking with the various subsystem computers, and maintaining the central processing unit. The computer vision system is resposible for detecting which billiard balls are on the table and where the billiard balls are. The CV system relies on the open-source software  OPENCV to meet the projects needs. VISION communicates with various subsystems through wired and wireless communication. I designed and tested many different communication methods such as ethernet, Wi-Fi, and Bluetooth for allowing the subsystems to communicate within the university's strict network. I am also responsible for configuring and maintaining the central processing unit used by VISION. VISION uses an NVIDIA Jetson Nano as the main processor. I installed and modified drivers for Wi-FI/Bluetooth connectivity, set up and maintain the software enviornment, and assist with the processors integration into other subsystems.
</p>

