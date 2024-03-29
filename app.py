import streamlit as st
import random
import io
import time
import numpy as np
import qrcode
from PIL import ImageDraw, ImageFont
import matplotlib.pyplot as plt
import sqlite3
st.set_option('deprecation.showPyplotGlobalUse', False)
# Connect to SQLite database
def connect_db():
    return sqlite3.connect('player_data.db')

def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_data
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT, Player_Name TEXT, Score INTEGER, Fame TEXT)''')
    conn.commit()
    conn.close()

def main():
    create_table()
    st.title("Guess the Number Game")
    st.write("I will be guessing a number between 1-3 it will change after each tries, you have total of 3 chances")

    name_entered = False


    user_ans_yes = st.radio("Already a user?", ('Yes', 'No'))
    if user_ans_yes == 'Yes':
        name = st.text_input('Enter Full Name')
        name = name.upper()
        if name:
            name_entered = True
            st.write('Hi,', name)
            time.sleep(0.5)
            st.write("Setting up game for you")
            time.sleep(1)
            st.write("Game begins")
            time.sleep(2)
            game(name)
        
    else:
        st.write("Exiting from game, Thank you")

    if not name_entered:
        return


def game(name):
    j = 0
    m = 0
    s = 0
    streak = np.nan
    for i in range(2,-1,-1):
        a = random.randint(1, 3)
        ans_text = st.text_input("Guess a number (Press Enter to proceed)",key=f"guess_{i}")
        if ans_text.strip():  # Check if the input is not empty
            try:
                ans = int(ans_text)
            except ValueError:
                st.write("Please enter a valid integer.")
                continue
        if a == ans:
            j += 1
            s += 1
            st.write("Bravo")
            if j == 2:
                streak = 'Classic'
                st.write(streak)
            if j == 3:
                streak = 'KING OF KINGS'
                st.write(streak)
                break
            continue
        if a != ans:
            st.write("Oh no!! I guessed", a)
            time.sleep(0.5)
            st.write(f"Try again......")
            m += 1
            if m == 3:
                streak = 'LOOSSER'
                st.write(streak)
            continue
    st.write('SCORE :', s)

    # Connect to SQLite database
    conn = connect_db()
    c = conn.cursor()
    
    # Insert data into SQLite database
    sql = "INSERT INTO player_data (Player_Name, Score, Fame) VALUES (?, ?, ?)"
    val = (name, s, streak)
    c.execute(sql, val)
    conn.commit()
    
    st.write("Data saved to SQLite database")
    

    st.write('Three streaks --- king of kings')
    st.write('Two streaks ---- classic')
    st.write('All losses --- Looser')
    
    user_ans_yes = st.radio("Wanna help developer to buy a dosa?", ('Yes', 'No'))
    upi_id = "70@axisb"
    if user_ans_yes == 'Yes':
        st.write("1. Buy a plain dosa (Rs 30)")
        st.write("2. Buy a masala dosa (Rs 50)")
        st.write("3. Buy a special masala dosa XL (Rs 100)")
        st.set_option('deprecation.showPyplotGlobalUse', False) 
        choice = st.radio("Enter the option you want to select from above", (1, 2, 3))
        if choice in [1, 2, 3]:
            price = 30 if choice == 1 else 50 if choice == 2 else 100
            qr_data = f"upi://pay?pa={upi_id}&am={price}&pn=Dosa Payment"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color=(230, 250, 250))
        
            plt.figure(figsize=(3, 3))
    
            plt.imshow(qr_img)
            plt.axis('off')
            st.pyplot(border_pad=0)  # Adjust borderpad parameter to control the border size
        
            # Display a message after the plot
            st.write("Thank you! for your generosity :)")

    else:
        st.write("No problem! Maybe next time.")

if __name__ == "__main__":
    main()
