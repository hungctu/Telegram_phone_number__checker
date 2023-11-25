import phonenumbers
from flag import flag

def get_country_flag(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        country_code = parsed_number.country_code

        country = phonenumbers.region_code_for_number(parsed_number)
        c_flag = flag(country)

        return f"{c_flag}"
    except phonenumbers.phonenumberutil.NumberParseException:
        return "Invalid phone number format"





