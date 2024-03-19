import streamlit as st
import random
import pandas as pd
import time
import numpy as np
import qrcode
from PIL import ImageDraw,ImageFont
import matplotlib.pyplot as plt

def main():
    st.title("Guess the Number Game")
    st.write("I will be guessing a number between 1-3 it will change after each tries, you have total of 3 chances")

    res = st.radio("Are you ready?", ('Yes', 'No'))
    if res == 'Yes':
        user_ans = st.radio("Already a user?", ('Yes', 'No'))
        if user_ans == 'Yes':
            name = st.text_input('Enter Full Name')
            name = name.upper()
            st.write('Hi,', name)
            time.sleep(0.5)
            st.write("Setting up game for you")
            time.sleep(1)
            st.write("Game begins")
            time.sleep(2)
            game(name)
        else:
            st.write("Exiting from game, Thank you")
    else:
        st.write("Exiting from game, Thank you")


def game(name):
    j = 0
    m = 0
    s = 0
    streak = np.nan
    for i in range(3):
        a = random.randint(1, 3)
        ans = st.number_input("Guess a number", min_value=1, max_value=3)
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

    df = pd.read_csv('player_data.csv')
    player_id = None
    if name in df['Player Name'].values:
        player_id = df.loc[df['Player Name'] == name, 'ID'].iloc[0]
    else:
        if len(df) == 0:
            player_id = 1
        else:
            player_id = df['ID'].max() + 1

    new_record = {'ID': player_id, 'Player Name': name, 'Score': s, 'Fame': streak}
    df = df.append(new_record, ignore_index=True)
    df.to_csv('player_data.csv', index=False)

    new_res = st.radio("Want to know Fame info?", ('Yes', 'No'))
    if new_res == 'Yes':
        st.write('Three streaks --- king of kings')
        st.write('Two streaks ---- classic')
        st.write('All losses --- Looser')
    else:
        st.write("No problem! Maybe next time.")

    user_ans = st.radio("Wanna help developer to buy a dosa?", ('Yes', 'No'))
    upi_id = "70@axisb"
    if user_ans == 'Yes':
        st.write("1. Buy a plain dosa (Rs 30)")
        st.write("2. Buy a masala dosa (Rs 50)")
        st.write("3. Buy a special masala dosa XL (Rs 100)")

        choice = st.radio("Enter the option you want to select from above", (1, 2, 3))
        if choice in [1, 2, 3]:
            price = 30 if choice == 1 else 50 if choice == 2 else 100
            qr_data = f"upi://pay?pa={upi_id}&am={price}&pn=Dosa Payment"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color=(230, 250, 250))
            title = f'    Contributing Rs.{price} for Dosa'
            draw = ImageDraw.Draw(qr_img)
            font_size = 24
            draw.text((10, qr_img.size[1] - 40), title, fill='black', font=ImageFont.truetype("arial.ttf", font_size))

            plt.figure(figsize=(3, 3))
            plt.imshow(qr_img)
            plt.axis('off')
            st.pyplot()
            st.write("Thank you! for your generosity :)")
        else:
            st.write("Invalid choice!")

    else:
        st.write("No problem! Maybe next time.")

if __name__ == "__main__":
    main()
