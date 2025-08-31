import frappe
from frappe.model.document import Document

class ESLStudent(Document):
    def validate(self):
        """Validate ESL Student data"""
        if self.email:
            # Ensure email is unique
            existing = frappe.db.get_value("ESL Student", {"email": self.email, "name": ("!=", self.name)})
            if existing:
                frappe.throw(f"Email {self.email} is already registered for another student")
        
        # Auto-assign teacher if not set
        if not self.teacher:
            self.auto_assign_teacher()
    
    def auto_assign_teacher(self):
        """Auto-assign a teacher based on availability"""
        # Get teachers with ESL Teacher role
        teachers = frappe.get_all("User", 
            filters={"enabled": 1},
            fields=["name", "full_name"]
        )
        
        # Filter teachers who have ESL Teacher role
        esl_teachers = []
        for teacher in teachers:
            roles = frappe.get_roles(teacher.name)
            if "ESL Teacher" in roles:
                esl_teachers.append(teacher)
        
        if esl_teachers:
            # Simple round-robin assignment (can be enhanced)
            import random
            selected_teacher = random.choice(esl_teachers)
            self.teacher = selected_teacher.name
    
    def after_insert(self):
        """Actions after student is created"""
        # Create user account if email is provided and user doesn't exist
        if self.email and not frappe.db.exists("User", self.email):
            self.create_user_account()
    
    def create_user_account(self):
        """Create user account for the student"""
        try:
            user = frappe.get_doc({
                "doctype": "User",
                "email": self.email,
                "first_name": self.student_name.split()[0] if self.student_name else "Student",
                "last_name": " ".join(self.student_name.split()[1:]) if len(self.student_name.split()) > 1 else "",
                "send_welcome_email": 1,
                "user_type": "Website User"
            })
            user.insert(ignore_permissions=True)
            
            # Assign ESL Student role
            user.add_roles("ESL Student")
            
            frappe.msgprint(f"User account created for {self.email}")
        except Exception as e:
            frappe.log_error(f"Failed to create user account: {str(e)}")
    
    def get_lessons(self):
        """Get all lessons for this student"""
        return frappe.get_all("ESL Lesson",
            filters={"student": self.name},
            fields=["name", "title", "scheduled_time", "status", "meet_link"],
            order_by="scheduled_time desc"
        )

