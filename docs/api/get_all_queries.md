# Get All Queries Endpoint

This endpoint retrieves all flight query records from the Firebase database.

- **Endpoint:** `/get_all_queries`
- **Method:** `GET`

## Contract

### Response

- A JSON object containing all queries.
- HTTP status code 200 for a successful request.

The JSON object has keys representing dates. Each date key's value is an object. This object has keys that are unique query identifiers. Each unique query identifier key's value is an object with the following keys:

- `arrivalAirport`: A string representing the arrival airport.
- `departureAirport`: A string representing the departure airport.
- `departureDate`: A string representing the departure date.
- `queryDate`: A string representing the date when the query was made.
- `userEmail`: A string representing the user's email.

### Example

```json
"Date": {
    "Unique Query Identifier": {
        "arrivalAirport": "Airport",
        "departureAirport": "Airport",
        "departureDate": "Date",
        "queryDate": "Date",
        "userEmail": "Email"
    }
}
```

### Request Example

```http
GET /get_all_queries
```

### Response Example
```json
{
    "-NMK3JNMYjRC9hEbc3Yd": {
        "arrivalAirport": "SAO",
        "departureAirport": "FOR",
        "departureDate": "18 February 2023",
        "queryDate": "21 January 2023",
        "userEmail": "test@test.com"
    }
}

```
