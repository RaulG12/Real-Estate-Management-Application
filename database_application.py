# Michael Kosinski
# Raul Gandara
# Howard Rovira

import psycopg2

# conn must be declared globally, otherwise it is only valid in the scope of db_connect
conn = None

# function to connect to the database
def db_connect():
    global conn # instruct python that we are trying to modify the global con
    try:
        conn = psycopg2.connect(
            # dbname = "postgres",
            dbname = "FinalProject",
            user = "postgres",
            # password = "1234",
            password = "password", # you might need to replace this with whatever you set it to when you installed postgresql, I just sent mine to "password"
            host = "localhost",
            port = "5432"
        )
        print("Successfully connected to database!")
        return conn
    except Exception as e:
        print("Failed to connect to database: ", e)
        return None

# from here on, we set up various pages of the text display which can be navigated using keyboard input
# each one consists of a match-case statement which will either execute database actions or open other pages of the menu
# please follow these conventions as we create more pages in the application.
isLoggedIn=False
isLoggedInAsAgent=False
isLoggedInAsRenter=False
loggedInAs = None
# the first menu that the user sees is a login screen where they can choose to either log in as a renter or agent, and can register as either one
def menu_login_main():
    global isLoggedIn
    while isLoggedIn==False:
        print("Welcome to the Real Estate Management Application!")
        print()
        print("1. Login as Renter")
        print("2. Login as Agent")
        print("3. Register as a Renter or Agent")
        print("4. Quit")
        print()

        choice = input("Please select an option (1-4): ").strip()
        match choice:
            case "1":
                menu_login_renter()
            case "2":
                menu_login_agent()
            case "3":
                menu_register()
            case "4":
                break # this will close the application because no other code will run besides closing the database connection
            case _: # default case
                print("Invalid choice, please try again.")
    if isLoggedInAsAgent==True:
        agent_menu()
    if isLoggedInAsRenter==True:
        renter_menu()

# menu for logging in as a renter
def menu_login_renter():
    global isLoggedIn
    global isLoggedInAsRenter
    global loggedInAs
    email = input("Enter your email: ").strip()
    
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM renter WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        loggedInAs = result[0];
        isLoggedIn=True
        isLoggedInAsRenter=True
        renter_menu()
    else:
        print("User not registered as a renter!")

# menu for logging in as an agent
def menu_login_agent():
    global isLoggedIn
    global isLoggedInAsAgent
    global loggedInAs
    email = input("Enter your email: ").strip()
    
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM agent WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        loggedInAs = result[0];
        isLoggedIn=True
        isLoggedInAsAgent=True
        agent_menu()
    else:
        print("User not registered as an agent!")

# menu for creating agent or renter account
def menu_register():
    print("Is this account being made for a prospective renter or an agent?")
    print("1. Renter")
    print("2. Agent")
    choice = input().strip()

    match choice:
        case "1":
            createRenterAccount()
        case "2":
            createAgentAccount()
        case _: # default case
            print("Invalid choice, please try again.")

