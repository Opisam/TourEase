# 🌍 TourEase – Tour & Travel Booking Platform

TourEase is a full-stack web application built with Django that connects customers with tour providers through a streamlined booking request system. The platform enables tour companies to manage listings and bookings while allowing users to discover and request travel experiences بسهولة and efficiently.



##  Features

###  Customer Features

* Browse and search available tour packages
* Filter tours by location, price, duration, and type
* View detailed itineraries and images
* Submit booking requests
* Track booking status (Pending / Approved / Rejected)
* Communicate with tour providers via internal messaging
* Leave reviews and ratings after trips



###  Tour Provider Features

* Create and manage tour packages
* Upload images and detailed itineraries
* Receive and manage booking requests
* Accept or reject customer bookings
* Communicate with customers
* View performance insights (basic dashboard)



###  Admin Features

* Approve or reject tour providers
* Manage tour listings
* Monitor booking activity
* Manage users and platform content



##  Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, Tailwindcss (Django Templates)
* **Database:** SQLite (development) / PostgreSQL (production-ready)
* **Version Control:** Git & GitHub



##  System Architecture

The application follows a typical Django MVC (Model-View-Template) architecture:

* **Models:** Handle database structure (users, tours, bookings, reviews)
* **Views:** Manage business logic and workflows
* **Templates:** Render UI for users



## Core Modules

* User Authentication (Role-based: Customer, Provider, Admin)
* Tour Package Management
* Booking Request System
* Internal Messaging System
* Review & Rating System
* Admin Dashboard

---

## ⚙️ Installation & Setup

### 1. Clone the repository

git clone https://github.com/yourusername/tourease.git
cd tourease


### 2. Create a virtual environment

python -m venv venv


### 3. Activate the virtual environment

**Windows:**


venv\Scripts\activate


**Mac/Linux:**

source venv/bin/activate


### 4. Install dependencies

pip install -r requirements.txt

### 5. Run migrations

python manage.py migrate


### 6. Create a superuser

python manage.py createsuperuser

### 7. Run the development server


python manage.py runserver

##  Default Access

* Admin panel: `http://127.0.0.1:8000/admin/`



##  Future Improvements

* Payment integration
* Mobile app version
* AI-based trip recommendations
* Advanced analytics dashboard


## Note

This project is designed as a scalable SaaS solution for tour and travel businesses, focusing on simplicity, usability, and real-world applicability without reliance on third-party APIs.
