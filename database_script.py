#Semua database BERKAITAN DENGAN DATABASE

import sqlite3
db_name = 'quiz.sqlite'
conn = None # Membuat Koneksi ke database
cursor = None # Cursor untuk akses datanase

# Mekanisme Akses Database
## Buka Database
def open():
  global conn, cursor
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()

## Tutup Database
def close():
  cursor.close()
  conn.close()

## Jelajah Database
def do(query):
  cursor.execute(query)

## Reset Database
def clear_db():
  open()
  query1 = '''DROP TABLE IF EXISTS quiz_content'''
  query2 = '''DROP TABLE IF EXISTS questions'''
  query3 = '''DROP TABLE IF EXISTS quiz'''
  do(query1)
  do(query2)
  do(query3)
  close()
## Membuat Tabel
def create():
  open()
  cursor.execute('''PRAGMA foreign_keys=on''')

  query_create_quiz_table = '''
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR
    )
  '''
  query_create_questions_table = '''
      CREATE TABLE IF NOT EXISTS questions (
          id INTEGER PRIMARY KEY,
          question VARCHAR,
          answer VARCHAR,
          wrong1 VARCHAR,
          wrong2 VARCHAR,
          wrong3 VARCHAR
      )
    '''
  query_create_quiz_content_table = '''
        CREATE TABLE IF NOT EXISTS quiz_content (
            id INTEGER PRIMARY KEY,
            quiz_id INTEGER,
            question_id INTEGER,

            FOREIGN KEY (quiz_id) REFERENCES quiz(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
      '''
  do(query_create_quiz_table)
  do(query_create_questions_table)
  do(query_create_quiz_content_table)
  close()

## Membuat daftar pertanyaan
def add_questions():
  questions = [
    ("Which country has the most natural lakes?","Canada", "US", "Australia", "Brazil"),
    ("What is the longest mountain range above water?","Andes", "Himalayas", "Rockies", "Alps"),
    ("Which city is on two continents?","Istanbul", "Cairo", "Singapore", "Buenos Aires"),
    ("What is the smallest independent country?","Vatican City", "Monaco", "Liechtenstein", "San Marino"),
    
    ("Which planet has the most moons?","Saturn", "Jupiter", "Uranus", "Neptune"),
    ("What is the boundary surrounding a black hole called?", "Event horizon", "Accretion disk", "Singularity", "Photon sphere"),
    ("How long does sunlight take to reach Earth?", "8 minutes", "8 seconds", "8 hours", "24 hours"),
    ("Which element is most abundant in the universe?", "Hydrogen", "Helium", "Oxygen", "Carbon"),
    
    ("Who wrote Pride and Prejudice?", "Jane Austen", "Charlotte Brontë", "Mary Shelley", "George Eliot"),
    ("In 1984, what is the ruling leader figure called?", "Big Brother", "The Directorate", "The Overlords", "Supreme Council"),
    ("What is the captain's name in Moby-Dick?", "Captain Ahab", "Captain Bligh", "Captain Hook", "Captain Nemo"),
    ("Which play features \"To be, or not to be\"?", "Hamlet", "Macbeth", "Romeo and Juliet", "Othello"),
  ]

  open()
  cursor.executemany(
    '''
    INSERT INTO questions
    (question, answer, wrong1, wrong2, wrong3)
    VALUES(?, ?, ?, ?, ?)
    ''', questions
  )
  conn.commit()
  close()

## Membuat daftar Type Quiz
def add_quiz():
  quizes = [
    ('Geografi',),
    ('Astronomi',),
    ('Sastra',)
  ]
  open()
  cursor.executemany(
    '''
    INSERT INTO quiz(name) VALUES (?)
    ''', quizes
  )
  conn.commit()
  close()

## Membuat hubungan antara pertanyaan dan Type Quiz
def add_links():
  link = [
      (1, 1),
      (1, 2),
      (1, 3),
      (1, 4),
      (2, 5),
      (2, 6),
      (2, 7),
      (2, 8),
      (3, 9),
      (3, 10),
      (3, 11),
      (3, 12),
  ]
  open()
  cursor.execute('''PRAGMA foreign_keys=on''')
  cursor.executemany(
    '''
    INSERT INTO quiz_content(quiz_id, question_id) VALUES (?,?)
    ''', link
  )
  conn.commit()
  close()
  print('Data seeded successfully')

# Apa yang diperlukan untuk menampilkan pertanyaan berikutnya?
# Nomor pertanyaan yang sudah ditanyakann. 
# Nomor Quiz (Quiz id) 
                                                                                                                     
def get_question_after(question_id = 0, quiz_id = 1):
  open()
  query = '''
    SELECT
      quiz_content.id,
      questions.question,
      questions.answer,
      questions.wrong1,
      questions.wrong2,
      questions.wrong3
    FROM
      questions,
      quiz_content
    WHERE
      quiz_content.question_id == questions.id
      AND quiz_content.id > ?
      AND quiz_content.quiz_id == ?
    ORDER BY
      quiz_content.id
  '''

  cursor.execute(query, [question_id, quiz_id])
  result = cursor.fetchone() #fetchone for 1 data only (1 row)
  close()
  return result



## Entry Point untuk menjalankan program
def main():
  clear_db()
  create()
  add_questions()
  add_quiz()
  add_links()
  # get_questions_after(question_id = 0, quiz_id = 1)
  print(get_question_after(1,1))
  print(get_question_after(9,3))
  print(get_question_after(11,3))

if __name__ == "__main__":
  main()