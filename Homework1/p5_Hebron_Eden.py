"""
Encrypt/decrypt text with a Caesar cipher and analyze letter frequencies,
driven by an interactive terminal menu.
"""
import string


def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result += chr(base + shifted)
        else:
            result += char
    return result


def caesar_decipher(cyphertext, shift):
    return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
    frequency = {letter: 0 for letter in string.ascii_lowercase}
    for char in text.lower():
        if char.isalpha():
            frequency[char] += 1
    return frequency


def print_letter_frequency(frequency):
    print()
    for letter, count in frequency.items():
        if count > 0:
            print(f"{letter}: {count}")


def main():
    while True:
        print()
        print("1. Encrypt/decrypt a message")
        print("2. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            text = input("Enter your message: ")
            shift = int(input("Enter shift value: "))

            ciphertext = caesar_cipher(text, shift)
            print(f"\nCiphered text: {ciphertext}")

            frequency = letter_frequency(text)
            print("\nLetter frequency of original message:")
            print_letter_frequency(frequency)

            deciphered = caesar_decipher(ciphertext, shift)
            print(f"\nDeciphered text: {deciphered}")
        elif choice == "2":
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
