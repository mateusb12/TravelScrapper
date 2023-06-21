from graphene import ObjectType, String, Int, List, Field, Float


class LuggageLimits(ObjectType):
    hand_height = Int()
    hand_length = Int()
    hand_weight = Int()
    hand_width = Int()
    hold_dimensions_sum = Int()
    hold_height = Int()
    hold_length = Int()
    hold_weight = Int()
    hold_width = Int()
    personal_item_height = Int()
    personal_item_length = Int()
    personal_item_weight = Int()
    personal_item_width = Int()


class Flight(ObjectType):
    airlines = List(String)
    arrivalAirport = String()
    arrivalFormattedDateAndTime = String()
    arrivalTime = String()
    arrivalTimeUtc = String()
    departureAirport = String()
    departureFormattedDateAndTime = String()
    departureTime = String()
    departureTimeUtc = String()
    flightDuration = String()
    layoverDurations = List(String)
    link = String()
    luggageLimits = Field(LuggageLimits)
    luggagePrice = List(String)
    numberOfStops = Int()
    price = Float()
    quality = Float()
    queryDate = String()
    remainingSeats = Int()
    userEmail = String()
    uniqueId = String()


class Query(ObjectType):
    all_flights = List(Flight)

    def resolve_all_flights(self, info):
        # Implement your function that fetches flights from Firebase here
        all_flights = factory.firebase_flights.read_all_flights()
        return all_flights
