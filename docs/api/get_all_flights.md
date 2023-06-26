## Flight Price Monitor API

This API provides a GraphQL endpoint at `POST /graphql` that lets you query flight information. The API can provide details about flights, including their airlines, arrival and departure times, and prices.

### GraphQL Endpoint

Send a `POST` request to the `/graphql` endpoint with a JSON object in the body. The JSON object should have a `query` key. The `query` key's value should be a string containing a GraphQL query.

#### Example Request:

```http
POST /graphql
Content-Type: application/json

{
  "query": "
    query {
      allFlights(page: 1, size: 10) {
        flights {
          arrivalAirport
          departureAirport
          price
          numberOfStops
          queryDate
        }
        total
      }
    }
  "
}
```

#### Example Response:

```json
{
  "data": {
    "allFlights": {
      "flights": [
        {
          "arrivalAirport": "GIG",
          "departureAirport": "FOR",
          "price": 114.0,
          "numberOfStops": 2,
          "queryDate": "01 January 2023"
        }
        // more flights...
      ],
      "total": 100
    }
  }
}
```

### Querying All Fields

To query all fields for flights, include all field names in your query.

#### Example Request Querying All Fields:

```http
POST /graphql
Content-Type: application/json

{
  "query": "
    query {
      allFlights(page: 1, size: 10) {
        flights {
          airlines
          arrivalAirport
          arrivalFormattedDateAndTime
          arrivalTime
          arrivalTimeUtc
          departureAirport
          departureFormattedDateAndTime
          departureTime
          departureTimeUtc
          flightDuration
          layoverDurations
          link
          luggageLimits {
            handHeight
            handLength
            handWeight
            handWidth
            holdDimensionsSum
            holdHeight
            holdLength
            holdWeight
            holdWidth
            personalItemHeight
            personalItemLength
            personalItemWeight
            personalItemWidth
          }
          luggagePrice
          numberOfStops
          price
          quality
          queryDate
          remainingSeats
          userEmail
          uniqueId
        }
        total
      }
    }
  "
}
```

### Error Responses

If there is an error with your request, the server will respond with a JSON object containing an `errors` array. Each error object in the array has a `message` key.

#### Example Error Response:

```json
{
  "errors": [
    {
      "message": "<error_message>"
    }
  ]
}
```

The status code for an unsuccessful request is usually `400`, but may vary depending on the error.