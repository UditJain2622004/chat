import React from "react";
import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "../firebase";
import axios from "axios"; // or use fetch

const GoogleSignIn = ({ onSignInSuccess }) => {
  const handleGoogleSignIn = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;

      // Get the Firebase ID token
      const idToken = await user.getIdToken();

      // Send the token to your backend to sync the user
      const response = await axios.post(
        "http://127.0.0.1:5000/auth/sync-user",
        {},
        {
          headers: {
            Authorization: `Bearer ${idToken}`,
          },
        }
      );

      console.log("Backend response:", response.data);
      onSignInSuccess(); // Notify parent component
      // You can now store user state in your app (e.g., in context or Redux)
    } catch (error) {
      console.error("Error during Google sign-in:", error);
    }
  };

  return (
    <button className="btn btn-google" onClick={handleGoogleSignIn}>
      <span className="g-logo">G</span>
      Continue with Google
    </button>
  );
};

export default GoogleSignIn;
