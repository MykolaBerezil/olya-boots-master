from frappe import _

def get_data():
    """
    Return desktop icons and shortcuts for OLYA ESL app.
    
    This configures what appears in the Frappe desk for users.
    """
    return [
        {
            "module_name": "OLYA ESL",
            "category": "Modules",
            "label": _("OLYA ESL"),
            "color": "#9333ea",
            "icon": "fa fa-graduation-cap",
            "type": "module",
            "description": "ESL Teaching Platform"
        },
        {
            "module_name": "ESL Student",
            "category": "OLYA ESL", 
            "label": _("Students"),
            "color": "#ec4899",
            "icon": "fa fa-users",
            "type": "doctype",
            "link": "List/ESL Student",
            "description": "Manage ESL students"
        },
        {
            "module_name": "ESL Lesson",
            "category": "OLYA ESL",
            "label": _("Lessons"), 
            "color": "#8b5cf6",
            "icon": "fa fa-calendar",
            "type": "doctype",
            "link": "List/ESL Lesson",
            "description": "Schedule and manage lessons"
        },
        {
            "module_name": "Whiteboard",
            "category": "OLYA ESL",
            "label": _("Whiteboard"),
            "color": "#06b6d4", 
            "icon": "fa fa-edit",
            "type": "page",
            "link": "/whiteboard",
            "description": "Interactive whiteboard for lessons"
        },
        {
            "module_name": "Teacher Dashboard",
            "category": "OLYA ESL",
            "label": _("Teacher Dashboard"),
            "color": "#10b981",
            "icon": "fa fa-dashboard", 
            "type": "page",
            "link": "/app/teacher-dashboard",
            "description": "Teacher overview and statistics"
        },
        {
            "module_name": "Student Portal",
            "category": "OLYA ESL",
            "label": _("Student Portal"),
            "color": "#f59e0b",
            "icon": "fa fa-user-graduate",
            "type": "page", 
            "link": "/app/student-portal",
            "description": "Student dashboard and profile"
        }
    ]

def get_workspace_sidebar_items():
    """
    Return workspace sidebar items for OLYA ESL.
    """
    return [
        {
            "label": _("Students"),
            "type": "doctype",
            "name": "ESL Student"
        },
        {
            "label": _("Lessons"),
            "type": "doctype", 
            "name": "ESL Lesson"
        },
        {
            "label": _("Whiteboard"),
            "type": "page",
            "route": "/whiteboard"
        },
        {
            "label": _("Reports"),
            "type": "page",
            "route": "/app/query-report"
        }
    ]

