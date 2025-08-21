import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { onAuthStateChanged } from "firebase/auth";
import axios from "axios";
import { auth } from "../firebase";

const AuthContext = createContext({
  firebaseUser: null,
  idToken: null,
  dbUserId: null,
  isAuthReady: false,
});

export const AuthProvider = ({ children }) => {
  const [firebaseUser, setFirebaseUser] = useState(null);
  const [idToken, setIdToken] = useState(null);
  const [dbUserId, setDbUserId] = useState(null);
  const [isAuthReady, setIsAuthReady] = useState(false);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (user) => {
      try {
        setFirebaseUser(user);
        if (user) {
          const token = await user.getIdToken();
          setIdToken(token);
          // Ensure user exists in backend and capture DB _id
          const res = await axios.post(
            "http://127.0.0.1:5000/auth/sync-user",
            {},
            { headers: { Authorization: `Bearer ${token}` } }
          );
          const id = res?.data?.user?._id || null;
          setDbUserId(id);
          if (id) {
            localStorage.setItem("dbUserId", id);
          }
        } else {
          setIdToken(null);
          setDbUserId(null);
          localStorage.removeItem("dbUserId");
        }
      } finally {
        setIsAuthReady(true);
      }
    });
    return () => unsub();
  }, []);

  const value = useMemo(
    () => ({ firebaseUser, idToken, dbUserId, isAuthReady }),
    [firebaseUser, idToken, dbUserId, isAuthReady]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);


