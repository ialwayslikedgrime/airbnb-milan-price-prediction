property_type_dict = {
    # ---------------------------
    # APARTMENT / CONDO
    # ---------------------------
    "Entire rental unit": "Apartment/Condo",
    "Entire condo": "Apartment/Condo", 
    "Entire condominium": "Apartment/Condo",
    "Entire loft": "Apartment/Condo",
    "Entire serviced apartment": "Apartment/Condo",
    "Private room in rental unit": "Apartment/Condo",
    "Private room in condo": "Apartment/Condo",
    "Private room in condominium": "Apartment/Condo",
    "Private room in loft": "Apartment/Condo",
    "Private room in serviced apartment": "Apartment/Condo",
    "Private room in apartment": "Apartment/Condo",
    "Shared room in rental unit": "Apartment/Condo",
    "Shared room in condo": "Apartment/Condo",
    "Shared room in condominium": "Apartment/Condo",
    "Shared room in loft": "Apartment/Condo",
    "Shared room in apartment": "Apartment/Condo",
    "Room in aparthotel": "Apartment/Condo",
    "Room in serviced apartment": "Apartment/Condo",
    "Entire residential home": "Apartment/Condo",  # Often high-rise apartments

    # ---------------------------
    # HOUSE (Single-family homes, townhouses, villas)
    # ---------------------------
    "Entire home": "House",
    "Entire house": "House",
    "Entire vacation home": "House",
    "Entire villa": "House",
    "Entire townhouse": "House",
    "Entire cottage": "House",
    "Entire chalet": "House",
    "Entire bungalow": "House",
    "Entire cabin": "House",
    "Private room in home": "House",
    "Private room in house": "House",
    "Private room in villa": "House",
    "Private room in townhouse": "House",
    "Private room in vacation home": "House",
    "Private room in cottage": "House",
    "Private room in chalet": "House",
    "Private room in bungalow": "House",
    "Private room in cabin": "House",
    "Shared room in home": "House",
    "Shared room in house": "House",
    "Shared room in villa": "House",
    "Shared room in vacation home": "House",
    "Shared room in cottage": "House",

    # ---------------------------
    # GUEST / HOTEL / BnB
    # ---------------------------
    "Entire guesthouse": "Guest/Hotel",
    "Entire guest suite": "Guest/Hotel",
    "Entire bed and breakfast": "Guest/Hotel",
    "Private room in bed and breakfast": "Guest/Hotel",
    "Private room in guesthouse": "Guest/Hotel",
    "Private room in guest suite": "Guest/Hotel",
    "Private room in hostel": "Guest/Hotel",
    "Private room in casa particular": "Guest/Hotel",
    "Private room in minsu": "Guest/Hotel",  # Taiwan B&B
    "Private room in ryokan": "Guest/Hotel",  # Japanese inn
    "Room in hotel": "Guest/Hotel",
    "Room in boutique hotel": "Guest/Hotel",
    "Room in bed and breakfast": "Guest/Hotel",
    "Room in hostel": "Guest/Hotel",
    "Casa particular": "Guest/Hotel",
    "Shared room in bed and breakfast": "Guest/Hotel",
    "Shared room in hostel": "Guest/Hotel",
    "Shared room in hotel": "Guest/Hotel",
    "Shared room in guesthouse": "Guest/Hotel",

    # ---------------------------
    # UNIQUE STAYS
    # ---------------------------
    "Tiny home": "Unique",
    "Entire tiny home": "Unique",
    "Private room in tiny home": "Unique",
    "Camper/RV": "Unique",
    "Private room in camper/rv": "Unique",
    "Boat": "Unique",
    "Houseboat": "Unique",
    "Yacht": "Unique",
    "Private room in boat": "Unique",
    "Shipping container": "Unique",
    "Treehouse": "Unique",
    "Private room in treehouse": "Unique",
    "Cave": "Unique",
    "Private room in cave": "Unique",
    "Castle": "Unique",
    "Private room in castle": "Unique",
    "Tent": "Unique",
    "Yurt": "Unique",
    "Dome": "Unique",
    "Windmill": "Unique",
    "Lighthouse": "Unique",
    "Train": "Unique",
    "Plane": "Unique",
    "Tower": "Unique",
    "Earth house": "Unique",
    "Cycladic house": "Unique",
    "Dammuso": "Unique",  # Traditional Sicilian stone house
    "Riad": "Unique",     # Traditional Moroccan house
    "Private room in farm stay": "Unique",
    "Farm stay": "Unique",
    "Private room in nature lodge": "Unique",
    "Nature lodge": "Unique",

    # ---------------------------
    # AMBIGUOUS CASES - Need context for better classification
    # ---------------------------
    "Entire home/apt": "Ambiguous",  # Could be house or apartment
    "Entire place": "Ambiguous",     # Too vague
    "Private room": "Ambiguous",     # Missing property type context
    "Shared room": "Ambiguous",      # Missing property type context
    "Room in boutique hotel or B&B": "Guest/Hotel",  # Close enough
    
    # ---------------------------
    # FALLBACK
    # ---------------------------
    "Other": "Other",
    "": "Other",  # Empty string fallback
}

