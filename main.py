import pandas as pd

hotels = pd.read_csv("hotels.csv", dtype={"id": str})
cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
card_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = hotels.loc[hotels["id"] == hotel_id, "name"].squeeze()

    def book(self):
        hotels.loc[hotels["id"] == self.hotel_id, "available"] = "no"
        hotels.to_csv("hotels.csv", index=False)

    def available(self):
        availability = hotels.loc[hotels["id"] == self.hotel_id, "available"].squeeze()

        if availability == "yes":
            return True
        else:
            return False


class Reservation:
    def __init__(self, hotel_object, customer_name):
        self.hotel = hotel_object
        self.customer_name = customer_name

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        """

        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiry, holder_name, cvc):
        card_data = {"number": self.number, "expiration": expiry,
                     "holder": holder_name, "cvc": cvc}

        return card_data in cards


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = card_security.loc[card_security["number"] == self.number, "password"].squeeze()

        return password == given_password


print(hotels)
hotel_id = input("Enter the id of the hotel: ")

hotel = Hotel(hotel_id)

if hotel.available():
    credit_card = SecureCreditCard("1234567890123456")
    if credit_card.validate("12/26", "JOHN SMITH", "123"):
        pw = input("Input your password: ")

        if credit_card.authenticate(pw):
            hotel.book()
            name = input("Enter your name: ")
            reservation = Reservation(hotel, name)
            print(reservation.generate())
else:
    print("Hotel has no vacancies.")
