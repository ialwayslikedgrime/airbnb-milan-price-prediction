# location_hierarchy.py

# Hierarchical location mapping for Airbnb Milan analysis
LOCATION_HIERARCHY = {
    # Level 1: Milan (most local)
    "Milan": "Milan",
    
    # Level 2: Lombardy (regional)
    "Lombardy": "Lombardy",
    
    # Level 3: Northern Italy (macro-regional)
    "Piedmont": "Northern Italy",
    "Liguria": "Northern Italy", 
    "Veneto": "Northern Italy",
    "Friuli-Venezia Giulia": "Northern Italy",
    "Trentino-Alto Adige": "Northern Italy",
    "Valle d'Aosta": "Northern Italy",
    "Aosta Valley": "Northern Italy",
    "Emilia-Romagna": "Northern Italy",
    
    # Level 4: Central/Southern Italy
    "Lazio": "Central/Southern Italy",
    "Tuscany": "Central/Southern Italy", 
    "Campania": "Central/Southern Italy",
    "Sicily": "Central/Southern Italy",
    "Apulia": "Central/Southern Italy",
    "Calabria": "Central/Southern Italy",
    "Marche": "Central/Southern Italy",
    "Sardinia": "Central/Southern Italy",
    "Abruzzo": "Central/Southern Italy",
    "Umbria": "Central/Southern Italy",
    "Basilicata": "Central/Southern Italy",
    "Unknown_Italy": "Central/Southern Italy",  # assuming it's not Milan/Lombardy
    
    # Level 5: Europe (EU + close)
    "Switzerland": "Europe",
    "France": "Europe",
    "Germany": "Europe", 
    "Spain": "Europe",
    "Austria": "Europe",
    "Netherlands": "Europe",
    "Portugal": "Europe",
    "Denmark": "Europe",
    "Belgium": "Europe",
    "Luxembourg": "Europe",
    "Monaco": "Europe",
    "Cyprus": "Europe",
    "Albania": "Europe",
    "Andorra": "Europe",
    "Ukraine": "Europe",
    "Montenegro": "Europe",
    "San Marino": "Europe",
    "Malta": "Europe",
    "Sweden": "Europe",
    "Ireland": "Europe",
    "Turkey": "Europe",
    "Serbia": "Europe",
    
    # Level 6: Extra-EU (rest of world)
    "United States": "Extra-EU",
    "United Kingdom": "Extra-EU",  # post-Brexit
    "Mexico": "Extra-EU",
    "United Arab Emirates": "Extra-EU",
    "Australia": "Extra-EU", 
    "Brazil": "Extra-EU",
    "Indonesia": "Extra-EU",
    "Colombia": "Extra-EU",
    "Morocco": "Extra-EU",
    "Guinea-Bissau": "Extra-EU",
    "Philippines": "Extra-EU",
    "South Africa": "Extra-EU",
    "Russia": "Extra-EU",
    "Taiwan": "Extra-EU",
    "New Zealand": "Extra-EU",
    "Singapore": "Extra-EU",
    "Thailand": "Extra-EU",
    "Argentina": "Extra-EU",
    "Costa Rica": "Extra-EU",
    "Hong Kong": "Extra-EU",
    "Guadeloupe": "Extra-EU",
    "Nepal": "Extra-EU",
    "Ghana": "Extra-EU",
    "Egypt": "Extra-EU",
    "Dominican Republic": "Extra-EU"
}

# Function to apply the hierarchy
def categorize_location(location):
    """
    Categorize a location into the hierarchical system
    """
    return LOCATION_HIERARCHY.get(location, "Unknown")

# For easy analysis - create ordered categories
CATEGORY_ORDER = [
    "Milan",
    "Lombardy", 
    "Northern Italy",
    "Central/Southern Italy",
    "Europe",
    "Extra-EU"
]

# Function to get category counts
def analyze_location_distribution(df, location_column='location_category'):
    """
    Analyze the distribution of locations in the hierarchical categories
    """
    import pandas as pd
    
    # Apply categorization
    df['location_hierarchy'] = df[location_column].map(categorize_location)
    
    # Get counts
    hierarchy_counts = df['location_hierarchy'].value_counts()
    
    # Reorder according to our hierarchy
    ordered_counts = hierarchy_counts.reindex(CATEGORY_ORDER, fill_value=0)
    
    return ordered_counts
