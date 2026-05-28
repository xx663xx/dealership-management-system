from datetime import date


class ValidationError(ValueError):
    pass


def _require_text(value, field_name):
    if value is None or str(value).strip() == "":
        raise ValidationError(f"{field_name} is required")
    return str(value).strip()


def _parse_iso_date(value, field_name):
    text = _require_text(value, field_name)
    try:
        return date.fromisoformat(text)
    except ValueError as error:
        raise ValidationError(f"{field_name} must use YYYY-MM-DD format") from error


def _parse_non_negative_number(value, field_name):
    if value is None or str(value).strip() == "":
        raise ValidationError(f"{field_name} is required")
    try:
        number = float(value)
    except ValueError as error:
        raise ValidationError(f"{field_name} must be a number") from error
    if number < 0:
        raise ValidationError(f"{field_name} must be non-negative")
    return number


def validate_sale(car_status, sale_price, sale_date):
    if car_status != "доступна":
        raise ValidationError("car must be available for sale")
    _parse_non_negative_number(sale_price, "sale_price")
    _parse_iso_date(sale_date, "sale_date")


def validate_reservation(reservation_date, valid_until):
    start_date = _parse_iso_date(reservation_date, "reservation_date")
    if valid_until is None or str(valid_until).strip() == "":
        return
    end_date = _parse_iso_date(valid_until, "valid_until")
    if end_date < start_date:
        raise ValidationError("valid_until must not be earlier than reservation_date")


def validate_test_drive(test_drive_date, result):
    _parse_iso_date(test_drive_date, "test_drive_date")
    _require_text(result, "result")
