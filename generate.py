#!/usr/bin/env python3

import chess
import chess.pgn # read Portable Game Notation format
import chess.svg # Scalable Vector Graphics
from cairosvg import svg2png
import os
import io
from PIL import Image
from tqdm.auto import tqdm # Progress bar
from pydub import AudioSegment

images = dict([(os.path.splitext(f)[0], Image.open(f"images/{f}", 'r')) for f in os.listdir("images")]) # Open each image from the images folder
audio_clips = dict([(os.path.splitext(f)[0], AudioSegment.from_file(f"sound clips/{f}")[:1000]) for f in os.listdir("sound clips")])

with open("pgn/kasparov-deep-blue-1997.pgn") as f:
    first_game = chess.pgn.read_game(f)

def render_image(filename, chessboard_svg, image=None, is_check=False):
    buffer = io.BytesIO()
    svg2png(bytestring=chessboard_svg, write_to=buffer) # Chessboard to PNG in memory
    chessboard = Image.open(buffer)

    new_im = Image.new('RGB', (1920, 1080))
    new_im.paste(chessboard, (0,0,400,400))
    if image:
        new_im.paste(image, (400,0))
    if is_check:
        new_im.paste(images["king_under_threat"], (0, 400))
    new_im.save(filename)

board = first_game.board()
svg = chess.svg.board(board=board)
render_image("render/0.jpg", svg)

audio = AudioSegment.silent(duration=1000)

moves = list(first_game.mainline_moves())
for i, move in enumerate(tqdm(moves)):
    board.push(move)
    if board.is_game_over():
        print(board.result())
    piece_type = chess.piece_name(board.piece_type_at(move.to_square))
    svg = chess.svg.board(board=board, lastmove=move, size=400)
    render_image(f"render/{i + 1}.jpg", svg, images[piece_type], board.is_check())
    clip = audio_clips[piece_type]
    if board.is_check():
        clip = clip.overlay(audio_clips["alert"])
    audio += clip
audio.export("audio.mp3", format="mp3")