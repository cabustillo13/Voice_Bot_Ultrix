let isRecording = false;
let recognition;
let audioContext;
let mediaRecorder;
let waveformCanvas;
let waveformCtx;

document.addEventListener('DOMContentLoaded', () => {
    const recordBtn = document.getElementById('record-btn');
    const transcript = document.getElementById('transcript');
    waveformCanvas = document.getElementById('waveform');
    waveformCtx = waveformCanvas.getContext('2d');

    recordBtn.addEventListener('click', toggleRecording);

    if (!('webkitSpeechRecognition' in window)) {
        alert('Your browser does not support speech recognition. Please use Google Chrome.');
    } else {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = event => {
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }
            transcript.textContent = finalTranscript;
            if (finalTranscript) {
                speakText(finalTranscript);
            }
        };

        recognition.onerror = event => {
            console.error('Speech recognition error', event);
        };
    }
});

function toggleRecording() {
    isRecording = !isRecording;
    const recordBtn = document.getElementById('record-btn');

    if (isRecording) {
        recordBtn.textContent = 'Stop Recording';
        startRecording();
    } else {
        recordBtn.textContent = 'Start Recording';
        stopRecording();
    }
}

function startRecording() {
    if (recognition) {
        recognition.start();
    }

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createMediaStreamSource(stream);
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            visualizeAudio(source);
        }).catch(err => {
            console.error('Error accessing microphone', err);
        });
    }
}

function stopRecording() {
    if (recognition) {
        recognition.stop();
    }
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
    if (audioContext) {
        audioContext.close();
    }
}

function visualizeAudio(source) {
    const analyser = audioContext.createAnalyser();
    source.connect(analyser);
    analyser.fftSize = 2048;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
        if (!isRecording) return;

        requestAnimationFrame(draw);

        analyser.getByteTimeDomainData(dataArray);

        waveformCtx.fillStyle = 'rgba(200, 200, 200, 0.5)';
        waveformCtx.fillRect(0, 0, waveformCanvas.width, waveformCanvas.height);

        waveformCtx.lineWidth = 2;
        waveformCtx.strokeStyle = 'rgb(0, 0, 0)';

        waveformCtx.beginPath();
        const sliceWidth = waveformCanvas.width * 1.0 / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const v = dataArray[i] / 128.0;
            const y = v * waveformCanvas.height / 2;

            if (i === 0) {
                waveformCtx.moveTo(x, y);
            } else {
                waveformCtx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        waveformCtx.lineTo(waveformCanvas.width, waveformCanvas.height / 2);
        waveformCtx.stroke();
    };

    draw();
}

function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}
