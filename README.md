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

## Workflow

1. **User Interaction:**
   - Users scan their library card (RFID tag) and the items they wish to check out or return.
   - The RFID reader captures the UID from the tag and prints it serially.

2. **Data Transmission:**
   - The Arduino board formats the captured data into an HTTP request.
   - This request is sent over the WiFi network to the central server.

3. **Server Processing:**
   - The server receives the HTTP request and extracts the user and item information.
   - It updates the database to reflect the new status of the items (checked out or returned).

4. **Confirmation:**
   - The server sends a response back to the Arduino board.
   - The Arduino board provides feedback to the user, confirming the successful checkout or return.

## Benefits

- **Efficiency:** Automates the checkout and return process, reducing manual workload and speeding up operations.
- **User Convenience:** Allows users to manage their library transactions independently, enhancing their experience.
- **Accuracy:** Ensures precise tracking of library items, reducing the chances of errors and lost items.
- **Real-Time Updates:** Keeps the library inventory updated in real-time, ensuring accurate availability information.

This Library Management System represents a significant step forward in library automation, leveraging modern technology to improve service delivery and operational efficiency.
