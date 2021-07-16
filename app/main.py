import random

from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.db_ops import insert_data, load_data, rank_counts, update_rank_by_id

APP = Flask(__name__)
tweets = pd.read_csv('app/data/data.csv')['tweets']
pb_2020 = pd.read_csv('app/data/pb2020-data.csv')['tweets']


def random_tweet() -> str:
    if random.randint(0, 1) == 0:
        return random.choice(tweets)
    else:
        return random.choice(pb_2020)


@APP.route("/", methods=['GET', 'POST'])
def home():
    rank = request.form.get("rank")
    tweet = request.form.get("tweet")
    if rank in {'0', '1', '2', '3', '4', '5'} and tweet:
        insert_data(tweet, int(rank))
    return render_template(
        "home.html",
        tweet=random_tweet(),
    )


@APP.route("/entry", methods=['GET', 'POST'])
def entry():
    rank = request.form.get("rank")
    tweet = request.form.get("tweet")
    if rank in {'0', '1', '2', '3', '4', '5'} and tweet:
        insert_data(tweet, int(rank))
    return render_template("entry.html")


@APP.route("/edit", methods=['GET', 'POST'])
def edit():
    rank = request.form.get("rank")
    idx = request.form.get("idx")
    if rank in {'0', '1', '2', '3', '4', '5'} and idx:
        update_rank_by_id(idx=int(idx), rank=int(rank))
    return render_template("edit.html")


@APP.route("/view")
def view():
    labels = ['Rank 0', 'Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5']
    data = go.Pie(
        labels=labels,
        values=rank_counts(),
        textinfo='label+percent',
        showlegend=False,
        hole=0.5,
    )
    layout = go.Layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        colorway=px.colors.qualitative.Antique,
        height=600,
        width=750,
    )
    fig = go.Figure(data=data, layout=layout)
    return render_template(
        "view.html",
        graph_json=fig.to_json(),
        tweets=load_data(10),
    )


@APP.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    APP.run()
