#!flask/bin/python
from flask import Flask, render_template, redirect, url_for
import random
import os

app = Flask(__name__)

K = 32

images = []

#
# index page, display to random candidates for judgemnet
# Later: fixes Sort the array after smallest diffrence in elorank decending order
#


@app.route('/')
def home():
    index = random.sample(range(0, len(images)), 2)
    return render_template('index.html', data=[
        [index[0], images[index[0]][0], images[index[0]][1], images[index[0]][2], images[index[0]][3]],
        [index[1], images[index[1]][0], images[index[1]][1], images[index[1]][2], images[index[1]][3]]
    ])


#
# Define the vote route
# usage /vote/WinnersIndex/LosersIndex
#


@app.route('/vote/<id>/<idLoser>')
def vote(id, idLoser):

    # Convert inputs to ints
    id = int(id)
    idLoser = int(idLoser)

    # Add one win to the winners win count ant adding one lost to the losers dislike counter
    images[id][1] += 1
    images[idLoser][2] += 1

    ea = 1/(1 + 10 ** ((images[idLoser][3] - images[int(id)][3]) / 400))
    eb = 1/(1 + 10 ** ((images[int(id)][3]-images[int(idLoser)][3]) / 400))

    images[int(id)][3] = images[int(id)][3] + (K * (1 - ea))
    images[int(idLoser)][3] = images[int(idLoser)][3] + (K * (0 - eb))

    return redirect(url_for('home'))


if __name__ == '__main__':

    for file in os.listdir("C:/Users/Christian Nageby/PycharmProjects/fasemash/static/images"):
        if file.endswith(".jpg"):
            print file + " appended..."
        images.append([file, 0, 0, 1200])
    print images


    app.run(port=80, host='127.0.0.1')