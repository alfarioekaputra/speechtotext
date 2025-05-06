from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
import uuid
import threading
import time
import logging
from pydub import AudioSegment
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_audio'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory store for active transcription sessions
active_sessions = {}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/start_transcription', methods=['POST'])
def start_transcription():
    """Start a new transcription session"""
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        'text': '',
        'text_en': '',
        'is_active': True,
        'last_update': time.time()
    }
    return jsonify({'session_id': session_id})

@app.route('/stop_transcription', methods=['POST'])
def stop_transcription():
    """Stop an active transcription session"""
    session_id = request.json.get('session_id')
    if session_id in active_sessions:
        active_sessions[session_id]['is_active'] = False
    return jsonify({'success': True})

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """Process audio file and return transcription"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    session_id = request.form.get('session_id')
    if not session_id or session_id not in active_sessions:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    audio_file = request.files['audio']
    temp_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}.wav")
    
    try:
        audio_file.save(temp_filename)
        
        # Convert audio to WAV if it isn't already in that format
        audio = AudioSegment.from_file(temp_filename)
        audio.export(temp_filename, format="wav")
        
        # Process the audio file with SpeechRecognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='id-ID')  # Default to Indonesian
            text_en = GoogleTranslator(source='id', target='en').translate(text)
            # transcribed_text = f"ID: {text}\nEN: {text_en}"
            
            # Update the session with new transcription
            if active_sessions[session_id]['is_active']:
                active_sessions[session_id]['text'] += ' ' + text
                active_sessions[session_id]['text_en'] += ' ' + text_en
                active_sessions[session_id]['last_update'] = time.time()
            
        return jsonify({
            'success': True,
            'text': text,
            'text_en': text_en,
            'full_text': active_sessions[session_id]['text'].strip(),
            'full_text_en': active_sessions[session_id]['text_en'].strip()
        })
    
    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': 'Tidak terdengar jelas'})
    except sr.RequestError as e:
        return jsonify({'success': False, 'error': f'Error with speech recognition service: {str(e)}'})
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.route('/get_transcription', methods=['GET'])
def get_transcription():
    """Get the current transcription for a session"""
    session_id = request.args.get('session_id')
    if not session_id or session_id not in active_sessions:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    return jsonify({
        'text': active_sessions[session_id]['text'],
        'is_active': active_sessions[session_id]['is_active']
    })

# Clean up inactive sessions
def cleanup_sessions():
    """Remove inactive sessions after a period of inactivity"""
    while True:
        current_time = time.time()
        to_remove = []
        
        for session_id, session in active_sessions.items():
            if not session['is_active'] and current_time - session['last_update'] > 300:  # 5 minutes
                to_remove.append(session_id)
        
        for session_id in to_remove:
            del active_sessions[session_id]
        
        time.sleep(60)  # Check every minute

# Start the cleanup thread
cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)