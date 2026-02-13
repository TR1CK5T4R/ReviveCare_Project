# patient/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class Patient(models.Model):
    """Patient model with authentication and profile information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)  # Hashed password
    
    # Profile Information
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Medical Information
    info = models.TextField(max_length=3000, help_text="Medical history, diagnosis, surgery details")
    
    # Assigned Doctor
    assigned_doctor = models.ForeignKey(
        'Doctor.Doctor', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='patients'
    )
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        """Hash and set password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if provided password matches"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class ExerciseSession(models.Model):
    """Exercise session tracking for patients"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='exercise_sessions')
    exercise_type = models.CharField(max_length=50)  # e.g., 'side-lateral-raise', 'bicep-curl'
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    target_reps = models.IntegerField(default=12)
    completed_reps = models.IntegerField(default=0)
    excellent_reps = models.IntegerField(default=0)
    good_reps = models.IntegerField(default=0)
    partial_reps = models.IntegerField(default=0)
    accuracy_score = models.FloatField(default=0.0)  # Calculated percentage
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.name} - {self.exercise_type} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-start_time']


class ChatMessage(models.Model):
    """Chat message history between patient and AI assistant"""
    SENDER_CHOICES = [
        ('patient', 'Patient'),
        ('ai', 'AI Assistant'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    language = models.CharField(max_length=10, default='english')  # 'english' or 'hindi'
    seriousness_score = models.FloatField(default=0.0, help_text="AI-assessed severity (0.0-1.0)")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.name} - {self.sender} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['timestamp']


class PatientReport(models.Model):
    """Medical reports and documents for patients"""
    REPORT_TYPES = [
        ('lab', 'Lab Results'),
        ('imaging', 'Imaging/X-Ray'),
        ('discharge', 'Discharge Summary'),
        ('prescription', 'Prescription'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file_url = models.URLField(blank=True, null=True, help_text="URL to stored document")
    uploaded_by = models.ForeignKey(
        'Doctor.Doctor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_reports'
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.name} - {self.title}"

    class Meta:
        ordering = ['-created_at']
