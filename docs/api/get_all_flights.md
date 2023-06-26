## Contract

### Request

- **Endpoint:** `POST /graphql`
- **Headers:**
    - `Content-Type: application/json`
- **Body:** A JSON object with a `query` key. The `query` key's value should be a string containing a GraphQL query.

The GraphQL query should have the following format:

```graphql
query {
  allFlights(page: <page_number>, size: <page_size>) {
    flights {
      <field_name_1>
      <field_name_2>
    ...
    <field_name_n> {
    }
    total {
    }
  }
```
Replace `<page_number>`, `<page_size>`, and `<field_name_n>` with appropriate values.

### Response

- A JSON object with a `data` key. The `data` key's value is another JSON object with an `allFlights` key. The `allFlights` key's value is an object with the following keys:
    - `flights`: An array of objects. Each object has the fields specified in the GraphQL query.
    - `total`: An integer representing the total number of flights.

The status code for a successful request is `200`. 

### Errors

Errors are returned as a JSON object with an `errors` key. The `errors` key's value is an array of error objects.
Each error object has a `message` key.

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

## Request Example

### Request

In order to get all flights with their arrival airport, departure airport, price, number of stops and query date,
you would need send the following request:

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

### Response

The response would be a JSON object with the same structure as the request:

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

To get all fields, simply include all fields in your query. For example:

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


