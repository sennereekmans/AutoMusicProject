# 🎵 Automatische AI-muziekworkflow (Gratis)

## ✅ Workflow Overzicht

1. **Magenta** → genereert **MIDI patterns** (kick, snare, hats, bassline).
2. **LMMS + Vital + gratis samples** → synths en drums toevoegen.
3. **Python script** → alles samenvoegen en exporteren naar **WAV**.
4. **Spotify upload** → via **Spotipy API** (vereist een verified artist account).

---

## 🔹 Tools & Software

- **Magenta** (Python, open-source AI muziek)
  - [https://magenta.tensorflow.org](https://magenta.tensorflow.org)
- **LMMS** (gratis DAW)
  - [https://lmms.io](https://lmms.io)
- **Synths:**
  - **Vital** (gratis wavetable synth) → [https://vital.audio](https://vital.audio)
  - **Helm** (gratis synth) → [https://tytel.org/helm/](https://tytel.org/helm/)
- **Gratis drumkits:**
  - Zoek naar *"Free DnB sample packs"* of gebruik LMMS stock kits.

---

## ✅ Stappenplan

### **1. MIDI Genereren (Magenta)**
- Installeer Magenta:
  ```bash
  pip install magenta
  ```

- Genereer een drumloop:
  ```bash
  drumify --input_midi input.mid --output_midi drum_pattern.mid
  ```

- Genereer baslijnen en melodieën:
  ```bash
  melody_rnn_generate --config=attention_rnn --bundle_file=melody_rnn.mag --output_dir=./midi --num_outputs=
  ```

### **2. MIDI in LMMS Laden**

- Open LMMS en:

    - Voeg Vital als synth toe voor de bassline.

    - Voeg gratis drum samples toe voor kicks, snares en hats.

    - Gebruik de gegenereerde MIDI’s in het LMMS piano roll.


### **3. Automatisatie via Python**

- Gebruik een Python-script om:

    - MIDI → LMMS project te mappen.

    - LMMS in headless mode te renderen:
      ```bash
      lmms --export mytrack.wav myproject.mmp
      ```


### **4. Automatisch Uploaden naar Spotify**

- Installeer Spotipy:
  ```bash
  pip install spotipy
  ```
- Upload track via Spotify API (vereist Spotify for Artists account).

### **✅ Resultaat:**

- Volledig geautomatiseerde Drum & Bass / Techno track.

- Klaar om op Spotify gezet te worden, zonder betaalde tools!