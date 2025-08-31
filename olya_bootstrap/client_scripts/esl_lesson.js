// ESL Lesson Client Script
// Adds Google Meet integration and enhanced UI

frappe.ui.form.on('ESL Lesson', {
    refresh(frm) {
        // Add custom buttons
        add_custom_buttons(frm);
        
        // Style the form
        style_form(frm);
        
        // Add real-time status updates
        setup_status_updates(frm);
    },
    
    student(frm) {
        // Auto-populate teacher when student is selected
        if (frm.doc.student && !frm.doc.teacher) {
            frappe.db.get_value('ESL Student', frm.doc.student, 'teacher')
                .then(r => {
                    if (r.message && r.message.teacher) {
                        frm.set_value('teacher', r.message.teacher);
                    }
                });
        }
    },
    
    scheduled_time(frm) {
        // Validate scheduling time
        if (frm.doc.scheduled_time) {
            const now = new Date();
            const lessonTime = new Date(frm.doc.scheduled_time);
            
            if (lessonTime < now) {
                frappe.msgprint({
                    title: 'Invalid Time',
                    message: 'Cannot schedule lesson in the past',
                    indicator: 'red'
                });
                frm.set_value('scheduled_time', '');
            }
        }
    }
});

function add_custom_buttons(frm) {
    // Clear existing custom buttons
    frm.clear_custom_buttons();
    
    // Create Google Meet Link button
    if (!frm.doc.meet_link && frm.doc.scheduled_time) {
        frm.add_custom_button('Create Meet Link', async () => {
            try {
                frm.dashboard.set_headline_alert('Creating Google Meet link...', 'blue');
                
                // Get student email
                let student_email = null;
                if (frm.doc.student) {
                    const student_data = await frappe.db.get_value('ESL Student', frm.doc.student, 'email');
                    student_email = student_data.message?.email;
                }
                
                // Call API to create meet link
                const response = await frappe.call({
                    method: 'olya_bootstrap.api.calendar.create_google_meet',
                    args: {
                        title: frm.doc.title,
                        when: frm.doc.scheduled_time,
                        student_email: student_email
                    }
                });
                
                if (response.message && response.message.meet_link) {
                    frm.set_value('meet_link', response.message.meet_link);
                    await frm.save();
                    
                    frm.dashboard.clear_headline();
                    frappe.show_alert({
                        message: 'Google Meet link created and saved!',
                        indicator: 'green'
                    });
                    
                    // Refresh buttons
                    add_custom_buttons(frm);
                }
            } catch (error) {
                frm.dashboard.clear_headline();
                frappe.msgprint({
                    title: 'Error',
                    message: 'Failed to create Meet link. Please check Google API configuration.',
                    indicator: 'red'
                });
                console.error('Meet link creation error:', error);
            }
        }, 'Actions');
    }
    
    // Join Meet button (if link exists)
    if (frm.doc.meet_link) {
        frm.add_custom_button('Join Meet', () => {
            window.open(frm.doc.meet_link, '_blank');
        }, 'Actions');
    }
    
    // Quick status update buttons
    if (frm.doc.status === 'Scheduled') {
        frm.add_custom_button('Start Lesson', () => {
            frm.set_value('status', 'In Progress');
            frm.save();
        }, 'Status');
        
        frm.add_custom_button('Cancel Lesson', () => {
            frappe.prompt([
                {
                    label: 'Cancellation Reason',
                    fieldname: 'reason',
                    fieldtype: 'Small Text',
                    reqd: 1
                }
            ], (values) => {
                frm.set_value('status', 'Cancelled');
                const currentNotes = frm.doc.notes || '';
                frm.set_value('notes', currentNotes + `\n\nCancelled: ${values.reason}`);
                frm.save();
            }, 'Cancel Lesson', 'Cancel');
        }, 'Status');
    }
    
    if (frm.doc.status === 'In Progress') {
        frm.add_custom_button('Complete Lesson', () => {
            frm.set_value('status', 'Completed');
            frm.save();
        }, 'Status');
    }
    
    // Open Whiteboard button
    frm.add_custom_button('Open Whiteboard', () => {
        window.open('/whiteboard', '_blank');
    }, 'Tools');
    
    // Student Profile button
    if (frm.doc.student) {
        frm.add_custom_button('Student Profile', () => {
            frappe.set_route('Form', 'ESL Student', frm.doc.student);
        }, 'Tools');
    }
}

