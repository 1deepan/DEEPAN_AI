/* ============================================================
   J.A.R.V.I.S — Frontend Logic
   Particles, Waveform, HUD Interactions, System Stats
   ============================================================ */

const outputLog = document.getElementById('output-log');
const cmdInput = document.getElementById('cmd-input');
const voiceBtn = document.getElementById('voice-btn');
const startTime = Date.now();

// ===== PARTICLES =====
(function initParticles() {
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let W, H, particles = [];

    function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
    window.addEventListener('resize', resize);
    resize();

    for (let i = 0; i < 100; i++) {
        particles.push({
            x: Math.random() * W, y: Math.random() * H,
            vx: (Math.random() - 0.5) * 0.5, vy: (Math.random() - 0.5) * 0.5,
            r: Math.random() * 2 + 0.5
        });
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);
        ctx.fillStyle = 'rgba(0,200,255,0.35)';
        particles.forEach(p => {
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
            if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
        });
        // Connect nearby particles
        ctx.strokeStyle = 'rgba(0,200,255,0.06)';
        ctx.lineWidth = 0.5;
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = dx * dx + dy * dy;
                if (dist < 18000) {
                    ctx.beginPath(); ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y); ctx.stroke();
                }
            }
        }
        requestAnimationFrame(draw);
    }
    draw();
})();

// ===== WAVEFORM =====
const waveCanvas = document.getElementById('waveform');
const wCtx = waveCanvas.getContext('2d');
let waveActive = false;

function resizeWave() { waveCanvas.width = 120; waveCanvas.height = 40; }
resizeWave();

function drawWave() {
    wCtx.clearRect(0, 0, 120, 40);
    wCtx.strokeStyle = waveActive ? 'rgba(0,200,255,0.7)' : 'rgba(0,200,255,0.15)';
    wCtx.lineWidth = 1.5;
    wCtx.beginPath();
    const t = Date.now() / 200;
    for (let x = 0; x < 120; x++) {
        const amp = waveActive ? 12 : 2;
        const y = 20 + Math.sin(x * 0.08 + t) * amp * Math.sin(x * 0.02 + t * 0.5);
        x === 0 ? wCtx.moveTo(x, y) : wCtx.lineTo(x, y);
    }
    wCtx.stroke();
    requestAnimationFrame(drawWave);
}
drawWave();

