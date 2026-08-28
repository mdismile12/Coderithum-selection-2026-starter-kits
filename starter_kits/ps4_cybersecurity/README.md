# 🛡️ Cybersecurity Starter Kit — PS4: "Vulnerable Site Attack & Defense"

## 📁 Repository Structure
- `vulnerable_app/app.py`: Flask Web Application containing pre-seeded security vulnerabilities.
- `requirements.txt`: Python dependencies (`flask`, `pyjwt`).

## 🚀 How to Run the Vulnerable Web App
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the vulnerable server:
   ```bash
   python vulnerable_app/app.py
   ```
3. Open your browser or Postman and navigate to: `http://127.0.0.1:5000`

## 📝 Candidate Deliverables (2 Hours)
1. **Identify Vulnerabilities:** Discover at least 2 security vulnerabilities in the web application.
2. **Proof-of-Concept (PoC):** Document manual exploit payloads or cURL command scripts triggering the flaws.
3. **Risk Scoring:** Assign CVSS v3.1 severity scores and explain business impact.
4. **Code Remediation:** Provide exact Python source-code patches (`git diff` or fixed `app.py`) eliminating the vulnerabilities.
