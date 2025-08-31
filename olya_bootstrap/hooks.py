app_name = "olya_bootstrap"
app_title = "OLYA Bootstrap"
app_publisher = "OLYA ESL"
app_description = "Complete Frappe app for OLYA ESL platform with Coming Soon page, LMS integration, Google Meet, and teacher/student portal"
app_version = "0.1.0"
app_email = "team@olyaesl.com"
app_license = "MIT"

# Ensure these apps are present (Frappe Cloud can install them first)
required_apps = ["payments"]  # add "lms" later when ready

# Run setup after installation
after_install = "olya_bootstrap.after_install.run"

# Website route rules
website_route_rules = [
    {"from_route": "/", "to_route": "Home"},
    {"from_route": "/home", "to_route": "Home"},
    {"from_route": "/whiteboard", "to_route": "whiteboard"}
]

# Document Events
doc_events = {
    # Add any document event hooks here
}

# Scheduled Tasks
scheduler_events = {
    # Add any scheduled tasks here
}

# Override whitelisted methods
override_whitelisted_methods = {
    # Add any method overrides here
}

# Boot session
boot_session = "olya_bootstrap.utils.boot_session"

# Fixtures
fixtures = [
    # Add any fixtures here
]

# Installation
before_install = "olya_bootstrap.install.before_install"
after_install = "olya_bootstrap.install.after_install"

# Uninstallation  
before_uninstall = "olya_bootstrap.uninstall.before_uninstall"
after_uninstall = "olya_bootstrap.uninstall.after_uninstall"

# Desk Notifications
notification_config = "olya_bootstrap.notifications.get_notification_config"

# Website context
website_context = {
    "favicon": "/assets/olya_bootstrap/images/favicon.ico",
    "splash_image": "/assets/olya_bootstrap/images/splash.png"
}

# Include js, css files in header of desk.html
app_include_css = "/assets/olya_bootstrap/css/olya.css"
app_include_js = "/assets/olya_bootstrap/js/olya.js"

# Include js, css files in header of web template
web_include_css = "/assets/olya_bootstrap/css/olya.css"
web_include_js = "/assets/olya_bootstrap/js/olya.js"

# Home Pages
website_generators = ["Web Page"]

