from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair for server
server_key = RSA.generate(2048)

# List of connected clients, each as tuple (socket, aes_key)
clients = []

# Function to encrypt message with AES
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt message with AES
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Function to handle client connection
def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")
    
    try:
        # Send server's public key to client
        client_socket.send(server_key.publickey().export_key(format='PEM'))

        # Receive client's public key
        client_public_key_data = client_socket.recv(2048)
        client_public_key = RSA.import_key(client_public_key_data)

        # Generate AES key for this client
        aes_key = get_random_bytes(16)

        # Encrypt AES key with client's public RSA key
        cipher_rsa = PKCS1_OAEP.new(client_public_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)

        # Send encrypted AES key to client
        client_socket.send(encrypted_aes_key)

        # Add client to clients list
        clients.append((client_socket, aes_key))

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break

            # Decrypt message from client
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Received from {client_address}: {decrypted_message}")

            # Broadcast to other clients
            for c_socket, c_key in clients:
                if c_socket != client_socket:
                    encrypted_to_send = encrypt_message(c_key, decrypted_message)
                    c_socket.send(encrypted_to_send)

            if decrypted_message.lower() == "exit":
                print(f"Connection with {client_address} closed by client")
                break

    except Exception as e:
        print(f"Error with {client_address}: {e}")

    finally:
        # Remove client and close connection
        clients[:] = [c for c in clients if c[0] != client_socket]
        client_socket.close()

# Accept and handle client connections
print("Server is running and waiting for connections...")
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
