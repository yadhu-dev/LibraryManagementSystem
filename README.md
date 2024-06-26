# Library Management System

## Overview

The Library Management System (LMS) is designed to streamline and modernize library operations by enabling self-service checkouts and returns of books and other materials. This innovative system leverages RFID technology for identifying library items and an Internet of Things (IoT) infrastructure to communicate with a central server. It enhances user experience, reduces manual workload for library staff, and ensures efficient management of library resources.

## Key Features

- **Self-Service Checkouts and Returns:**
  - Users can check out and return books independently, reducing wait times and improving convenience.
  - The system uses RFID tags attached to library items, which can be scanned quickly and easily.

- **RFID Technology:**
  - Each library item is equipped with an RFID tag containing a unique identifier.
  - An RFID reader integrated with an Arduino board reads these tags to capture the item's details.

- **Standalone Application:**
  - The system connects to the local library for fetching necessary details without the need for online dependancy.
  - This eliminates any connectivity issues like latency and downtime.

- **Central Server Communication:**
  - The software sends HTTP requests to a central server to update the local database with checkout and return information.
  - The flask server handles these requests and manages the local library database which is implemented using mysql.

- **Database Integration:**
  - The server stores information about library items, user transactions, and inventory status.
  - This centralized database ensures that the library can track all items and user activities accurately.

## System Components

- **Arduino Board with RFID Reader:**
  - The heart of the system, responsible for reading RFID tags and sending data to the server.
  - Prepares UID for data mapping and it's only function is to fetch UID from the tags.
  - The board is made to be completely replaceable to avoid much of hardware dependancy.

- **Flask Server:**
  - A lightweight web server that reads the serial data from the micro controller and maps the data with the required UIDs.
  - Manages the database and provides APIs for updating item status.
  - Facilitates data mapping according to UID - Data.

- **RFID Tags:**
  - Attached to each library item, these tags store unique identifiers that can be read by the RFID reader.
  - Enable quick and accurate identification of items during checkouts and returns.

# Modules

## Data Mapping Module

1. **User Interaction:**
   - Users scan their library card (RFID tag) and the items they wish to check out or return.
   - The RFID reader captures the UID from the tag and prints it serially.

2. **Data Transmission:**
   - The serial data is read by the flask backend and printed on the frontend for data mapping.
   - The user can give the roll number that should be mapped to the UID received.
   - On submission, if no duplicates exist, push to the database and show confirmation.

3. **Server Processing:**
   - On receiving the mapped data, sends it to the flask server to store it in the local database.
   - The server sends a response back to the frontend to tell the user that the details has been updated.

## CRUD Module

1. **User Interaction:**
   - A table with all the registered users will be shown on the page loading.
   - The user can tap the RFID tag to search for the data associated with the UID scanned.
   - The user can perform the crud operation required and save changes to the local dataabse.

2. **Server Processing:**
   - On reading the RFID card, the data is sent serially to the backend for filtering the user.
   - The user data associated with the UID can be updated or deleted.
   - The updated data gets sent back to the flask backend to be updated in the local database.

## Keystroke Module

1. **User Interaction:**
   - The user can change the data mapping mode to keystroke mode by clicking the start keystroke button.
   - When this mode is active, the roll no or any number associated with the UID read will be printed on any input field as keystrokes.
   - This is useful for easily fetching the indentifying data through the UID of the tag without manually entering it.

2. **Data Transmission:**
   - The serial data is read by the flask backend and the associated data is fetched.
   - The data is typed on the focused input field as keystrokes for the use case.
   - No data is typed if the UID is not mapped.

3. **Server Processing:**
   - On activating keystroke mode, the data mapping mode ceases temporarily to avoid read clashes.
   - The serial data is read and the associated data is fetched and stored for typing.
   - On finding an input field, the data is typed in string format in the form of keystrokes and presses enter if necessary.

# Installation

  - Run `Installer.bat` as administrator as it installes all the software dependencies and packages required for the program to function.
  - If any super user prompt, click allow since it needs to install python and mysql which requires additional administrative privilages.
  - If installer fails, do the following:

    1. Install python 

# Benefits

- **Efficiency:** Automates the checkout and return process, reducing manual workload and speeding up operations.
- **User Convenience:** Allows users to manage their library transactions independently, enhancing their experience.
- **Accuracy:** Ensures precise tracking of library items, reducing the chances of errors and lost items.
- **Real-Time Updates:** Keeps the library inventory updated in real-time, ensuring accurate availability information.

This Library Management System represents a significant step forward in library automation, leveraging modern technology to improve service delivery and operational efficiency.
