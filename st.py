import psycopg2
from faker import Faker
import random

# Database connection setup
def get_connection():
    return psycopg2.connect(
        host="localhost",  # Update host as needed
        database="CRM",  # Replace with your database name
        user="postgres",  # Replace with your user name
        password="Leon9999"  # Replace with your password
    )

# Insert 1000 fake companies into BD_versicherungsunternehmen
def populate_versicherungsunternehmen(cur, fake: Faker):
    versicherungsunternehmen_ids = []
    for _ in range(1000):
        mandantkuerzel = fake.bothify(text="??###")[:10]
        mandantenname = fake.company()
        parent_id = random.choice([None] + versicherungsunternehmen_ids)
        
        cur.execute("""
            INSERT INTO BD_versicherungsunternehmen (mandantkuerzel, mandantenname, parent_id)
            VALUES (%s, %s, %s) RETURNING id;
        """, (mandantkuerzel, mandantenname, parent_id))
        
        new_id = cur.fetchone()[0]
        versicherungsunternehmen_ids.append(new_id)
    return versicherungsunternehmen_ids

# Insert 20000 fake contacts into Kontaktperson
def populate_kontaktperson(cur, fake: Faker, versicherungsunternehmen_ids):
    for _ in range(20000):
        versicherungsunternehmen_id = random.choice(versicherungsunternehmen_ids)
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        
        cur.execute("""
            INSERT INTO Kontaktperson (versicherungsunternehmen_id, name, email, phone)
            VALUES (%s, %s, %s, %s);
        """, (versicherungsunternehmen_id, name, email, phone))

# Main function
def main():
    fake = Faker()
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                print("Populating BD_versicherungsunternehmen...")
                versicherungsunternehmen_ids = populate_versicherungsunternehmen(cur, fake)
                
                print("Populating Kontaktperson...")
                populate_kontaktperson(cur, fake, versicherungsunternehmen_ids)
                
                print("Data population complete.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
