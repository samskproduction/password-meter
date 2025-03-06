import streamlit as st
import re
import math

# Streamlit Page Config
st.set_page_config(page_title="🔐 Password Strength Meter", layout="centered")

# Title with Emoji
st.markdown("<h1 style='text-align: center;'>🔐 Password Strength Meter</h1>", unsafe_allow_html=True)

# Function to calculate password entropy
def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(not c.isalnum() for c in password):
        charset_size += 32  # Approximate number of special characters
    if charset_size == 0:
        return 0
    return math.log2(charset_size) * len(password)

# Password Strength Criteria
requirements = [
    {"label": "At least 8 characters", "regex": r".{8,}"},
    {"label": "At least one lowercase letter", "regex": r"[a-z]"},
    {"label": "At least one uppercase letter", "regex": r"[A-Z]"},
    {"label": "At least one number", "regex": r"\d"},
    {"label": "At least one special character", "regex": r"[^\w]"}
]

# Password Input Field
password = st.text_input("Enter your password:", type="password")

if password:
    # Evaluate Password Against Requirements
    passed_requirements = [req for req in requirements if re.search(req["regex"], password)]
    score = len(passed_requirements) / len(requirements)

    # Calculate Entropy
    entropy = calculate_entropy(password)

    # Determine Strength
    if score == 1 and entropy > 60:
        feedback = "🚀 Super Strong"
        color = "#1f7a1f"
    elif score >= 0.8 and entropy > 50:
        feedback = "💪 Strong"
        color = "#2d8f2d"
    elif score >= 0.6 and entropy > 40:
        feedback = "🟠 Moderate"
        color = "#d98e00"
    else:
        feedback = "❌ Weak"
        color = "#c70039"

    # Display Strength Meter
    st.markdown(f"<h4 style='color: {color};'>Password Strength: {feedback}</h4>", unsafe_allow_html=True)
    st.progress(score)

    # Display Met & Unmet Requirements
    st.markdown("### ✅ Requirements Check")
    for req in requirements:
        is_met = bool(re.search(req["regex"], password))
        icon = "✅" if is_met else "❌"
        st.markdown(f"{icon} {req['label']}")

    # Show Entropy Score
    st.markdown(f"🔢 **Entropy Score:** {entropy:.2f} bits (Higher is better)")

else:
    st.warning("🔑 Enter a password to check its strength!")

# Footer with Security Tips
st.markdown("---")
st.markdown("""
### 🔐 Password Security Tips:
- Use a **password manager** for stronger, unique passwords.
- Avoid **dictionary words** or **personal information** in passwords.
- Enable **Two-Factor Authentication (2FA)** wherever possible.
- Consider passphrases instead of single-word passwords.
""")
