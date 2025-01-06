import streamlit as st
import os
import pandas as pd
from datetime import datetime
import random
<<<<<<< HEAD

# --- Page Configuration ---
st.set_page_config(page_title="Delis Burger", layout="wide")

# --- Define Image and Excel Directories ---
img_folder = os.path.join(os.getcwd(), "Img")  # Folder for images
excel_file_path = os.path.join(os.getcwd(), "Order.xlsx")  # Excel file for orders

# --- Initialize Session State ---
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'order' not in st.session_state:
    st.session_state.order = {}
if 'order_number' not in st.session_state:
    st.session_state.order_number = None

# --- Menu Items ---
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

# --- Page Navigation ---
if st.session_state.page == "menu":
    # Page 1: Menu Page
    st.title("Selamat Datang di DELIS BURGER")

    # Banner Image
    banner_path = os.path.join(img_folder, "Banner.jpg")
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)
    else:
        st.error("Banner image not found!")

    # Sidebar Navigation
    st.sidebar.title("Menu List")
    selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

    # Display Menu Items
    st.title(selected_category)
    for item, item_data in menu_items[selected_category].items():
        image_file = item_data["image"]
        price = item_data["price"]

        # Image path for each menu item
        image_path = os.path.join(img_folder, image_file)

        # Layout with columns
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

    # Sidebar: Display Cart
    st.sidebar.header("Your Order")
    total_price = 0
    if st.session_state.order:
        for ordered_item, quantity in st.session_state.order.items():
            for category, items in menu_items.items():
                if ordered_item in items:
                    price = items[ordered_item]["price"]
                    total_price += price * quantity

                    # Display item with remove button
                    col1, col2 = st.sidebar.columns([3, 1])
                    col1.write(f"{ordered_item} {quantity}x")
                    if col2.button("Remove", key=f"remove_{ordered_item}"):
                        del st.session_state.order[ordered_item]

        # Total Price and Review Button
        st.sidebar.subheader(f"Total: Rp.{total_price:.3f}")
        if st.sidebar.button("Review Order"):
            st.session_state.page = "review"
    else:
        st.sidebar.write("Your cart is empty.")

elif st.session_state.page == "review":
    # Page 2: Order Review Page
    st.title("Review Your Order")

    # Display Order Details
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
        
        # Create DataFrame for Order Summary
        df = pd.DataFrame(order_summary, columns=["Item", "Quantity", "Price", "Total Price"])
        st.table(df)
        st.write(f"**Total Price: Rp.{total_price:.3f}**")

        # Back Button
        if st.button("Back to Menu"):
            st.session_state.page = "menu"

        # Pay Button
        if st.button("Pay"):
            order_number = random.randint(1000, 9999)
            st.session_state.order_number = order_number
            st.session_state.page = "confirmation"
    else:
        st.error("Your cart is empty.")

elif st.session_state.page == "confirmation":
    # Page 3: Confirmation Page
    st.title("Order Confirmation")
    if st.session_state.order_number:
        st.write("Thank you for your order!")
        st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>Order #{st.session_state.order_number}</h1>", unsafe_allow_html=True)
        st.write("Please show this number at the counter.")

        if st.button("Done"):
            st.session_state.page = "menu"
            st.session_state.order = {}
            st.session_state.order_number = None
=======

# --- Page Configuration ---
st.set_page_config(page_title="Delis Burger", layout="wide")

# --- Define Image and Excel Directories ---
img_folder = os.path.join(os.getcwd(), "Img")  # Folder for images
excel_file_path = os.path.join(os.getcwd(), "Order.xlsx")  # Excel file for orders

# --- Initialize Session State ---
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'order' not in st.session_state:
    st.session_state.order = {}
if 'order_number' not in st.session_state:
    st.session_state.order_number = None

# --- Menu Items ---
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

# --- Page Navigation ---
if st.session_state.page == "menu":
    # Page 1: Menu Page
    st.title("Selamat Datang di DELIS BURGER")

    # Banner Image
    banner_path = os.path.join(img_folder, "Banner.jpg")
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)
    else:
        st.error("Banner image not found!")

    # Sidebar Navigation
    st.sidebar.title("Menu List")
    selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

    # Display Menu Items
    st.title(selected_category)
    for item, item_data in menu_items[selected_category].items():
        image_file = item_data["image"]
        price = item_data["price"]

        # Image path for each menu item
        image_path = os.path.join(img_folder, image_file)

        # Layout with columns
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

    # Sidebar: Display Cart
    st.sidebar.header("Your Order")
    total_price = 0
    if st.session_state.order:
        for ordered_item, quantity in st.session_state.order.items():
            for category, items in menu_items.items():
                if ordered_item in items:
                    price = items[ordered_item]["price"]
                    total_price += price * quantity

                    # Display item with remove button
                    col1, col2 = st.sidebar.columns([3, 1])
                    col1.write(f"{ordered_item} {quantity}x")
                    if col2.button("Remove", key=f"remove_{ordered_item}"):
                        del st.session_state.order[ordered_item]

        # Total Price and Review Button
        st.sidebar.subheader(f"Total: Rp.{total_price:.3f}")
        if st.sidebar.button("Review Order"):
            st.session_state.page = "review"
    else:
        st.sidebar.write("Your cart is empty.")

elif st.session_state.page == "review":
    # Page 2: Order Review Page
    st.title("Review Your Order")

    # Display Order Details
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
        
        # Create DataFrame for Order Summary
        df = pd.DataFrame(order_summary, columns=["Item", "Quantity", "Price", "Total Price"])
        st.table(df)
        st.write(f"**Total Price: Rp.{total_price:.3f}**")

        # Back Button
        if st.button("Back to Menu"):
            st.session_state.page = "menu"

        # Pay Button
        if st.button("Pay"):
            order_number = random.randint(1000, 9999)
            st.session_state.order_number = order_number
            st.session_state.page = "confirmation"
    else:
        st.error("Your cart is empty.")

elif st.session_state.page == "confirmation":
    # Page 3: Confirmation Page
    st.title("Order Confirmation")
    if st.session_state.order_number:
        st.write("Thank you for your order!")
        st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>Order #{st.session_state.order_number}</h1>", unsafe_allow_html=True)
        st.write("Please show this number at the counter.")

        if st.button("Done"):
            st.session_state.page = "menu"
            st.session_state.order = {}
            st.session_state.order_number = None

>>>>>>> 9bc360e468bbd8c6e94294f057708ec33238f742