function style_form(frm) {
    // Add custom CSS for better form styling
    if (!document.getElementById('olya-lesson-styles')) {
        const style = document.createElement('style');
        style.id = 'olya-lesson-styles';
        style.textContent = `
            .form-layout .section-head {
                background: linear-gradient(135deg, #9333ea, #ec4899);
                color: white;
                padding: 0.75rem 1rem;
                margin-bottom: 1rem;
                border-radius: 8px;
                font-weight: 600;
            }
            
            .form-column .form-section:first-child .section-head {
                margin-top: 0;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #9333ea, #ec4899) !important;
                border: none !important;
                transition: all 0.3s ease !important;
            }
            
            .btn-primary:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 5px 15px rgba(147, 51, 234, 0.3) !important;
            }
            
            .form-control:focus {
                border-color: #9333ea !important;
                box-shadow: 0 0 0 2px rgba(147, 51, 234, 0.1) !important;
            }
            
            .meet-link-display {
                background: #f0f9ff;
                border: 2px solid #0ea5e9;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
                text-align: center;
            }
            
            .meet-link-display a {
                color: #0ea5e9;
                font-weight: 600;
                text-decoration: none;
                font-size: 1.1rem;
            }
            
            .meet-link-display a:hover {
                text-decoration: underline;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add Meet link display if exists
    if (frm.doc.meet_link && !frm.meet_link_displayed) {
        const meetLinkHtml = `
            <div class="meet-link-display">
                <strong>Google Meet Link:</strong><br>
                <a href="${frm.doc.meet_link}" target="_blank">${frm.doc.meet_link}</a>
            </div>
        `;
        
        // Add after the meet_link field
        setTimeout(() => {
            const meetLinkField = frm.get_field('meet_link');
            if (meetLinkField && meetLinkField.$wrapper) {
                meetLinkField.$wrapper.after(meetLinkHtml);
                frm.meet_link_displayed = true;
            }
        }, 100);
    }
}

function setup_status_updates(frm) {
    // Real-time status indicator
    if (frm.doc.scheduled_time) {
        const now = new Date();
        const lessonTime = new Date(frm.doc.scheduled_time);
        const timeDiff = lessonTime - now;
        
        let statusMessage = '';
        let statusColor = 'blue';
        
        if (timeDiff < 0) {
            // Lesson time has passed
            if (frm.doc.status === 'Scheduled') {
                statusMessage = 'Lesson time has passed - please update status';
                statusColor = 'orange';
            }
        } else if (timeDiff < 15 * 60 * 1000) {
            // Less than 15 minutes
            statusMessage = 'Lesson starting soon!';
            statusColor = 'green';
        } else if (timeDiff < 60 * 60 * 1000) {
            // Less than 1 hour
            statusMessage = 'Lesson starting in less than 1 hour';
            statusColor = 'blue';
        }
        
        if (statusMessage) {
            frm.dashboard.set_headline_alert(statusMessage, statusColor);
        }
    }
}

// Global helper functions
window.olya_lesson_utils = {
    formatDuration: function(minutes) {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        
        if (hours > 0) {
            return `${hours}h ${mins}m`;
        }
        return `${mins}m`;
    },
    
    getStatusColor: function(status) {
        const colors = {
            'Scheduled': '#3b82f6',
            'In Progress': '#f59e0b',
            'Completed': '#10b981', 
            'Cancelled': '#ef4444',
            'Rescheduled': '#8b5cf6'
        };
        return colors[status] || '#6b7280';
    },
    
    copyMeetLink: function(link) {
        navigator.clipboard.writeText(link).then(() => {
            frappe.show_alert({
                message: 'Meet link copied to clipboard!',
                indicator: 'green'
            });
        });
    }
};

