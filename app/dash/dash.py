from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from app.auth.models import User
import calendar
from datetime import datetime
import requests
from icalendar import Calendar as ICSParser

dashBP = Blueprint("dashBP", __name__, template_folder="templates", static_folder="static")

@dashBP.route("/dashboard")
def dashboard():
    if "userEmail" not in session:
        flash("Please login first")
        return redirect(url_for("authBP.login"))

    currentUser = User.query.filter_by(email=session["userEmail"]).first()

    return render_template("dashboard.html", fullName=currentUser.fullName)

@dashBP.route("/calendar")
def calendarView():
    now = datetime.now()
    year, month = now.year, now.month

    firstDayWeekday, totalDays = calendar.monthrange(year, month)

    icsURL = "https://ical.timetables.qmul.ac.uk/default.aspx?StudentiCalHash&p1=d5fd113b1c1305768f2f15f7619b43e6"
    eventsByDay = {}

    try:
        response = requests.get(icsURL)
        if response.status_code == 200:
            cal_data = ICSParser.from_ical(response.text)

            for component in cal_data.walk("vevent"):
                dtstart = component.get("dtstart")
                if dtstart:
                    event_date = dtstart.dt
                    if isinstance(event_date, datetime):
                        event_date = event_date.date()

                        if event_date.year == year and event_date.month == month:
                            day_num = int(event_date.day)

                            start_prop = component.get("dtstart")
                            end_prop = component.get("dtend")

                            start_dt = start_prop.dt if start_prop else None
                            end_dt = end_prop.dt if end_prop else None

                            start_time_str = start_dt.strftime("%H:%M") if isinstance(start_dt, datetime) else ""
                            end_time_str = end_dt.strftime("%H:%M") if (end_dt and isinstance(end_dt, datetime)) else ""

                            summary = str(component.get("summary"))

                            event_obj = {"start": start_time_str,
                                         "end": end_time_str,
                                         "summary": summary,
                                         "sort_key": start_time_str}

                            if day_num not in eventsByDay:
                                eventsByDay[day_num] = []

                            if event_obj not in eventsByDay[day_num]:
                                eventsByDay[day_num].append(event_obj)

            for day_num in eventsByDay:
                eventsByDay[day_num].sort(key=lambda x: x["sort_key"])

    except Exception as e:
        print(f"Could not load timetable feed: {e}")

    return render_template("calendar.html", firstDayWeekday=firstDayWeekday, totalDays=totalDays, monthName=calendar.month_name[month], eventsByDay=eventsByDay)

@dashBP.route("/assignments")
def assignments():
    return render_template("assignments.html")

@dashBP.route("/studyPlan")
def studyPlan():
    return render_template("studyPlan.html")

@dashBP.route("/modules")
def modulesView():
    icsURL = "https://ical.timetables.qmul.ac.uk/default.aspx?StudentiCalHash&p1=d5fd113b1c1305768f2f15f7619b43e6"
    unique_modules = set()
    
    try:
        response = requests.get(icsURL)
        if response.status_code == 200:
            cal_data = ICSParser.from_ical(response.text)
            
            for component in cal_data.walk("vevent"):
                summary = str(component.get("summary"))
                if summary and summary != "None":
                    unique_modules.add(summary)
                    
    except Exception as e:
        print(f"Could not load modules feed: {e}")

    # Sort them alphabetically
    sorted_modules = sorted(list(unique_modules))

    return render_template("modules.html", modules=sorted_modules)