from flask import Flask, render_template, session, redirect
from boggle import Boggle

app = Flask(__name__)
app.secret_key = "nerea"

# instance of the game
boggle_game = Boggle()


# start page
@app.route("/start")
def start_game():
    # initialize a new session board
    session['board'] = []

    return redirect("/board")


# Welcome page
@app.route("/")
def welcome():
    return render_template("welcome.html")


# Showing the board
@app.route("/board")
def show_board():
    # if session exists or not
    if session['board'] != []:
        board = session['board']
    else:
        board = boggle_game.make_board()
        session['board'] = board

    return render_template("board.html", board=board)
