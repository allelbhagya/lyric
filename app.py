from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import random

app = Flask(__name__)

def load_lyrics(csv_file):
    df = pd.read_csv(csv_file)
    lyrics_data = df[['Title', 'Lyric']].dropna()
    return lyrics_data

def build_markov_chain(lyrics_data):
    markov_chain = {}

    for _, row in lyrics_data.iterrows():
        lyrics = row['Lyric']
        words = lyrics.split()
        
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]

            if current_word not in markov_chain:
                markov_chain[current_word] = []

            markov_chain[current_word].append(next_word)

    return markov_chain

def generate_lyrics(markov_chain, num_lines=5):
    generated_lyrics = []

    for _ in range(num_lines):
        current_word = random.choice(list(markov_chain.keys()))
        line = [current_word]

        for _ in range(10):  # Set a limit to avoid infinite loops
            next_word = random.choice(markov_chain.get(current_word, ['']))
            if next_word:
                line.append(next_word)
                current_word = next_word
            else:
                break

        generated_lyrics.append(' '.join(line))

    return generated_lyrics

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics_route():
    artist = request.form.get('artist')

    artist_folder = 'D:\code\lyrics\music\db'  # Replace with the actual path
    selected_csv = os.path.join(artist_folder, f'{artist}.csv')

    # Check if the file exists before attempting to read it
    if os.path.exists(selected_csv):
        lyrics_data = load_lyrics(selected_csv)
        markov_chain = build_markov_chain(lyrics_data)
        generated_lyrics = generate_lyrics(markov_chain)
        return jsonify({'generated_lyrics': generated_lyrics})
    else:
        return jsonify({'error': 'Selected artist CSV file not found'})


@app.route('/artists')
def get_artists():
    artist_folder = 'D:\code\lyrics\music\db'  # Replace with the actual path
    artists = [folder for folder in os.listdir(artist_folder) if os.path.isdir(os.path.join(artist_folder, folder))]
    print('Artists:', artists)  # Add this line for debugging
    return jsonify({'artists': artists})

if __name__ == '__main__':
    app.run(debug=True)