// ===== TIME & UPTIME =====
function updateClock() {
    const now = new Date();
    const d = document.getElementById('live-date');
    const t = document.getElementById('live-time');
    if (d) d.textContent = now.toLocaleDateString('en-US', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' });
    if (t) t.textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    // Uptime
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const h = String(Math.floor(elapsed / 3600)).padStart(2, '0');
    const m = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0');
    const s = String(elapsed % 60).padStart(2, '0');
    const u = document.getElementById('uptime');
    if (u) u.textContent = `UPTIME: ${h}:${m}:${s}`;
}
setInterval(updateClock, 1000);
updateClock();

// Set initial time on welcome message
const initTimeEl = document.getElementById('init-time');
if (initTimeEl) initTimeEl.textContent = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

// ===== SYSTEM STATS =====
async function fetchStats() {
    try {
        const res = await fetch('/stats');
        if (!res.ok) return;
        const d = await res.json();
        setBar('cpu', d.cpu); setBar('ram', d.ram);
        setBar('bat', d.battery); setBar('disk', d.disk);
    } catch (e) { /* silent */ }
}

function setBar(id, val) {
    const fill = document.getElementById(id + '-fill');
    const txt = document.getElementById(id + '-val');
    if (fill && val !== null && val !== undefined) {
        fill.style.width = val + '%';
        if (txt) txt.textContent = val + '%';
    }
}

fetchStats();
setInterval(fetchStats, 5000);

// ===== PARSE RESPONSE =====
function parseResponse(text) {
    // Convert [CODE:lang]...[/CODE] to styled code blocks
    text = text.replace(/\[LESSON:\s*(.*?)\]/g, '<span class="lesson-title">$1</span>');
    text = text.replace(/\[CODE:(\w+)\]([\s\S]*?)\[\/CODE\]/g,
        (_, lang, code) => `<span class="code-label">${lang.toUpperCase()}</span><span class="code-block">${escapeHtml(code.trim())}</span>`
    );
    // Bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong style="color:var(--primary)">$1</strong>');
    // Bullet points
    text = text.replace(/^• /gm, '<span style="color:var(--primary)">▸ </span>');
    // Images
    text = text.replace(/\[IMAGE:\s*(.*?)\]/g, '<div class="log-img-wrap"><img src="$1" class="log-img" alt="Generated Intelligence Analogue"><div class="img-overlay"></div></div>');
    return text;
}

function escapeHtml(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ===== ACTION HANDLER =====
function handleAction(action) {
    if (!action) return;
    console.log("Handling action:", action);

    // If running inside the Android WebView, try to call native methods
    const isAndroid = typeof Android !== 'undefined';

    switch (action.type) {
        case 'open_url':
            if (isAndroid && Android.launchUrl) {
                Android.launchUrl(action.url);
            } else {
                window.open(action.url, '_blank');
            }
            break;
        case 'play_youtube':
            const ytUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(action.query)}`;
            if (isAndroid && Android.playYoutube) {
                Android.playYoutube(action.query);
            } else if (isAndroid && Android.launchUrl) {
                Android.launchUrl(ytUrl);
            } else {
                window.open(ytUrl, '_blank');
            }
            break;
        case 'open_app':
            if (isAndroid && Android.launchApp) {
                Android.launchApp(action.name || action.url);
            } else if (action.url) {
                window.open(action.url, '_blank');
            }
            break;
    }
}

// ===== ADD LOG ENTRY =====
function addLog(text, who) {
    const entry = document.createElement('div');
    entry.className = `log-entry ${who === 'JARVIS' ? 'jarvis-log' : 'user-log'}`;

    const time = new Date().toLocaleTimeString('en-US', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
    const timeEl = document.createElement('span'); timeEl.className = 'log-time'; timeEl.textContent = time;
    const whoEl = document.createElement('span'); whoEl.className = 'log-who'; whoEl.textContent = who;
    const textEl = document.createElement('div'); textEl.className = 'log-text';

    if (who === 'JARVIS') {
        textEl.innerHTML = parseResponse(text);
    } else {
        textEl.textContent = text;
    }

    entry.appendChild(timeEl);
    entry.appendChild(whoEl);
    entry.appendChild(textEl);
    outputLog.appendChild(entry);
    outputLog.scrollTop = outputLog.scrollHeight;
}

function showProcessing() {
    const el = document.createElement('div');
    el.id = 'proc-indicator';
    el.className = 'log-entry jarvis-log';
    el.innerHTML = '<span class="log-time">' + new Date().toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit',second:'2-digit'}) + '</span><span class="log-who">JARVIS</span><div class="processing-indicator"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>';
    outputLog.appendChild(el);
    outputLog.scrollTop = outputLog.scrollHeight;
}

function hideProcessing() {
    const el = document.getElementById('proc-indicator');
    if (el) el.remove();
}

// ===== SEND COMMAND =====
async function sendCommand() {
    const text = cmdInput.value.trim();
    if (!text) return;
    addLog(text, 'USER');
    cmdInput.value = '';
    cmdInput.focus();
    waveActive = true;
    showProcessing();

    try {
        const res = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        if (!res.ok) throw new Error('Server error ' + res.status);
        const data = await res.json();
        hideProcessing();
        waveActive = false;
        addLog(data.reply, 'JARVIS');
        
        // Handle client-side action
        if (data.action) {
            handleAction(data.action);
        }
    } catch (err) {
        hideProcessing();
        waveActive = false;
        addLog('System error: ' + err.message, 'JARVIS');
    }
}

// ===== VOICE =====
async function voiceCommand() {
    voiceBtn.classList.add('listening');
    waveActive = true;
    addLog('Voice input activated. Listening...', 'JARVIS');

    try {
        const res = await fetch('/voice');
        if (!res.ok) throw new Error('Server error ' + res.status);
        const data = await res.json();
        voiceBtn.classList.remove('listening');
        waveActive = false;
        // Remove "Listening..." entry
        const entries = outputLog.querySelectorAll('.log-entry');
        const last = entries[entries.length - 1];
        if (last && last.textContent.includes('Listening')) last.remove();

        if (data.heard) addLog(data.heard, 'USER');
        addLog(data.reply, 'JARVIS');

        // Handle client-side action
        if (data.action) {
            handleAction(data.action);
        }
    } catch (err) {
        voiceBtn.classList.remove('listening');
        waveActive = false;
        addLog('Voice error: ' + err.message, 'JARVIS');
    }
}

// ===== QUICK COMMAND =====
function qc(cmd) {
    if (cmd.endsWith(' ')) {
        cmdInput.value = cmd;
        cmdInput.focus();
        return;
    }
    cmdInput.value = cmd;
    sendCommand();
}

// ===== ENTER KEY =====
cmdInput.addEventListener('keydown', e => { if (e.key === 'Enter') sendCommand(); });

// ===== FOCUS =====
window.addEventListener('load', () => {
    cmdInput.focus();
    // Register Service Worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js').catch(err => console.log("SW error:", err));
    }
});

// ===== FILE UPLOAD =====
function triggerUpload() {
    document.getElementById('file-input').click();
}

async function handleFileUpload(input) {
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    addLog(`Uploading file: ${file.name}...`, 'USER');
    
    const formData = new FormData();
    formData.append('file', file);

    showProcessing();
    try {
        const res = await fetch('/upload', { method: 'POST', body: formData });
        const data = await res.json();
        hideProcessing();
        addLog(data.reply, 'JARVIS');
        
        if (data.notes) {
            // Give JARVIS a small delay before showing notes for better effect
            setTimeout(() => {
                addLog(`**Tactical Document Analysis:**\n\n${data.notes}`, 'JARVIS');
            }, 800);
        }
    } catch (err) {
        hideProcessing();
        addLog('Upload failed: ' + err.message, 'JARVIS');
    }
    input.value = ''; // Reset
}
