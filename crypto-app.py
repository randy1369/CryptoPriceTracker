import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd


st.set_page_config(layout="wide")

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


image = Image.open('bg.png')

st.image(image, width=1000)


st.subheader("Wazirx Price App")
st.markdown("""
            A simple cryptocurrency price app pulling price data from the Wazirx API
            """)

expand_bar = st.expander("About")
expand_bar.markdown("""
* **A Crypto 24hr price data app, where you can select which coins to display.**
* **You can also add fav coins and only display those or you can custom type all the coins
 you want to see by typing the coin names**
* **You should search for adainr or adaeth or adabtc  or adawrx not just ada** 
                    """)


# --------------------------------------------------------------------------------------

col1 = st.sidebar
col2, col3 = st.columns((4, 1))

# --------------------------------------------------------------------------------------

df = pd.read_json('https://api.wazirx.com/sapi/v1/tickers/24hr')

#------------------------------------------------------------------------------------------------

## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['symbol'] )


fav_coins = ['adainr','adausdt','avaxinr','avaxusdt','uniinr','uniusdt','trxusdt','trxinr','winusdt',
             'wininr','flokiinr','flokiusdt','dogeusdt','dogeinr','hotinr','hotusdt','maticinr','maticusdt','ethusdt','ethinr'
            'oneinr','oneusdt','xrpinr','xrpusdt','batinr','batusdt','manainr','manausdt','wrxinr','wrxusdt','wininr','winusdt',
            'shibinr','shibusdt','eosinr','eosusdt','btcinr','btcusdt']

selected_coin_option = col1.radio('Select Coins Option', ['All Coins', 'Favorite Coins', 'Custom Coins'])

if selected_coin_option == 'All Coins':
    selected_coin = col1.multiselect('Select Coins', sorted_coin, default=sorted_coin)
    fav_coins = selected_coin  # Update favorite coins list with selected coins from All Coins
elif selected_coin_option == 'Favorite Coins':
    add_to_fav_coins = col1.text_input('Add coin to Favorite Coins:')
    if add_to_fav_coins:
        fav_coins.append(add_to_fav_coins.strip())  # Add the entered coin to fav_coins
    selected_coin = col1.multiselect('Select Coins', fav_coins, default=fav_coins)
    # Additional option to add a coin to favorite coins

else:
    custom_coins = col1.text_input('Enter comma-separated coin symbols:')
    selected_coin = [coin.strip() for coin in custom_coins.split(',')]



selected_coin = df[ (df['symbol'].isin(selected_coin)) ] # Filtering data

## Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = selected_coin[:num_coin]

# Sidebar - Sort data option
sort_data = col1.checkbox('Sort Data', value=True)

if sort_data:
    df_coins = df_coins.sort_values(by=['symbol'])  # You can change 'symbol' to any column you want to sort by

col2.dataframe(df_coins)

