# Blockchain-passcode-book

A simple illustration of how blockchain technology can be used to securely save and manage passcodes — with encryption, deletion, and controlled viewing features to demonstrate data integrity and immutability.

## Overview

This project illustrates how blockchain principles can be applied to securely store data — in this case, user passcodes. The key features include:

- **Blockchain Structure:**  
  Each passcode is stored in a block containing an index, timestamp, encrypted passcode data, the previous block’s hash, and its own hash.
- **Encryption:**  
  Passcodes are encrypted using Fernet symmetric encryption from the `cryptography` library, making them securely saved even if the data is exposed.
- **Web Interface:**  
  A simple Flask-based UI allows you to:
  - Submit a passcode through a form, which is then encrypted and added to the blockchain.
  - Hide passcodes by default on the view page.
  - Mark a passcode as deleted (soft deletion) without removing it from the blockchain.
  - Reveal the actual passcode only if a secret view key is provided.

## Features

- The blockchain structure retains the history of added passcodes and ensures integrity of data by linking each block with the hash of the previous block.
- Instead of physically removing data, passcodes can be marked as deleted, which ensures the blockchain’s immutability and still provides a mechanism to manage outdated or unwanted passcodes.
- Passcodes are hidden by default on the public interface. A separate secure route allows users to reveal the actual passcode after entering a secret view key.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Cryptography

### Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/jsinn003/Blockchain-passcode-book.git
    cd Blockchain-passcode-book
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    ```

    **On Windows:**

    ```bash
    venv\Scripts\activate
    ```

    **On macOS/Linux:**

    ```bash
    source venv/bin/activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install Flask cryptography
    ```

4. **Run the Application:**

    ```bash
    python app.py
    ```

    The application will start a local development server.

## Security Notes

- **Debug Mode:**  
  The application runs in debug mode by default for development purposes. **Do not use debug mode in production** as it can expose sensitive information.
- **Encryption & Keys:**  
  The encryption key is generated at runtime and the view key is hardcoded (`VIEW_KEY = "mysecretkey"`). For production or sensitive applications, please consider managing these keys via environment variables or secure configuration files.
- **Local Use:**  
  This project is designed for educational purposes and local testing. It is not intended for public use without additional security measures.

## License

This project is licensed under the MIT License.
