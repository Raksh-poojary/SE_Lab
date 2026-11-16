import math
import string

import pytest
from hypothesis import given, strategies as st

from airline_baggage import parse_booking, tag_label, total_weight


@st.composite
def booking_codes(draw):
    airline = draw(st.text(alphabet=string.ascii_letters, min_size=1))
    flight = draw(st.integers(min_value=0))
    seat_number = draw(st.integers(min_value=1, max_value=999))
    seat_letter = draw(st.sampled_from("ABCDEFGHJK"))
    return f"{airline}-{flight}-{seat_number}{seat_letter}"


@given(booking_codes())
def test_parse_booking_valid_code_returns_normalized_parts(code):
    airline, flight, seat = code.split("-")
    result = parse_booking(code)

    assert result == (airline.upper(), int(flight), seat[-1].upper())


@given(st.text().filter(lambda code: code.count("-") != 2))
def test_parse_booking_rejects_wrong_number_of_parts(code):
    with pytest.raises(ValueError):
        parse_booking(code)


@given(st.text(min_size=1).filter(lambda value: not value.lstrip("+-").isdigit()))
def test_parse_booking_rejects_non_integer_flight(flight):
    with pytest.raises(ValueError):
        parse_booking(f"AI-{flight}-12A")


@given(st.one_of(st.none(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.booleans(), st.lists(st.text())))
def test_parse_booking_rejects_non_string_input(value):
    with pytest.raises((TypeError, ValueError)):
        parse_booking(value)


@st.composite
def valid_weight_lists(draw):
    weights = draw(st.lists(st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False), min_size=1, max_size=10))
    return weights, ",".join(repr(weight) for weight in weights)


@given(valid_weight_lists())
def test_total_weight_sums_valid_nonnegative_weights(case):
    weights, weights_csv = case
    result = total_weight(weights_csv)

    assert math.isclose(result, sum(weights), rel_tol=1e-12, abs_tol=1e-12)


@given(st.text().filter(lambda value: any(not part.strip() or not _is_float(part) for part in value.split(","))))
def test_total_weight_rejects_empty_or_non_numeric_entries(weights_csv):
    with pytest.raises(ValueError):
        total_weight(weights_csv)


@given(st.one_of(st.none(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.booleans(), st.lists(st.text())))
def test_total_weight_rejects_non_string_input(value):
    with pytest.raises((TypeError, ValueError)):
        total_weight(value)


def _is_float(value):
    try:
        float(value)
    except ValueError:
        return False
    return True


@given(
    st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
    st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
)
def test_tag_label_formats_first_and_last_name(first, last):
    result = tag_label(f"{first} {last}")

    assert result == f"{first[0].upper()}. {last.upper()}"


@given(st.text().filter(lambda name: len(name.split()) < 2))
def test_tag_label_rejects_missing_first_or_last_name(name):
    with pytest.raises(ValueError):
        tag_label(name)


@given(st.one_of(st.none(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.booleans(), st.lists(st.text())))
def test_tag_label_rejects_non_string_input(value):
    with pytest.raises((TypeError, ValueError)):
        tag_label(value)
