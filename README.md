# RunTrack Training Log Web Application

## Overview
RunTrack is a simple app to log and track your running activities, designed for all users. Record your distance, duration, location, and we’ll track your progress to see how far you've come. Whether you’re training for a race or just enjoying a casual jog, RunTrack keeps every step of your journey in one place.

## Features
- Create a user account
    - Choose username and password
    - Login with your credentials
- Log your running activities
    - Use New Activity button to create a new activity.
    - Click 'edit' on an activity to make modifications.
- Toggle between imperial and metric unit systems on Training Log page.
- See your weekly, year-to-date, and all-time activity statistics on Training Log page.

## Implementation Details
- Project is deployed on AWS EC2 instance and can be accessed at the following public IPv4 address:
    ```
    3.137.168.206
    ```
- Project was build using Django web framework
- Microservice architecture utilized to implement the following features:
    - Weekly snapshot statistics display
    - YTD activity calculations
    - All-time activity calculations
    - Imperial/metric unit conversion
- This project was done as part of the CS361 (Software Engineering 1) final course project at Oregon State University.

## Screenshots of Application
- Login Page:
![](/screenshots/runtrack_login.png?raw=true)

- Training Log Page
![](/screenshots/runtrack_training_log.png?raw=true)

- About Page
![](/screenshots/runtrack_about.png?raw=true)

- Create New Activity Form
![](/screenshots/runtrack_new_activity.png?raw=true)
