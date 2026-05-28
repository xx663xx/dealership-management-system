def format_money(value):
    if value is None:
        return ""
    try:
        number = float(value)
    except ValueError:
        return value
    if number.is_integer():
        return f"{int(number):,}".replace(",", " ")
    return f"{number:,.2f}".replace(",", " ")


def format_integer(value):
    if value is None:
        return ""
    try:
        return f"{int(value):,}".replace(",", " ")
    except ValueError:
        return value


def safe_contract_filename(value):
    allowed = []
    for char in value:
        if char.isalnum() or char in ("-", "_"):
            allowed.append(char)
        else:
            allowed.append("_")
    return "".join(allowed).strip("_") or "contract"
