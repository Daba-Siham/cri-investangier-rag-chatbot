from scripts.test_generation_stability import marker_matches, normalize_numeric_text


def test_numeric_normalization_accepts_thousands_formats():
    for value in ("15,286", "15 286", "15\u00a0286", "15\u202f286", "15.286", "15286"):
        assert marker_matches(value, ("15286",))
    assert normalize_numeric_text("15.286") == "15286"
