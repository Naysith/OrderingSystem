import streamlit as st
import os
import pandas as pd
from datetime import datetime
import random
from openpyxl import Workbook

# --- konfig halaman ---
st.set_page_config(page_title="Delis Burger", layout="wide")

# --- path file gambar & excel ---
img_folder = os.path.join(os.getcwd(), "Img")  # Folder for images
excel_file_path = os.path.join(os.getcwd(), "Order.xlsx")  # Excel file for orders

# --- penampung sementara data sesi ---
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'order' not in st.session_state:
    st.session_state.order = {}
if 'order_number' not in st.session_state:
    st.session_state.order_number = None

# --- menu makanan ---
menu_items = {
    "Burgers": {
        "Classic Burger": {"image": "Burger.png", "price": 12.000},
        "Cheese Burger": {"image": "CheeseBurger.png", "price": 15.000},
        "Chicken Burger": {"image": "ChickenBurger.png", "price": 12.000},
        "Double Cheese Burger": {"image": "DoubleCheese.png", "price": 25.000},
        "MEGA BURGER": {"image": "MEGABurger.png", "price": 40.000}
    },
    "Drinks": {
        "Coca-Cola": {"image": "CocaCola.png", "price": 5.000},
        "Sprite": {"image": "Sprite.png", "price": 5.000},
        "Lemon Tea": {"image": "LemonTea.png", "price": 5.000},
        "Milo": {"image": "Milo.png", "price": 5.000},
        "Aer Putih": {"image": "Aer.png", "price": 2.500}
    },
    "Snacks": {
        "Kebab": {"image": "Kebab.png", "price": 16.000},
        "Nugget": {"image": "Nugget.png", "price": 10.000},
        "Nugget (L)": {"image": "Lnugget.png", "price": 18.000},
        "Salad": {"image": "Salad.png", "price": 10.000},
        "Chicken Wings": {"image": "Wing.png", "price": 18.000}
    }
}

# --- Function buat save orderan ke excel ---
def save_order_to_excel(order, order_number, total_price):
    # buat dataframe dari order buat excel
    order_data = []
    for item, quantity in order.items():
        for category, items in menu_items.items():
            if item in items:
                price = items[item]["price"]
                order_data.append([order_number, item, quantity, price, price * quantity])

    df = pd.DataFrame(order_data, columns=["Order Number", "Item", "Quantity", "Price", "Total"])
    
    # ceklist excel ada atau tidak
    if os.path.exists(excel_file_path):
        try:
            # coba buka file excel yang sudah ada
            existing_df = pd.read_excel(excel_file_path, engine='openpyxl')
            
            # pakai func pd.concat untuk nambah order
            updated_df = pd.concat([existing_df, df], ignore_index=True)
        except Exception as e:
            # kalau error buat file baru dan log error
            st.error(f"Error reading the existing Excel file: {e}")
            st.write("Creating a new Excel file instead.")
            updated_df = df
    else:
        # jika tidak ada file excel buat baru 
        updated_df = df

    # ngesave data order ke excel
    updated_df.to_excel(excel_file_path, index=False, engine='openpyxl')


# --- Navigasi halaman ---
if st.session_state.page == "menu":
    # halaman 1: Menu Page
    st.title("Selamat Datang di DELIS BURGER")

    # Banner gambar
    banner_path = os.path.join(img_folder, "Banner.jpg")
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)
    else:
        st.error("Banner image not found!")

    # Sidebar
    st.sidebar.title("Menu List")
    selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

    # Display makanan
    st.title(selected_category)
    for item, item_data in menu_items[selected_category].items():
        image_file = item_data["image"]
        price = item_data["price"]

        # path gambar setiap menu
        image_path = os.path.join(img_folder, image_file)

        # Layout kolom
        col1, col2 = st.columns([1, 3])
        with col1:
            if os.path.exists(image_path):
                st.image(image_path, width=100)
            else:
                st.error(f"Image for {item} not found!")
        with col2:
            st.write(f"**{item}** - Rp.{price:.3f}")
            if st.button(f"Add {item} to Order", key=f"add_{item}"):
                st.session_state.order[item] = st.session_state.order.get(item, 0) + 1
                st.success(f"{item} has been added to your order!")

    # Sidebar: isi order yang dipilih
    st.sidebar.header("Your Order")
    total_price = 0
    if st.session_state.order:
        for ordered_item, quantity in st.session_state.order.items():
            for category, items in menu_items.items():
                if ordered_item in items:
                    price = items[ordered_item]["price"]
                    total_price += price * quantity

                    # display orderan dengan tombol remove
                    col1, col2 = st.sidebar.columns([3, 1])
                    col1.write(f"{ordered_item} {quantity}x")
                    if col2.button("Remove", key=f"remove_{ordered_item}"):
                        del st.session_state.order[ordered_item]

        # total harga dan tombol next
        st.sidebar.subheader(f"Total: Rp.{total_price:.3f}")
        if st.sidebar.button("Review Order"):
            st.session_state.page = "review"
    else:
        st.sidebar.write("Your cart is empty.")

elif st.session_state.page == "review":
    # halaman 2: buat liat order yang dipilih dan total
    st.title("Review Your Order")

    # Display detail orderan
    if st.session_state.order:
        order_summary = []
        total_price = 0
        for item, quantity in st.session_state.order.items():
            for category, items in menu_items.items():
                if item in items:
                    price = items[item]["price"]
                    order_summary.append((item, quantity, price, price * quantity))
                    total_price += price * quantity
                    break
        
        # buat tabel untuk list yang sudah diorder
        df = pd.DataFrame(order_summary, columns=["Item", "Quantity", "Price", "Total Price"])
        st.table(df)
        st.write(f"**Total Price: Rp.{total_price:.3f}**")

        # tombol balik k halaman 1
        if st.button("Back to Menu"):
            st.session_state.page = "menu"

        # tombol Bayar
        if st.button("Pay"):
            order_number = random.randint(1000, 9999)
            st.session_state.order_number = order_number
            # simpan orderan ke excel
            save_order_to_excel(st.session_state.order, order_number, total_price)
            st.session_state.page = "confirmation"
    else:
        st.error("Your cart is empty.")

elif st.session_state.page == "confirmation":
    # halaman 3: nomor pesanan
    st.title("Order Confirmation")
    if st.session_state.order_number:
        st.write("Thank you for your order!")
        st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>Order #{st.session_state.order_number}</h1>", unsafe_allow_html=True)
        st.write("Please show this number at the counter.")

        if st.button("Done"):
            st.session_state.page = "menu"
            st.session_state.order = {}
            st.session_state.order_number = None
