# Get All Queries Endpoint

**Endpoint:** `/get_all_queries`

**Method:** `GET`

**Response:** 

- A JSON object containing all queries.
- HTTP status code 200

**Description:** 

This endpoint returns all queries from Firebase when accessed with a GET request.

```json
"Date": Date {
    "Unique Query Identifier": {
        "arrivalAirport": String,
        "departureAirport": String,
        "departureDate": String,
        "queryDate": String,
        "userEmail": String
    }
}
```

## Example

### Request
```http
GET /get_all_queries
```

### Response
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
