DATASOURCE = {
    1: {
        'name': 'Acme Lightbulbs',
        'annual_spend': 923468,
        'offices_in': ['US', 'GB', 'DK']
        },
    2: {
        'name': 'Bargain Basements',
        'annual_spend': 4578,
        'offices_in': ['US', 'FR', 'ZA', 'SE']
        },
    3: {
        'name': 'Nordic Ventures',
        'annual_spend': 1350000,
        'offices_in': ['SE', 'NO', 'DK']
        },
    4: {
        'name': 'Pacific Techware',
        'annual_spend': 245000,
        'offices_in': ['US', 'CA', 'AU']
        },
    5: {
        'name': 'EuroMart Wholesale',
        'annual_spend': 78543,
        'offices_in': ['DE', 'NL', 'BE']
        },
    6: {
        'name': 'Baltic Logistics',
        'annual_spend': 312000,
        'offices_in': ['LT', 'LV', 'EE', 'SE']
        },
    7: {
        'name': 'Aurora Foods',
        'annual_spend': 1689000,
        'offices_in': ['NO', 'SE']
        },
    8: {
        'name': 'Sapphire Systems',
        'annual_spend': 501200,
        'offices_in': ['GB', 'IE']
        },
    9: {
        'name': 'Maple Outfitters',
        'annual_spend': 91000,
        'offices_in': ['CA']
        },
    10: {
        'name': 'Andes Apparel',
        'annual_spend': 120450,
        'offices_in': ['AR', 'CL', 'PE']
        },
    11: {
        'name': 'Sahara Solar',
        'annual_spend': 200340,
        'offices_in': ['MA', 'DZ', 'TN']
        },
    12: {
        'name': 'Peninsula Banking',
        'annual_spend': 2200000,
        'offices_in': ['US', 'DK']
        },
    13: {
        'name': 'Boreal Analytics',
        'annual_spend': 760000,
        'offices_in': ['FI', 'SE']
        },
    14: {
        'name': 'Harbor Freightliners',
        'annual_spend': 305600,
        'offices_in': ['US', 'MX']
        },
    15: {
        'name': 'Tundra Telecommunications',
        'annual_spend': 1420000,
        'offices_in': ['NO', 'IS']
        },
    16: {
        'name': 'Desert Bloom Farms',
        'annual_spend': 67000,
        'offices_in': ['US']
        },
    17: {
        'name': 'Emerald Retail Group',
        'annual_spend': 455000,
        'offices_in': ['IE', 'GB']
        },
    18: {
        'name': 'Monsoon Textiles',
        'annual_spend': 890000,
        'offices_in': ['IN', 'BD', 'VN']
        },
    19: {
        'name': 'Summit Outdoor',
        'annual_spend': 120000,
        'offices_in': ['US', 'CA']
        },
    20: {
        'name': 'Lagoon BioTech',
        'annual_spend': 1310000,
        'offices_in': ['SE', 'DK']
        },
    21: {
        'name': 'Crimson Media',
        'annual_spend': 230450,
        'offices_in': ['US']
        },
    22: {
        'name': 'Blue Ridge Beverages',
        'annual_spend': 56000,
        'offices_in': ['US']
        },
    23: {
        'name': 'Silverline Security',
        'annual_spend': 720500,
        'offices_in': ['GB', 'SE']
        },
    24: {
        'name': 'Orion Robotics',
        'annual_spend': 1999900,
        'offices_in': ['JP', 'US', 'DK']
        },
    25: {
        'name': 'Alpine Sportswear',
        'annual_spend': 84500,
        'offices_in': ['CH', 'AT']
        },
    26: {
        'name': 'Celtic Creatives',
        'annual_spend': 43000,
        'offices_in': ['IE']
        },
    27: {
        'name': 'Harbor Health',
        'annual_spend': 367000,
        'offices_in': ['US']
        },
    28: {
        'name': 'Zenith Aero',
        'annual_spend': 1570000,
        'offices_in': ['US', 'SE']
        },
    29: {
        'name': 'Prairie Grain Co',
        'annual_spend': 250000,
        'offices_in': ['US', 'CA']
        },
    30: {
        'name': 'Coastal Clean Energy',
        'annual_spend': 980000,
        'offices_in': ['DK', 'DE']
        }
    }

def get_customer_list():
    return [{"id": id, "name": customer['name']} for id, customer in DATASOURCE.items()]

def get_customer_annual_spend(id):
    return DATASOURCE[id]['annual_spend']

def get_customer_office_locations(id):
    return DATASOURCE[id]['offices_in']