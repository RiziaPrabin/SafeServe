# SafeServe: Hotel Food Safety Monitoring System

**SafeServe** is a comprehensive, database-driven web application designed to reduce food poisoning incidents by improving the monitoring and management of food safety practices in hotels. It provides a transparent and efficient platform for customers, hotel managers, and food safety inspectors to interact, report issues, and track compliance.

The core mission of SafeServe is to build a safer dining community by leveraging technology to bring transparency and accountability to the forefront of the hospitality industry.

## Key Features

SafeServe is built with a role-based access system, providing a unique and tailored experience for each user type.

### For Customers (Public Users)

* **View Hotel Listings:** Browse a list of registered and active hotels, complete with contact details and safety ratings.

* **Submit Feedback:** Provide general feedback about dining experiences at specific hotels.

* **Report Food Poisoning Incidents:** Submit a formal report if a food poisoning incident is suspected. This report is sent directly to an inspector for official review.

* **Track Reported Cases:** View the status and conclusion of the cases they have personally reported, closing the feedback loop.

### For Hotel Managers

* **Secure Login:** Access a dedicated dashboard for their specific hotel.

* **View Inspection History:** See a complete history of all inspections conducted at their establishment.

* **Review Customer Feedback:** Read feedback submitted by customers.

### For Food Safety Inspectors

* **Secure Login:** Access a comprehensive dashboard with administrative and oversight capabilities.

* **Add New Hotels:** Officially register new hotels into the SafeServe system.

* **Manage Food Poisoning Cases:** View all customer-reported food poisoning incidents, investigate them, and update their status and conclusion.

* **Conduct Inspections:** Initiate and submit detailed inspection reports for any hotel in the system.

## Technology Stack

This project is built with a modern and reliable technology stack:

* **Frontend:** HTML5, CSS3, JavaScript 

* **Backend:** Python with the Flask web framework

* **Database:** MySQL

* **Password Hashing:** Bcrypt for secure password storage

## Setup and Installation

To run this project locally, please follow these steps:

**1. Prerequisites:**

* Python 3.x installed

* MySQL Server installed and running

**2. Clone the Repository:**


git clone <your-repository-url>
cd <your-project-directory>


**3. Set Up the Database:**

* Create a database in MySQL named `food_security_db`.

* Run the provided SQL scripts to create all the necessary tables (`hotels`, `inspectors`, `customers`, etc.).

* Ensure your database connection details in `app.py` (host, user, password) match your local MySQL setup.

**4. Run the Application:**


python app.py


The application will be available at `http://127.0.0.1:5000`.
