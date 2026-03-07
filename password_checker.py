"""
Password Strength Checker
A beginner-friendly Python project using Tkinter GUI
"""

import tkinter as tk
from tkinter import ttk
import re
import math


# ─────────────────────────────────────────────
#  CORE LOGIC  (no GUI here – pure functions)
# ─────────────────────────────────────────────

def calculate_entropy(password):
    """
    Entropy measures how unpredictable a password is.
    Formula: entropy = length × log2(pool_size)
    Higher entropy = harder to crack.
    """
    pool = 0
    if re.search(r'[a-z]', password):
        pool += 26          # lowercase letters
    if re.search(r'[A-Z]', password):
        pool += 26          # uppercase letters
    if re.search(r'\d', password):
        pool += 10          # digits
    if re.search(r'[!@#$%^&*(),.?":{}|<>_\-\+\=\[\]\\\/;\'`~]', password):
        pool += 32          # special characters

    if pool == 0:
        return 0
    return round(len(password) * math.log2(pool), 2)


def analyze_password(password):
    """
    Checks the password against several rules and returns:
    - score       (0–100)
    - label       (Weak / Fair / Good / Strong / Very Strong)
    - color       (for the progress bar)
    - suggestions (list of tips to improve)
    """
    if not password:
        return 0, "", "#444", []

    score = 0
    suggestions = []

    # ── Length checks ──────────────────────────────
    length = len(password)
    if length >= 8:
        score += 20
    else:
        suggestions.append("🔴 Use at least 8 characters")

    if length >= 12:
        score += 10
    else:
        suggestions.append("🟡 12+ characters makes it much stronger")

    if length >= 16:
        score += 10

    # ── Character-type checks ──────────────────────
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-\+\=\[\]\\\/;\'`~]', password))

    if has_lower:
        score += 10
    else:
        suggestions.append("🔴 Add lowercase letters (a–z)")

    if has_upper:
        score += 15
    else:
        suggestions.append("🔴 Add uppercase letters (A–Z)")

    if has_digit:
        score += 15
    else:
        suggestions.append("🟡 Add numbers (0–9)")

    if has_special:
        score += 20
    else:
        suggestions.append("🟡 Add special characters (!@#$% etc.)")

    # ── Penalty: repeated characters ──────────────
    if re.search(r'(.)\1{2,}', password):       # e.g. "aaa" or "111"
        score -= 10
        suggestions.append("⚠️  Avoid repeating characters (e.g. 'aaa')")

    # ── Penalty: common patterns ───────────────────
    common = ["password", "123456", "qwerty", "abc123", "letmein", "welcome"]
    if any(c in password.lower() for c in common):
        score -= 20
        suggestions.append("⚠️  Avoid common words like 'password' or '123456'")

    # ── Entropy bonus ──────────────────────────────
    entropy = calculate_entropy(password)
    if entropy > 50:
        score += 5
    if entropy > 70:
        score += 5

    # ── Clamp score between 0 and 100 ─────────────
    score = max(0, min(score, 100))

    # ── Map score to label + colour ───────────────
    if score < 20:
        label, color = "Very Weak",  "#e74c3c"
    elif score < 40:
        label, color = "Weak",       "#e67e22"
    elif score < 60:
        label, color = "Fair",       "#f1c40f"
    elif score < 80:
        label, color = "Strong",     "#2ecc71"
    else:
        label, color = "Very Strong","#27ae60"

    if not suggestions:
        suggestions.append("✅ Great password! No improvements needed.")

    return score, label, color, suggestions


# ─────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────

