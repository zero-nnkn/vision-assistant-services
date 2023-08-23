from pathlib import Path

TEST_PATH = Path(__file__).resolve().parent
SAMPLES_PATH = TEST_PATH / 'samples'


def test_transcribe_audio(client):
    audio_path = SAMPLES_PATH / 'sample0.wav'

    with open(audio_path, 'rb') as f:
        files = {'audio_file': ('audio.wav', f, 'audio/wav')}
        response = client.post(
            '/stt/transcription/audio',
            headers={'accept': 'application/json'},
            files=files,
        )
    assert response.status_code == 200
    response_data = response.json()

    assert response_data.get('message') == 'success'

    # Check the 'transcripts' field
    assert 'info' in response_data
    assert 'segments' in response_data
    for segment in response_data['segments']:
        assert isinstance(segment['text'], str)


def test_transcribe_error(client):
    files = {'audio_file': ('audio.wav', b'', 'audio/wav')}
    response = client.post(
        '/stt/transcription/audio', headers={'accept': 'application/json'}, files=files
    )

    assert response.status_code == 500
    response_data = response.json()

    assert response_data.get('message') == 'transcribe error'
