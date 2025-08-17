import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

try:
    # Get the path to the service account key from environment variables
    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    print(cred_path)
    if not cred_path:
        raise ValueError("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully.")

except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")

def verify_token(id_token):
    """Verifies the Firebase ID token."""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None
