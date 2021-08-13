import datetime


class Request:
    origin: int #networx-node(pointer?)
    destination: int
    tor: datetime.datetime #TimeOfRequest
    tolp: datetime.datetime #TimeOfLastPickup - latest time avilable for pickup
    top: datetime.datetime #TimeOfPickup - called pickup time in the article. The time the request was actually picked up.
    toed: datetime.datetime #TimeOfExpextedDropoff -  expected drop off time
    toe: datetime.datetime #TimeOfEarliest - the earliest possible time at which the destination could be reached