def createAgentAccount():
    email = input("Enter your email: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    job_title = input("Enter your job title: ")
    phone_number = input("Enter your phone number: ")
    agency_name = input("Enter your agency's name: ")

    try:
        with conn.cursor() as cur:
            # Insert into users
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            user_exists = cur.fetchone()
            if user_exists:
                print("User already registered, not adding another entry.")
            else:
                cur.execute("""
                INSERT INTO users (email, first_name, last_name)
                VALUES (%s, %s, %s)
            """, (email, first_name, last_name))

            cur.execute("SELECT 1 FROM agent WHERE email = %s", (email,))
            agent_exists = cur.fetchone()
            if agent_exists:
                print("Agent already registered, not adding another entry.")
            else:
                # Insert into agent
                cur.execute("""
                    INSERT INTO agent (job_title, email, phone_number, agency_name)
                    VALUES (%s, %s, %s, %s)
                """, (job_title, email, phone_number, agency_name))

            conn.commit()
            print("Agent account created")
    except Exception as e:
        print("Error creating agent account:", e)
        conn.rollback()

def createRenterAccount():
    email = input("Enter your email: ").strip()
    first_name = input("Enter your first name: ").strip()
    last_name = input("Enter your last name: ")
    move_in_date = int(input("Enter your move-in year (e.g., 2025): ").strip())
    budget = float(input("Enter your budget: ").strip())
    location = input("Enter preferred location: ").strip()

    try:
        with conn.cursor() as cur:
            # Insert into users
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            user_exists = cur.fetchone()
            if user_exists:
                print("User already registered, not adding another entry.")
            else:
                cur.execute("""
                    INSERT INTO users (email, first_name, last_name)
                    VALUES (%s, %s, %s)
                """, (email, first_name, last_name))

            # Insert into renter
            cur.execute("SELECT 1 FROM renter WHERE email = %s", (email,))
            renter_exists = cur.fetchone()
            if renter_exists:
                print("Renter already registered, not adding another entry.")
            else:
                cur.execute("""
                    INSERT INTO renter (email, move_in_date, budget, location)
                    VALUES (%s, %s, %s, %s)
                """, (email, move_in_date, budget, location))

            conn.commit()
            print("Renter account created")
    except Exception as e:
        print("Error creating renter account:", e)
        conn.rollback()

def renter_menu():
    global loggedInAs
    global isLoggedIn
    global isLoggedInAsRenter
    rewardPoints = None;
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT points FROM rewards WHERE email = %s", (loggedInAs,))
            rewardPoints = cur.fetchone()[0]
    except Exception as e:
        conn.rollback()

    while True:
        print("\n--- Renter Menu ---")
        print()
        print("Logged in as " + loggedInAs)
        if rewardPoints:
            print("Reward Points: " + str(rewardPoints))
        else:
            print("Not a Rewards member! Consider signing up to earn rent rewards.")
        print()
        print("1. Search for properties")
        print("2. Book a property")
        print("3. View/Cancel bookings")
        print("4. Manage payment methods")
        print("5. Manage addresses")
        print("6. Logout")

        choice = input("Choose an option (1-6): ")

        match choice:
            case "1":
                search_properties_renter()
            case "2":
                book_property()
            case "3":
                manage_bookings()
            case "4":
                payments()
            case "5":
                addresses()
            case "6":
                print("Logging out...\n")
                isLoggedIn = False
                isLoggedInAsRenter = False
                loggedInAs = None
                return
            case _:
                print("Invalid option. Please try again.")

def search_properties_renter():
    print("\n--- Property Search ---")
    try:
        with conn.cursor() as cursor:
            # get renter's known preferences
            cursor.execute("SELECT move_in_date, location, budget FROM renter WHERE email = %s", (loggedInAs,))
            renter_pref = cursor.fetchone()
            move_in_date, location, budget = renter_pref

            max_bedrooms = None
            sort_order = None

            print("Your preferences:")
            print("- Move-in date: " + str(move_in_date))
            print("- Location: " + location)
            print("- Budget: " + str(budget))
            print()
            property_type = input("Specify desired property type (all, house, vacation_home, land, apartment, commercial): ").strip().lower()
            rent_sale_pref = input("Optional: specify purchase preference (rent, sale): ").strip().lower()

            match property_type:
                case "house":
                    max_bedrooms = input("Optional: specify max number of bedrooms: ").strip()
                    sort_order = input("Optional: specify sorting by (price) or (bedrooms): ").strip().lower()
                case "vacation_home":
                    max_bedrooms = input("Optional: specify max number of bedrooms: ").strip()
                    sort_order = input("Optional: specify sorting by (price) or (bedrooms): ").strip().lower()
                case "apartment":
                    max_bedrooms = input("Optional: specify max number of bedrooms: ").strip()
                    sort_order = input("Optional: specify sorting by (price) or (bedrooms): ").strip().lower()
                case "all":
                    max_bedrooms = input("Optional: specify max number of bedrooms: ").strip()
                    sort_order = input("Optional: specify sorting by (price) or (bedrooms): ").strip().lower()
                case _:
                    pass

            if property_type == "house" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN house
                        NATURAL JOIN neighborhood
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if max_bedrooms:
                    query += " AND bedrooms <= %s"
                    params.append(max_bedrooms)
                if rent_sale_pref:
                    query += " AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                if sort_order:
                    query += f" ORDER BY {sort_order}"
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- House Properties ---")
                    for row in results:
                        neighborhood_name, id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date, bedrooms, crime_rate, nearby_schools = row
                        print(f"{street_addr}\n{neighborhood_name}, {city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date}\n{sqft} sqft | {bedrooms} Bedrooms | {nearby_schools} Nearby Schools | Crime Rate: {crime_rate}\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo house properties found matching search criteria.")

                
            if property_type == "vacation_home" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN vacation_home
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if max_bedrooms:
                    query += " AND bedrooms <= %s"
                    params.append(max_bedrooms)
                if rent_sale_pref:
                    query += " AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                if sort_order:
                    query += f" ORDER BY {sort_order}"
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- Vacation Home Properties ---")
                    for row in results:
                        id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date, bedrooms = row
                        print(f"{street_addr}\n{city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date}\n{sqft} sqft | {bedrooms} Bedrooms\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo vacation home properties found matching search criteria.")

            if property_type == "land" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN land
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if rent_sale_pref:
                    query += " AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- Land Properties ---")
                    for row in results:
                        id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date = row
                        print(f"{street_addr}\n{city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date} | {sqft} sqft\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo land found matching search criteria.")

            if property_type == "apartment" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN apartment
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if max_bedrooms:
                    query += " AND bedrooms <= %s"
                    params.append(max_bedrooms)
                if rent_sale_pref:
                    query += " AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                if sort_order:
                    query += f" ORDER BY {sort_order}"
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- Apartment Properties ---")
                    for row in results:
                        id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date, bedrooms, apt_building_type = row
                        print(f"{street_addr}\n{city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date}\n{sqft} sqft | {bedrooms} Bedrooms | Building Type: {apt_building_type}\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo apartment properties found matching search criteria.")

            if property_type == "commercial" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN commercial
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if rent_sale_pref:
                    query += "AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- Commercial Properties ---")
                    for row in results:
                        id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date, commercial_building_type = row
                        print(f"{street_addr}\n{city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date}\n{sqft} sqft | Building Type: {commercial_building_type}\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo commercial properties found matching search criteria.")
    except Exception as e:
        print("Error searching properties:", e)         

def book_property():
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, street_addr, city, state, zip, price FROM property")
            properties = cur.fetchall()

            if not properties:
                print("No properties available.")
                return

            print("\n--- Available Properties ---")
            for i, (pid, addr, city, state, zip_code, price) in enumerate(properties, 1):
                print(f"{i}. ID: {pid} | Address: {addr}, {city}, {state} {zip_code} | Price per day: ${price:.2f}")

            selected_id = input("\nEnter the ID of the property you want to book: ").strip()
            ini_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()

            cur.execute("SELECT number FROM card WHERE email = %s", (loggedInAs,))
            cards = cur.fetchall()
            if not cards:
                print("You have no saved cards. Please add one first.")
                return

            print("\nYour cards:")
            for i, (card,) in enumerate(cards, 1):
                print(f"{i}. {card}")

            card_index = int(input("Select card by number: ").strip()) - 1
            selected_card = cards[card_index][0]

            # calculate duration and total cost
            cur.execute("SELECT price FROM property WHERE id = %s", (selected_id,))
            daily_price = cur.fetchone()[0]

            from datetime import datetime
            days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(ini_date, "%Y-%m-%d")).days
            if days <= 0:
                print("Invalid rental period.")
                return
            total_cost = daily_price * days

            cur.execute("""
                INSERT INTO booking (property_id, card_number, ini_time, end_time, status)
                VALUES (%s, %s, %s, %s, 'booked')
            """, (selected_id, selected_card, ini_date, end_date))

            # update reward points
            cur.execute("SELECT 1 FROM rewards WHERE email = %s", (loggedInAs,))
            if cur.fetchone():
                cur.execute("UPDATE rewards SET points = points + %s WHERE email = %s", (total_cost, loggedInAs))
            else:
                cur.execute("INSERT INTO rewards (email, points) VALUES (%s, %s)", (loggedInAs, total_cost))

            conn.commit()

            print("\nBooking successfully made.")
            print(f"Rental Period: {ini_date} to {end_date} ({days} days)")
            print(f"Total Cost: ${total_cost:.2f} | Payment Method: {selected_card}")

    except Exception as e:
        print("Error booking property:", e)
        conn.rollback()

