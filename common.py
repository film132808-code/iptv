"""Shared helpers."""

COUNTRY_NAMES = {
    "AL": "Albania", "AR": "Argentina", "AT": "Austria", "AU": "Australia",
    "BA": "Bosnia", "BD": "Bangladesh", "BE": "Belgium", "BG": "Bulgaria",
    "BR": "Brazil", "CA": "Canada", "CH": "Switzerland", "CL": "Chile",
    "CN": "China", "CO": "Colombia", "CZ": "Czechia", "DE": "Germany",
    "DK": "Denmark", "EG": "Egypt", "ES": "Spain", "FI": "Finland",
    "FR": "France", "GB": "United Kingdom", "GR": "Greece", "HK": "Hong Kong",
    "HR": "Croatia", "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland",
    "IL": "Israel", "IN": "India", "IQ": "Iraq", "IR": "Iran", "IT": "Italy",
    "JP": "Japan", "KE": "Kenya", "KR": "South Korea", "LK": "Sri Lanka",
    "LT": "Lithuania", "LV": "Latvia", "MA": "Morocco", "MX": "Mexico",
    "MY": "Malaysia", "NG": "Nigeria", "NL": "Netherlands", "NO": "Norway",
    "NP": "Nepal", "NZ": "New Zealand", "PE": "Peru", "PH": "Philippines",
    "PK": "Pakistan", "PL": "Poland", "PT": "Portugal", "QA": "Qatar",
    "RO": "Romania", "RS": "Serbia", "RU": "Russia", "SA": "Saudi Arabia",
    "SE": "Sweden", "SG": "Singapore", "SI": "Slovenia", "SK": "Slovakia",
    "TH": "Thailand", "TR": "Turkey", "TW": "Taiwan", "UA": "Ukraine",
    "UK": "United Kingdom", "US": "United States", "VN": "Vietnam",
    "ZA": "South Africa", "AE": "UAE", "AF": "Afghanistan", "MM": "Myanmar",
    "KH": "Cambodia", "MV": "Maldives", "BH": "Bahrain", "KW": "Kuwait",
    "OM": "Oman", "JO": "Jordan", "LB": "Lebanon", "SY": "Syria",
    "DZ": "Algeria", "TN": "Tunisia", "ET": "Ethiopia", "GH": "Ghana",
    "TZ": "Tanzania", "UG": "Uganda", "ZW": "Zimbabwe", "SN": "Senegal",
    "CI": "Ivory Coast", "CM": "Cameroon", "MZ": "Mozambique",
    "EC": "Ecuador", "UY": "Uruguay", "VE": "Venezuela", "PY": "Paraguay",
    "BO": "Bolivia", "CR": "Costa Rica", "PA": "Panama", "GT": "Guatemala",
    "DO": "Dominican Rep.", "JM": "Jamaica", "TT": "Trinidad",
    "KZ": "Kazakhstan", "UZ": "Uzbekistan", "AZ": "Azerbaijan", "GE": "Georgia",
    "AM": "Armenia", "BY": "Belarus", "MD": "Moldova", "MN": "Mongolia",
    "CY": "Cyprus", "MT": "Malta", "IS": "Iceland", "LU": "Luxembourg",
    "EE": "Estonia", "MK": "North Macedonia", "ME": "Montenegro", "XK": "Kosovo",
    "AD": "Andorra", "MC": "Monaco", "SM": "San Marino", "LI": "Liechtenstein",
    "GI": "Gibraltar", "FO": "Faroe Islands", "GL": "Greenland",
    "PR": "Puerto Rico", "CU": "Cuba", "HT": "Haiti", "HN": "Honduras",
    "SV": "El Salvador", "NI": "Nicaragua", "BZ": "Belize", "BB": "Barbados",
    "BS": "Bahamas", "GY": "Guyana", "SR": "Suriname", "FJ": "Fiji",
    "PG": "Papua New Guinea", "WS": "Samoa", "TO": "Tonga", "VU": "Vanuatu",
    "MU": "Mauritius", "SC": "Seychelles", "MG": "Madagascar", "RW": "Rwanda",
    "ZM": "Zambia", "BW": "Botswana", "NA": "Namibia", "AO": "Angola",
    "SD": "Sudan", "LY": "Libya", "SO": "Somalia", "DJ": "Djibouti",
    "ER": "Eritrea", "BF": "Burkina Faso", "ML": "Mali", "NE": "Niger",
    "TD": "Chad", "GN": "Guinea", "SL": "Sierra Leone", "LR": "Liberia",
    "TG": "Togo", "BJ": "Benin", "GA": "Gabon", "CG": "Congo",
    "CD": "DR Congo", "MW": "Malawi", "LS": "Lesotho", "SZ": "Eswatini",
}


FLAG = {}


def flag_of(cc):
    cc = (cc or "").upper()
    if len(cc) != 2 or not cc.isalpha():
        return ""
    if cc not in FLAG:
        FLAG[cc] = chr(0x1F1E6 + ord(cc[0]) - 65) + chr(0x1F1E6 + ord(cc[1]) - 65)
    return FLAG[cc]
