
import psycopg2
from faker import Faker
import random

fake = Faker()

try:
    connection = psycopg2.connect(
        dbname="logistics_fastapi", 
        user="postgres",         
        password="postgres",    
        host="localhost",             
        port="5432"                  
    )
    cursor = connection.cursor()

    def generate_and_insert_drivers(n=500000):
        for _ in range(n):
            name = fake.name()
            vehicle_number = fake.license_plate()
            phone_number = fake.phone_number()
            is_available = fake.boolean(chance_of_getting_true=70)  

            cursor.execute(
                """
                INSERT INTO drivers (name, vehicle_number, phone_number, is_available)
                VALUES (%s, %s, %s, %s)
                """,
                (name, vehicle_number, phone_number, is_available)
            )
        print(f"{n} drivers inserted successfully.")

    def generate_and_insert_shipments(n=500000):
        cursor.execute("SELECT id FROM drivers")
        driver_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(n):
            origin = fake.city()
            destination = fake.city()
            status = fake.random_element(elements=["Shipped", "Delivered", "Pending"])
            driver_id = random.choice(driver_ids)  

          
            cursor.execute(
                """
                INSERT INTO shipments (origin, destination, status, driver_id)
                VALUES (%s, %s, %s, %s)
                """,
                (origin, destination, status, driver_id)
            )
        print(f"{n} shipments inserted successfully.")

    generate_and_insert_drivers(500000)
    generate_and_insert_shipments(500000)

    connection.commit()

except psycopg2.Error as e:
    print(f"Database error: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")
