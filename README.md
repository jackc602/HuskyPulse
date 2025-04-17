# HuskyPulse

This is an application developed by Shrey Sahni, Yuansi Jiang, Elton Neman, and Jack Carroll.

## App Details

The issue we are trying to resolve is the lack of a centralized platform for all of Northeastern's amazing student organizations to share all of their events and programs on. HuskyPulse is meant as a one stop shop for both students and clubs to be able to interact and exchange information, to run all of these groups as effciently as possible. We have implemented a lightweight frontend using python and streamlit, as well as a REST API using flask connecting the frontend to a MySQL database. The program is run entirely within docker containers. While this is not a complete piece of software, the foundation we have built encapsulates many of the essential capabilities for this platform, and hopefully one day HuskyPulse will benifit many Northeastern students.

## [Video Demo](https://drive.google.com/file/d/1u3LwrY58f7rSUai8FowW2fwv5YLcyWpR/view)

## Features

Our app is structured around 4 different user personas, a club leader, a student, a system administrator, and an analyst. 

### Persona 1 - Club Leader
- Make a post and display to either club members or the general public
- Schedule club events and convey this information to attendees
- Allow leaders to track RSVPs to their events
- Edit events and posts
- Receive applications to the club and notify applicants

### Persona 2 - Student
- View upcoming posts and events
- Search through clubs by name and by interests
- Apply to clubs that are interesting and hear back on the status of my application
- RSVP to events I am intested in
- Leave comments on posts

### Persona 3 - Administrator
- Monitor information of clubs and students
- Receive feedback on the site from clubs and students
- Assign user roles
- Create database backups

### Persona 4 - Analyst
- Receive data driven insights about how clubs are functioning
- Monitor booking quanitities
- View where club demands are shifting


## How to Run
1. Clone repository locally
2. Rename ".env.template" to ".env" and input custom password and key
3. Ensure docker is installed, then in command line run "docker compose up --build"
4. Go to "localhost:8501" in your browser
