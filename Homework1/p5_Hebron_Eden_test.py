"""
Unit tests for the Caesar cipher and letter frequency functions in
p5_Hebron_Eden.py.
"""
import unittest

from p5_Hebron_Eden import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):
    def test_basic_shift(self):
        self.assertEqual(caesar_cipher("abc", 1), "bcd")

    def test_wraps_around_alphabet(self):
        self.assertEqual(caesar_cipher("xyz", 3), "abc")

    def test_preserves_case(self):
        self.assertEqual(caesar_cipher("AbC", 2), "CdE")

    def test_preserves_spaces_and_punctuation(self):
        self.assertEqual(caesar_cipher("hi there!", 5), "mn ymjwj!")

    def test_negative_shift(self):
        self.assertEqual(caesar_cipher("bcd", -1), "abc")

    def test_zero_shift(self):
        self.assertEqual(caesar_cipher("hello", 0), "hello")


class TestCaesarDecipher(unittest.TestCase):
    def test_basic_decipher(self):
        self.assertEqual(caesar_decipher("bcd", 1), "abc")

    def test_round_trip(self):
        text = "The Quick Brown Fox!"
        for shift in range(26):
            ciphertext = caesar_cipher(text, shift)
            self.assertEqual(caesar_decipher(ciphertext, shift), text)


class TestLetterFrequency(unittest.TestCase):
    def test_counts_letters_ignoring_case(self):
        freq = letter_frequency("AaBb")
        self.assertEqual(freq["a"], 2)
        self.assertEqual(freq["b"], 2)

    def test_ignores_non_alphabetic_characters(self):
        freq = letter_frequency("a1 b2! c3?")
        self.assertEqual(freq["a"], 1)
        self.assertEqual(freq["b"], 1)
        self.assertEqual(freq["c"], 1)
        self.assertEqual(sum(freq.values()), 3)

    def test_all_letters_present_with_zero_default(self):
        freq = letter_frequency("")
        self.assertEqual(len(freq), 26)
        self.assertTrue(all(count == 0 for count in freq.values()))


if __name__ == "__main__":
    unittest.main()
