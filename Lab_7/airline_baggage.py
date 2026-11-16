import math


def parse_booking(code):
    if not isinstance(code, str):
        raise TypeError("booking code must be a string")

    parts = code.split('-')
    if len(parts) != 3:
        raise ValueError("booking code must contain airline, flight, and seat separated by hyphens")

    airline, flight_text, seat = parts
    if not airline.strip():
        raise ValueError("airline code must not be empty")
    if not seat:
        raise ValueError("seat identifier must not be empty")

    try:
        flight_number = int(flight_text)
    except ValueError as error:
        raise ValueError("flight number must be an integer") from error
    if flight_number < 0:
        raise ValueError("flight number must not be negative")

    return airline.upper(), flight_number, seat[-1].upper()

def total_weight(weights_csv):
    if not isinstance(weights_csv, str):
        raise TypeError("weights_csv must be a string")

    entries = weights_csv.split(',')
    if any(not entry.strip() for entry in entries):
        raise ValueError("weight list must not contain empty entries")

    weights = []
    for entry in entries:
        try:
            weight = float(entry)
        except ValueError as error:
            raise ValueError(f"invalid weight value: {entry!r}") from error
        if not math.isfinite(weight):
            raise ValueError("weights must be finite numbers")
        if weight < 0:
            raise ValueError("weights must not be negative")
        weights.append(weight)

    total = sum(weights)
    if not math.isfinite(total):
        raise ValueError("total weight is too large")
    return total

def tag_label(name):
    if not isinstance(name, str):
        raise TypeError("name must be a string")

    parts = name.split()
    if len(parts) < 2:
        raise ValueError("name must contain a first and last name")
    return parts[0][0].upper() + '. ' + parts[1].upper()

def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter a booking code (e.g. AI-203-12A): ")
    result = parse_booking(user_input)
    print("Airline, Flight and Seat Letter:", result)

    print("\n==== Running total_weight ====")
    user_input = input("Enter bag weights in kg as CSV (e.g. 12.5,7,23): ")
    result = total_weight(user_input)
    print("Total Weight:", result)

    print("\n==== Running tag_label ====")
    user_input = input("Enter a passenger name (first and last): ")
    result = tag_label(user_input)
    print("Tag Label:", result)

if __name__ == "__main__":
    main()
