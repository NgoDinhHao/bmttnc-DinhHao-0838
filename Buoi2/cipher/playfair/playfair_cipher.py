class PlayfairCipher:
    def __init__(self):
        pass
    
    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()  # Replace J with I
        key_unique = []
        for char in key:
            if char not in key_unique and char.isalpha():
                key_unique.append(char)
        
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J is excluded
        for letter in alphabet:
            if letter not in key_unique:
                key_unique.append(letter)

        # Create 5x5 matrix
        matrix = [key_unique[i:i+5] for i in range(0, 25, 5)]
        return matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None, None  # In case letter not found (shouldn't happen)
    
    def preprocess_plaintext(self, plain_text):
        # Replace J with I, remove non-alpha, and handle duplicate pairs by inserting X
        plain_text = plain_text.replace("J", "I").upper()
        plain_text = ''.join(filter(str.isalpha, plain_text))

        result = ""
        i = 0
        while i < len(plain_text):
            char1 = plain_text[i]
            if i + 1 < len(plain_text):
                char2 = plain_text[i + 1]
                if char1 == char2:
                    result += char1 + "X"
                    i += 1
                else:
                    result += char1 + char2
                    i += 2
            else:
                result += char1 + "X"
                i += 1
        return result
    
    def playfair_encrypt(self, plain_text, matrix):
        plain_text = self.preprocess_plaintext(plain_text)
        encrypted_text = ""

        for i in range(0, len(plain_text), 2):
            row1, col1 = self.find_letter_coords(matrix, plain_text[i])
            row2, col2 = self.find_letter_coords(matrix, plain_text[i + 1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text
    
    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            row1, col1 = self.find_letter_coords(matrix, cipher_text[i])
            row2, col2 = self.find_letter_coords(matrix, cipher_text[i + 1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        # Remove 'X' used for padding or duplicates if appropriate
        cleaned_text = ""
        i = 0
        while i < len(decrypted_text):
            if i+2 < len(decrypted_text) and decrypted_text[i] == decrypted_text[i+2] and decrypted_text[i+1] == 'X':
                cleaned_text += decrypted_text[i]
                i += 2
            else:
                cleaned_text += decrypted_text[i]
                i += 1

        # If the last character is 'X', likely padding, remove it
        if cleaned_text.endswith('X'):
            cleaned_text = cleaned_text[:-1]

        return cleaned_text
