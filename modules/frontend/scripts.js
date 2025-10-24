// const API_URL = "https://YOUR-HF-SPACE-URL.hf.space/process";
const API_URL = "http://127.0.0.1:8000/process";

const fileInput = document.getElementById('imageInput');
const processBtn = document.getElementById('processBtn');
const originalImg = document.getElementById('original');
const processedImg = document.getElementById('processed');
const statusP = document.getElementById('status');

fileInput.addEventListener('change', () => {
    const f = fileInput.files[0];
    if (!f) return;

    if (!f.type.startsWith('image/')) {
        alert('Seleziona solo immagini!');
        fileInput.value = '';
        return;
    }

    originalImg.src = URL.createObjectURL(f);
    processedImg.src = '';
});

function getSelectedPhase() {
    const selected = document.querySelector('input[name="phase"]:checked');
    return selected ? selected.value : null;
}

processBtn.addEventListener('click', async () => {
    if (!fileInput.files[0]) {
        alert("Carica prima un'immagine.");
        return;
    }

    const phase = getSelectedPhase();
    if (!phase) {
        alert("Seleziona una fase.");
        return;
    }

    statusP.textContent = 'Invio al server...';
    statusP.style.color = 'goldenrod';
    processBtn.disabled = true;

    const form = new FormData();
    form.append('file', fileInput.files[0]);
    form.append('phase', phase);

    try {
        const res = await fetch(API_URL, {
            method: 'POST',
            body: form
        });

        if (!res.ok) {
            const txt = await res.text();
            throw new Error(`Server error: ${res.status} ${txt}`);
        }

        const data = await res.json();

        if (!data.processed_image) {
            throw new Error('Risposta API non contiene processed_image');
        }

        processedImg.src = 'data:image/png;base64,' + data.processed_image;
        statusP.textContent = 'Elaborazione Completata.';
        statusP.style.color = 'green';
    } catch (err) {
        console.error(err);
        statusP.textContent = 'Errore: ' + err.message;
        statusP.style.color = 'red';
    } finally {
        processBtn.disabled = false;
    }
});

