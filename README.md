# Hotel Room Booking System

## Overview

This is a Django-based web application designed for hotel room booking. It allows users to register, log in, browse available rooms, filter them by various criteria, and make bookings. The system includes user authentication, room management, and booking history functionalities.

## Features

1. **User Authentication**: Users can register, log in, and log out securely.
2. **Room Browsing**: View all available rooms with details such as capacity, price, and location.
3. **Room Filtering**: Filter rooms by check-in/check-out dates, capacity, and price range.
4. **Booking System**: Authenticated users can book rooms for specific dates, with validation to prevent overlapping bookings.
5. **Booking History**: Users can view their past and upcoming bookings.
6. **Responsive Design**: Templates are designed to work across devices (requires frontend styling).

## Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (default, configurable for other databases)
- **Frontend**: HTML templates with Django's templating engine (extendable with CSS/JS frameworks)
- **Authentication**: Django's built-in authentication system with custom user model
- **Media**: Support for room images via Django's media handling

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/hotel-booking-system.git
   cd hotel-booking-system
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (Optional)**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://localhost:8000`.

## Project Structure

- **booking_system/**: Main project directory with settings and URL configurations.
- **auth_system/**: Handles user authentication (register, login, logout).
- **booking/**: Manages room browsing, booking, and history functionalities.
- **Templates**:
  - `bookingapp/index.html`: Main page with room search and listing.
  - `bookingapp/room_list.html`: Displays all rooms.
  - `bookingapp/booking.html`: Room booking form.
  - `bookingapp/booking_success.html`: Booking confirmation page.
  - `bookingapp/booking_history.html`: User booking history.
  - `bookingapp/about.html`: About page.
  - `auth_system/register.html`: User registration form.
  - `auth_system/login.html`: User login form.

## Models

- **CustomUser**: Extends Django's `AbstractUser` with additional fields (`email`, `phone_number`).
- **Category**: Represents room categories.
- **Room**: Stores room details (number, capacity, location, price, image).
- **Booking**: Tracks user bookings with references to users and rooms.

## URLs

- `/`: Main page with room search.
- `/rooms/`: List of all rooms.
- `/booking/`: Room booking page (requires authentication).
- `/bookings/`: User booking history (requires authentication).
- `/about/`: About page.
- `/register/`: User registration.
- `/login/`: User login.
- `/logout/`: User logout.
- `/admin/`: Django admin panel.

## Usage

1. **Register or Log In**: Create an account or log in to access booking features.
2. **Search Rooms**: Use the main page to filter rooms by dates, capacity, and price.
3. **Book a Room**: Select a room and specify check-in/check-out dates to book.
4. **View Booking History**: Check past and upcoming bookings in the history section.
5. **Admin Access**: Use the admin panel to manage users, rooms, categories, and bookings.

## Future Improvements

- Add frontend styling with CSS frameworks (e.g., Bootstrap, Tailwind).
- Implement pagination for room listings and booking history.
- Add room availability calendar.
- Support multiple languages.
- Integrate payment processing for bookings.
