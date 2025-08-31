import frappe

def get_portal_menu_items():
    """
    Return portal menu items for OLYA ESL platform.
    
    This function defines the navigation menu that appears in the portal
    for students and teachers.
    """
    return [
        {
            "title": "Dashboard",
            "route": "/app",
            "role": "All",
            "icon": "dashboard"
        },
        {
            "title": "My Lessons", 
            "route": "/app/esl-lesson",
            "role": "ESL Teacher",
            "reference_doctype": "ESL Lesson",
            "icon": "calendar"
        },
        {
            "title": "My Students",
            "route": "/app/esl-student", 
            "role": "ESL Teacher",
            "reference_doctype": "ESL Student",
            "icon": "users"
        },
        {
            "title": "My Profile",
            "route": "/app/esl-student",
            "role": "ESL Student", 
            "reference_doctype": "ESL Student",
            "icon": "user"
        },
        {
            "title": "My Lessons",
            "route": "/app/esl-lesson",
            "role": "ESL Student",
            "reference_doctype": "ESL Lesson", 
            "icon": "calendar"
        },
        {
            "title": "Whiteboard",
            "route": "/whiteboard",
            "role": "All",
            "icon": "edit"
        },
        {
            "title": "Resources",
            "route": "/resources",
            "role": "All",
            "icon": "book"
        }
    ]

def get_portal_settings():
    """
    Return portal settings for OLYA ESL platform.
    """
    return {
        "default_role": "ESL Student",
        "default_portal_home": "/app",
        "hide_standard_menu": False,
        "custom_css": """
        .portal-sidebar {
            background: linear-gradient(135deg, #9333ea, #ec4899);
        }
        
        .portal-sidebar .sidebar-item {
            border-radius: 8px;
            margin: 0.25rem 0;
            transition: all 0.3s ease;
        }
        
        .portal-sidebar .sidebar-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        .portal-sidebar .sidebar-item.active {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .portal-header {
            background: linear-gradient(135deg, #9333ea, #ec4899);
            color: white;
        }
        
        .portal-header .navbar-brand {
            color: white !important;
            font-weight: 700;
        }
        """
    }

@frappe.whitelist()
def get_user_portal_data():
    """
    Get personalized portal data for the current user.
    
    Returns different data based on user role (Teacher vs Student).
    """
    try:
        user = frappe.session.user
        user_roles = frappe.get_roles(user)
        
        data = {
            "user": user,
            "roles": user_roles,
            "is_teacher": "ESL Teacher" in user_roles,
            "is_student": "ESL Student" in user_roles,
            "is_admin": "ESL Administrator" in user_roles
        }
        
        if data["is_teacher"]:
            # Get teacher-specific data
            data.update(get_teacher_portal_data(user))
        elif data["is_student"]:
            # Get student-specific data  
            data.update(get_student_portal_data(user))
        
        return data
        
    except Exception as e:
        frappe.log_error(f"Failed to get portal data: {str(e)}")
        return {"error": str(e)}

def get_teacher_portal_data(teacher_email):
    """Get portal data specific to teachers"""
    try:
        # Get teacher's students
        students = frappe.get_all("ESL Student",
            filters={"teacher": teacher_email},
            fields=["name", "student_name", "email", "level"],
            limit=10
        )
        
        # Get upcoming lessons
        upcoming_lessons = frappe.get_all("ESL Lesson",
            filters={
                "teacher": teacher_email,
                "status": "Scheduled",
                "scheduled_time": [">=", frappe.utils.now()]
            },
            fields=["name", "title", "student", "scheduled_time"],
            order_by="scheduled_time",
            limit=5
        )
        
        # Get recent lessons
        recent_lessons = frappe.get_all("ESL Lesson",
            filters={"teacher": teacher_email},
            fields=["name", "title", "student", "scheduled_time", "status"],
            order_by="scheduled_time desc",
            limit=5
        )
        
        return {
            "students": students,
            "upcoming_lessons": upcoming_lessons,
            "recent_lessons": recent_lessons,
            "student_count": len(students)
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to get teacher portal data: {str(e)}")
        return {}

def get_student_portal_data(student_email):
    """Get portal data specific to students"""
    try:
        # Find student record
        student_record = frappe.get_value("ESL Student", {"email": student_email}, 
            ["name", "student_name", "teacher", "level", "goals"], as_dict=True)
        
        if not student_record:
            return {"error": "Student profile not found"}
        
        # Get student's lessons
        lessons = frappe.get_all("ESL Lesson",
            filters={"student": student_record.name},
            fields=["name", "title", "scheduled_time", "status", "meet_link"],
            order_by="scheduled_time desc",
            limit=10
        )
        
        # Get upcoming lessons
        upcoming_lessons = [l for l in lessons if l.status == "Scheduled"]
        
        # Get teacher info
        teacher_info = None
        if student_record.teacher:
            teacher_info = frappe.get_value("User", student_record.teacher,
                ["full_name", "email"], as_dict=True)
        
        return {
            "student_profile": student_record,
            "lessons": lessons,
            "upcoming_lessons": upcoming_lessons,
            "teacher_info": teacher_info,
            "lesson_count": len(lessons)
        }
        
    except Exception as e:
        frappe.log_error(f"Failed to get student portal data: {str(e)}")
        return {"error": str(e)}

