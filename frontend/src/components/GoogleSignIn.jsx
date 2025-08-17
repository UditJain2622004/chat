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
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <button
        onClick={handleGoogleSignIn}
        style={{ padding: "10px 20px", fontSize: "16px" }}
      >
        Sign in with Google
      </button>
    </div>
  );
};

export default GoogleSignIn;
