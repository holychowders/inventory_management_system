# TODO: Understand how this works, its constraints, and try to simplify it
def format_phone_number(phone_number: str) -> str:
    # Borrowed from:
    #   - "What's the best way to format a phone number in Python?"
    #   - https://stackoverflow.com/a/7058216/13327811
    return format(int(phone_number[:-1]), ",").replace(",", "-") + phone_number[-1]
