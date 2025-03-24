from sqlalchemy.orm import Session
from app.crud.therapist import create_therapist
from app.schemas.therapist import TherapistCreate
from app.db.session import SessionLocal, engine
from app.models.therapist import Base
from app.models.journal import Journal
from app.models.user import User
from datetime import datetime
import uuid

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

initial_journals = [
  {
    "title": "Morning Reflections",
    "content": "I woke up early today, just before sunrise. The house was silent, and I took a moment to enjoy the stillness before stepping outside to breathe in the crisp morning air. It felt refreshing. I made myself a cup of green tea and sat by the window, watching as the golden sunlight slowly spread across the sky. It’s moments like these that remind me to slow down and appreciate the little things. Before diving into my day, I decided to meditate for ten minutes. Sitting in stillness, I focused on my breath, letting go of any worries or distractions. The practice helped set a calm tone for my morning. I then wrote down my intentions for the day, reminding myself to stay present and embrace every experience. I realized that starting my day with peace makes a huge difference in my overall mood. It’s a habit I want to maintain. After finishing my tea, I stretched for a bit and then got ready to tackle my tasks with a fresh mind. I’m grateful for this quiet morning, and I hope to create more such moments for myself.",
    "tags": ["morning", "mindfulness", "gratitude"],
    "createdAt": "2025-02-10T08:30:00Z",
    "updatedAt": "2025-02-10T08:30:00Z"
  },
  {
    "title": "Productive Workday",
    "content": "Today was one of those rare days where I felt completely in the zone. From the moment I sat at my desk, I knew it would be a productive day. I started by organizing my tasks into a checklist, prioritizing the most important ones. Having clarity about what needed to be done helped me stay focused. I tackled my first major task without distractions, and before I knew it, an hour had passed. Feeling accomplished, I moved on to the next item on my list. I made sure to take short breaks in between, which surprisingly made me even more efficient. By lunchtime, I had completed almost everything I had planned. The sense of accomplishment was rewarding. I wrapped up my workday by reviewing my progress and setting goals for tomorrow. Productivity isn't just about doing more; it’s about working smart and maintaining balance. I realized that proper planning and taking mindful breaks really make a difference. If I can continue this rhythm, I’ll be able to achieve my long-term goals without feeling overwhelmed. Ending the day on a positive note, I treated myself to a relaxing evening with a book and some soothing music.",
    "tags": ["work", "productivity", "success"],
    "createdAt": "2025-02-11T18:45:00Z",
    "updatedAt": "2025-02-11T18:45:00Z"
  },
  {
    "title": "A Rainy Evening",
    "content": "It rained all afternoon today, and I found myself lost in the peaceful rhythm of the raindrops against my window. There’s something magical about a rainy day, especially when you don’t have to be anywhere. I made myself a hot cup of coffee, grabbed my favorite book, and settled into my cozy armchair. The world outside seemed to slow down, and for the first time in a while, I allowed myself to just be. I read a few chapters of my book, but eventually, I just stared outside, watching the rain dance on the pavement. It reminded me of childhood days when I used to run outside and jump in puddles. It’s funny how the simplest memories can bring the most comfort. The soft thunder in the distance and the cool breeze that slipped through my window made everything feel even more serene. I took a deep breath and allowed myself to fully enjoy this moment. No distractions, no worries—just me, the rain, and the quiet sense of peace it brought. As the evening faded into night, I felt a deep sense of gratitude for these little joys that life offers.",
    "tags": ["rain", "relaxation", "peace"],
    "createdAt": "2025-02-12T19:15:00Z",
    "updatedAt": "2025-02-12T19:15:00Z"
  },
  {
    "title": "A Walk in the Park",
    "content": "This evening, I decided to take a long walk in the nearby park. Lately, I’ve been spending too much time indoors, caught up in work and responsibilities, and I felt the need to reconnect with nature. As I stepped onto the winding path, I immediately felt lighter. The fresh air, the distant sound of birds chirping, and the sight of trees swaying gently in the wind created a calming atmosphere. I walked slowly, observing everything around me—the golden hue of the setting sun, the laughter of children playing, the rhythmic crunch of leaves beneath my feet. I found a quiet bench near the lake and sat down for a while. Watching the ripples in the water, I felt a sense of stillness settle over me. I realized how rarely I allow myself to just sit and observe without feeling the need to do something. In that moment, I felt deeply at peace. As I made my way back home, I promised myself to take more walks like this—to disconnect from screens and immerse myself in the beauty of the real world.",
    "tags": ["nature", "peace", "self-care"],
    "createdAt": "2025-02-13T17:00:00Z",
    "updatedAt": "2025-02-13T17:00:00Z"
  },
  {
    "title": "Cooking Experiment",
    "content": "Today, I stepped out of my comfort zone and tried cooking a new recipe—spicy Thai curry. Cooking has always been something I enjoy, but I usually stick to familiar dishes. This time, I wanted to challenge myself. I gathered all the ingredients, carefully following the recipe while adding my own little tweaks along the way. The kitchen was soon filled with the aromatic blend of coconut milk, fresh herbs, and exotic spices. As I stirred the simmering curry, I felt a sense of accomplishment. The best part of cooking is watching simple ingredients transform into something delicious. When I finally sat down to eat, I was pleasantly surprised—it tasted even better than I had imagined! Cooking is not just about the final dish; it’s about the process, the patience, and the creativity involved. I realized that stepping out of my routine and trying new things brings excitement and joy. Inspired by today’s success, I plan to experiment with more recipes in the coming weeks. Maybe next time, I’ll try baking something sweet!",
    "tags": ["food", "hobby", "creativity"],
    "createdAt": "2025-02-14T20:30:00Z",
    "updatedAt": "2025-02-14T20:30:00Z"
  },
  {
    "title": "An Afternoon at the Coffee Shop",
    "content": "I decided to work from a coffee shop today instead of staying at home. The change of scenery felt refreshing. I found a cozy corner by the window, ordered a cappuccino, and set up my laptop. The background hum of conversations, the occasional clinking of cups, and the soft jazz music playing in the background created the perfect atmosphere for focus. I managed to get a lot of work done, much more than I do at home. There's something about being surrounded by people that keeps me motivated. After a productive few hours, I put my laptop away and just observed the world around me. A group of friends laughed over shared stories, a man sat reading a book, and the barista carefully crafted a beautiful latte. It reminded me how important it is to step outside our usual spaces and experience life in different settings. Before leaving, I took a deep breath, savoring the smell of coffee beans and the warmth of the space. I think I’ll make this a regular habit.",
    "tags": ["coffee shop", "productivity", "change"],
    "createdAt": "2025-02-15T14:20:00Z",
    "updatedAt": "2025-02-15T14:20:00Z"
  },
  {
    "title": "Learning Something New",
    "content": "Today, I started learning Spanish. It’s something I’ve always wanted to do, but I never made the time for it. I downloaded an app and completed my first lesson. The words felt foreign on my tongue, but there was an excitement in the challenge. I practiced simple greetings—'Hola,' 'Buenos días,' 'Gracias.' It felt good to engage my brain in a new way. I realized that learning a language is more than just memorizing words; it’s about understanding a culture, a way of thinking, and a new way of expressing oneself. I watched a short Spanish movie with subtitles, trying to pick up words I recognized. It made me appreciate how complex yet beautiful languages are. I’ve set a goal for myself: practice a little every day. I don’t expect to be fluent overnight, but even small progress is still progress. This journey is about enjoying the process and not just reaching a destination. Learning something new makes me feel alive.",
    "tags": ["learning", "language", "growth"],
    "createdAt": "2025-02-16T10:00:00Z",
    "updatedAt": "2025-02-16T10:00:00Z"
  },
  {
    "title": "Decluttering My Space",
    "content": "I spent the entire morning decluttering my room. It was long overdue. I started with my closet, sorting clothes I haven’t worn in years. It was hard to let go of some pieces, but I reminded myself that if I haven’t used them in months, I probably never will. I set aside a bag for donation. Next, I tackled my desk—old papers, broken pens, random things I had been hoarding. The act of clearing out unnecessary items felt therapeutic. With each item I removed, I felt lighter, as if I was making space not just in my room but also in my mind. A clean, organized space brings a sense of clarity. I lit a scented candle afterward, enjoying the fresh energy in the room. Decluttering isn’t just about physical space; it’s also about clearing mental clutter. I feel more at peace now, and I plan to keep my space this way.",
    "tags": ["minimalism", "organization", "mental clarity"],
    "createdAt": "2025-02-17T12:30:00Z",
    "updatedAt": "2025-02-17T12:30:00Z"
  },
  {
    "title": "Reconnecting with an Old Friend",
    "content": "Today, I had a long phone call with an old friend I hadn’t spoken to in years. Life had taken us in different directions, and somehow, we lost touch. But today, we picked up right where we left off. We talked about our lives, the things that changed, and the things that remained the same. There was so much laughter, nostalgia, and shared memories. It made me realize how important it is to nurture relationships, even when life gets busy. Some friendships are timeless, and no matter how much time passes, they remain as strong as ever. I promised myself that I won’t let so much time pass before reaching out again. It’s easy to get caught up in daily routines and forget to check in with people who matter. This conversation was a reminder that friendships, like plants, need care and attention to grow.",
    "tags": ["friendship", "connection", "nostalgia"],
    "createdAt": "2025-02-18T18:00:00Z",
    "updatedAt": "2025-02-18T18:00:00Z"
  },
  {
    "title": "A Day Without Social Media",
    "content": "I decided to take a break from social media today. No endless scrolling, no checking notifications—just a full day of being present. At first, I felt the urge to reach for my phone, but I resisted. Instead, I spent my morning reading a book and journaling. I went outside for a walk without feeling the need to take a picture or post about it. I noticed things I usually overlook—the pattern of clouds in the sky, the way the wind made the leaves dance. It was refreshing. I realized how much time I unconsciously spend on social media and how little of it actually adds value to my life. Today, I felt lighter, more focused, and more connected to the world around me. I think I’ll make this a regular habit—disconnecting to truly connect.",
    "tags": ["digital detox", "mindfulness", "self-care"],
    "createdAt": "2025-02-19T09:00:00Z",
    "updatedAt": "2025-02-19T09:00:00Z"
  },
  {
    "title": "An Evening of Stargazing",
    "content": "Tonight, I lay outside under the night sky, staring at the stars. The vastness of space always puts things into perspective for me. It makes my worries seem small, reminding me of how big the universe truly is. I tried to spot constellations, though I could only recognize a few. I sat in silence, listening to the distant sounds of crickets and feeling the cool breeze against my skin. It was a moment of pure serenity. I thought about how ancient civilizations navigated using these very stars and how much history is written in the night sky. In that moment, I felt both small and infinite at the same time. There is something deeply comforting about realizing that life moves on, the stars continue to shine, and everything finds its place in the universe. I need more nights like this—simple, quiet, and full of wonder.",
    "tags": ["stargazing", "perspective", "peace"],
    "createdAt": "2025-02-20T22:15:00Z",
    "updatedAt": "2025-02-20T22:15:00Z"
  },
  {
    "title": "Trying Yoga for the First Time",
    "content": "Today, I tried yoga for the first time. I’ve always heard about its benefits, but I never really gave it a shot. I followed a beginner’s routine online, starting with simple stretches. At first, my body felt stiff, and my balance was terrible, but as I moved through the poses, I started to feel more connected to my body. I focused on my breathing, something I rarely do consciously. The final pose, Savasana, was my favorite—it allowed me to fully relax. After just 30 minutes, I felt calmer and more present. It’s amazing how something so simple can have such a profound effect. I think I’ll make this a daily habit and see where it takes me.",
    "tags": ["yoga", "self-care", "wellness"],
    "createdAt": "2025-02-21T07:30:00Z",
    "updatedAt": "2025-02-21T07:30:00Z"
  },
  {
    "title": "A Random Act of Kindness",
    "content": "Today, I experienced the joy of giving without expecting anything in return. I was at a café when I noticed an elderly man struggling to carry his tray. Without thinking twice, I walked over and helped him find a seat. He looked at me with the warmest smile and said, ‘Thank you, young one. You made my day.’ That moment stayed with me. It made me realize how small acts of kindness can create ripples of positivity. We often underestimate the impact of simple gestures—a kind word, a helping hand, or even a genuine smile. The world feels a little better when we choose kindness, and today, I felt that firsthand.",
    "tags": ["kindness", "humanity", "positivity"],
    "createdAt": "2025-02-22T11:00:00Z",
    "updatedAt": "2025-02-22T11:00:00Z"
  },
  {
    "title": "Overcoming Self-Doubt",
    "content": "I caught myself today, doubting my own abilities. I was about to start a new project, but the fear of failure crept in. ‘What if I’m not good enough? What if I fail?’ But then I stopped. I reminded myself that every expert was once a beginner. Growth happens through action, not through overthinking. So, I took a deep breath and started. The more I worked, the more confident I felt. I realized that self-doubt is just a voice—it doesn’t have to define me. Moving forward, I will choose progress over perfection. I will remind myself that I am capable, and I deserve to try.",
    "tags": ["self-doubt", "motivation", "growth"],
    "createdAt": "2025-02-23T15:30:00Z",
    "updatedAt": "2025-02-23T15:30:00Z"
  },
  {
    "title": "Sunday Reset",
    "content": "Today, I dedicated my entire Sunday to resetting my mind and space. I started with a deep clean—laundry, organizing my desk, and changing my bedsheets. Then, I spent an hour planning my week ahead, listing down priorities and setting small goals. I made time for self-care too—took a long shower, applied a face mask, and read a few chapters of my book. By evening, I felt refreshed and ready for the new week. Sundays like these are essential for my mental well-being. They remind me that taking care of myself is just as important as being productive.",
    "tags": ["self-care", "routine", "reset"],
    "createdAt": "2025-02-24T20:00:00Z",
    "updatedAt": "2025-02-24T20:00:00Z"
  },
  {
    "title": "A Moment of Gratitude",
    "content": "Before bed, I took a moment to reflect on the things I’m grateful for. It’s easy to get caught up in what’s missing, but today, I focused on what’s present. I’m grateful for my health, for the roof over my head, and for the people in my life who love me. I’m grateful for small joys—the warmth of my blanket, the taste of my favorite tea, and the peaceful silence of the night. Gratitude shifts my perspective. It turns ordinary moments into something meaningful. I want to make this a daily habit—ending each day with a grateful heart.",
    "tags": ["gratitude", "reflection", "peace"],
    "createdAt": "2025-02-25T22:45:00Z",
    "updatedAt": "2025-02-25T22:45:00Z"
  },
  {
    "title": "Stepping Outside My Comfort Zone",
    "content": "Today, I did something that scared me—I spoke in front of a group. Public speaking has always been a fear of mine, but I pushed myself to do it anyway. My hands trembled at first, but as I spoke, I realized that people were actually listening. By the time I finished, I felt exhilarated. Fear only has power if we let it. Pushing past discomfort is how we grow. I’m proud of myself today, and I know that if I keep challenging my limits, I’ll only get better.",
    "tags": ["growth", "courage", "self-improvement"],
    "createdAt": "2025-02-26T14:15:00Z",
    "updatedAt": "2025-02-26T14:15:00Z"
  },
  {
    "title": "An Unplugged Day",
    "content": "I spent the whole day away from screens today—no phone, no laptop, no TV. Instead, I read, wrote in my journal, and went for a long walk. It felt strange at first, but soon, I found myself more present in each moment. I realized how often I rely on technology for distraction. Today, I felt more in tune with myself and the world around me. I laughed more, I noticed more, and I felt lighter. Sometimes, we need to disconnect to reconnect with what truly matters.",
    "tags": ["mindfulness", "digital detox", "presence"],
    "createdAt": "2025-02-27T08:00:00Z",
    "updatedAt": "2025-02-27T08:00:00Z"
  },
  {
    "title": "A Day of Creativity",
    "content": "I spent the entire afternoon painting today. I had no plan, no specific image in mind—I just let the brush guide me. The colors blended in unexpected ways, creating something beautiful. Art, for me, is an escape. It’s a way to express feelings I can’t put into words. By the time I finished, I felt lighter, freer. I want to create more often—not for perfection, but for the joy of creating itself.",
    "tags": ["creativity", "art", "expression"],
    "createdAt": "2025-02-28T16:30:00Z",
    "updatedAt": "2025-02-28T16:30:00Z"
  }
]



def generate_uuid():
    return str(uuid.uuid4())

def seed_db(db: Session) -> None:
    # First, check if we already have data
    # existing_user = db.query(User).filter(User.email == "admin@example.com").first()
    # if existing_user:
    #     print("Database already has seed data. Skipping...")
    #     return
        
    # Seed therapists
    # for therapist_data in initial_therapists:
    #     therapist = TherapistCreate(**therapist_data)
    #     create_therapist(db, therapist)
    
    # Create a test user for journals
    test_user = User(
        id=generate_uuid(),
        email="test@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        full_name="Test User",
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    # Seed journals
    for journal_data in initial_journals:
        # Parse the date strings to datetime objects
        created_at = datetime.fromisoformat(journal_data["createdAt"].replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(journal_data["updatedAt"].replace("Z", "+00:00"))
        
        journal = Journal(
            id=generate_uuid(),
            title=journal_data["title"],
            content=journal_data["content"],
            tags=journal_data["tags"],
            createdAt=created_at,
            updatedAt=updated_at,
            user_id=test_user.id
        )
        db.add(journal)
    
    db.commit()

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
