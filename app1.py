import streamlit as st
import random
import pandas as pd
import time
import numpy as np
import qrcode
import matplotlib.pyplot as plt
from PIL import ImageDraw,ImageFont

def main():
    j = 0
    m = 0
    s = 0
    streak = np.nan
    st.title("Guess the Number Game")
    st.write("I will be guessing a number between 1-3. It will change after each try, and you have a total of 3 chances.")

    res = st.radio("Are you ready?", ('Yes', 'No'))
    if res == 'Yes':
        name = st.text_input('Enter Full Name', key='name_input').upper()
        if name:
            st.write('Hi,', name)
            st.write("Setting up the game for you...")
            time.sleep(2)
            st.write("Game begins!")
            time.sleep(2)
            for i in range(2, -1, -1):
                a = random.randint(1, 3)
                ans = st.number_input("Guess a number:", min_value=1, max_value=3, key=f"guess_{i}")
                if ans:
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
                    else:
                        st.write(f"Oh no!! I guessed {a}")
                        time.sleep(0.5)
                        st.write("Try again......")
                        m += 1
                        if m == 3:
                            streak = 'LOOSSER'
                            st.write(streak)
            st.write('')
            st.write("SCORE :", s)

            df = pd.DataFrame(columns=['ID', 'Player Name', 'Score', 'Fame'])

            if st.radio("Already a user?", ('Yes', 'No')) == 'Yes':
                if name in df['Player Name'].values:
                    player_id = df.loc[df['Player Name'] == name, 'ID'].iloc[0]
                else:
                    if len(df) == 0:
                        player_id = 1
                    else:
                        player_id = df['ID'].max() + 1

                new_record = {'ID': player_id, 'Player Name': name, 'Score': s, 'Fame': streak}
                df = df.append(new_record, ignore_index=True)

                st.write("Data saved.")
            else:
                st.write("No problem! Maybe next time.")

            st.write('Three streaks --- king of kings')
            st.write('Two streaks ---- classic')
            st.write('All losses --- Looser')

            if st.radio("Wanna help developer to buy a dosa?", ('Yes', 'No')) == 'Yes':
                st.write("1. Buy a plain dosa (Rs 30)")
                st.write("2. Buy a masala dosa (Rs 50)")
                st.write("3. Buy a special masala dosa XL (Rs 100)")

                choice = st.radio("Enter the option you want to select from above", (1, 2, 3))
                if choice in [1, 2, 3]:
                    price = 30 if choice == 1 else 50 if choice == 2 else 100
                    upi_id = "70@axisb"
                    qr_data = f"upi://pay?pa={upi_id}&am={price}&pn=Dosa Payment"
                    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                    qr.add_data(qr_data)
                    qr.make(fit=True)
                    qr_img = qr.make_image(fill_color="black", back_color=(230, 250, 250))

                    plt.figure(figsize=(3, 3))
                    plt.imshow(qr_img)
                    plt.axis('off')
                    st.pyplot()  # Show the QR code in the app
                    st.write("Thank you! for your generosity :)")

                else:
                    st.write("Invalid choice!")
            else:
                st.write("No problem! Maybe next time.")
        else:
            st.write("Please enter your name.")
    else:
        st.write("Exiting from the game. Thank you.")

if __name__ == "__main__":
    main()
