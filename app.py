from stories import Story
from flask import Flask, render_template, request, redirect, flash, jsonify
app = Flask(__name__, static_folder='static')
app.config["SECRET_KEY"] = "samie"


@app.route("/")
def home():
    """ Render the form on the homepage """
    return render_template('index.html')


# Fake DB set of movies
movies = {"mageiva", "solo", "home alone"}


@app.route("/old")
def redirect_to_home():
    flash("We moved - here is our new page.")
    return redirect("/")


@app.route("/movies")
def show_movies():
    return render_template("movies.html", movies=movies)


@app.route("/movies/new", methods=["POST"])
def submit_movie():
    movie = request.form["movie"]
    if movie in movies:
        flash("Movie already added.", 'error')
    else:
        movies.add(movie)
        flash("Movie added!")
    return redirect("/movies")


@app.route("/movies/json")
def return_json():

    return jsonify(list(movies))


# Variable to store the template selected
template = None


@app.route("/form")
def show_form():
    """ Render the form to collect story attributes """

    # Get selected template
    global template
    template = request.args["story_template"]

    return render_template('form.html')


@app.route("/story")
def show_story():
    """ A method to costruct the story and render it on the page """

    # Extarct all the story words from the form once submitted
    place = request.args.get("place", "no-where")
    noun = request.args.get("noun", "na-la")
    verb = request.args.get("verb", "_ _ _")
    adjective = request.args.get("adjective", "_ _ _'")
    plural_noun = request.args.get("plural_noun", "_ _ _")

    # Add all the story words into an attributes list
    attributes = {"place": place, "noun": noun, "verb": verb,
                  "adjective": adjective, "plural_noun": plural_noun}

    # Get an instance of the story class with the story structure.
    story_templates = {"default": default, "farmyard": farmyard, "pirate": pirate,
                       "space": space, "superhero": superhero, "disaster": disaster}

    blurb = story_templates[template].generate(attributes)

    return render_template("story.html", story=blurb)


default = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a time in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}.""")

farmyard = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once in a hilarious {place}, there lived a wacky {adjective} {noun}.
       It enjoyed {verb} with the crazy {plural_noun} all day long."""
)

pirate = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """In a hidden {place}, a brave {adjective} {noun} roamed, always
       on a quest to {verb} for treasure with a bunch of goofy {plural_noun}."""
)

space = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Aboard a {place} in space, an {adjective} {noun} explored the cosmos.
       Its mission: {verb} with the aliens and crack jokes with funny {plural_noun}."""
)

superhero = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Above the city of {place}, a zany {adjective} {noun} fought crime
       by {verb} and saving kittens stuck in trees. The cheers of the {plural_noun}
       echoed all around."""
)

disaster = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """In a wild {place}, a time-traveling {adjective} {noun} went on epic adventures.
       One day, it accidentally {verb} back to the age of the dinosaurs and met some
       hilarious {plural_noun}."""
)