def payments():
    global loggedInAs
    print("\n--- Card Management ---\n")
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT number, exp_date
                FROM card
                WHERE email = %s
            """, (loggedInAs,))
            cards = cur.fetchall()
            if cards:
                print("All cards associated with your email address are listed below.")
                print("\nType a card's number to remove it from your account, or type 'new' to add a new one.")
                print("Or, if you try to add a new card that is already in your account, it will update that card's data instead.")
                print("Note that a card's address MUST match one you have on file (see 5. Manage addresses)\n")
                for number, exp_date in cards:
                    print(f"Card Number: {number} | Exp: {exp_date}")
            else:
                print("You have no saved cards yet. Type 'new' to add a new one.")
                print("Note that a card's address MUST match one you have on file (see 5. Manage addresses)\n")

            choice = input("\n").strip().lower()
            if choice == "new":
                number = input("Enter card number (16 digits, only numbers, no spaces): ").strip()
                name_on_card = input("Enter the name on the card: ").strip()
                exp_date = input("Enter the card's expiration date (MM/YY): ").strip()
                street_addr = input("Enter the billing address street: ").strip()
                city = input("Enter the billing address city: ").strip()
                state = input("Enter the billing address state: ").strip()
                zip = input("Enter the billing address zip: ").strip()

                cur.execute("""
                    INSERT INTO card (number, email, name_on_card, exp_date, street_addr, city, state, zip)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (number) DO UPDATE
                    SET name_on_card = EXCLUDED.name_on_card, exp_date = EXCLUDED.exp_date, street_addr = EXCLUDED.street_addr, city = EXCLUDED.city, state = EXCLUDED.state, zip = EXCLUDED.zip
                """, (number, loggedInAs, name_on_card, exp_date, street_addr, city, state, zip))
                conn.commit()
                print("New card was added or updated successfully!")

            elif choice.isdigit() and len(choice) == 16:
                cur.execute("""
                    DELETE FROM card
                    WHERE number = %s AND email = %s
                """, (choice, loggedInAs))
                if cur.rowcount > 0:
                    conn.commit()
                    print("Card deleted successfully!")
                else:
                    print("No card found with that number.")

            else:
                print("Invalid input, please try again.")

    except Exception as e:
        print("Error looking up/managing card info:", e)
        conn.rollback()

def addresses():
    global loggedInAs
    print("\n--- Address Management ---\n")
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT street_addr, city, state, zip
                FROM user_address
                WHERE email = %s
            """, (loggedInAs,))
            addresses = cur.fetchall()
            if addresses:
                print("All addresses associated with your account are listed below.")
                print("\nType a street address to remove it from your account, or type 'new' to add a new one.")
                print("Or, if you try to add a new address that is already in your account, it will update that address's data instead.")
                print("Note that you cannot remove an address that is associated with one of your payment methods (see 4. Manage payment methods)\n")
                for street_addr, city, state, zip in addresses:
                    print(f"{street_addr} | {city}, {state} {zip}")
            else:
                print("You have no saved addresses yet. Type 'new' to add a new one.")

            choice = input("\n").strip()
            if choice.lower() == "new":
                street_addr = input("Enter the street address: ").strip()
                city = input("Enter the city: ").strip()
                state = input("Enter the state: ").strip()
                zip = input("Enter the zip: ").strip()

                # SQL wants to be a real great guy and just not let us use ON CONFLICT so we're gonna have to delete the addres
                cur.execute("""
                    DELETE FROM user_address
                    WHERE email = %s AND street_addr = %s AND city = %s AND state = %s AND zip = %s
                """, (loggedInAs, street_addr, city, state, zip))
                
                cur.execute("""
                    INSERT INTO user_address (email, street_addr, city, state, zip)
                    VALUES (%s, %s, %s, %s, %s)
                """, (loggedInAs, street_addr, city, state, zip))
                conn.commit()
                print("New address was added or updated successfully!")

            else:
                cur.execute("""
                    DELETE FROM user_address
                    WHERE street_addr = %s AND email = %s
                """, (choice, loggedInAs))
                if cur.rowcount > 0:
                    conn.commit()
                    print("Address deleted successfully!")
                else:
                    print("Unable to delete the given address!")

    except Exception as e:
        print("Error looking up/managing addresses:", e)
        conn.rollback()

def agent_menu():
    global loggedInAs
    global isLoggedIn
    global isLoggedInAsAgent
    while True:
        print("\n--- Agent Menu ---\n")
        print("1. Search for properties")
        print("2. Add properties")
        print("3. Delete properties")
        print("4. Modify properties")
        print("5. Manage bookings")
        print("6. Logout")

        choice = input("Choose an option (1-6): ")

        match choice:
            case "1":
                search_properties_agent()
            case "2":
                add_property()
            case "3":
                delete_property()
            case "4":
                modify_property()
            case "5":
                manage_bookings()
            case "6":
                print("Logging out...\n")
                isLoggedIn = False
                isLoggedInAsAgent = False
                loggedInAs = None
                return
            case _:
                print("Invalid option. Please try again.")

