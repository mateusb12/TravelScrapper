from typing import List

from ariadne import ObjectType, gql, make_executable_schema

from firebase_data.firebase_factory import getFactoryInstance

# Define your ObjectType for Flight
flight = ObjectType("Flight")


# Define resolvers for each field in Flight
@flight.field("airlines")
def resolve_airlines(obj, info):
    return obj.airlines


# ... define rest of the fields for Flight here

# Define Query type
query = ObjectType("Query")


@query.field("allFlights")
def resolve_all_flights(obj, info, page: int = 1, size: int = 10) -> dict:
    factory = getFactoryInstance()
    all_flights = factory.firebase_flights.read_all_flights()
    flightPot = []
    for date, flightData in all_flights.items():
        for uniqueId, singleFlight in flightData.items():
            flightPot.append(singleFlight)

    start = (page - 1) * size
    end = start + size
    flights = flightPot[start:end]

    return {"flights": flights, "total": len(flightPot)}


# Create a dictionary of resolvers
resolvers = [query, flight]

# Define your type_defs
type_defs = gql("""
    type LuggageLimits {
        handHeight: Int
        handLength: Int
        handWeight: Int
        handWidth: Int
        holdDimensionsSum: Int
        holdHeight: Int
        holdLength: Int
        holdWeight: Int
        holdWidth: Int
        personalItemHeight: Int
        personalItemLength: Int
        personalItemWeight: Int
        personalItemWidth: Int
    }

    type Flight {
        airlines: [String]
        arrivalAirport: String
        arrivalFormattedDateAndTime: String
        arrivalTime: String
        arrivalTimeUtc: String
        departureAirport: String
        departureFormattedDateAndTime: String
        departureTime: String
        departureTimeUtc: String
        flightDuration: String
        layoverDurations: [String]
        link: String
        luggageLimits: LuggageLimits
        luggagePrice: [String]
        numberOfStops: Int
        price: Float
        quality: Float
        queryDate: String
        remainingSeats: Int
        userEmail: String
        uniqueId: String
    }
    
    type FlightPage {
        flights: [Flight]
        total: Int
    }


    type Query {
        allFlights(page: Int, size: Int): FlightPage
    }
""")


def __main():
    schema = make_executable_schema(type_defs, resolvers)
    print(schema)
    return


if __name__ == "__main__":
    __main()
