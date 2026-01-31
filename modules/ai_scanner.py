import os
import numpy as np
from flask import Blueprint, render_template, request, flash, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

scanner_bp = Blueprint('scanner', __name__)

# ==========================================
# 🧠 1. LOAD BOTH MODELS
# ==========================================
# PADDY MODEL
try:
    paddy_model = load_model('models/paddy_model.h5')
    print("✅ Paddy Model Loaded!")
except:
    paddy_model = None
    print("⚠️ Paddy Model NOT found (Check models/paddy_model.h5)")

# PLANT MODEL
try:
    plant_model = load_model('models/plant_model.h5')
    print("✅ General Plant Model Loaded!")
except:
    plant_model = None
    print("⚠️ Plant Model NOT found (Check models/plant_model.h5)")

# ==========================================
# 📝 2. DEFINE EXACT CLASS LISTS
# ==========================================
PADDY_CLASSES = [
    "bacterial_leaf_blight", "bacterial_leaf_streak", "bacterial_panicle_blight",
    "blast", "brown_spot", "dead_heart", "downy_mildew", "hispa", "normal", "tungro"
]

PLANT_CLASSES = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry___Powdery_mildew", "Cherry___healthy",
    "Corn___Gray_leaf_spot", "Corn___Common_rust", "Corn___Northern_Leaf_Blight", "Corn___healthy",
    "Grape___Black_rot", "Grape___Esca", "Grape___Leaf_blight", "Grape___healthy",
    "Orange___Haunglongbing", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper_bell___Bacterial_spot", "Pepper_bell___healthy", 
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy", 
    "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew", 
    "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot", 
    "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold", 
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites", "Tomato___Target_Spot", 
    "Tomato___Yellow_Leaf_Curl", "Tomato___Mosaic_virus", "Tomato___healthy"
]

def model_predict(img_path, model, class_list):
    # 1. Resize Image
    img = image.load_img(img_path, target_size=(224, 224))
    
    # 2. Convert to Array
    x = image.img_to_array(img)
    
    # 🛑 THE FIX: We removed the division by 255.0
    # Many models (like Teachable Machine or standard Transfer Learning) 
    # prefer raw pixel values (0-255) instead of normalized (0-1).
    # x = x / 255.0  <-- COMMENTED OUT TO FIX "BLIND AI" ISSUE
    
    x = np.expand_dims(x, axis=0)

    # 3. Predict
    preds = model.predict(x)
    pred_index = np.argmax(preds, axis=1)[0]
    confidence = np.max(preds)
    
    # --- DEBUGGING PRINT ---
    print(f"\n📊 Prediction Index: {pred_index}")
    print(f"🎯 Confidence Score: {confidence}")
    
    if pred_index < len(class_list):
        result = class_list[pred_index]
    else:
        result = f"Unknown_Class_{pred_index}"
        
    print(f"📸 Final Result: {result}\n")
    return result

@scanner_bp.route('/scan', methods=['GET', 'POST'])
def scan_crop():
    if request.method == 'POST':
        crop_type = request.form.get('crop')  # 'paddy' or 'plant'
        
        if 'image' not in request.files: return redirect(request.url)
        file = request.files['image']
        if file.filename == '': return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join("static/uploads", filename)
            file.save(filepath)

            try:
                # 🧠 SWITCH BRAINS
                if crop_type == 'paddy':
                    if paddy_model:
                        # Use Paddy Model & List
                        prediction = model_predict(filepath, paddy_model, PADDY_CLASSES)
                    else:
                        flash("Paddy Model Error", "danger")
                        return redirect(request.url)
                else:
                    if plant_model:
                        # Use Plant Model & List
                        prediction = model_predict(filepath, plant_model, PLANT_CLASSES)
                    else:
                        flash("Plant Model Error", "danger")
                        return redirect(request.url)

                return redirect(url_for('solutions.show_treatment', disease_name=prediction))
                
            except Exception as e:
                print(f"Error: {e}")
                return redirect(request.url)

    return render_template('scanner/result.html')