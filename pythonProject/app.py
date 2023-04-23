import musicbrainzngs
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = "bogus"


@app.route("/")
def start_up():
    session['users'] = {}
    return redirect(url_for("welcome_page"))


@app.route("/welcome", methods=["POST", "GET"])
def welcome_page():
    if request.method == "POST":
        if request.form.get('login'):
            return redirect(url_for("login_page"))
        elif request.form.get('new_acc'):
            return redirect(url_for("new_account"))
    else:
        return render_template("welcome.html")


@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        if request.form.get("leave"):
            return redirect(url_for("welcome_page"))
        else:
            user = request.form.get("username")
            pw = request.form.get("password")
            if user in session['users']:
                if pw == session['users'][user][0]:
                    return redirect(url_for("menu_user", usr=user))
                else:
                    return render_template("login.html", message="Incorrect Password.")
            else:
                return render_template("login.html", message="User not found. Try again, or create an account.")
    else:
        return render_template("login.html", message="")


@app.route("/create_account", methods=["POST", "GET"])
def new_account():
    if request.method == "POST":
        if request.form.get("leave"):
            return redirect(url_for("welcome_page"))
        else:
            user = request.form.get("username")
            pw = request.form.get("password")
            if user in session['users']:
                return render_template("create_account.html", message="Username in use")
            else:
                session['users'][user] = [pw, {}]
                session.modified = True
                return redirect(url_for("menu_user", usr=user))
    else:
        return render_template("create_account.html", message="")


@app.route("/menu/<usr>", methods=["POST", "GET"])
def menu_user(usr):
    if request.method == "POST":
        if request.form.get("create_review"):
            return redirect(url_for("album_search", usr=usr))
        elif request.form.get("my_reviews"):
            return redirect(url_for("list_reviews", usr=usr))
        elif request.form.get("user_list"):
            return redirect(url_for("list_users", usr=usr))
        elif request.form.get("logoff"):
            return redirect(url_for("welcome_page"))

    else:
        return render_template("main_menu.html", usr=usr)


@app.route("/list_users/<usr>", methods=["POST", "GET"])
def list_users(usr):
    if request.method == "POST":
        if request.form.get("back"):
            return redirect(url_for("menu_user", usr=usr))
    else:
        return render_template("list_users.html", usr=usr, session=session)


@app.route("/<usr>/reviews", methods=["POST", "GET"])
def list_reviews(usr):
    if request.method == "POST":
        if request.form.get("back"):
            return redirect(url_for("menu_user", usr=usr))
    else:
        return render_template("list_reviews.html", usr=usr)


@app.route("/<usr>/search_albums", methods=["POST", "GET"])
def album_search(usr):
    if request.method == "POST":
        if request.form.get("back"):
            return redirect(url_for("menu_user", usr=usr))
        elif request.form.get("submit"):
            album = request.form.get("input")
            musicbrainzngs.set_useragent('SWS_class_proj', '0.0', contact='kurtzma4@msu.edu')
            result = musicbrainzngs.search_release_groups(album)
            search_dict = {}
            for i, album in enumerate(result['release-group-list']):
                if i == 51:
                    break
                try:
                    if album['primary-type'] == 'Album':
                        search_dict[album['title']] = album['artist-credit'][0]['artist']['name']
                except KeyError:
                    pass
            return render_template("list_search_results.html", usr=usr, album=album, search_dict=search_dict)
        else:
            for i in request.form.keys():
                choice = i
                break
            return redirect(url_for("write_review", usr=usr, choice=choice))
    else:
        return render_template("album_search.html", usr=usr)


@app.route("/<usr>/<choice>/write_review", methods=["POST", "GET"])
def write_review(usr, choice):
    t, a = choice.split(" - ")
    if request.method == "POST":
        if request.form.get("back"):
            return redirect(url_for("menu_user", usr=usr))
        else:
            session['users'][usr][1][t] = {'title': t, 'artist': a, 'text': request.form.get('review')}
            session.modified = True
            return redirect(url_for("menu_user", usr=usr))
    else:
        return render_template("write_review.html", usr=usr, a=a, t=t)


if __name__ == "__main__":
    app.run(debug=True)
