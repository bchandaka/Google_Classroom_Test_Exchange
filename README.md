# Google Classroom Test Exchange
This project was created for my school's Science Olympiad Team in order to allow partners studying together for multiple different events to easily send and receive self-made practice tests.
## The Process
1. Team members submit practice tests and their respective keys for all of their events with a specific filename format
2. Using data in the filename, the user's submitted tests and keys are mapped to the respective partner of each event using the database data
3. When desired, emails can be sent out to all members on the team containing links to view the tests/answer keys from their respective partners for each event.

## Various Services utilized in this project
- Flask Web Framework
  - Used to connect various entities(like the database, API references, etc) into one, cohesive program
- Sqlite Database
  - Holds user info(name, email, events, and event partners)
  - Holds Google Classroom Assignment Info
- Heroku Cloud Platform
  - Allows the application to run autonomously from the cloud
- Google Classroom API
  - Used to access test/key documents submitted to Google Classroom
- Google Drive API
  - Used to share google documents with partners
- Google Sheets API
  - Used to load data into the database from a google sheets document
- Google Pub/Sub API
  - Allows the program to receive instant updates on assignments created/documents submitted to Google Classroom 
  - Depending on the type of message received from Google Pub/Sub, the program can add new assigment info to the database, send an email to correct the filename format of a submitted document, or share the submitted documents at a predefined time.
- Sendgrid Email API
  - Used to send customized emails to users



