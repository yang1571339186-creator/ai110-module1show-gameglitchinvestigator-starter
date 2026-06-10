import pytest
from logic_utils import check_guess, parse_guess, update_score


class TestCheckGuess:
    """Tests for the check_guess function."""

    def test_winning_guess(self):
        """If the secret is 50 and guess is 50, it should be a win."""
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert message == "🎉 Correct!"

    def test_guess_too_high(self):
        """If secret is 50 and guess is 60, hint should be 'Too High'."""
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_guess_too_low(self):
        """If secret is 50 and guess is 40, hint should be 'Too Low'."""
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"

    def test_guess_much_higher(self):
        """Test with a much higher guess."""
        outcome, message = check_guess(100, 1)
        assert outcome == "Too High"

    def test_guess_much_lower(self):
        """Test with a much lower guess."""
        outcome, message = check_guess(1, 100)
        assert outcome == "Too Low"

    def test_guess_with_strings(self):
        """Test that function handles string comparison."""
        outcome, message = check_guess("50", "50")
        assert outcome == "Win"


class TestParseGuess:
    """Tests for the parse_guess function."""

    def test_valid_integer_guess(self):
        """Parse a valid integer string."""
        ok, guess, error = parse_guess("42")
        assert ok is True
        assert guess == 42
        assert error is None

    def test_valid_float_guess(self):
        """Parse a valid float string (should convert to int)."""
        ok, guess, error = parse_guess("42.7")
        assert ok is True
        assert guess == 42
        assert error is None

    def test_empty_string(self):
        """Empty string should return error."""
        ok, guess, error = parse_guess("")
        assert ok is False
        assert guess is None
        assert error == "Enter a guess."

    def test_none_input(self):
        """None input should return error."""
        ok, guess, error = parse_guess(None)
        assert ok is False
        assert guess is None
        assert error == "Enter a guess."

    def test_invalid_number(self):
        """Non-numeric string should return error."""
        ok, guess, error = parse_guess("hello")
        assert ok is False
        assert guess is None
        assert error == "That is not a number."

    def test_negative_number(self):
        """Negative numbers should parse correctly."""
        ok, guess, error = parse_guess("-5")
        assert ok is True
        assert guess == -5
        assert error is None

    def test_zero(self):
        """Zero should parse correctly."""
        ok, guess, error = parse_guess("0")
        assert ok is True
        assert guess == 0
        assert error is None


class TestUpdateScore:
    """Tests for the update_score function."""

    def test_win_first_attempt(self):
        """Winning on first attempt (attempt 0) should award 90 points."""
        new_score = update_score(0, "Win", 0)
        assert new_score == 90

    def test_win_second_attempt(self):
        """Winning on second attempt (attempt 1) should award 80 points."""
        new_score = update_score(0, "Win", 1)
        assert new_score == 80

    def test_win_many_attempts(self):
        """Winning after many attempts should have minimum of 10 points."""
        new_score = update_score(0, "Win", 10)
        assert new_score == 10

    def test_too_high_even_attempt(self):
        """Too High on even attempt number should add 5 points."""
        new_score = update_score(0, "Too High", 0)
        assert new_score == 5

    def test_too_high_odd_attempt(self):
        """Too High on odd attempt number should subtract 5 points."""
        new_score = update_score(10, "Too High", 1)
        assert new_score == 5

    def test_too_low_always_subtracts(self):
        """Too Low should always subtract 5 points."""
        new_score = update_score(10, "Too Low", 0)
        assert new_score == 5

    def test_too_low_multiple_times(self):
        """Test Too Low multiple times."""
        score = 20
        score = update_score(score, "Too Low", 1)
        score = update_score(score, "Too Low", 2)
        assert score == 10

    def test_accumulating_score(self):
        """Test accumulating score through multiple guess outcomes."""
        score = 0
        score = update_score(score, "Too High", 0)  # +5
        score = update_score(score, "Too High", 1)  # -5
        score = update_score(score, "Too Low", 2)   # -5
        assert score == -5
