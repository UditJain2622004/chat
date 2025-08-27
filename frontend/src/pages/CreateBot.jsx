/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext.jsx";

const behaviourOptions = [
  {value: "friendly", label: "Friendly"},
  {value: "neutral", label: "Neutral"},
  {value: "sassy", label: "Sassy"},
  {value: "snarky", label: "Snarky"},
  {value: "sarcastic", label: "Sarcastic"},
  {value: "witty", label: "Witty"},
  {value: "dry", label: "Dry"},
  {value: "funny", label: "Funny"},
  {value: "serious", label: "Serious"},
  {value: "professional", label: "Professional"},
  {value: "cute", label: "Cute"},
  {value: "sexy", label: "Sexy"},
  {value: "hot", label: "Hot"},
  {value: "cool", label: "Cool"},
  {value: "chill", label: "Chill"},
  {value: "laid_back", label: "Laid Back"},
  {value: "relaxed", label: "Relaxed"},
];

const CreateBot = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    picture: "",
    likings: "",
    behaviour: behaviourOptions[0].value,
    ethnicity: "Any",
    age: null,
    hair_color: "Any",
    hair_style: "Any",
    eyes: "Any",
    skin_color: "Any",
    physique: "Any",
    relationship_with_user: "Any",
    backstory: "",
    prologue: "",
  });
  const { dbUserId, isAuthReady } = useAuth();
  const [step, setStep] = useState(1);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (!dbUserId) return; // cannot create without owner
      const payload = {
        bot_details: {
          name: form.name.trim(),
          picture: form.picture.trim() || undefined,
          likings: form.likings
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
          behaviour: form.behaviour,
          ethnicity: form.ethnicity || "Any",
          age: form.age || null,
          hair_color: form.hair_color || "Any",
          hair_style: form.hair_style || "Any",
          eyes: form.eyes || "Any",
          skin_color: form.skin_color || "Any",
          physique: form.physique || "Any",
          relationship_with_user: form.relationship_with_user || "Any",
          backstory: (form.backstory || "").trim() || undefined,
          prologue: (form.prologue || "").trim() || undefined,
        },
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
          <div className="form-steps">Step {step} of 3</div>

          {step === 1 && (
            <>
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

              <div className="form-actions">
                <button type="button" className="btn btn-primary btn-block" onClick={() => setStep(2)}>Next</button>
              </div>
            </>
          )}

          {step === 2 && (
            <>
              <div className="form-grid-2">
                <div className="form-field">
                  <label>Ethnicity</label>
                  <input name="ethnicity" value={form.ethnicity} onChange={handleChange} />
                </div>
                <div className="form-field">
                  <label>Hair</label>
                  <input name="hair_color" value={form.hair_color} onChange={handleChange} />
                </div>
                <div className="form-field">
                  <label>Hair Style</label>
                  <input name="hair_style" value={form.hair_style} onChange={handleChange} />
                </div>
                <div className="form-field">
                <label>Physique</label>
                <input name="physique" value={form.physique} onChange={handleChange} />
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
                <label>Relationship</label>
                <input name="relationship_with_user" value={form.relationship_with_user} onChange={handleChange} />
              </div>

              

              <div className="form-actions">
                <button type="button" className="btn" onClick={() => setStep(1)}>Back</button>
                <button type="button" className="btn btn-primary btn-block" onClick={() => setStep(3)}>Next</button>
              </div>
            </>
          )}

          {step === 3 && (
            <>
              <div className="form-field">
                <label>Backstory</label>
                <textarea
                  name="backstory"
                  value={form.backstory}
                  onChange={handleChange}
                  placeholder="Who are they? Key life events, motivations, quirks..."
                  rows={4}
                />
              </div>

              <div className="form-field">
                <label>Prologue</label>
                <textarea
                  name="prologue"
                  value={form.prologue}
                  onChange={handleChange}
                  placeholder="How does their story begin when meeting the user?"
                  rows={3}
                />
              </div>

              <div className="form-actions">
                <button type="button" className="btn" onClick={() => setStep(2)}>Back</button>
                <button className="btn btn-primary btn-block" type="submit">Create Bot</button>
              </div>
            </>
          )}
        </form>
      </div>
    </div>
  );
};

export default CreateBot;