def search_properties_agent():
    print("\n--- Agent Property Search ---\n")
    try:
        with conn.cursor() as cursor:
            move_in_date = input("Specify move-in date: ").strip()
            location = input("Specify location (city): ").strip()
            budget = input("Specify a budget: ").strip()

            max_bedrooms = None
            sort_order = None

            property_type = input("Specify desired property type (all, house, vacation_home, land, apartment, commercial): ").strip().lower()
            rent_sale_pref = input("Optional: specify purchase preference (rent, sale): ").strip().lower()

            match property_type:
                case "house":
                    max_bedrooms = input("Optional: specify max number of bedrooms: ").strip()
                    sort_order = input("Optional: specify sorting by (price) or (bedrooms): ").strip().lower()
                case "vacation_home":
                    max_bedrooms = input("Optional: specify max number of bedrooms: ").strip()
                    sort_order = input("Optional: specify sorting by (price) or (bedrooms): ").strip().lower()
                case "apartment":
                    max_bedrooms = input("Optional: specify max number of bedrooms: ").strip()
                    sort_order = input("Optional: specify sorting by (price) or (bedrooms): ").strip().lower()
                case "all":
                    max_bedrooms = input("Optional: specify max number of bedrooms: ").strip()
                    sort_order = input("Optional: specify sorting by (price) or (bedrooms): ").strip().lower()
                case _:
                    pass

            if property_type == "house" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN house
                        NATURAL JOIN neighborhood
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if max_bedrooms:
                    query += " AND bedrooms <= %s"
                    params.append(max_bedrooms)
                if rent_sale_pref:
                    query += " AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                if sort_order:
                    query += f" ORDER BY {sort_order}"
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- House Properties ---")
                    for row in results:
                        neighborhood_name, id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date, bedrooms, crime_rate, nearby_schools = row
                        print(f"{street_addr}\n{neighborhood_name}, {city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date}\n{sqft} sqft | {bedrooms} Bedrooms | {nearby_schools} Nearby Schools | Crime Rate: {crime_rate}\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo house properties found matching search criteria.")

                
            if property_type == "vacation_home" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN vacation_home
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if max_bedrooms:
                    query += " AND bedrooms <= %s"
                    params.append(max_bedrooms)
                if rent_sale_pref:
                    query += " AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                if sort_order:
                    query += f" ORDER BY {sort_order}"
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- Vacation Home Properties ---")
                    for row in results:
                        id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date, bedrooms = row
                        print(f"{street_addr}\n{city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date}\n{sqft} sqft | {bedrooms} Bedrooms\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo vacation home properties found matching search criteria.")

            if property_type == "land" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN land
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if rent_sale_pref:
                    query += " AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- Land Properties ---")
                    for row in results:
                        id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date = row
                        print(f"{street_addr}\n{city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date} | {sqft} sqft\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo land found matching search criteria.")

            if property_type == "apartment" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN apartment
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if max_bedrooms:
                    query += " AND bedrooms <= %s"
                    params.append(max_bedrooms)
                if rent_sale_pref:
                    query += " AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                if sort_order:
                    query += f" ORDER BY {sort_order}"
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- Apartment Properties ---")
                    for row in results:
                        id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date, bedrooms, apt_building_type = row
                        print(f"{street_addr}\n{city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date}\n{sqft} sqft | {bedrooms} Bedrooms | Building Type: {apt_building_type}\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo apartment properties found matching search criteria.")

            if property_type == "commercial" or property_type == "all":
                query = """
                        SELECT *
                        FROM property
                        NATURAL JOIN commercial
                        WHERE city = %s
                        AND move_in_date = %s
                        AND price <= %s
                    """
                params = [location, move_in_date, budget]
                if rent_sale_pref:
                    query += "AND rent_or_sale = %s"
                    params.append(rent_sale_pref)
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    print("\n--- Commercial Properties ---")
                    for row in results:
                        id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date, commercial_building_type = row
                        print(f"{street_addr}\n{city}, {state} {zip}\n{description}\nPrice: ${price:.2f} | For {rent_or_sale} | Move-in Date: {move_in_date}\n{sqft} sqft | Building Type: {commercial_building_type}\nManaged by {agency_name} | ID: {id}")
                else:
                    print("\nNo commercial properties found matching search criteria.")
    except Exception as e:
        print("Error searching properties:", e)    

