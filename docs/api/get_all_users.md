# Get All Users Endpoint

**Endpoint:** `/get_all_users`

**Method:** `GET`

**Response:** 

- A JSON object containing all users, each with the following details:
    - `displayName`
    - `email`
    - `phoneNumber`
    - `uniqueId`
- HTTP status code 200

**Description:** 

This endpoint returns all users from Firebase when accessed with a GET request. Each user object includes the display name, email, phone number, and a unique identifier.
