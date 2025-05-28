class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        if num_rails == 1:
            return plain_text

        rails = ['' for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1 for down, -1 for up

        for char in plain_text:
            rails[rail_index] += char
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        return ''.join(rails)

    def rail_fence_decrypt(self, cipher_text, num_rails):
        if num_rails == 1:
            return cipher_text

        # Determine the pattern of positions
        pattern = [0] * len(cipher_text)
        rail_index = 0
        direction = 1

        for i in range(len(cipher_text)):
            pattern[i] = rail_index
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        # Count how many letters go to each rail
        rail_counts = [pattern.count(i) for i in range(num_rails)]

        # Slice the cipher_text into rails
        rails = []
        idx = 0
        for count in rail_counts:
            rails.append(cipher_text[idx:idx + count])
            idx += count

        # Reconstruct the plaintext
        rail_positions = [0] * num_rails
        result = ''
        for i in range(len(cipher_text)):
            rail = pattern[i]
            result += rails[rail][rail_positions[rail]]
            rail_positions[rail] += 1

        return result
