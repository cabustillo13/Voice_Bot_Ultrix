let isRecording = false; // Flag to track recording state
let recognition; // Speech recognition object
let audioContext; // Audio context for waveform visualization
let mediaRecorder; // Media recorder for audio stream
let waveformCanvas; // Canvas element for waveform
let waveformCtx; // Canvas 2D context

document.addEventListener('DOMContentLoaded', () => {
    const recordBtn = document.getElementById('record-btn');
    const languageSelect = document.getElementById('language-select');
    const transcript = document.getElementById('transcript');
    const processedTranscript = document.getElementById('processed-transcript');
    waveformCanvas = document.getElementById('waveform');
    waveformCtx = waveformCanvas.getContext('2d');

    recordBtn.addEventListener('click', toggleRecording);

    // Check if the browser supports the Web Speech API
    if (!('webkitSpeechRecognition' in window)) {
        alert('Your browser does not support speech recognition. Please use Google Chrome.');
    } else {
        // Initialize the speech recognition object
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = event => {
            let finalTranscript = '';
            // Aggregate the final results
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }
            transcript.textContent = finalTranscript; // Display the transcript
            if (finalTranscript) {
                // Display the transcribed text first
                transcript.textContent = finalTranscript;
                // Call the server to process the text
                processAndDisplayText(finalTranscript);
            }
        };

        recognition.onerror = event => {
            console.error('Speech recognition error', event);
        };

        // Set the initial language
        recognition.lang = languageSelect.value;

        // Update the language when the selection changes
        languageSelect.addEventListener('change', () => {
            recognition.lang = languageSelect.value;
        });
    }
});

// Function to toggle recording state
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

// Function to start recording
function startRecording() {
    if (recognition) {
        recognition.start();
    }

    // Get access to the user's microphone
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createMediaStreamSource(stream);
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            visualizeAudio(source); // Start visualizing audio
        }).catch(err => {
            console.error('Error accessing microphone', err);
        });
    }
}

// Function to stop recording
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

// Function to visualize audio
function visualizeAudio(source) {
    const analyser = audioContext.createAnalyser();
    source.connect(analyser);
    analyser.fftSize = 2048;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    // Recursive function to draw the waveform
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

    draw(); // Start the drawing loop
}

// Function to process and display the transcribed text
async function processAndDisplayText(text) {
    try {
        const response = await fetch('/process_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        const result = await response.json();
        const processedTranscript = document.getElementById('processed-transcript');
        processedTranscript.textContent = result.text;
        speakText(result.text);
    } catch (error) {
        console.error('Error processing text:', error);
    }
}

// Function to speak the text
function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}
