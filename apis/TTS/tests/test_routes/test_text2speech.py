def test_transcribe_string(client):
    response = client.post(
        '/tts/transcription/text',
        headers={'accept': 'application/json'},
        data={
            'text': 'Hello, I am Vision Asistant, a smart assistant for visually impaired people'
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)


def test_transcribe_number(client):
    response = client.post(
        '/tts/transcription/text',
        headers={'accept': 'application/json'},
        data={'text': '1 2 3 4 5 6 7 8 9'},
    )
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)


def test_transcribe_dot(client):
    response = client.post(
        '/tts/transcription/text',
        headers={'accept': 'application/json'},
        data={'text': '...'},
    )
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)


def test_transcribe_empty(client):
    response = client.post(
        '/tts/transcription/text',
        headers={'accept': 'application/json'},
        data={'text': '   '},
    )
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
