# 🔐 Password Strength Checker

A beginner Python security project that analyzes password strength in real-time using a clean GUI built with Tkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=flat-square)
![Security](https://img.shields.io/badge/Domain-Cybersecurity-red?style=flat-square)
![Level](https://img.shields.io/badge/Level-Beginner-brightgreen?style=flat-square)

---

## 📸 Features

| Feature | Description |
|--------|-------------|
| 🟩 **Strength Meter** | Visual progress bar that fills and changes color (red → green) |
| ⚡ **Real-time Feedback** | Analyzes password as you type — no button needed |
| 👁️ **Show/Hide Toggle** | Reveal or hide your password with one click |
| 💡 **Smart Suggestions** | Tells you exactly what to fix to make it stronger |
| 📊 **Entropy Score** | Shows how mathematically unpredictable your password is |

---

## 🚀 How to Run

### 1. Make sure Python is installed
```bash
python --version   # Should be 3.8 or higher
```

### 2. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/password-strength-checker.git
cd password-strength-checker
```

### 3. Run the app (no installs needed — uses built-in libraries only!)
```bash
python password_checker.py
```

> ✅ No `pip install` required. Tkinter comes built into Python.

---

## 🧠 What I Learned

### 🔑 Regex (Regular Expressions)
Used to detect character types inside a password:
```python
import re

re.search(r'[A-Z]', password)   # checks for uppercase letters
re.search(r'\d', password)      # checks for digits
re.search(r'[!@#$]', password)  # checks for special chars
```

### 📐 Entropy Calculation
Password entropy measures unpredictability:
```
entropy = length × log₂(pool_size)
```
- **pool_size** = total possible characters (e.g. 26 lowercase + 10 digits = 36)
- **Higher entropy** = harder to brute-force crack

Example: `"hello"` → ~23 bits | `"H3ll0!xK"` → ~52 bits

### 🖥️ Tkinter GUI
- `tk.Entry` — text input field
- `ttk.Progressbar` — animated strength bar
- `tk.Text` — suggestions display box
- `trace_add("write", callback)` — triggers function on every keystroke

---

## 📁 Project Structure

```
password-strength-checker/
│
├── password_checker.py    # Main application (all-in-one)
└── README.md              # This file
```

---

## 🔍 How the Scoring Works

| Check | Points |
|-------|--------|
| Length ≥ 8 | +20 |
| Length ≥ 12 | +10 |
| Length ≥ 16 | +10 |
| Has lowercase | +10 |
| Has uppercase | +15 |
| Has digits | +15 |
| Has special chars | +20 |
| High entropy (>50 bits) | +5 |
| Very high entropy (>70 bits) | +5 |
| Repeated characters (e.g. "aaa") | −10 |
| Common patterns (e.g. "password") | −20 |

| Score | Label | Color |
|-------|-------|-------|
| 0–19 | Very Weak | 🔴 Red |
| 20–39 | Weak | 🟠 Orange |
| 40–59 | Fair | 🟡 Yellow |
| 60–79 | Strong | 🟢 Green |
| 80–100 | Very Strong | 💚 Dark Green |

---

## 🛡️ Security Concepts Covered

- **Entropy** — measuring password unpredictability
- **Character pools** — why mixing letters/numbers/symbols matters
- **Brute-force resistance** — how password length exponentially increases crack time
- **Common password attacks** — dictionary attacks and why "password123" is dangerous

---

## 🔮 Future Improvements (Ideas)

- [ ] Add a "Generate Strong Password" button
- [ ] Check against a list of 10,000 most common passwords
- [ ] Show estimated crack time (e.g. "cracked in 3 seconds vs 400 years")
- [ ] Export password analysis report as PDF
- [ ] Add dark/light theme toggle

---

## 👨‍💻 Author

**Maryam**  
🔗 [GitHub](https://github.com/Maryamikra1n) · [LinkedIn](https://linkedin.com/in/maryam-ikram-83543a392)

---

## 📜 License

This project is open source under the [MIT License](LICENSE).

---

> 💬 *"A strong password is your first line of defense. This tool helps you build one."*
