# app.py
from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json

from class_mapping import CLASS_NAMES

app = Flask(__name__)

model = tf.keras.models.load_model("mobilenet_traffic_sign.h5")

with open("labels.json", "r") as f:
    class_indices = json.load(f)
INDEX_TO_CLASSID = {v: int(k) for k, v in class_indices.items()}


def preprocess_image(image):
    image = image.convert("RGB").resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


def bentuk_hasil(class_id, confidence):
    info = CLASS_NAMES[class_id]
    return {
        "nama": info["name_id"],
        "kategori": info["category"],
        "keterangan": info["keterangan"],
        "confidence": round(confidence * 100, 2)
    }


# ---------- Routing halaman ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/klasifikasi")
def klasifikasi_page():
    return render_template("klasifikasi.html")

@app.route("/tentang-dataset")
def tentang_dataset_page():
    return render_template("tentang_dataset.html")

@app.route("/tentang-teknologi")
def tentang_teknologi_page():
    return render_template("tentang_teknologi.html")

@app.route("/tentang-kami")
def tentang_kami_page():
    return render_template("tentang_kami.html")

@app.route("/cara-penggunaan")
def cara_penggunaan_page():
    return render_template("cara_penggunaan.html")


# ---------- Endpoint prediksi ----------
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400

    file = request.files["file"]
    try:
        image = Image.open(io.BytesIO(file.read()))
    except Exception:
        return jsonify({"error": "File yang diunggah bukan gambar yang valid"}), 400

    processed = preprocess_image(image)
    prediction = model.predict(processed)[0]
    top3_idx = prediction.argsort()[-3:][::-1]

    hasil_utama = None
    alternatif = []
    for urutan, idx in enumerate(top3_idx):
        class_id = INDEX_TO_CLASSID[int(idx)]
        hasil = bentuk_hasil(class_id, float(prediction[idx]))
        if urutan == 0:
            hasil_utama = hasil
        else:
            alternatif.append(hasil)

    return jsonify({"hasil_utama": hasil_utama, "alternatif": alternatif})


if __name__ == "__main__":
    app.run(debug=True)