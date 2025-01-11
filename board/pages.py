from flask import Blueprint, render_template, request
from random import randint
from constants import *
from suggestion_service import SuggestionsClient
from conv_client import ConversionClient
from help_client import HelpClient
from wishlist_client import WishListClient

# flask --app board run --debug

bp = Blueprint("pages", __name__)

hike_log = []
cumulative_stats = [0,0,0,0,0]

@bp.route("/")
def home():
    """Home Page"""
    return render_template("pages/home.html")

@bp.route("/about", methods=['GET', 'POST'])
def about():
    """Help Page"""
    if request.method == 'POST':
        topic = request.form.get("help")
        print(topic)
        client = HelpClient()
        response = client.get_text(topic)
        if response is None:
            response = "Error: Please try again later."
        return render_template("pages/help_topic.html", response = response)
    return render_template("pages/about.html")

@bp.route("/add", methods=['GET', 'POST'])
def add():
    """Add Hike Page"""
    return render_template("pages/add.html")

@bp.route("/suggest", methods=['GET', 'POST'])
def suggest():
    """Suggestion Page"""
    if request.method == 'POST':
        stats = calc_stats()
        if len(hike_log) > 0:
            print(f"searching by average distance of: {stats[3]}")
            client = SuggestionsClient()            # Needs to be added to your main program

            suggestion = client.request_suggestion(stats[3])     # All that needs called to make a request and get an answer back.

            print(type(suggestion), suggestion)                 # Show the data type and value(s) of what is returned.
            return render_template("pages/hike_suggested.html", suggestion = suggestion)
        else:
            print("no hikes logged!")
            return render_template("pages/suggestno.html")
    return render_template("pages/suggest.html")

@bp.route("/manual", methods=['GET', 'POST'])
def manual():
    """Manual Add Hike"""
    if request.method == 'POST':
        hike_name = request.form.get("hike_name")
        distance = request.form.get("distance")
        elevation = request.form.get("elevation")

        temp = [hike_name, distance, elevation]
        hike_log.append(temp)
        return render_template("pages/success.html")
    return render_template("pages/manual.html")

@bp.route("/stats", methods=['GET', 'POST'])
def stats():
    """Cumulative Stats Page"""
    if len(hike_log) == 0:
        return render_template("pages/statsno.html")
    compiled_stats = calc_stats()
    if request.method == 'POST':
        client = ConversionClient()

        conv_stats = client.convert_obj(compiled_stats)
        print("conv stats:", conv_stats)
        return render_template("pages/stats_metric.html", hike_log = hike_log, cumulative_stats = conv_stats)

    print(compiled_stats)
    return render_template("pages/stats.html", hike_log = hike_log, cumulative_stats = compiled_stats)


@bp.route("/statsmetric", methods=['GET', 'POST'])
def statsmetric():
    """Display metric stats"""
    compiled_stats = calc_stats()
    if request.method == 'POST':
        return render_template("pages/stats.html", hike_log = hike_log, cumulative_stats = compiled_stats)

    print(compiled_stats)
    return render_template("pages/stats_metric.html", hike_log = hike_log, cumulative_stats = compiled_stats)

@bp.route("/preselected", methods=['GET', 'POST'])
def preselected():
    """Add preselected hike to hike log"""
    if request.method == 'POST':
        selected_hike = request.form.get("hikes")
        hike_name = ""
        distance = ""
        elevation = ""
        if selected_hike == 'saddle_mountain':
            hike_name = "Saddle Mountain"
            distance = "5.2"
            elevation = "1900"
        if selected_hike == 'triple_falls':
            hike_name = "Triple Falls"
            distance = "3.6"
            elevation = "680"
        if selected_hike == 'warrior_point':
            hike_name = "Warrior Point"
            distance = "7.0"
            elevation = "10"
        if selected_hike == 'ape_caves':
            hike_name = "Ape Caves"
            distance = "4.7"
            elevation = "640"
        temp = [hike_name, distance, elevation]
        hike_log.append(temp)
        print(temp)
        return render_template("pages/success.html")

    return render_template("pages/preselected.html")

@bp.route("/hikelog", methods=['GET', 'POST'])
def hikelog():
    """Hike log page"""
    if len(hike_log) == 0:
        return render_template("pages/emptyhikelog.html")
    if request.method == 'POST':
        selected_hike = request.form.get('hikes')
        print(selected_hike)
        hike_log_copy = hike_log
        for hike in hike_log_copy:
            if selected_hike == hike[0]:
                hike_log.remove(hike)
        return render_template("pages/delete_success.html")

    return render_template("pages/hike_log.html", hike_log = hike_log)

@bp.route("/wishlist", methods=['GET'])
def wishlist():
    """Wish list page"""
    client = WishListClient()
    null_list = [None, None, None]
    current_wl = client.add_hike(null_list)
    print("current wishlist: ", current_wl)
    if current_wl is -1 or len(current_wl) == 0:
        return render_template("pages/emptywishlist.html")

    return render_template("pages/wishlist.html" , current_wl = current_wl)

@bp.route("/addwishlist", methods=['GET', 'POST'])
def addwishlist():
    """Add to wish list"""
    if request.method == 'POST':
        hike_name = request.form.get("hike_name")
        distance = request.form.get("distance")
        elevation = request.form.get("elevation")

        new_wl_hike = [hike_name, distance, elevation]
        client = WishListClient()
        new_wl = client.add_hike(new_wl_hike)
        return render_template("pages/wishlist.html", current_wl = new_wl)

    return render_template("pages/addwishlist.html")

def calc_stats():
    """Method to calculate cumulative stats of hike log"""
    if len(hike_log) > 0:
        cumulative_stats[0] = len(hike_log)
        distance_total = 0
        elevation_total = 0
        for entry in hike_log:
            distance_total += float(entry[1])
            elevation_total += float(entry[2])
        cumulative_stats[1] = float(distance_total)
        cumulative_stats[2] = float(elevation_total)
        cumulative_stats[3] = round(float(distance_total/len(hike_log)), 2)
        cumulative_stats[4] = round(float(elevation_total/len(hike_log)), 2)
        return cumulative_stats
