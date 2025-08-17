/* eslint-disable no-unused-vars */
import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { auth } from "../firebase";

const behaviourOptions = [
  { value: "soft", label: "Soft" },
  { value: "between_soft_and_hard", label: "Between Soft and Hard" },
  { value: "hard", label: "Hard" },
  { value: "ease_into_it", label: "Ease into it" },
];

const CreateBot = () => {
  const navigate = useNavigate();
  const defaultUid = useMemo(() => {
    if (typeof crypto !== "undefined" && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    return String(Date.now());
  }, []);

  const [form, setForm] = useState({
    uid: defaultUid,
    name: "",
    picture: "",
    likings: "",
    behaviour: behaviourOptions[0].value,
    ethnicity: "Any",
    hairs: "Any",
    eyes: "Any",
    skin_color: "Any",
    physique: "Any",
  });
  const [dbUserId, setDbUserId] = useState("");

  useEffect(() => {
    const ensureDbUser = async () => {
      if (!auth.currentUser) return;
      try {
        const token = await auth.currentUser.getIdToken();
        const syncRes = await axios.post(
          "http://127.0.0.1:5000/auth/sync-user",
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        const id = syncRes.data?.user?._id;
        if (id) setDbUserId(id);
      } catch (e) {
        // no-op; user creation will fail without user id
      }
    };
    ensureDbUser();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        // create a random uid string for the bot
        const uid = Math.random().toString(36).substring(2, 15);
      const payload = {
        uid: uid,
        name: form.name.trim(),
        picture: form.picture.trim() || undefined,
        likings: form.likings
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
        behaviour: form.behaviour,
        ethnicity: form.ethnicity || "Any",
        hairs: form.hairs || "Any",
        eyes: form.eyes || "Any",
        skin_color: form.skin_color || "Any",
        physique: form.physique || "Any",
        user_id: dbUserId,
      };

      const res = await axios.post("http://127.0.0.1:5000/bots/", payload);
      if (res.status === 201) {
        navigate("/welcome");
      }
    } catch (err) {
      console.error("Failed to create bot", err);
    }
  };

  return (
    <div className="page page-auth">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Create a new bot</h2>
          <p>Define their persona and appearance</p>
        </div>
        <form onSubmit={handleSubmit} className="auth-form">
          {/* <div className="form-field">
            <label>Bot UID</label>
            <input
              name="uid"
              type="text"
              value={form.uid}
              onChange={handleChange}
              placeholder="Unique identifier for the bot"
              required
            />
          </div> */}

          <div className="form-field">
            <label>Name</label>
            <input
              name="name"
              type="text"
              value={form.name}
              onChange={handleChange}
              placeholder="Bot name"
              required
            />
          </div>

          <div className="form-field">
            <label>Picture URL</label>
            <input
              name="picture"
              type="url"
              value={form.picture}
              onChange={handleChange}
              placeholder="https://..."
            />
          </div>

          <div className="form-field">
            <label>Likings (comma separated)</label>
            <input
              name="likings"
              type="text"
              value={form.likings}
              onChange={handleChange}
              placeholder="music, travel, mystery novels"
            />
          </div>

          <div className="form-field">
            <label>Behaviour</label>
            <select name="behaviour" value={form.behaviour} onChange={handleChange}>
              {behaviourOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <div className="form-grid-2">
            <div className="form-field">
              <label>Ethnicity</label>
              <input name="ethnicity" value={form.ethnicity} onChange={handleChange} />
            </div>
            <div className="form-field">
              <label>Hair</label>
              <input name="hairs" value={form.hairs} onChange={handleChange} />
            </div>
          </div>

          <div className="form-grid-2">
            <div className="form-field">
              <label>Eyes</label>
              <input name="eyes" value={form.eyes} onChange={handleChange} />
            </div>
            <div className="form-field">
              <label>Skin Color</label>
              <input name="skin_color" value={form.skin_color} onChange={handleChange} />
            </div>
          </div>

          <div className="form-field">
            <label>Physique</label>
            <input name="physique" value={form.physique} onChange={handleChange} />
          </div>

          <button className="btn btn-primary btn-block" type="submit">Create Bot</button>
        </form>
      </div>
    </div>
  );
};

export default CreateBot;


