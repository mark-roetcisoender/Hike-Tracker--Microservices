from flask import Blueprint, render_template, request

bp = Blueprint("pages", __name__)

hike_log = []
cumulative_stats = [0,0,0,0,0]

@bp.route("/")
def home():
    return render_template("pages/home.html")

@bp.route("/about")
def about():
    return render_template("pages/about.html")

@bp.route("/add", methods=['GET', 'POST'])
def add():
    return render_template("pages/add.html")

@bp.route("/manual", methods=['GET', 'POST'])
def manual():
    if request.method == 'POST':
        hike_name = request.form.get("hike_name")
        distance = request.form.get("distance")
        elevation = request.form.get("elevation")

        temp = [hike_name, distance, elevation]
        hike_log.append(temp)
        return render_template("pages/success.html")
    return render_template("pages/manual.html")

@bp.route("/stats")
def stats():
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

    print(cumulative_stats)
    return render_template("pages/stats.html", hike_log = hike_log, cumulative_stats = cumulative_stats)

@bp.route("/preselected", methods=['GET', 'POST'])
def preselected():
    if request.method == 'POST':
        selected_hike = request.form.get("hikes")
        hike_name = ""
        distance = ""
        elevation = ""
        # print(selected_hike)
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
    print("hikelog")
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
