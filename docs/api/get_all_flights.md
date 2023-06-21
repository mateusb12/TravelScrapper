# Get All Flights Query

**Endpoint:** `/graphql`

**Method:** `POST`

**Request:**

- A GraphQL query in the request body

**Response:** 

- A JSON object containing the requested fields
- HTTP status code 200

**Description:** 

This query returns a list of all flights. A successful response returns a `200 OK` HTTP status code along with a JSON object. The structure of the JSON object depends on the requested fields in the GraphQL query.

In GraphQL, the client specifies the needed fields in the request. The structure of the response will mirror the structure of the request. This differs from REST where the structure of the response is determined by the server.

## Example

### Request
In GraphQL, you make requests by sending a POST request with a JSON object that contains your query. For example, to get all flights with their airlines, arrival airport, and arrival time, you'd send this request:

```http
POST /graphql
Content-Type: application/json

{
  "query": "
    {
      allFlights {
        airlines
        arrivalAirport
        arrivalTime
      }
    }
  "
}
```

### Response
The response will be a JSON object with the same structure as the request:

```json
{
  "data": {
    "allFlights": [
      {
        "airlines": [
          "AD"
        ],
        "arrivalAirport": "GIG",
        "arrivalTime": "2023-02-07T18:45:00.000Z"
      },
      // more flights...
    ]
  }
}
```

To get all fields, simply include all fields in your query. Note that in GraphQL, you don't need to send separate requests to different endpoints to get different types of data. You can get all the data you need in a single request by including all the fields you need in your query. For example:

```http
POST /graphql
Content-Type: application/json

{
  "query": "
    {
      allFlights {
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
    }
  "
}
```
