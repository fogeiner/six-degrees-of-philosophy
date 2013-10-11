#!/usr/bin/python

# Here are imports, do not worry about them
import setpath
from flask import Flask, render_template, session, request, g, redirect, url_for, flash
from getpage import getPage

app = Flask(__name__)

app.secret_key = "Any secret value"

MESSAGE_SUCCESS='success'
MESSAGE_FAIL='fail'

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/new-game', methods=["POST"])
def newGame():
    session["article"] = request.form["article"]
    session["hops"] = 0
    return redirect(url_for('game'))

@app.route('/game', methods=["GET"])
def game():
    article = session["article"]
    title, hrefs = getPage(article)
# needed in case API returns another name (for example with accents) or redirection
    session["article"] = title
    if title == "Philosophy":
        if session["hops"] == 0:
            flash("You have started playing starting from the target article.", MESSAGE_SUCCESS)
        else:
            flash("You have won with " + str(session["hops"]) +" hops!", MESSAGE_SUCCESS)
        return redirect('/')
    if title is None:
        flash("The requested article " + article + " doesn't exist.", MESSAGE_FAIL)
        return redirect('/')
    if hrefs == []:
        if session["hops"] == 0:
            flash("You have started from an article that doesn't have links.", MESSAGE_FAIL)
        else:
            flash("There are no links in the " + title + " article. You have lost.",MESSAGE_FAIL)
        return redirect('/')
    return render_template('game.html', article=title, hrefs=hrefs, hops = session["hops"])

@app.route('/move', methods=["POST"])
def move():
    savedArticle = session["article"]
    currentArticle = request.form["currentArticle"]

    # check for several browser windows sharing the same session
    if savedArticle != currentArticle:
        flash("Currently you are on the article "
                + savedArticle + " (you submitted from "
                + currentArticle + ").", MESSAGE_FAIL)
        return redirect(url_for('game'))

    targetArticle = request.form["article"]
    _, allowedLinks = getPage(savedArticle)

    # check for allowed move
    if targetArticle not in allowedLinks:
        flash("There are no direct links from "
                + savedArticle + " to " + targetArticle, MESSAGE_FAIL)
        return redirect(url_for("game"))


    session["article"] = targetArticle
    session["hops"] += 1
    return redirect(url_for("game"))

# new routes should be defined here

if __name__ == '__main__':
  app.run(host='0.0.0.0')

