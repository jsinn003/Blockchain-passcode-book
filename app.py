import hashlib
import datetime as date
from flask import Flask, request, render_template, redirect, url_for
from cryptography.fernet import Fernet

# Set your key to unlock saved passwords
VIEW_KEY = "mysecretkey"
key = Fernet.generate_key()
cipher_suite = Fernet(key)
app = Flask(__name__)


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(hash_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        # here
        self.deleted_indices = set()

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def add_passcode(self, passcode):
        encrypted_passcode = cipher_suite.encrypt(passcode.encode()).decode()
        new_block = Block(len(self.chain), date.datetime.now(), encrypted_passcode, self.get_latest_block().hash)
        self.add_block(new_block)

    def get_passcode(self, index):
        if index < len(self.chain):
            encrypted_passcode = self.chain[index].data
            decrypted_passcode = cipher_suite.decrypt(encrypted_passcode.encode()).decode()
            return decrypted_passcode
        else:
            return None

    def delete_passcode(self, index):
        if index > 0 and index < len(self.chain):
            self.deleted_indices.add(index)


blockchain = Blockchain()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_passcode', methods=['GET', 'POST'])
def add_passcode():
    if request.method == 'POST':
        passcode = request.form['passcode']
        blockchain.add_passcode(passcode)
        return redirect(url_for('view_passcodes'))
    return render_template('add_passcode.html')


@app.route('/view_passcodes')
def view_passcodes():
    passcodes = []
    for i in range(1, len(blockchain.chain)):
        if i in blockchain.deleted_indices:
            display = "Deleted"
        else:
            display = "Hidden"  # Always hide the actual passcode
        passcodes.append({'index': i, 'display': display})
    return render_template('view_passcodes.html', passcodes=passcodes)


@app.route('/delete_passcode/<int:index>', methods=['POST'])
def delete_passcode(index):
    if index > 0 and index < len(blockchain.chain):
        blockchain.delete_passcode(index)
    return redirect(url_for('view_passcodes'))


@app.route('/reveal_passcode/<int:index>', methods=['GET', 'POST'])
def reveal_passcode(index):
    error = None
    if request.method == 'POST':
        input_key = request.form.get('view_key')
        if input_key == VIEW_KEY:
            if index in blockchain.deleted_indices:
                passcode = "This passcode has been deleted."
            else:
                passcode = blockchain.get_passcode(index)
            return render_template('reveal_passcode.html', index=index, passcode=passcode)
        else:
            error = "Invalid view key"
    return render_template('enter_view_key.html', index=index, error=error)


if __name__ == '__main__':
    app.run()
