from sqlalchemy.orm import Session
from app.crud.therapist import create_therapist
from app.schemas.therapist import TherapistCreate
from app.db.session import SessionLocal, engine
from app.models.therapist import Base

# Create all tables
Base.metadata.create_all(bind=engine)

initial_therapists = [
  {
    "name": "Shaily Tandon",
    "category": "Trauma Therapist",
    "qualification": "MS (Psychology)",
    "experience": "15 years",
    "description": "Shaily Tandon helps you in processing, healing, and reclaiming your strength after difficult experiences.",
    "rating": 4.8,
    "specialization": ["PTSD", "Trauma Counselling", "CBT"]
  },
  {
    "name": "Dr. Arjun Mehta",
    "category": "Clinical Psychologist",
    "qualification": "PhD in Clinical Psychology",
    "experience": "10 years",
    "description": "Dr. Arjun Mehta specializes in diagnosing and treating severe mental health disorders with a holistic approach.",
    "rating": 4.7,
    "specialization": ["Schizophrenia", "Bipolar Disorder", "Depression"]
  },
  {
    "name": "Neha Kapoor",
    "category": "Marriage & Family Therapist",
    "qualification": "MFT (Marriage & Family Therapy)",
    "experience": "12 years",
    "description": "Neha Kapoor helps couples and families navigate relationship challenges and build stronger bonds.",
    "rating": 4.6,
    "specialization": ["Relationship Issues", "Family Conflict", "Couples Therapy"]
  },
  {
    "name": "Dr. Vikram Shah",
    "category": "Child Psychologist",
    "qualification": "PhD in Child Psychology",
    "experience": "8 years",
    "description": "Dr. Vikram Shah provides psychological support to children facing developmental and emotional challenges.",
    "rating": 4.9,
    "specialization": ["ADHD", "Autism Spectrum", "Behavioral Therapy"]
  },
  {
    "name": "Riya Sen",
    "category": "Cognitive Behavioral Therapist",
    "qualification": "MS in Cognitive Psychology",
    "experience": "9 years",
    "description": "Riya Sen uses CBT techniques to help clients overcome negative thought patterns and build healthier habits.",
    "rating": 4.7,
    "specialization": ["CBT", "Anxiety Disorders", "Phobias"]
  },
  {
    "name": "Dr. Manish Khanna",
    "category": "Neuropsychologist",
    "qualification": "PhD in Neuropsychology",
    "experience": "14 years",
    "description": "Dr. Manish Khanna specializes in understanding the connection between brain function and behavior.",
    "rating": 4.8,
    "specialization": ["Brain Injury Recovery", "Memory Disorders", "Cognitive Therapy"]
  },
  {
    "name": "Sanya Verma",
    "category": "Trauma Therapist",
    "qualification": "MS in Psychology",
    "experience": "11 years",
    "description": "Sanya Verma helps individuals heal from past traumas and rebuild their emotional resilience.",
    "rating": 4.6,
    "specialization": ["PTSD", "Grief Counselling", "Somatic Therapy"]
  },
  {
    "name": "Dr. Rajat Singh",
    "category": "Forensic Psychologist",
    "qualification": "PhD in Forensic Psychology",
    "experience": "16 years",
    "description": "Dr. Rajat Singh provides psychological assessments for legal cases and works with criminal behavior analysis.",
    "rating": 4.7,
    "specialization": ["Criminal Profiling", "Witness Testimony", "Legal Consulting"]
  },
  {
    "name": "Meera Iyer",
    "category": "Depression & Anxiety Specialist",
    "qualification": "MS in Clinical Psychology",
    "experience": "10 years",
    "description": "Meera Iyer helps clients manage and overcome depression and anxiety through evidence-based therapy.",
    "rating": 4.9,
    "specialization": ["Anxiety Disorders", "Mindfulness-Based Therapy", "CBT"]
  },
  {
    "name": "Dr. Aditya Rao",
    "category": "Addiction Therapist",
    "qualification": "PhD in Addiction Studies",
    "experience": "13 years",
    "description": "Dr. Aditya Rao specializes in helping individuals recover from substance abuse and addictive behaviors.",
    "rating": 4.6,
    "specialization": ["Substance Abuse", "Rehabilitation Therapy", "Motivational Interviewing"]
  },
  {
    "name": "Tanya Malhotra",
    "category": "Grief Counselor",
    "qualification": "MS in Counseling Psychology",
    "experience": "7 years",
    "description": "Tanya Malhotra supports individuals coping with loss and grief to help them find peace and acceptance.",
    "rating": 4.8,
    "specialization": ["Bereavement Support", "Loss Counseling", "Trauma Healing"]
  },
  {
    "name": "Dr. Nikhil Sharma",
    "category": "Sports Psychologist",
    "qualification": "PhD in Sports Psychology",
    "experience": "9 years",
    "description": "Dr. Nikhil Sharma helps athletes improve mental resilience and peak performance.",
    "rating": 4.7,
    "specialization": ["Performance Anxiety", "Mental Conditioning", "Focus Training"]
  },
  {
    "name": "Ananya Choudhary",
    "category": "Behavioral Therapist",
    "qualification": "MS in Behavioral Psychology",
    "experience": "12 years",
    "description": "Ananya Choudhary uses behavioral interventions to help clients change negative habits and patterns.",
    "rating": 4.6,
    "specialization": ["Behavior Modification", "Anger Management", "Impulse Control"]
  },
  {
    "name": "Dr. Pranav Joshi",
    "category": "Pediatric Psychologist",
    "qualification": "PhD in Pediatric Psychology",
    "experience": "14 years",
    "description": "Dr. Pranav Joshi provides psychological care for children with emotional and developmental challenges.",
    "rating": 4.8,
    "specialization": ["Child Trauma", "Learning Disabilities", "Family Counseling"]
  },
  {
    "name": "Simran Batra",
    "category": "Mindfulness Coach",
    "qualification": "MS in Mindfulness-Based Therapy",
    "experience": "6 years",
    "description": "Simran Batra guides individuals in mindfulness practices to reduce stress and improve mental well-being.",
    "rating": 4.9,
    "specialization": ["Meditation", "Stress Reduction", "Mindfulness-Based CBT"]
  },
  {
    "name": "Dr. Rahul Menon",
    "category": "Geriatric Psychologist",
    "qualification": "PhD in Geriatric Psychology",
    "experience": "15 years",
    "description": "Dr. Rahul Menon specializes in mental health support for older adults dealing with aging-related issues.",
    "rating": 4.7,
    "specialization": ["Dementia Care", "Depression in Elderly", "End-of-Life Counseling"]
  },
  {
    "name": "Nikita Arora",
    "category": "LGBTQ+ Affirmative Therapist",
    "qualification": "MS in Gender Studies & Psychology",
    "experience": "10 years",
    "description": "Nikita Arora provides a safe and inclusive space for LGBTQ+ individuals seeking mental health support.",
    "rating": 4.9,
    "specialization": ["Gender Identity", "Coming Out Support", "Queer Mental Health"]
  },
  {
    "name": "Dr. Sameer Verma",
    "category": "Workplace Psychologist",
    "qualification": "PhD in Industrial Psychology",
    "experience": "12 years",
    "description": "Dr. Sameer Verma helps employees and organizations improve mental well-being in the workplace.",
    "rating": 4.6,
    "specialization": ["Workplace Stress", "Burnout Prevention", "Leadership Coaching"]
  },
  {
    "name": "Ishita Mukherjee",
    "category": "Art Therapist",
    "qualification": "MA in Art Therapy",
    "experience": "8 years",
    "description": "Ishita Mukherjee uses creative expression to support emotional healing and mental well-being.",
    "rating": 4.8,
    "specialization": ["Art-Based Therapy", "Trauma Healing", "Expressive Arts Therapy"]
  },
  {
    "name": "Dr. Kunal Sethi",
    "category": "Hypnotherapist",
    "qualification": "PhD in Hypnotherapy",
    "experience": "11 years",
    "description": "Dr. Kunal Sethi helps clients access their subconscious to overcome fears, trauma, and bad habits.",
    "rating": 4.7,
    "specialization": ["Hypnosis for Anxiety", "Smoking Cessation", "Past-Life Regression"]
  }
]


def seed_db(db: Session) -> None:
    for therapist_data in initial_therapists:
        therapist = TherapistCreate(**therapist_data)
        create_therapist(db, therapist)

def main() -> None:
    db = SessionLocal()
    try:
        seed_db(db)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
