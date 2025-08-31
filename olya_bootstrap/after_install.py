import frappe

def run():
    """
    Runs after app installation to automatically configure the site
    """
    create_theme()
    create_homepage()
    create_whiteboard_page()
    enable_portal_menu()
    make_roles()
    setup_website_settings()
    frappe.db.commit()

def create_theme():
    """Create OLYA ESL website theme"""
    if not frappe.db.exists("Website Theme", "OLYA ESL Theme"):
        doc = frappe.get_doc({
            "doctype": "Website Theme",
            "theme": "OLYA ESL Theme",
            "primary_color": "#9333ea",  # Purple
            "secondary_color": "#ec4899",  # Pink
            "text_color": "#1f2937",
            "background_color": "#ffffff",
            "app_logo": "",
            "font_size": "16px",
            "google_font": "Inter",
            "custom_scss": """
            .olya-hero {
                min-height: 70vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #fdf2f8, #f3e8ff);
            }
            .olya-card {
                max-width: 720px;
                background: #fff;
                border-radius: 16px;
                padding: 32px;
                box-shadow: 0 10px 30px rgba(0,0,0,.08);
                text-align: center;
            }
            .olya-card h1 {
                margin: 0 0 8px;
                color: #9333ea;
                font-size: 3rem;
                font-weight: 700;
            }
            .olya-card h3 {
                margin: 0 0 16px;
                color: #ec4899;
                font-size: 1.5rem;
                font-weight: 500;
            }
            .olya-card p {
                color: #6b7280;
                font-size: 1.1rem;
                margin: 0;
            }
            """
        })
        doc.insert(ignore_permissions=True)
        frappe.db.set_single_value("Website Settings", "website_theme", "OLYA ESL Theme")

def create_homepage():
    """Create coming soon homepage"""
    if not frappe.db.exists("Web Page", "Home"):
        html = """
        <section class="olya-hero">
          <div class="olya-card">
            <h1>OLYA ESL</h1>
            <h3>Empowering ESL Teachers Worldwide</h3>
            <p>Coming Soon. Fair pricing. Real tools. No exploitation.</p>
            <div style="margin-top: 24px;">
              <p style="font-size: 0.9rem; color: #9ca3af;">
                Building a platform that puts teachers first
              </p>
            </div>
          </div>
        </section>
        """
        doc = frappe.get_doc({
            "doctype": "Web Page",
            "title": "Home",
            "route": "",
            "published": 1,
            "content_type": "HTML",
            "html": html,
            "meta_title": "OLYA ESL - Empowering ESL Teachers Worldwide",
            "meta_description": "Coming soon - A fair platform for ESL teachers with real tools and honest pricing."
        })
        doc.insert(ignore_permissions=True)

def create_whiteboard_page():
    """Create whiteboard page with Excalidraw integration"""
    if not frappe.db.exists("Web Page", "Whiteboard"):
        html = """
        <div style="width: 100%; height: 100vh; border: none;">
          <iframe 
            src="https://excalidraw.com" 
            style="width: 100%; height: 100%; border: none;"
            title="Whiteboard - Excalidraw">
          </iframe>
        </div>
        """
        doc = frappe.get_doc({
            "doctype": "Web Page",
            "title": "Whiteboard",
            "route": "whiteboard",
            "published": 1,
            "content_type": "HTML",
            "html": html,
            "meta_title": "Whiteboard - OLYA ESL",
            "meta_description": "Interactive whiteboard for ESL lessons"
        })
        doc.insert(ignore_permissions=True)

def enable_portal_menu():
    """Setup portal menu items for students and teachers"""
    # Clear existing portal menu items for this app
    frappe.db.delete("Portal Menu Item", {"app": "olya_bootstrap"})
    
    # Add new portal menu items
    portal_items = [
        {
            "title": "My Lessons",
            "route": "/app/esl-lesson",
            "role": "ESL Teacher",
            "reference_doctype": "ESL Lesson"
        },
        {
            "title": "My Profile", 
            "route": "/app/esl-student",
            "role": "ESL Student",
            "reference_doctype": "ESL Student"
        },
        {
            "title": "Whiteboard",
            "route": "/whiteboard", 
            "role": "All"
        }
    ]
    
    for item in portal_items:
        if not frappe.db.exists("Portal Menu Item", {"title": item["title"], "app": "olya_bootstrap"}):
            doc = frappe.get_doc({
                "doctype": "Portal Menu Item",
                "title": item["title"],
                "route": item["route"],
                "role": item["role"],
                "reference_doctype": item.get("reference_doctype"),
                "app": "olya_bootstrap"
            })
            doc.insert(ignore_permissions=True)

def make_roles():
    """Create ESL-specific roles"""
    roles = ["ESL Teacher", "ESL Student", "ESL Administrator"]
    
    for role_name in roles:
        if not frappe.db.exists("Role", role_name):
            doc = frappe.get_doc({
                "doctype": "Role", 
                "role_name": role_name,
                "desk_access": 1 if role_name in ["ESL Teacher", "ESL Administrator"] else 0
            })
            doc.insert(ignore_permissions=True)

def setup_website_settings():
    """Configure website settings"""
    website_settings = frappe.get_single("Website Settings")
    website_settings.home_page = ""  # Use root route
    website_settings.title_prefix = "OLYA ESL - "
    website_settings.website_theme = "OLYA ESL Theme"
    website_settings.banner_html = ""
    website_settings.copyright = "© 2025 OLYA ESL. All rights reserved."
    website_settings.save(ignore_permissions=True)

