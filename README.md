# Airbnb Clone Backend

Welcome to the Airbnb Clone Backend repository! This project is a backend clone of the popular accommodation booking platform, Airbnb. It's built using Python and Flask, focusing on replicating the core functionalities of Airbnb's backend services.

## Overview

The backend of this Airbnb clone is designed to handle various functionalities such as user management, property listings, bookings, and reviews. It aims to provide a solid foundation for a full-stack application by ensuring efficient data handling and API services.

## Features

- **User Authentication and Authorization:** Securely manage user registrations, logins, and access controls.
- **Property Listings:** Allow users to list, update, and remove properties.
- **Bookings:** Enable users to book accommodations, manage bookings, and view booking history.
- **Reviews:** Support for users to leave reviews on properties they have stayed in.

## Technologies

- **Python:** A powerful programming language that emphasizes readability and efficiency.
- **Flask:** A lightweight WSGI web application framework in Python, perfect for building scalable web apps quickly.
- **SQLAlchemy:** An SQL toolkit and Object-Relational Mapping (ORM) library for Python, facilitating database operations.

## What’s Cooking in Part 1?
Sketching with UML: You’ll kick things off by drawing out the backbone of our application using UML (Unified Modeling Language). Think of it like creating the architectural blueprint for a building. It’s where you decide how your classes and components will interact.
Testing Our Logic: After setting up our blueprint, it’s time to make sure everything works as planned. You’ll create tests for the API and business logic. It’s like making sure all the gears turn smoothly in a machine.
Building the API: Now, for the real deal - implementing the API. This is where your blueprint comes to life. You’ll use Flask to create an API that plays well with our business logic and file-based persistence (for now).
File-Based Data Storage: We’re starting simple with a file-based system for storing our data. Choose your format – text, JSON, XML – you name it. Keep in mind that we’ll shift to a database later, so build it smart!
Packaging with Docker: Finally, you’ll wrap everything up in a neat Docker image. It’s like packing your app in a container that can be easily moved and deployed anywhere.

## The Three Layers of Our API Cake:
Services Layer: This is where our API greets the world. It handles all the requests and responses.
Business Logic Layer: The brain of the operation. This is where all the processing and decision-making happens.
Persistence Layer: For now, it’s our humble file system, but we’ll graduate to a database in the future.

## The Data Model: Key Entities
Places: These are the heart of our app. Each place (like a house, apartment, or room) has characteristics like name, description, address, city, latitude, longitude, host, number of rooms, bathrooms, price per night, max guests, amenities, and reviews.
Users: Users are either owners (hosts) or reviewers (commenters) of places. They have attributes like email, password, first name, and last name. A user can be a host for multiple places and can also write reviews for places they don’t own.
Reviews: Represent user feedback and ratings for a place. This is where users share their experiences.
Amenities: These are features of places, like Wi-Fi, pools, etc. Users can pick from a catalog or add new ones.
Country and City: Every place is tied to a city, and each city belongs to a country. This is important for categorizing and searching places.

## Business Logic: Rules to Live By
Unique Users: Each user is unique and identified by their email.
One Host per Place: Every place must have exactly one host.
Flexible Hosting: A user can host multiple places or none at all.
Open Reviewing: Users can write reviews for places they don’t own.
Amenity Options: Places can have multiple amenities from a catalog, and users can add new ones.
City-Country Structure: A place belongs to a city, cities belong to countries, and a country can have multiple cities.

As you design and implement these features, remember that our application will grow. The choices you make now should allow for easy additions and changes later, especially when we switch from file-based to database storage.

In our pursuit of creating a robust and efficient application, it’s crucial that every entity in our data model, except for Country includes the following attributes.:

- Unique ID (UUID4): Every object - whether it’s a Place, User, Review, Amenity or City - must have a unique identifier. This ID should be generated using UUID4 to ensure global uniqueness. This is critical for identifying and managing entities across our application consistently.
- Creation Date (created_at): This attribute will record the date and time when an object is created. It’s vital for tracking the lifespan of our data and understanding the usage patterns.
- Update Date (updated_at): Similarly, each object should have an attribute to record the last update made. This helps in maintaining the historical accuracy of our data and is essential for any modifications or audit trails.

## Why These Attributes Matter?

- Uniqueness: The UUID4 ensures that each entity is distinct, eliminating any confusion or overlap, especially crucial when we scale up.
- Traceability: With created_at and updated_at, we can track the lifecycle of each entity, which is invaluable for debugging, auditing, and understanding user interactions over time.

When designing your classes and database schemas (in the later stages), make sure these attributes are included as a standard part of every entity.

Utilize Python’s uuid module to generate UUID4 ids.

Leverage Python’s datetime module to record timestamps for creation and updates.

## Authors
- Victor Colon
- Oscar Rapale
- Christian Diaz

