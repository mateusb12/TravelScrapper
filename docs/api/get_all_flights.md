# Get All Queries Endpoint

**Endpoint:** `/get_all_flights`

**Method:** `GET`

**Response:** 

- A JSON object containing all queries.
- HTTP status code 200

**Description:** 

A successful response returns a `200 OK` HTTP status code along with a JSON object. The JSON object structure is as follows:

```json
Date: {
    "Unique Flight Identifier": {
        "airlines": [String],
        "arrivalAirport": String,
        "arrivalFormattedDateAndTime": String,
        "arrivalTime": String,
        "arrivalTimeUtc": String,
        "departureAirport": String,
        "departureFormattedDateAndTime": String,
        "departureTime": String,
        "departureTimeUtc": String,
        "flightDuration": String,
        "layoverDurations": [String],
        "link": String,
        "luggageLimits": {
            "hand_height": Number,
            "hand_length": Number,
            "hand_weight": Number,
            "hand_width": Number,
            "hold_dimensions_sum": Number,
            "hold_height": Number,
            "hold_length": Number,
            "hold_weight": Number,
            "hold_width": Number,
            "personal_item_height": Number,
            "personal_item_length": Number,
            "personal_item_weight": Number,
            "personal_item_width": Number
        },
        "luggagePrice": [String],
        "numberOfStops": Number,
        "price": Number,
        "quality": Number,
        "queryDate": String,
        "remainingSeats": Number,
        "userEmail": String,
        "uniqueId": String
    }
}
```

## Example

### Request
```http
GET /get_all_flights
```

### Response
```json
{
   "01 January 2023":{
      "-NKihnIPT9ZNKSCpSZKn":{
         "airlines":[
            "AD"
         ],
         "arrivalAirport":"GIG",
         "arrivalFormattedDateAndTime":"7th February 2023 at 06:45 PM",
         "arrivalTime":"2023-02-07T18:45:00.000Z",
         "arrivalTimeUtc":"2023-02-07T21:45:00.000Z",
         "departureAirport":"FOR",
         "departureFormattedDateAndTime":"7th February 2023 at 01:05 PM",
         "departureTime":"2023-02-07T13:05:00.000Z",
         "departureTimeUtc":"2023-02-07T16:05:00.000Z",
         "flightDuration":"5h40min",
         "layoverDurations":[
            "0 hours 55 min"
         ],
         "link":"link",
         "luggageLimits":{
            "hand_height":38,
            "hand_length":57,
            "hand_weight":10,
            "hand_width":20,
            "hold_dimensions_sum":158,
            "hold_height":52,
            "hold_length":78,
            "hold_weight":23,
            "hold_width":28,
            "personal_item_height":25,
            "personal_item_length":45,
            "personal_item_weight":2,
            "personal_item_width":20
         },
         "luggagePrice":[
            "1 luggage costs 25.392",
            "2 luggage costs 59.248"
         ],
         "numberOfStops":2,
         "price":114,
         "quality":171.33319,
         "queryDate":"01 January 2023",
         "remainingSeats":5,
         "userEmail":"user@example.com",
         "uniqueId":"-NKihnIPT9ZNKSCpSZKn"
      }
   }
}
```