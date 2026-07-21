# train_model.py

import os
import json
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')  # biar bisa jalan tanpa tampilan GUI (server/headless)
import matplotlib.pyplot as plt
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

print(tf.__version__)

# 1. Load MobileNetV2 tanpa top layer, freeze semua layer
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# 2. Tambah layer klasifikasi baru (43 kelas rambu)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
outputs = Dense(43, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=outputs)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# 3. ImageDataGenerator (horizontal_flip dimatikan, rambu tidak boleh dicerminkan)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.15,
    horizontal_flip=False,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    'dataset/Train', target_size=(224, 224), batch_size=32,
    class_mode='categorical', subset='training'
)
val_generator = train_datagen.flow_from_directory(
    'dataset/Train', target_size=(224, 224), batch_size=32,
    class_mode='categorical', subset='validation'
)

# Simpan mapping index generator -> nomor kelas asli (folder diurutkan alfabetis, bukan angka)
with open('labels.json', 'w') as f:
    json.dump(train_generator.class_indices, f)

# 4. Training
epochs = 15
history = model.fit(train_generator, validation_data=val_generator, epochs=epochs)

# 5. Evaluasi pakai data validasi (folder Test tidak punya label valid)
val_loss, val_acc = model.evaluate(val_generator)
print(f'Akurasi Validasi Model: {val_acc:.4f}')

# 6. Simpan model
model.save('mobilenet_traffic_sign.h5')

# 7. Buat & simpan grafik akurasi + loss ke static/img
os.makedirs('static/img', exist_ok=True)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Akurasi Training', color='#1E4B8F')
plt.plot(history.history['val_accuracy'], label='Akurasi Validasi', color='#2E9E5B')
plt.title('Grafik Akurasi Model')
plt.xlabel('Epoch')
plt.ylabel('Akurasi')
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Loss Training', color='#C0392B')
plt.plot(history.history['val_loss'], label='Loss Validasi', color='#E67E22')
plt.title('Grafik Loss Model')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('static/img/grafik_training.png', dpi=150)
plt.close()

print("Model tersimpan sebagai mobilenet_traffic_sign.h5")
print("Grafik training tersimpan di static/img/grafik_training.png")