def add_property():
    agency_name = "Agency INC"
    # autofill agency_name with the agent's agency from the table
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT agency_name FROM agent WHERE email = %s", (loggedInAs,))
            agency_name = cur.fetchone()[0]
    except Exception as e:
        print("Error fetching agency name from agent:", e)

    isDone=False
    isDone2=False
    isDone3=False

    while isDone==False:
        prop_id=input("Enter the id for this new property: ")
        try:
            prop_price=float(input("Enter the price of this new property: "))
            prop_sqft=float(input("Enter the square feet of this new property: "))
        except ValueError:
            print("Invalid input. Enter a number")
            break
        prop_description=input("Add a description for this new property: ")
        prop_street_address=input("Enter the street address of this new property (Only enter street number and street name): ")
        prop_city=input("Enter the city this new property belongs to: ")
        prop_state=input("Enter the state this new property belongs to: ")
        prop_zip=input("Enter the zip code of this new property: ")
        prop_rent_or_sale=input("Enter whether this property should be up for (rent) or (sale): ")
        prop_move_in_date=input("Enter the date this property will become available for move-in: ")

        while isDone2==False:
            print("What type of property is this?")
            print("1. House")
            print("2. Apartment")
            print("3. Commercial")
            print("4. Vacation Home")
            print("5. Land")
            prop_type_choice=input("Choose an option (1-5): ")

            match prop_type_choice:
                case "1":
                    while isDone3==False:
                        totalRooms=0
                        try:
                            totalRooms = float(input("Enter the amount of rooms in this house: "))
                        except ValueError:
                            print("Invalid input. Enter a number")
                            break
                        prop_neighborhood=input("Enter this house's neighborhood: ")

                        try:
                            with conn.cursor() as cur:
                                # Insert into users
                                cur.execute("""
                                    INSERT INTO property (id, price, sqft, description, Street_addr, city, state, zip, Agency_name, rent_or_sale, move_in_date)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (prop_id, prop_price, prop_sqft, prop_description, prop_street_address, prop_city,
                                      prop_state, prop_zip, agency_name, prop_rent_or_sale, prop_move_in_date))

                                conn.commit()

                        except Exception as e:
                            print("Error creating property:", e)
                            conn.rollback()

                        try:
                            with conn.cursor() as cur:
                                # Insert into users
                                cur.execute("""
                                    INSERT INTO house (id, bedrooms, neighborhood_name)
                                    VALUES (%s, %s, %s)
                                """, (prop_id, totalRooms, prop_neighborhood))

                                conn.commit()
                                print("House successfully added")
                        except Exception as e:
                            print("Error creating house:", e)
                            conn.rollback()
                        isDone3=True
                    if isDone3==True:
                        isDone2=True


                case "2":
                    while isDone3 == False:
                        totalRooms = 0
                        try:
                            totalRooms = float(input("Enter the amount of rooms in this apartment: "))
                        except ValueError:
                            print("Invalid input. Enter a number")
                            break
                        commercialType=input("What type of building is this?: ")

                        try:
                            with conn.cursor() as cur:
                                # Insert into users
                                cur.execute("""
                                    INSERT INTO property (id, price, sqft, description, Street_addr, city, state, zip, Agency_name, rent_or_sale, move_in_date)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (prop_id, prop_price, prop_sqft, prop_description, prop_street_address, prop_city,
                                      prop_state, prop_zip, agency_name, prop_rent_or_sale, prop_move_in_date))

                                conn.commit()

                        except Exception as e:
                            print("Error creating property:", e)
                            conn.rollback()

                        try:
                            with conn.cursor() as cur:
                                # Insert into users
                                cur.execute("""
                                    INSERT INTO apartment (id, bedrooms, apt_building_type)
                                    VALUES (%s, %s, %s)
                                """, (prop_id, totalRooms, commercialType))

                                conn.commit()
                                print("Apartment successfully added")
                        except Exception as e:
                            print("Error creating house:", e)
                            conn.rollback()
                        isDone3 = True
                    if isDone3 == True:
                        isDone2 = True
                case "3":
                    while isDone3 == False:

                        commercialType = input("What type of building is this?: ")

                        try:
                            with conn.cursor() as cur:
                                # Insert into users
                                cur.execute("""
                                    INSERT INTO property (id, price, sqft, description, Street_addr, city, state, zip, Agency_name, rent_or_sale, move_in_date)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (prop_id, prop_price, prop_sqft, prop_description, prop_street_address, prop_city,
                                      prop_state, prop_zip, agency_name, prop_rent_or_sale, prop_move_in_date))

                                conn.commit()

                        except Exception as e:
                            print("Error creating property:", e)
                            conn.rollback()

                        try:
                            with conn.cursor() as cur:
                                # Insert into users
                                cur.execute("""
                                    INSERT INTO commercial (id, commercial_building_type)
                                    VALUES (%s, %s)
                                """, (prop_id, commercialType))

                                conn.commit()
                                print("Commercial building successfully added")
                        except Exception as e:
                            print("Error creating commercial building:", e)
                            conn.rollback()
                        isDone3 = True
                    if isDone3 == True:
                        isDone2 = True
                case "4":
                    while isDone3 == False:
                        totalRooms = 0
                        try:
                            totalRooms = float(input("Enter the amount of rooms in this vacation home: "))
                        except ValueError:
                            print("Invalid input. Enter a number")
                            break

                        try:
                            with conn.cursor() as cur:
                                # Insert into users
                                cur.execute("""
                                    INSERT INTO property (id, price, sqft, description, Street_addr, city, state, zip, Agency_name, rent_or_sale, move_in_date)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (prop_id, prop_price, prop_sqft, prop_description, prop_street_address, prop_city,
                                      prop_state, prop_zip, agency_name, prop_rent_or_sale, prop_move_in_date))

                                conn.commit()

                        except Exception as e:
                            print("Error creating property:", e)
                            conn.rollback()

                        try:
                            with conn.cursor() as cur:
                                # Insert into users
                                cur.execute("""
                                    INSERT INTO vacation_home (id, bedrooms)
                                    VALUES (%s, %s)
                                """, (prop_id, totalRooms))

                                conn.commit()
                                print("Vacation home successfully added")
                        except Exception as e:
                            print("Error creating vacation home:", e)
                            conn.rollback()
                        isDone3 = True
                    if isDone3 == True:
                        isDone2 = True
                case "5":
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                    INSERT INTO property (id, price, sqft, description, Street_addr, city, state, zip, Agency_name, rent_or_sale, move_in_date)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (prop_id, prop_price, prop_sqft, prop_description, prop_street_address, prop_city,
                                      prop_state, prop_zip, agency_name, prop_rent_or_sale, prop_move_in_date))

                            conn.commit()

                    except Exception as e:
                        print("Error creating property:", e)
                        conn.rollback()

                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                INSERT INTO land (id)
                                VALUES (%s)
                            """, (prop_id,))

                            conn.commit()
                            print("Land successfully added")
                    except Exception as e:
                        print("Error creating land:", e)
                        conn.rollback()


                    isDone2=True
                case _:
                    print("Invalid option. Please try again.")

        isDone=True


def delete_property():
    #Deletion seems to work
    cursor=conn.cursor()
    prop_id=input("Enter the property id: ")
    cursor.execute("""select 1 from house where id=%s""", (prop_id,))
    house_exists=cursor.fetchone()
    if house_exists:
        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                    delete from house where id = %s
                """, (prop_id,))
                conn.commit()
                print("House successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                    delete from property where id = %s
                """, (prop_id,))
                conn.commit()
                print("Property successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

    cursor.execute("""select 1 from commercial where id=%s""", (prop_id,))
    commercial_exists = cursor.fetchone()
    if commercial_exists:
        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                        delete from commercial where id = %s
                    """, (prop_id,))
                conn.commit()
                print("Commercial successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                        delete from property where id = %s
                    """, (prop_id,))
                conn.commit()
                print("Property successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

    cursor.execute("""select 1 from apartment where id=%s""", (prop_id,))
    apartment_exists = cursor.fetchone()
    if apartment_exists:
        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                            delete from apartment where id = %s
                        """, (prop_id,))
                conn.commit()
                print("Apartment successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                            delete from property where id = %s
                        """, (prop_id,))
                conn.commit()
                print("Property successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

    cursor.execute("""select 1 from land where id=%s""", (prop_id,))
    land_exists = cursor.fetchone()
    if land_exists:
        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                                delete from land where id = %s
                            """, (prop_id,))
                conn.commit()
                print("Land successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                                delete from property where id = %s
                            """, (prop_id,))
                conn.commit()
                print("Property successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

    cursor.execute("""select 1 from vacation_home where id=%s""", (prop_id,))
    vacation_exists = cursor.fetchone()
    if vacation_exists:
        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                                    delete from vacation_home where id = %s
                                """, (prop_id,))
                conn.commit()
                print("Vacation home successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()

        try:
            with conn.cursor() as cur:
                # Insert into users
                cur.execute("""
                                    delete from property where id = %s
                                """, (prop_id,))
                conn.commit()
                print("Property successfully deleted")
        except Exception as e:
            print("Error occured while deleting:", e)
            conn.rollback()
    if (house_exists==None) and (land_exists==None) and (apartment_exists==None) and (vacation_exists==None) and (commercial_exists==None):
        print("Property not found")


def modify_property():

    cursor = conn.cursor()
    prop_id = input("Enter the property id: ")
    cursor.execute("""select 1 from house where id=%s""", (prop_id,))
    house_exists = cursor.fetchone()
    if house_exists:

        print("1. Price")
        print("2. Square Feet")
        print("3. Description")
        print("4. Street Address")
        print("5. City")
        print("6. State")
        print("7. Zip code")
        print("8. Rent Or Sale")
        print("9. Move In Date")
        print("10. Number Of Rooms")
        print("11. Neighborhood")
        choice=input("Choose an option (1-11): ")
        print()



        match choice:
            case "1":
                prop_price = ''
                try:
                    prop_price = float(input("Enter the new price of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_price != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                    update property set price=%s where id=%s
                                """, (prop_price,prop_id))
                            conn.commit()
                            print("Price updated")
                    except Exception as e:
                        print("Error occurred updating the price:", e)
                        conn.rollback()

            case "2":
                prop_sqft = ''
                try:
                    prop_sqft = float(input("Enter the new square feet of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_sqft != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                    update property set sqft=%s where id=%s
                                                """, (prop_sqft, prop_id))
                            conn.commit()
                            print("Square feet updated")
                    except Exception as e:
                        print("Error occurred updating the square feet:", e)
                        conn.rollback()
            case "3":
                prop_desc=input("Enter new description: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                update property set description=%s where id=%s
                                            """, (prop_desc, prop_id))
                        conn.commit()
                        print("Description updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "4":
                prop_street = input("Enter new street: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                update property set street_addr=%s where id=%s
                                                            """, (prop_street, prop_id))
                        conn.commit()
                        print("Street updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "5":
                prop_city = input("Enter new city: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                update property set city=%s where id=%s
                                                            """, (prop_city, prop_id))
                        conn.commit()
                        print("City updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "6":
                prop_state = input("Enter new state: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                update property set state=%s where id=%s
                                                            """, (prop_state, prop_id))
                        conn.commit()
                        print("State updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "7":
                prop_zip = input("Enter new zip code: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                update property set zip=%s where id=%s
                                                            """, (prop_zip, prop_id))
                        conn.commit()
                        print("Zip code updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "8":
                prop_rent_or_sale = input("Enter either rent or sale: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                update property set rent_or_sale=%s where id=%s
                                                            """, (prop_rent_or_sale, prop_id))
                        conn.commit()
                        print("Rent or sale updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "9":

                prop_year = ''
                try:
                    prop_year = float(input("Enter the new move in year: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_year!='':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                                    update property set move_in_date=%s where id=%s
                                                                """, (prop_year, prop_id))
                            conn.commit()
                            print("Year updated")
                    except Exception as e:
                        print("Error occurred:", e)
                        conn.rollback()
            case "10":
                prop_room = ''
                try:
                    prop_room = float(input("Enter room total: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_room != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                                                    update house set bedrooms=%s where id=%s
                                                                                """, (prop_room, prop_id))
                            conn.commit()
                            print("Rooms updated")
                    except Exception as e:
                        print("Error occurred:", e)
                        conn.rollback()
            case "11":
                prop_neighborhood = input("Enter new neighborhood: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                                update house set neighborhood_name=%s where id=%s
                                                                            """, (prop_neighborhood, prop_id))
                        conn.commit()
                        print("Neighborhood updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case _:
                print("Invalid option. Please try again.")

    cursor.execute("""select 1 from commercial where id=%s""", (prop_id,))
    commercial_exists = cursor.fetchone()
    if commercial_exists:
        print("1. Price")
        print("2. Square Feet")
        print("3. Description")
        print("4. Street Address")
        print("5. City")
        print("6. State")
        print("7. Zip code")
        print("8. Rent Or Sale")
        print("9. Move In Date")
        print("10. Commercial Building Type")
        choice = input("Choose an option (1-10): ")
        print()

        match choice:
            case "1":
                prop_price = ''
                try:
                    prop_price = float(input("Enter the new price of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_price != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                            update property set price=%s where id=%s
                                        """, (prop_price, prop_id))
                            conn.commit()
                            print("Price updated")
                    except Exception as e:
                        print("Error occurred updating the price:", e)
                        conn.rollback()

            case "2":
                prop_sqft = ''
                try:
                    prop_sqft = float(input("Enter the new square feet of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_sqft != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                            update property set sqft=%s where id=%s
                                                        """, (prop_sqft, prop_id))
                            conn.commit()
                            print("Square feet updated")
                    except Exception as e:
                        print("Error occurred updating the square feet:", e)
                        conn.rollback()
            case "3":
                prop_desc = input("Enter new description: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                        update property set description=%s where id=%s
                                                    """, (prop_desc, prop_id))
                        conn.commit()
                        print("Description updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "4":
                prop_street = input("Enter new street: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set street_addr=%s where id=%s
                                                                    """, (prop_street, prop_id))
                        conn.commit()
                        print("Street updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "5":
                prop_city = input("Enter new city: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set city=%s where id=%s
                                                                    """, (prop_city, prop_id))
                        conn.commit()
                        print("City updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "6":
                prop_state = input("Enter new state: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set state=%s where id=%s
                                                                    """, (prop_state, prop_id))
                        conn.commit()
                        print("State updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "7":
                prop_zip = input("Enter new zip code: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set zip=%s where id=%s
                                                                    """, (prop_zip, prop_id))
                        conn.commit()
                        print("Zip code updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "8":
                prop_rent_or_sale = input("Enter either rent or sale: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set rent_or_sale=%s where id=%s
                                                                    """, (prop_rent_or_sale, prop_id))
                        conn.commit()
                        print("Rent or sale updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "9":

                prop_year = ''
                try:
                    prop_year = float(input("Enter the new move in year: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_year != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                                            update property set move_in_date=%s where id=%s
                                                                        """, (prop_year, prop_id))
                            conn.commit()
                            print("Year updated")
                    except Exception as e:
                        print("Error occurred:", e)
                        conn.rollback()
            case "10":

                prop_commercial_type= input("Enter new commercial building type: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                                        update commercial set commercial_building_type=%s where id=%s
                                                                                    """, (prop_commercial_type, prop_id))
                        conn.commit()
                        print("Commercial building updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case _:
                print("Invalid option. Please try again.")

    cursor.execute("""select 1 from apartment where id=%s""", (prop_id,))
    apartment_exists = cursor.fetchone()
    if apartment_exists:
        print("1. Price")
        print("2. Square Feet")
        print("3. Description")
        print("4. Street Address")
        print("5. City")
        print("6. State")
        print("7. Zip code")
        print("8. Rent Or Sale")
        print("9. Move In Date")
        print("10. Number Of Rooms")
        print("11. Apartment Building Type")
        choice = input("Choose an option (1-11): ")
        print()

        match choice:
            case "1":
                prop_price = ''
                try:
                    prop_price = float(input("Enter the new price of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_price != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                            update property set price=%s where id=%s
                                        """, (prop_price, prop_id))
                            conn.commit()
                            print("Price updated")
                    except Exception as e:
                        print("Error occurred updating the price:", e)
                        conn.rollback()

            case "2":
                prop_sqft = ''
                try:
                    prop_sqft = float(input("Enter the new square feet of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_sqft != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                            update property set sqft=%s where id=%s
                                                        """, (prop_sqft, prop_id))
                            conn.commit()
                            print("Square feet updated")
                    except Exception as e:
                        print("Error occurred updating the square feet:", e)
                        conn.rollback()
            case "3":
                prop_desc = input("Enter new description: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                        update property set description=%s where id=%s
                                                    """, (prop_desc, prop_id))
                        conn.commit()
                        print("Description updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "4":
                prop_street = input("Enter new street: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set street_addr=%s where id=%s
                                                                    """, (prop_street, prop_id))
                        conn.commit()
                        print("Street updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "5":
                prop_city = input("Enter new city: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set city=%s where id=%s
                                                                    """, (prop_city, prop_id))
                        conn.commit()
                        print("City updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "6":
                prop_state = input("Enter new state: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set state=%s where id=%s
                                                                    """, (prop_state, prop_id))
                        conn.commit()
                        print("State updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "7":
                prop_zip = input("Enter new zip code: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set zip=%s where id=%s
                                                                    """, (prop_zip, prop_id))
                        conn.commit()
                        print("Zip code updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "8":
                prop_rent_or_sale = input("Enter either rent or sale: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set rent_or_sale=%s where id=%s
                                                                    """, (prop_rent_or_sale, prop_id))
                        conn.commit()
                        print("Rent or sale updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "9":

                prop_year = ''
                try:
                    prop_year = float(input("Enter the new move in year: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_year != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                                            update property set move_in_date=%s where id=%s
                                                                        """, (prop_year, prop_id))
                            conn.commit()
                            print("Year updated")
                    except Exception as e:
                        print("Error occurred:", e)
                        conn.rollback()
            case "10":
                prop_room = ''
                try:
                    prop_room = float(input("Enter room total: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_room != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                                                            update apartment set bedrooms=%s where id=%s
                                                                                        """, (prop_room, prop_id))
                            conn.commit()
                            print("Rooms updated")
                    except Exception as e:
                        print("Error occurred:", e)
                        conn.rollback()
            case "11":
                prop_apartment_type = input("Enter new apartment type: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                                        update apartment set apt_building_type=%s where id=%s
                                                                                    """, (prop_apartment_type, prop_id))
                        conn.commit()
                        print("Apartment type updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case _:
                print("Invalid option. Please try again.")

    cursor.execute("""select 1 from land where id=%s""", (prop_id,))
    land_exists = cursor.fetchone()
    if land_exists:
        print("1. Price")
        print("2. Square Feet")
        print("3. Description")
        print("4. Street Address")
        print("5. City")
        print("6. State")
        print("7. Zip code")
        print("8. Rent Or Sale")
        print("9. Move In Date")

        choice = input("Choose an option (1-9): ")
        print()

        match choice:
            case "1":
                prop_price = ''
                try:
                    prop_price = float(input("Enter the new price of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_price != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                            update property set price=%s where id=%s
                                        """, (prop_price, prop_id))
                            conn.commit()
                            print("Price updated")
                    except Exception as e:
                        print("Error occurred updating the price:", e)
                        conn.rollback()

            case "2":
                prop_sqft = ''
                try:
                    prop_sqft = float(input("Enter the new square feet of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_sqft != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                            update property set sqft=%s where id=%s
                                                        """, (prop_sqft, prop_id))
                            conn.commit()
                            print("Square feet updated")
                    except Exception as e:
                        print("Error occurred updating the square feet:", e)
                        conn.rollback()
            case "3":
                prop_desc = input("Enter new description: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                        update property set description=%s where id=%s
                                                    """, (prop_desc, prop_id))
                        conn.commit()
                        print("Description updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "4":
                prop_street = input("Enter new street: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set street_addr=%s where id=%s
                                                                    """, (prop_street, prop_id))
                        conn.commit()
                        print("Street updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "5":
                prop_city = input("Enter new city: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set city=%s where id=%s
                                                                    """, (prop_city, prop_id))
                        conn.commit()
                        print("City updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "6":
                prop_state = input("Enter new state: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set state=%s where id=%s
                                                                    """, (prop_state, prop_id))
                        conn.commit()
                        print("State updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "7":
                prop_zip = input("Enter new zip code: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set zip=%s where id=%s
                                                                    """, (prop_zip, prop_id))
                        conn.commit()
                        print("Zip code updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "8":
                prop_rent_or_sale = input("Enter either rent or sale: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set rent_or_sale=%s where id=%s
                                                                    """, (prop_rent_or_sale, prop_id))
                        conn.commit()
                        print("Rent or sale updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "9":

                prop_year = ''
                try:
                    prop_year = float(input("Enter the new move in year: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_year != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                                            update property set move_in_date=%s where id=%s
                                                                        """, (prop_year, prop_id))
                            conn.commit()
                            print("Year updated")
                    except Exception as e:
                        print("Error occurred:", e)
                        conn.rollback()

            case _:
                print("Invalid option. Please try again.")

    cursor.execute("""select 1 from vacation_home where id=%s""", (prop_id,))
    vacation_exists = cursor.fetchone()
    if vacation_exists:
        print("1. Price")
        print("2. Square Feet")
        print("3. Description")
        print("4. Street Address")
        print("5. City")
        print("6. State")
        print("7. Zip code")
        print("8. Rent Or Sale")
        print("9. Move In Date")
        print("10. Number Of Rooms")
        choice = input("Choose an option (1-10): ")
        print()

        match choice:
            case "1":
                prop_price = ''
                try:
                    prop_price = float(input("Enter the new price of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_price != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                            update property set price=%s where id=%s
                                        """, (prop_price, prop_id))
                            conn.commit()
                            print("Price updated")
                    except Exception as e:
                        print("Error occurred updating the price:", e)
                        conn.rollback()

            case "2":
                prop_sqft = ''
                try:
                    prop_sqft = float(input("Enter the new square feet of this property: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_sqft != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                            update property set sqft=%s where id=%s
                                                        """, (prop_sqft, prop_id))
                            conn.commit()
                            print("Square feet updated")
                    except Exception as e:
                        print("Error occurred updating the square feet:", e)
                        conn.rollback()
            case "3":
                prop_desc = input("Enter new description: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                        update property set description=%s where id=%s
                                                    """, (prop_desc, prop_id))
                        conn.commit()
                        print("Description updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "4":
                prop_street = input("Enter new street: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set street_addr=%s where id=%s
                                                                    """, (prop_street, prop_id))
                        conn.commit()
                        print("Street updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "5":
                prop_city = input("Enter new city: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set city=%s where id=%s
                                                                    """, (prop_city, prop_id))
                        conn.commit()
                        print("City updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "6":
                prop_state = input("Enter new state: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set state=%s where id=%s
                                                                    """, (prop_state, prop_id))
                        conn.commit()
                        print("State updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "7":
                prop_zip = input("Enter new zip code: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set zip=%s where id=%s
                                                                    """, (prop_zip, prop_id))
                        conn.commit()
                        print("Zip code updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "8":
                prop_rent_or_sale = input("Enter either rent or sale: ")
                try:
                    with conn.cursor() as cur:
                        # Insert into users
                        cur.execute("""
                                                                        update property set rent_or_sale=%s where id=%s
                                                                    """, (prop_rent_or_sale, prop_id))
                        conn.commit()
                        print("Rent or sale updated")
                except Exception as e:
                    print("Error occurred:", e)
                    conn.rollback()
            case "9":

                prop_year = ''
                try:
                    prop_year = float(input("Enter the new move in year: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_year != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                                            update property set move_in_date=%s where id=%s
                                                                        """, (prop_year, prop_id))
                            conn.commit()
                            print("Year updated")
                    except Exception as e:
                        print("Error occurred:", e)
                        conn.rollback()
            case "10":
                prop_room = ''
                try:
                    prop_room = float(input("Enter room total: "))
                except ValueError:
                    print("Invalid input. Enter a number")
                if prop_room != '':
                    try:
                        with conn.cursor() as cur:
                            # Insert into users
                            cur.execute("""
                                                                                            update vacation_home set bedrooms=%s where id=%s
                                                                                        """, (prop_room, prop_id))
                            conn.commit()
                            print("Rooms updated")
                    except Exception as e:
                        print("Error occurred:", e)
                        conn.rollback()

            case _:
                print("Invalid option. Please try again.")
    if (house_exists==None) and (land_exists==None) and (apartment_exists==None) and (vacation_exists==None) and (commercial_exists==None):
        print("Property not found")

def manage_bookings():
    try:
        with conn.cursor() as cursor:
            if isLoggedInAsAgent:
                cursor.execute("""
                    SELECT b.id, b.property_id, b.ini_time, b.end_time, b.status, b.card_number,
                           p.street_addr, p.city, p.state, p.zip, p.price
                    FROM booking b
                    JOIN property p ON b.property_id = p.id
                    WHERE p.agency_name = (
                        SELECT agency_name FROM agent WHERE email = %s
                    )
                """, (loggedInAs,))
                bookings = cursor.fetchall()

                if not bookings:
                    print("No bookings found for your properties.")
                    return

                print("\n--- Bookings for Your Properties ---")
                for i, (bid, pid, ini, end, status, card, addr, city, state, zip_code, price) in enumerate(bookings, 1):
                    print(f"{i}. Booking ID: {bid}, Property ID: {pid}, Period: {ini} to {end}, Status: {status}, Payment: {card}")
                    print(f"   Address: {addr}, {city}, {state} {zip_code}, Price: ${price:.2f}")

                cancel = input("\nDo you want to cancel any booking? (y/n): ").strip().lower()
                if cancel == 'y':
                    bid_to_cancel = input("Enter the Booking ID to cancel: ").strip()
                    cursor.execute("UPDATE booking SET status = 'cancelled' WHERE id = %s AND status = 'booked'", (bid_to_cancel,))
                    conn.commit()
                    print("Booking marked as cancelled and refund processed.")

            else:
                cursor.execute("""
                    SELECT b.id, b.property_id, b.ini_time, b.end_time, b.status, b.card_number,
                           p.street_addr, p.city, p.state, p.zip, p.price
                    FROM booking b
                    JOIN property p ON b.property_id = p.id
                    JOIN card c ON b.card_number = c.number
                    WHERE c.email = %s
                """, (loggedInAs,))
                bookings = cursor.fetchall()
                print(loggedInAs)
                if not bookings:
                    print("You have no bookings.")
                    return

                print("\n--- Your Bookings ---")
                for i, (bid, pid, ini, end, status, card, addr, city, state, zip_code, price) in enumerate(bookings, 1):
                    print(f"{i}. Booking ID: {bid}, Property ID: {pid}, Period: {ini} to {end}, Status: {status}, Payment: {card}")
                    print(f"   Address: {addr}, {city}, {state} {zip_code}, Price: ${price:.2f}")

                cancel = input("\nDo you want to cancel any booking? (y/n): ").strip().lower()
                if cancel == 'y':
                    bid_to_cancel = input("Enter the Booking ID to cancel: ").strip()
                    cursor.execute("UPDATE booking SET status = 'cancelled' WHERE id = %s AND status = 'booked'", (bid_to_cancel,))
                    conn.commit()
                    print("Booking marked as cancelled and refund processed.")
    except Exception as e:
        print("Error managing bookings:", e)
        conn.rollback()



# begin the program itself
# this IF statement always triggers when the program is ran, but never when the code is referenced
if __name__ == "__main__":
    # conn does not need to be specified as global here because it is in the same scope as it was initially defined
    conn = db_connect()
    if conn:
        # open the main menu
        menu_login_main()
        # if the menu is ever quit, we end up here. close the database and then just end the program
        conn.close()