class PasswordCheckerApp:
    """Main application window."""

    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Strength Checker")
        self.root.geometry("520x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")   # dark navy background

        self.show_password = False          # toggle state
        self._build_ui()

    # ── Build every widget ────────────────────────
    def _build_ui(self):
        BG      = "#1a1a2e"
        CARD    = "#16213e"
        ACCENT  = "#0f3460"
        TEXT    = "#e0e0e0"
        MUTED   = "#a0a0b0"
        ENTRY_BG= "#0f3460"
        FONT_H  = ("Courier New", 22, "bold")
        FONT_B  = ("Courier New", 11)
        FONT_S  = ("Courier New", 10)

        # ── Title ─────────────────────────────────
        tk.Label(
            self.root, text="🔐 Password Strength Checker",
            bg=BG, fg="#e94560", font=FONT_H
        ).pack(pady=(28, 4))

        tk.Label(
            self.root, text="Check how strong your password really is",
            bg=BG, fg=MUTED, font=FONT_S
        ).pack(pady=(0, 20))

        # ── Input card ────────────────────────────
        card = tk.Frame(self.root, bg=CARD, bd=0, relief="flat")
        card.pack(padx=30, fill="x")

        tk.Label(card, text="Enter Password", bg=CARD, fg=MUTED,
                 font=FONT_S).pack(anchor="w", padx=16, pady=(14, 4))

        input_row = tk.Frame(card, bg=CARD)
        input_row.pack(padx=16, pady=(0, 14), fill="x")

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self._on_type)   # real-time update

        self.entry = tk.Entry(
            input_row,
            textvariable=self.password_var,
            show="●",                               # hide chars by default
            font=("Courier New", 14),
            bg=ENTRY_BG, fg=TEXT,
            insertbackground=TEXT,
            relief="flat", bd=0,
            width=26
        )
        self.entry.pack(side="left", ipady=8, padx=(0, 8))
        self.entry.focus()

        # Show / Hide toggle button
        self.toggle_btn = tk.Button(
            input_row,
            text="👁 Show",
            command=self._toggle_password,
            bg=ACCENT, fg=TEXT,
            font=FONT_S, relief="flat",
            cursor="hand2", bd=0,
            padx=8, pady=6
        )
        self.toggle_btn.pack(side="left")

        # ── Strength label ────────────────────────
        self.strength_label = tk.Label(
            self.root, text="", bg=BG, fg=TEXT,
            font=("Courier New", 13, "bold")
        )
        self.strength_label.pack(pady=(18, 4))

        # ── Progress bar ──────────────────────────
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Strength.Horizontal.TProgressbar",
            troughcolor=ACCENT,
            background="#e94560",   # will be updated dynamically
            thickness=18
        )
        self.progress = ttk.Progressbar(
            self.root, orient="horizontal",
            length=460, mode="determinate",
            style="Strength.Horizontal.TProgressbar"
        )
        self.progress.pack(padx=30)

        # Score + entropy row
        info_row = tk.Frame(self.root, bg=BG)
        info_row.pack(pady=(6, 16), padx=30, fill="x")

        self.score_lbl = tk.Label(info_row, text="Score: —", bg=BG,
                                  fg=MUTED, font=FONT_S)
        self.score_lbl.pack(side="left")

        self.entropy_lbl = tk.Label(info_row, text="Entropy: —", bg=BG,
                                    fg=MUTED, font=FONT_S)
        self.entropy_lbl.pack(side="right")

        # ── Suggestions box ───────────────────────
        tk.Label(self.root, text="💡 Suggestions", bg=BG,
                 fg=MUTED, font=FONT_S).pack(anchor="w", padx=30)

        sug_frame = tk.Frame(self.root, bg=CARD)
        sug_frame.pack(padx=30, fill="both", expand=True, pady=(4, 24))

        self.suggestions_text = tk.Text(
            sug_frame,
            bg=CARD, fg=TEXT,
            font=FONT_B,
            relief="flat", bd=0,
            state="disabled",       # read-only
            height=7,
            wrap="word",
            padx=12, pady=10,
            cursor="arrow"
        )
        self.suggestions_text.pack(fill="both", expand=True)

    # ── Real-time callback ────────────────────────
    def _on_type(self, *args):
        """Called every time the user types a character."""
        pwd = self.password_var.get()
        score, label, color, suggestions = analyze_password(pwd)
        self._update_ui(score, label, color, suggestions)

    # ── Update all widgets ────────────────────────
    def _update_ui(self, score, label, color, suggestions):
        # Progress bar value
        self.progress["value"] = score

        # Bar colour (re-configure style)
        style = ttk.Style()
        style.configure("Strength.Horizontal.TProgressbar", background=color)

        # Strength label
        self.strength_label.config(
            text=f"Strength: {label}" if label else "",
            fg=color
        )

        # Score + entropy
        pwd = self.password_var.get()
        entropy = calculate_entropy(pwd)
        self.score_lbl.config(text=f"Score: {score}/100")
        self.entropy_lbl.config(text=f"Entropy: {entropy} bits")

        # Suggestions text box
        self.suggestions_text.config(state="normal")
        self.suggestions_text.delete("1.0", "end")
        for tip in suggestions:
            self.suggestions_text.insert("end", tip + "\n")
        self.suggestions_text.config(state="disabled")

    # ── Show / Hide toggle ────────────────────────
    def _toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.entry.config(show="")
            self.toggle_btn.config(text="🙈 Hide")
        else:
            self.entry.config(show="●")
            self.toggle_btn.config(text="👁 Show")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()
