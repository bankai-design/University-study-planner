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

@dashBP.route("/modules")
def modulesView():
    icsURL = "https://ical.timetables.qmul.ac.uk/default.aspx?StudentiCalHash&p1=d5fd113b1c1305768f2f15f7619b43e6"
    
    # Store unique modules by code to avoid duplicate entries
    modules_dict = {}
    
    try:
        response = requests.get(icsURL)
        if response.status_code == 200:
            cal_data = ICSParser.from_ical(response.text)
            
            for component in cal_data.walk("vevent"):
                summary = str(component.get("summary"))
                if summary and summary != "None":
                    # Extract just the code (e.g., "SEF3000U-A26")
                    code = summary.split()[0]
                    
                    # Store both code and full title
                    if code not in modules_dict:
                        modules_dict[code] = {
                            "code": code,
                            "full_title": summary
                        }
                    
    except Exception as e:
        print(f"Could not load modules feed: {e}")

    # Sort modules alphabetically by code
    sorted_modules = sorted(modules_dict.values(), key=lambda x: x["code"])

    return render_template("modules.html", modules=sorted_modules)

@dashBP.route("/assignments")
def assignments_view():
    icsURL = "https://ical.timetables.qmul.ac.uk/default.aspx?StudentiCalHash&p1=d5fd113b1c1305768f2f15f7619b43e6"
    assignments = []
    
    try:
        response = requests.get(icsURL)
        if response.status_code == 200:
            cal_data = ICSParser.from_ical(response.text)
            
            for component in cal_data.walk("vevent"):
                summary = str(component.get("summary", ""))
                start_prop = component.get("dtstart")
                
                if start_prop and summary and summary != "None":
                    start_dt = start_prop.dt
                    event_date = start_dt.date() if isinstance(start_dt, datetime) else start_dt
                    
                    if event_date >= datetime.now().date():
                        start_time_str = start_dt.strftime("%H:%M") if isinstance(start_dt, datetime) else ""
                        
                        event_obj = {
                            "date": event_date.strftime("%d %B %Y"),
                            "start": start_time_str,
                            "summary": summary,
                            "sort_key": start_dt
                        }
                        
                        if any(keyword in summary.lower() for keyword in ["deadline", "submission", "coursework", "due"]):
                            if event_obj not in assignments:
                                assignments.append(event_obj)
                                
            assignments.sort(key=lambda x: x["sort_key"])
            
    except Exception as e:
        print(f"Could not load assignments feed: {e}")

    return render_template("assignments.html", assignments=assignments)


@dashBP.route("/exams")
def exams_view():
    icsURL = "https://ical.timetables.qmul.ac.uk/default.aspx?StudentiCalHash&p1=d5fd113b1c1305768f2f15f7619b43e6"
    exams = []
    
    try:
        response = requests.get(icsURL)
        if response.status_code == 200:
            cal_data = ICSParser.from_ical(response.text)
            
            for component in cal_data.walk("vevent"):
                summary = str(component.get("summary", ""))
                start_prop = component.get("dtstart")
                end_prop = component.get("dtend")
                
                if start_prop and summary and summary != "None":
                    start_dt = start_prop.dt
                    event_date = start_dt.date() if isinstance(start_dt, datetime) else start_dt
                    
                    if event_date >= datetime.now().date():
                        start_time_str = start_dt.strftime("%H:%M") if isinstance(start_dt, datetime) else ""
                        end_time_str = end_prop.dt.strftime("%H:%M") if (end_prop and isinstance(end_prop.dt, datetime)) else ""
                        
                        event_obj = {
                            "date": event_date.strftime("%d %B %Y"),
                            "start": start_time_str,
                            "end": end_time_str,
                            "summary": summary,
                            "sort_key": start_dt
                        }
                        
                        if any(keyword in summary.lower() for keyword in ["exam", "test", "assessment"]):
                            if event_obj not in exams:
                                exams.append(event_obj)
                                
            exams.sort(key=lambda x: x["sort_key"])
            
    except Exception as e:
        print(f"Could not load exams feed: {e}")

    return render_template("exams.html", exams=exams)

@dashBP.route("/studyPlan")
def studyPlanView():
    icsURL = "https://ical.timetables.qmul.ac.uk/default.aspx?StudentiCalHash&p1=d5fd113b1c1305768f2f15f7619b43e6"
    all_tasks = []
    now = datetime.now()
    
    try:
        response = requests.get(icsURL)
        if response.status_code == 200:
            cal_data = ICSParser.from_ical(response.text)
            
            for component in cal_data.walk("vevent"):
                summary = str(component.get("summary", ""))
                start_prop = component.get("dtstart")
                
                if start_prop and summary and summary != "None":
                    event_dt = start_prop.dt
                    
                    # Ensure it's a valid datetime object for comparison
                    if isinstance(event_dt, datetime):
                        # Only look at future events
                        if event_dt >= now:
                            lower_summary = summary.lower()
                            
                            # Determine type and base weight (Exams get higher precedence)
                            if any(k in lower_summary for k in ["exam", "test", "assessment"]):
                                task_type = "Exam"
                                weight = 2.0 # Higher weight for exams
                            elif any(k in lower_summary for k in ["deadline", "submission", "coursework", "due"]):
                                task_type = "Assignment"
                                weight = 1.0
                            else:
                                continue # Skip regular lectures/labs for the study plan
                                
                            # Calculate time remaining in hours
                            time_remaining = event_dt - now
                            hours_left = time_remaining.total_seconds() / 3600
                            days_left = hours_left / 24
                            
                            # Precedence score formula: Lower hours left = Higher score
                            # Multiplying exam weight makes exams rank higher if timelines are similar
                            precedence_score = (1 / hours_left) * weight * 10000 
                            
                            # Assign visual priority level based on days left
                            if days_left <= 3:
                                priority_level = "High"
                            elif days_left <= 7:
                                priority_level = "Medium"
                            else:
                                priority_level = "Low"
                                
                            all_tasks.append({
                                "title": summary,
                                "type": task_type,
                                "date_str": event_dt.strftime("%d %B %Y at %H:%M"),
                                "days_left": round(days_left, 1),
                                "priority": priority_level,
                                "sort_score": precedence_score # Used for sorting
                            })
                            
            # Sort tasks from highest precedence (most urgent) to lowest
            all_tasks.sort(key=lambda x: x["sort_score"], reverse=True)
            
    except Exception as e:
        print(f"Could not load study plan feed: {e}")

    return render_template("studyPlan.html", tasks=all_tasks)