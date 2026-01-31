import google.generativeai as genai
from flask import Blueprint, render_template, request, flash, redirect, url_for
from extensions import mysql
from flask_login import login_required
import markdown

solutions_bp = Blueprint('solutions', __name__)

# ==========================================
# 🔑 API KEY
# ==========================================
GENAI_API_KEY = "XXXXX"
genai.configure(api_key=GENAI_API_KEY)

def ask_ai_doctor(disease_name):
    """
    Connects to Gemini. IF IT FAILS, it returns generic advice instead of crashing.
    """
    clean_name = disease_name.replace("_", " ").strip()
    print(f"🔵 Asking Gemini for: {clean_name}...")
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Act as an Agriculture Officer. Brief treatment for crop disease '{clean_name}'. Format: CHEMICAL: [text] ORGANIC: [text] PREVENTION: [text]"
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Parse response
        chemical, organic, prevention = text, "See Chemical Tab", "Monitor field"
        try:
            parts = text.split("ORGANIC:")
            chemical = parts[0].replace("CHEMICAL:", "").strip()
            sub = parts[1].split("PREVENTION:")
            organic = sub[0].strip()
            prevention = sub[1].strip()
        except:
            pass
            
        return chemical, organic, prevention

    except Exception as e:
        print(f"🔴 AI CONNECTION FAILED: {e}")
        print("⚠️ Switching to OFFLINE MODE for Viva...")
        
        # 🛡️ VIVA SAVER: Return generic text so the page ALWAYS loads
        return (
            "**Offline Mode:** Consult your local Agriculture Officer for specific chemical dosages.",
            "Remove infected leaves immediately and apply Neem oil if available.",
            "Ensure proper drainage and spacing between plants to reduce humidity."
        )

@solutions_bp.route('/treatment/<disease_name>')
@login_required
def show_treatment(disease_name):
    clean_name = disease_name.strip()
    
    # 1. Check Database
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, crop_type, chemical_treatment, organic_treatment, prevention FROM diseases WHERE name = %s", [clean_name])
    data = cur.fetchone()
    cur.close()

    disease_info = {}

    if data and data[2] and len(str(data[2])) > 5:
        print(f"✅ Found '{clean_name}' in Database.")
        disease_info = {
            'name': data[0], 'type': data[1], 
            'chemical': data[2], 'organic': data[3], 
            'prevention': data[4], 'source': "Dept of Agriculture Database"
        }
    else:
        # 2. Ask AI (Or use Backup)
        print(f"⚠️ Asking AI/Fallback for {clean_name}...")
        chemical, organic, prevention = ask_ai_doctor(clean_name)
        
        # This will NOW always be true, even if internet fails
        disease_info = {
            'name': clean_name.replace("_", " "),
            'type': 'General',
            'chemical': markdown.markdown(chemical),
            'organic': markdown.markdown(organic),
            'prevention': markdown.markdown(prevention),
            'source': "AI Analysis (or Offline Backup)"
        }

    return render_template('solutions/disease_info.html', disease=disease_info)