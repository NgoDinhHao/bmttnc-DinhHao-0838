from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher

app = Flask(__name__)

# router routes for home page
@app.route('/')
def home():
    return render_template('index.html')

# router routes for caesar cypher
@app.route('/caesar')
def caesar():
    return render_template('caesar.html')

@app.route('/encrypt', methods=['POST'])
def caesar_encrypt():
    text = request.form['InputPlaintext']
    key = int(request.form['InputKeyCipher'])
    caesar = CaesarCipher()
    encrypt_text = caesar.encrypt_text(text, key)
    return f"<text>{text}<br/>skey: {key}<br/>encrypted text: {encrypt_text}"

@app.route('/decrypt', methods=['POST'])
def caesar_decrypt():
    text = request.form['InputCipherText']
    key = int(request.form['InputKeyCipher'])
    caesar = CaesarCipher()
    decrypt_text = caesar.decrypt_text(text, key)
    return f"<text>{text}<br/>skey: {key}<br/>decrypted text: {decrypt_text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)