import frappe
import json
import random
import string
from datetime import datetime, timedelta

@frappe.whitelist()
def create_google_meet(title: str, when: str, student_email: str = None):
    """
    Create Google Meet link and calendar event.
    
    This is currently a stub implementation that generates a pseudo Meet link.
    Replace this with actual Google Calendar API integration when ready.
    
    Args:
        title: Lesson title
        when: ISO datetime string for lesson time
        student_email: Student's email for calendar invite
    
    Returns:
        dict: Contains meet_link and event_id
    """
    try:
        # For now, generate a pseudo Meet link for testing
        # TODO: Replace with actual Google Calendar API calls
        
        # Generate realistic-looking Meet code
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        meet_link = f"https://meet.google.com/{code}"
        
        # Generate pseudo event ID
        event_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))
        
        # Log the request for debugging
        frappe.logger().info(f"Created Meet link for lesson: {title} at {when}")
        
        return {
            "meet_link": meet_link,
            "event_id": event_id,
            "status": "success",
            "message": "Meet link created successfully (stub implementation)"
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to create Google Meet link: {str(e)}")
        frappe.throw("Failed to create Google Meet link. Please try again.")

@frappe.whitelist()
def create_google_meet_real(title: str, when: str, student_email: str = None):
    """
    Real Google Calendar API implementation (to be activated later).
    
    This function shows how to integrate with Google Calendar API using
    service account or OAuth credentials stored in Frappe.
    """
    try:
        # Get Google credentials from Social Login Key or custom settings
        google_settings = get_google_credentials()
        
        if not google_settings:
            frappe.throw("Google Calendar integration not configured. Please set up Google credentials.")
        
        # Import Google Calendar API client
        from googleapiclient.discovery import build
        from google.oauth2.service_account import Credentials
        
        # Set up credentials
        credentials = Credentials.from_service_account_info(
            google_settings["service_account_json"],
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        
        # Build Calendar service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Parse datetime
        start_time = datetime.fromisoformat(when.replace('Z', '+00:00'))
        end_time = start_time + timedelta(hours=1)  # Default 1 hour lesson
        
        # Create calendar event
        event = {
            'summary': title,
            'description': f'ESL Lesson: {title}',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            },
            'attendees': []
        }
        
        # Add student email if provided
        if student_email:
            event['attendees'].append({'email': student_email})
        
        # Create the event
        created_event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()
        
        # Extract Meet link
        meet_link = None
        if 'conferenceData' in created_event and 'entryPoints' in created_event['conferenceData']:
            for entry_point in created_event['conferenceData']['entryPoints']:
                if entry_point['entryPointType'] == 'video':
                    meet_link = entry_point['uri']
                    break
        
        return {
            "meet_link": meet_link,
            "event_id": created_event['id'],
            "status": "success",
            "message": "Google Meet link created successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Google Calendar API error: {str(e)}")
        frappe.throw(f"Failed to create Google Meet link: {str(e)}")

def get_google_credentials():
    """
    Get Google API credentials from Frappe settings.
    
    This can be stored in:
    1. Social Login Key (for OAuth)
    2. Custom DocType for service account
    3. Site config
    """
    try:
        # Option 1: Check for service account in site config
        service_account_json = frappe.conf.get("google_service_account_json")
        if service_account_json:
            return {"service_account_json": json.loads(service_account_json)}
        
        # Option 2: Check for Social Login Key
        google_login = frappe.get_doc("Social Login Key", {"provider_name": "Google"})
        if google_login and google_login.client_secret:
            return {
                "client_id": google_login.client_id,
                "client_secret": google_login.client_secret
            }
        
        # Option 3: Check custom settings (you can create a DocType for this)
        # google_settings = frappe.get_single("Google Integration Settings")
        # return google_settings
        
        return None
        
    except Exception:
        return None

@frappe.whitelist()
def get_lesson_calendar_data(student=None, teacher=None, start_date=None, end_date=None):
    """
    Get lesson data formatted for calendar display.
    
    Args:
        student: Filter by student name
        teacher: Filter by teacher email
        start_date: Start date for filtering
        end_date: End date for filtering
    
    Returns:
        list: Calendar events in FullCalendar format
    """
    try:
        filters = {}
        
        if student:
            filters["student"] = student
        if teacher:
            filters["teacher"] = teacher
        if start_date:
            filters["scheduled_time"] = [">=", start_date]
        if end_date:
            if "scheduled_time" in filters:
                filters["scheduled_time"] = ["between", [start_date, end_date]]
            else:
                filters["scheduled_time"] = ["<=", end_date]
        
        lessons = frappe.get_all("ESL Lesson",
            filters=filters,
            fields=["name", "title", "student", "teacher", "scheduled_time", "duration", "status", "meet_link"],
            order_by="scheduled_time"
        )
        
        # Format for FullCalendar
        events = []
        for lesson in lessons:
            # Get student name
            student_name = frappe.db.get_value("ESL Student", lesson.student, "student_name") if lesson.student else "Unknown"
            
            # Calculate end time
            start_time = datetime.fromisoformat(lesson.scheduled_time.replace('Z', '+00:00'))
            end_time = start_time + timedelta(minutes=lesson.duration or 60)
            
            # Set color based on status
            color_map = {
                "Scheduled": "#3b82f6",
                "In Progress": "#f59e0b", 
                "Completed": "#10b981",
                "Cancelled": "#ef4444",
                "Rescheduled": "#8b5cf6"
            }
            
            events.append({
                "id": lesson.name,
                "title": f"{lesson.title} - {student_name}",
                "start": lesson.scheduled_time,
                "end": end_time.isoformat(),
                "backgroundColor": color_map.get(lesson.status, "#6b7280"),
                "borderColor": color_map.get(lesson.status, "#6b7280"),
                "extendedProps": {
                    "student": student_name,
                    "teacher": lesson.teacher,
                    "status": lesson.status,
                    "meet_link": lesson.meet_link,
                    "lesson_id": lesson.name
                }
            })
        
        return events
        
    except Exception as e:
        frappe.log_error(f"Failed to get calendar data: {str(e)}")
        return []

@frappe.whitelist()
def update_lesson_status(lesson_id: str, status: str):
    """
    Update lesson status via API.
    
    Args:
        lesson_id: ESL Lesson document name
        status: New status value
    
    Returns:
        dict: Success/error response
    """
    try:
        lesson = frappe.get_doc("ESL Lesson", lesson_id)
        lesson.status = status
        lesson.save()
        
        return {
            "status": "success",
            "message": f"Lesson status updated to {status}"
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to update lesson status: {str(e)}")
        frappe.throw(f"Failed to update lesson status: {str(e)}")

@frappe.whitelist()
def get_teacher_dashboard_data(teacher_email=None):
    """
    Get dashboard data for teachers.
    
    Returns:
        dict: Dashboard statistics and recent lessons
    """
    try:
        if not teacher_email:
            teacher_email = frappe.session.user
        
        # Get teacher's lessons
        lessons = frappe.get_all("ESL Lesson",
            filters={"teacher": teacher_email},
            fields=["name", "title", "student", "scheduled_time", "status"],
            order_by="scheduled_time desc",
            limit=10
        )
        
        # Calculate statistics
        total_lessons = len(lessons)
        completed_lessons = len([l for l in lessons if l.status == "Completed"])
        upcoming_lessons = len([l for l in lessons if l.status == "Scheduled"])
        
        # Get students count
        students = frappe.get_all("ESL Student",
            filters={"teacher": teacher_email},
            fields=["name"]
        )
        
        return {
            "stats": {
                "total_lessons": total_lessons,
                "completed_lessons": completed_lessons,
                "upcoming_lessons": upcoming_lessons,
                "total_students": len(students)
            },
            "recent_lessons": lessons,
            "students": students
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to get teacher dashboard data: {str(e)}")
        return {"error": str(e)}

