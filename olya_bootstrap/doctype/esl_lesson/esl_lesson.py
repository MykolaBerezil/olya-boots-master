import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class ESLLesson(Document):
    def validate(self):
        """Validate ESL Lesson data"""
        if self.scheduled_time:
            # Ensure lesson is not scheduled in the past
            if frappe.utils.get_datetime(self.scheduled_time) < frappe.utils.now_datetime():
                if self.status == "Scheduled":
                    frappe.throw("Cannot schedule lesson in the past")
        
        # Auto-assign teacher from student if not set
        if self.student and not self.teacher:
            student_doc = frappe.get_doc("ESL Student", self.student)
            if student_doc.teacher:
                self.teacher = student_doc.teacher
    
    def before_save(self):
        """Actions before saving the lesson"""
        # Update status based on time
        if self.scheduled_time and self.status == "Scheduled":
            now = frappe.utils.now_datetime()
            lesson_time = frappe.utils.get_datetime(self.scheduled_time)
            
            if lesson_time < now - timedelta(hours=2):
                # Lesson was more than 2 hours ago, mark as completed if no status change
                if not self.get_doc_before_save() or self.get_doc_before_save().status == "Scheduled":
                    self.status = "Completed"
    
    def after_insert(self):
        """Actions after lesson is created"""
        # Send notification to student and teacher
        self.send_lesson_notification()
    
    def send_lesson_notification(self):
        """Send email notification about the lesson"""
        if not self.student or not self.teacher:
            return
            
        try:
            # Get student email
            student_doc = frappe.get_doc("ESL Student", self.student)
            teacher_doc = frappe.get_doc("User", self.teacher)
            
            # Email to student
            if student_doc.email:
                frappe.sendmail(
                    recipients=[student_doc.email],
                    subject=f"ESL Lesson Scheduled: {self.title}",
                    message=f"""
                    <h3>Your ESL lesson has been scheduled!</h3>
                    <p><strong>Lesson:</strong> {self.title}</p>
                    <p><strong>Teacher:</strong> {teacher_doc.full_name}</p>
                    <p><strong>Time:</strong> {frappe.utils.format_datetime(self.scheduled_time)}</p>
                    <p><strong>Duration:</strong> {self.duration} minutes</p>
                    {f'<p><strong>Meet Link:</strong> <a href="{self.meet_link}">{self.meet_link}</a></p>' if self.meet_link else ''}
                    <p>Please be ready 5 minutes before the scheduled time.</p>
                    """
                )
            
            # Email to teacher
            if teacher_doc.email:
                frappe.sendmail(
                    recipients=[teacher_doc.email],
                    subject=f"ESL Lesson Scheduled: {self.title}",
                    message=f"""
                    <h3>You have a new ESL lesson scheduled!</h3>
                    <p><strong>Lesson:</strong> {self.title}</p>
                    <p><strong>Student:</strong> {student_doc.student_name}</p>
                    <p><strong>Time:</strong> {frappe.utils.format_datetime(self.scheduled_time)}</p>
                    <p><strong>Duration:</strong> {self.duration} minutes</p>
                    {f'<p><strong>Meet Link:</strong> <a href="{self.meet_link}">{self.meet_link}</a></p>' if self.meet_link else ''}
                    <p>Access the lesson form to add lesson plans and materials.</p>
                    """
                )
        except Exception as e:
            frappe.log_error(f"Failed to send lesson notification: {str(e)}")
    
    def create_google_meet_link(self):
        """Create Google Meet link for this lesson"""
        try:
            # Call the API to create meet link
            from olya_bootstrap.api.calendar import create_google_meet
            
            student_doc = frappe.get_doc("ESL Student", self.student) if self.student else None
            student_email = student_doc.email if student_doc else None
            
            result = create_google_meet(
                title=self.title,
                when=self.scheduled_time,
                student_email=student_email
            )
            
            if result.get("meet_link"):
                self.meet_link = result["meet_link"]
                self.save()
                return result["meet_link"]
        except Exception as e:
            frappe.log_error(f"Failed to create Google Meet link: {str(e)}")
            frappe.throw("Failed to create Google Meet link. Please check Google API configuration.")
    
    def get_student_info(self):
        """Get detailed student information"""
        if not self.student:
            return None
            
        return frappe.get_doc("ESL Student", self.student)
    
    def mark_completed(self):
        """Mark lesson as completed"""
        self.status = "Completed"
        self.save()
        
    def cancel_lesson(self, reason=None):
        """Cancel the lesson"""
        self.status = "Cancelled"
        if reason:
            self.notes = f"{self.notes}\n\nCancellation reason: {reason}" if self.notes else f"Cancellation reason: {reason}"
        self.save()

