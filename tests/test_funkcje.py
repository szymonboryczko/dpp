import pytest
from logic.funkcje import *

def test_is_palindrome():
    assert is_palindrome("kajak")
    assert is_palindrome("Kobyła ma mały bok")
    assert not is_palindrome("python")
    assert is_palindrome("")
    assert is_palindrome("A")

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55
    with pytest.raises(ValueError):
        fibonacci(-1)

def test_count_vowels():
    assert count_vowels("Python") == 2
    assert count_vowels("AEIOUY") == 6
    assert count_vowels("bcd") == 0
    assert count_vowels("") == 0
    assert count_vowels("Próba żółwia") == 5

def test_calculate_discount():
    assert calculate_discount(100, 0.2) == 80.0
    assert calculate_discount(50, 0) == 50.0
    assert calculate_discount(200, 1) == 0.0
    with pytest.raises(ValueError):
        calculate_discount(100, -0.1)
    with pytest.raises(ValueError):
        calculate_discount(100, 1.5)

def test_flatten_list():
    assert flatten_list([1, 2, 3]) == [1, 2, 3]
    assert flatten_list([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]
    assert flatten_list([]) == []
    assert flatten_list([[[1]]]) == [1]
    assert flatten_list([1, [2, [3, [4]]]]) == [1, 2, 3, 4]

def test_word_frequencies():
    assert word_frequencies("To be or not to be") == {"to": 2, "be": 2, "or": 1, "not": 1}
    assert word_frequencies("Hello, hello!") == {"hello": 2}
    assert word_frequencies("") == {}
    assert word_frequencies("Python Python python") == {"python": 3}
    assert word_frequencies("Ala ma kota, a kot ma Ale.") == {
        "ala": 1, "ma": 2, "kota": 1, "a": 1, "kot": 1, "ale": 1
    }

def test_is_prime():
    assert is_prime(2)
    assert is_prime(3)
    assert not is_prime(4)
    assert not is_prime(0)
    assert not is_prime(1)
    assert is_prime(97)