# Price Alert

## Overview

The system allows for the user to set a target price and send an alert in the form of a mail when target is reached.

## Setup

1. **Create a `.env` file locally:**

   Create a `.env` file in the root directory of the project and add the following parameters:

   ```env
   POSTGRES_DB=<your_postgres_db_name>
   POSTGRES_USER=<your_postgres_user>
   POSTGRES_DB_PASSWORD=<your_postgres_password>
   EMAIL_HOST=<your_email_host>
   EMAIL_PORT=<your_email_port>
   EMAIL_HOST_USER=<your_email_host_user>
   EMAIL_HOST_PASSWORD=<your_email_host_password>
   DJANGO_SETTINGS_MODULE=pricealert.settings
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

2. **Run the project using Docker Compose:**

   Execute the following command to build and start the Docker containers:

   ```sh
   docker-compose up --build
   ```

   This command will set up the PostgreSQL database, Django application, Celery workers, and Redis service.

## Endpoints

### User Registration and Authentication

- **Register User:**
  - **URL:** `/register`
  - **Method:** `POST`
  - **Description:** Registers a new user.
  
- **Obtain Token:**
  - **URL:** `/token`
  - **Method:** `POST`
  - **Description:** Obtain JWT token.

- **Refresh Token:**
  - **URL:** `/token/refresh`
  - **Method:** `POST`
  - **Description:** Refresh JWT token.

- **User Details:**
  - **URL:** `/user`
  - **Method:** `GET`
  - **Description:** Retrieve user details.
  - **Authentication:** Required

### Alerts Management

- **Create Alert:**
  - **URL:** `/alerts/create`
  - **Method:** `POST`
  - **Description:** Creates a new alert.
  - **Authentication:** Required

- **Delete Alert:**
  - **URL:** `/alerts/delete/<int:pk>`
  - **Method:** `DELETE`
  - **Description:** Deletes an alert by its ID.
  - **Authentication:** Required

- **Fetch Alerts:**
  - **URL:** `/alerts/`
  - **Method:** `GET`
  - **Description:** Retrieve a list of alerts for the authenticated user.
  - **Authentication:** Required

## Solution for Sending Alerts

   The WebSocket continuously fetches real-time price data and stores it in Redis.
   Celery Beat runs every minute to trigger a Celery worker that checks whether the price has reached or exceeded the user-defined target price.
   If the target price condition is met, the system:
   - Updates the alert status to "triggered".
   - Sends an email notification to the user using Django's `send_mail` function.

   The email content includes details about the triggered alert and the current price.


## Project Structure and Architecture

1. **Django Application:**

   - It defines the database schema using Django's ORM, Handles HTTP requests and returns responses and Converts querysets and model instances to Python datatypes that can be rendered into json.

2. **Celery:**

   - It performs background tasks that can be executed asynchronously. Here the task is `process_alerts` which checks if the target price has been reached and sends an email if the condition is met.
   - Celery Beat is a scheduler that triggers tasks at regular intervals. It runs the `process_alerts` task every minute.

3. **Redis:**

   - Redis acts as the message broker for Celery, handling the messaging between the Django application and the Celery workers.
   - It also stores real-time price data fetched via WebSocket.

4. **PostgreSQL:**

   - Stores user data and alert information. Managed using Django's ORM for seamless interaction with the Django application.

5. **WebSocket Fetcher:**

   - A script that connects to a WebSocket to fetch real-time price data and stores it in Redis for quick access by the Celery tasks.

6. **Email Sending:**

   - Emails are sent using Django's `send_mail` function, which is configured via environment variables in the `.env` file.

7. **Docker:**

   - Manages multi-container Docker applications, setting up the PostgreSQL database, Django application, Celery workers, and Redis service.