/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext.jsx";

const behaviourOptions = [
  { value: "soft", label: "Soft" },
  { value: "between_soft_and_hard", label: "Between Soft and Hard" },
  { value: "hard", label: "Hard" },
  { value: "ease_into_it", label: "Ease into it" },
];

const CreateBot = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
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
  const { dbUserId, isAuthReady } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (!dbUserId) return; // cannot create without owner
      const payload = {
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


