# OLYA Bootstrap

Complete Frappe app for OLYA ESL platform with Coming Soon page, LMS integration, Google Meet, and teacher/student portal.

## Overview

This Frappe app automatically sets up:

- **Website Theme** with OLYA ESL branding
- **Coming Soon Homepage** at root URL
- **Portal Menu** with student/teacher navigation
- **DocTypes**: ESL Student, ESL Lesson
- **Google Meet Integration** via client scripts
- **API endpoints** for calendar/meet functionality
- **Automated installation** via hooks

## Installation

### On Frappe Cloud

1. Go to **App Installer** → **Install from Git URL**
2. Enter: `https://github.com/MykolaBerezil/olya-boots-master.git`
3. Click **Install**
4. The app will automatically configure your site

### Local Development

```bash
# Get the app
bench get-app https://github.com/MykolaBerezil/olya-boots-master.git

# Install on site
bench --site [your-site] install-app olya_bootstrap
```

## Features

### Automatic Setup
- Creates OLYA ESL theme with purple/pink branding
- Publishes coming soon homepage
- Enables portal with teacher/student menus
- Creates ESL Student and ESL Lesson DocTypes
- Sets up Google Meet integration button

### DocTypes
- **ESL Student**: Name, email, teacher, level, goals
- **ESL Lesson**: Title, student, time, meet link, status

### Integration Ready
- **Payments**: Compatible with Frappe Payments app
- **LMS**: Ready for Frappe LMS integration
- **Google**: OAuth setup for Calendar/Meet API
- **Portal**: Student and teacher dashboards

## File Structure

```
olya_bootstrap/
├── README.md
├── MANIFEST.in
├── setup.py
├── requirements.txt
└── olya_bootstrap/
   ├── __init__.py
   ├── hooks.py
   ├── after_install.py
   ├── www/
   │  └── index.html
   ├── public/
   │  └── css/olya.css
   ├── config/
   │  └── desktop.py
   ├── portal/
   │  └── menu.py
   ├── client_scripts/
   │  └── esl_lesson.js
   ├── api/
   │  └── calendar.py
   └── doctype/
      ├── esl_student/
      │  └── esl_student.json
      └── esl_lesson/
         └── esl_lesson.json
```

## Usage

After installation:

1. **Visit your site** - Coming soon page will be live
2. **Access portal** - Students/teachers can log in
3. **Create lessons** - Use ESL Lesson DocType
4. **Generate Meet links** - Click button in lesson form
5. **Add payments** - Install Frappe Payments app
6. **Add courses** - Install Frappe LMS when ready

## Configuration

### Google Meet Setup
1. Create Google Cloud project
2. Enable Calendar API
3. Add OAuth credentials to Social Login Keys
4. Update `api/calendar.py` with real API calls

### Theme Customization
Edit colors in `after_install.py`:
```python
"primary_color": "#9333ea",  # Purple
"secondary_color": "#ec4899"  # Pink
```

## License

MIT License - Free for commercial and personal use.

## Support

For issues and questions, please use GitHub Issues or contact team@olyaesl.com.

