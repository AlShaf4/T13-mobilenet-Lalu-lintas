// scripts.js
// Upload & drag-drop foto, kirim ke /predict, tampilkan hasil,
// navigasi mobile (hamburger), dan animasi scroll reveal

document.addEventListener("DOMContentLoaded", function () {

    // ---------- Navbar mobile ----------
    const navToggle = document.getElementById("navToggle");
    const navMenu = document.getElementById("navMenu");
    if (navToggle) {
        navToggle.addEventListener("click", () => navMenu.classList.toggle("show"));
    }

    // ---------- Scroll reveal ----------
    const revealEls = document.querySelectorAll(".reveal");
    if (revealEls.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) entry.target.classList.add("visible");
            });
        }, { threshold: 0.15 });
        revealEls.forEach((el) => observer.observe(el));
    }

    // ---------- Upload & klasifikasi ----------
    const uploadBox = document.getElementById("uploadBox");
    if (!uploadBox) return;  // halaman selain klasifikasi.html berhenti di sini

    const fileInput = document.getElementById("fileInput");
    const previewArea = document.getElementById("previewArea");
    const previewImage = document.getElementById("previewImage");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const validationMessage = document.getElementById("validationMessage");
    const loadingArea = document.getElementById("loadingArea");
    const progressBarFill = document.getElementById("progressBarFill");
    const resultCard = document.getElementById("resultCard");

    let selectedFile = null;

    uploadBox.addEventListener("click", () => fileInput.click());

    uploadBox.addEventListener("dragover", (e) => { e.preventDefault(); uploadBox.classList.add("dragover"); });
    uploadBox.addEventListener("dragleave", () => uploadBox.classList.remove("dragover"));
    uploadBox.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadBox.classList.remove("dragover");
        if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        if (!file.type.startsWith("image/")) {
            validationMessage.textContent = "File yang dipilih harus berupa gambar (JPG/PNG).";
            return;
        }
        validationMessage.textContent = "";
        selectedFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewArea.style.display = "block";
        };
        reader.readAsDataURL(file);

        analyzeBtn.disabled = false;
        resultCard.style.display = "none";
    }

    analyzeBtn.addEventListener("click", () => {
        if (!selectedFile) {
            validationMessage.textContent = "Silakan pilih foto rambu terlebih dahulu.";
            return;
        }

        validationMessage.textContent = "";
        resultCard.style.display = "none";
        loadingArea.style.display = "block";
        analyzeBtn.disabled = true;

        let progress = 0;
        const progressInterval = setInterval(() => {
            progress = Math.min(progress + 10, 90);
            progressBarFill.style.width = progress + "%";
        }, 150);

        const formData = new FormData();
        formData.append("file", selectedFile);

        fetch("/predict", { method: "POST", body: formData })
            .then((res) => res.json())
            .then((data) => {
                clearInterval(progressInterval);
                progressBarFill.style.width = "100%";
                setTimeout(() => {
                    loadingArea.style.display = "none";
                    progressBarFill.style.width = "0%";
                    analyzeBtn.disabled = false;
                    if (data.error) { validationMessage.textContent = data.error; return; }
                    tampilkanHasil(data);
                }, 300);
            })
            .catch(() => {
                clearInterval(progressInterval);
                loadingArea.style.display = "none";
                analyzeBtn.disabled = false;
                validationMessage.textContent = "Terjadi kesalahan saat menghubungi server, coba lagi.";
            });
    });

    function tampilkanHasil(data) {
        const utama = data.hasil_utama;

        document.getElementById("resultTag").textContent =
            utama.kategori === "wajib" ? "Rambu Wajib / Petunjuk" : "Rambu Larangan / Bahaya";

        const resultName = document.getElementById("resultName");
        resultName.textContent = utama.nama;
        resultName.className = "result-name " + utama.kategori;

        document.getElementById("confidenceFill").style.width = utama.confidence + "%";
        document.getElementById("confidenceValue").textContent = utama.confidence + "%";
        document.getElementById("resultDescription").textContent = utama.keterangan;

        const alternatifList = document.getElementById("alternatifList");
        alternatifList.innerHTML = "";
        data.alternatif.forEach((item) => {
            const li = document.createElement("li");
            li.innerHTML = `<span>${item.nama}</span><span>${item.confidence}%</span>`;
            alternatifList.appendChild(li);
        });

        resultCard.style.display = "block";
    }
});
