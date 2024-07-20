# MarketMinds

## Overview

designed to help restaurants and cafes monitor and analyze their online reputation across various social media platforms by doing sentiment analysis on reviews using ML models for both English and Arabic (Egyptian dialect). It includes endpoints for user management, brand management, and analytics, and is integrated with PostgreSQL and MongoDB databases.

## Technologies Used

- **FastAPI**: For building the API.
- **PostgreSQL**: For relational database management.
- **MongoDB**: For NoSQL data storage.
- **SQLAlchemy**: For Object-Relational Mapping (ORM).
- **Alembic**: For database migrations.
- **Pydantic**: For data validation and settings management.
- **Postman**: For API testing.


## Functionalities

1. **User Registration and Authentication**
   - The web portal provides user registration functionality for new customers.
   - The system authenticates users logging in.

2. **Adding & Removing Brands**
   - Users can manage their brands by adding new ones and removing existing ones.
  

3. **Adding & Removing Brand Alternative Names**
   - Users can add or remove alternative names for brands, which are used in brand analysis.

4. **View Analytics**
   - Users can analyze their brand's public opinion on multiple social media platforms.
   - The system provides insights into the most frequent words used to describe their products.

5. **Generate Report**
   - Users can generate formal reports about their brand based on analysis results.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- MongoDB

