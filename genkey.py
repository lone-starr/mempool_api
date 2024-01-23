import secrets


def generate_random_hex(length):
    # Generate random bytes and convert them to hex
    random_bytes = secrets.token_bytes(length // 2)
    random_hex = random_bytes.hex()
    return random_hex


# Specify the desired length of the hex text
hex_length = 32

# Generate random hex text
random_hex_text = generate_random_hex(hex_length)

print(random_hex_text)
