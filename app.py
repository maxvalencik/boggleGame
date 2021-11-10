from flask import Flask, render_template, session, redirect, jsonify, request
from boggle import Boggle

app = Flask(__name__)
app.secret_key = "nerea"

# instance of the game
boggle_game = Boggle()


# start page
@app.route("/start")
def start_game():
    """Star of the game with an empty board in sesison"""

    # initialize a new session board, highscore and number of plauys
    session['board'] = []
    session['highscore'] = 0
    session['play'] = 0

    return redirect("/board")


# Welcome page
@app.route("/")
def welcome():
    """Show a welcome page with instructions and start button"""

    return render_template("welcome.html")


# Showing the board
@app.route("/board")
def show_board():
    """Show the board in html"""

    board = boggle_game.make_board()
    session['board'] = board
    play = session['play']
    play += 1
    session['play'] = play

    return render_template("board.html", board=board)


# Check the word guessed when request received
@app.route("/word")
def check_word():
    """Check if word is valid"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/end", methods=['POST'])
def end_game():
    """post final score and return higher score, also counts the number of times player played in session"""

    score = request.json['finalScore']
    highscore = session.get('highscore')
    session['highscore'] = max(score, highscore)

    final_highscore = session['highscore']
    final_play = session['play']

    return jsonify({'record': f'{final_highscore}', 'plays': f'{final_play}'})
