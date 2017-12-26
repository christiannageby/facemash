#!flask/bin/python
from flask import Flask, render_template, redirect, url_for
import random
import os
import sys

app = Flask(__name__)

K = 32

images = []

def vote(id, idLoser):
    # Convert inputs to ints
    id = int(id)
    idLoser = int(idLoser)

    # Add one win to the winners win count ant adding one lost to the losers dislike counter
    images[id][1] += 1
    images[idLoser][2] += 1

    ea = 1 / (1 + 10 ** ((images[idLoser][3] - images[int(id)][3]) / 400))
    eb = 1 / (1 + 10 ** ((images[int(id)][3] - images[int(idLoser)][3]) / 400))

    images[int(id)][3] = images[int(id)][3] + (K * (1 - ea))
    images[int(idLoser)][3] = images[int(idLoser)][3] + (K * (0 - eb))

    for i in range(len(images)):
        for j in range((len(images)-1) - i):
            if images[j][3] < images[j + 1][3]:
                images[j], images[j + 1] = images[j + 1], images[j]
#
# index page, display to random candidates for judgemnet
# Later: fixes Sort the array after smallest diffrence in elorank decending order - Fixed
#


@app.route('/')
def home():
    index = random.sample(range(0, len(images)), 2)
    return render_template('index.html', data=[
        [index[0], images[index[0]][0], images[index[0]][1], images[index[0]][2], images[index[0]][3]],
        [index[1], images[index[1]][0], images[index[1]][1], images[index[1]][2], images[index[1]][3]]
    ])


@app.route('/toplist')
def toplist():
    return render_template('toplist.html', data=[
        [0, images[0][0], images[0][1], images[0][2], images[0][3]],
        [1, images[1][0], images[1][1], images[1][2], images[1][3]]
    ])


@app.route('/vote/<id>/<idLoser>')
def normal_vote(id, idLoser):
    vote(id, idLoser)
    return redirect(url_for('home'))

@app.route('/hottest-vote/<id>/<idLoser>')
def hottestVote(id, idLoser):
    vote(id, idLoser)
    return redirect(url_for('toplist'))

if __name__ == '__main__':

    for file in os.listdir(os.getcwd()+"/static/images"):
        if file.endswith(".jpg"):
            print file + " appended..."
        images.append([file, 0, 0, 1200])
    print images


    app.run(port=1337, host='127.0.0.1')
