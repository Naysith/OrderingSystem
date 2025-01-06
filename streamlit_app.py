import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- Title ---
st.title("Selamat Datang di DELIS BURGER")

# --- Define Image and Excel Directories ---
img_folder = os.path.join(os.getcwd(), "Img")  # Folder for images
excel_file_path = os.path.join(os.getcwd(), "Order.xlsx")  # Excel file for orders

# --- Banner Image ---
banner_path = os.path.join(img_folder, "Banner.jpg")
if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)
else:
    st.error("Banner image not found!")

# --- Menu Items and Prices ---
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

# --- Initialize Order State ---
if 'order' not in st.session_state:
    st.session_state.order = {}

# --- Sidebar Navigation ---
st.sidebar.title("Menu List")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# --- Display Menu Category ---
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

# --- Display Cart in Sidebar ---
st.sidebar.header("Your Order")
total_price = 0  # Initialize total price
items_to_remove = []  # Temporary list to store items for removal

if st.session_state.order:
    for ordered_item, quantity in st.session_state.order.items():
        # Get item details (price)
        for category, items in menu_items.items():
            if ordered_item in items:
                price = items[ordered_item]["price"]
                item_total = price * quantity  # Calculate total price for this item
                total_price += item_total  # Add to the overall total

                # Display item name, quantity, and price in the sidebar
                col1, col2 = st.sidebar.columns([2, 1])
                col1.write(f"{ordered_item} {quantity}x")
                col2.write(f"Rp.{item_total:.3f}")

                # Button to remove an item (mark for removal)
                if col2.button("Remove", key=f"remove_{ordered_item}"):
                    items_to_remove.append(ordered_item)

    # Remove items after iterating
    for item in items_to_remove:
        del st.session_state.order[item]

    # Display total price above the "Order Now" button
    st.sidebar.subheader(f"Total: Rp.{total_price:.3f}")

    # Order button
    if st.sidebar.button("Place Order"):
        # Add order to Excel file
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare order data
        order_data = []
        for item, quantity in st.session_state.order.items():
            for category, items in menu_items.items():
                if item in items:
                    price = items[item]["price"]
                    order_data.append({
                        "Item": item,
                        "Quantity": quantity,
                        "Time": order_time,
                        "Price": price
                    })
                    break

        # Append to existing Excel file or create a new one
        if os.path.exists(excel_file_path):
            with pd.ExcelWriter(excel_file_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                pd.DataFrame(order_data).to_excel(writer, sheet_name="Orders", index=False, header=False, startrow=writer.sheets['Orders'].max_row)
        else:
            pd.DataFrame(order_data).to_excel(excel_file_path, sheet_name="Orders", index=False)

        # Clear the cart
        st.session_state.order = {}
        
        # Show success message in the sidebar
        st.sidebar.success("Your order has been placed! Thank you!")
        st.sidebar.info("Refresh the page to start a new order!")

else:
    st.sidebar.write("Your cart is empty. Start adding items!")

# --- Footer ---
st.sidebar.write("---")
st.sidebar.write("Thank you for visiting DELIS BURGER!")
