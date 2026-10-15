import streamlit as st
import io
from gtts import gTTS
from fastapi import APIRouter, HTTPException, File, UploadFile, Form

st.markdown(
    """
    <style>
    div[data-testid="stAlert"] {
        color: #1F2937 !important;
        border-radius: 10px;
    }

    div[data-testid="stAlert"] p {
        color: #1F2937 !important;
        font-weight: 500;
    }

    div[data-testid="stAlert"] svg {
        color: #1F2937 !important;
        fill: #1F2937 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import requests
from datetime import date, datetime
from streamlit_mic_recorder import mic_recorder

from pathlib import Path


st.set_page_config(
    page_title="कृषिमित्र AI",
    page_icon="🌾",
    layout="wide"
)
# Load the external CSS file
css_path = Path(__file__).parent / "static" / "style.css"

with open(css_path, "r", encoding="utf-8") as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True
    )
API_URL = "https://krishimitra-ai-lw7w.onrender.com"
farms = []

try:
    farm_response = requests.get(
        f"{API_URL}/farms",
        timeout=5
    )

    if farm_response.status_code == 200:
        farms = farm_response.json()

except requests.RequestException:
    farms = []

# =========================================================
# HEADER
# =========================================================

st.title("🌾 कृषिमित्र AI")
# 🌿 KrishiMitra AI Sidebar
with st.sidebar:
    st.markdown("# 🌿 कृषिमित्र AI")
    st.caption("तुमच्या शेतीचा डिजिटल साथीदार")

    st.divider()

    page = st.radio(
    "मुख्य मेनू",
    [
        "🏠 डॅशबोर्ड",
        "🌾 शेती व्यवस्थापन",
        "🌱 पीक व्यवस्थापन",
        "🐄 जनावरांचे व्यवस्थापन",
        "🥛 दूध नोंद",
        "👷 कामगार व्यवस्थापन",
        "🏪 दुकान व्यवस्थापन",
        "🤖 शेती AI सहाय्यक",
        "🌦️ हवामान व शेती सूचना",
    ],
    key="main_navigation",
    index=0
)

    st.divider()
    st.caption("🌱 स्मार्ट शेती, सोपे व्यवस्थापन")
# Page content based on sidebar selection


if page == "🏠 डॅशबोर्ड":
    st.title("🌿 नमस्कार! कृषिमित्र AI मध्ये स्वागत आहे")
    st.caption("तुमच्या शेतीचा आजचा आढावा")

    st.divider()

    
    # Farming banner image
    image_path = Path(__file__).resolve().parent / "static" / "farm_banner.jpg"

    if image_path.exists():
        st.image(
            str(image_path),
            use_container_width=True,
            caption="🌾 आपली शेती, आपली प्रगती"
        )
    else:
        st.warning(f"फोटो सापडला नाही: {image_path}")


    st.info(
        "👈 संपूर्ण माहिती पाहण्यासाठी डावीकडील "
        "मेनूमधून विभाग निवडा."
    )

else:
    st.subheader("शेतकऱ्यांसाठी स्मार्ट सहाय्यक")

st.divider()

st.divider()

if page == "🌾 शेती व्यवस्थापन":
    # =========================================================
    # FARM MANAGEMENT
    # =========================================================

    st.header("🌱 माझी शेती")

    farmer_name = st.text_input(
        "👨‍🌾 शेतकऱ्याचे नाव",
        key="farmer_name"
    )

    farm_name = st.text_input(
        "🌾 शेताचे नाव",
        key="farm_name"
    )

    location = st.text_input(
        "📍 ठिकाण",
        key="farm_location"
    )

    total_acres = st.number_input(
        "📐 एकूण क्षेत्रफळ (एकर)",
        min_value=0.0,
        step=0.5,
        key="total_acres"
    )

    if st.button(
        "💾 शेतीची माहिती जतन करा",
        key="save_farm"
    ):

        if farmer_name and farm_name and location and total_acres > 0:

            response = requests.post(
                f"{API_URL}/farms",
                params={
                    "farmer_name": farmer_name,
                    "farm_name": farm_name,
                    "location": location,
                    "total_acres": total_acres
                }
            )

            if response.status_code == 200:
                st.success(
                    "✅ शेतीची माहिती यशस्वीरित्या जतन झाली!"
                )
            else:
                st.error(
                    "❌ माहिती जतन करता आली नाही."
                )

        else:
            st.warning(
                "⚠️ कृपया सर्व माहिती भरा."
            )


    # =========================================================
    # SHOW FARMS
    # =========================================================

    st.divider()

    st.header("📋 माझ्या शेतीची माहिती")

    farm_response = requests.get(
        f"{API_URL}/farms"
    )

    farms = []

    if farm_response.status_code == 200:

        farms = farm_response.json()

        if farms:

            for farm in farms:

                st.write(
                    f"👨‍🌾 **शेतकरी:** {farm['farmer_name']}"
                )

                st.write(
                    f"🌾 **शेत:** {farm['farm_name']}"
                )

                st.write(
                    f"📍 **ठिकाण:** {farm['location']}"
                )

                st.write(
                    f"📐 **क्षेत्रफळ:** {farm['total_acres']} एकर"
                )

                if st.button(
                    "🗑️ शेती हटवा",
                    key=f"delete_farm_{farm['id']}"
                ):
                    response = requests.delete(
                        f"{API_URL}/farms/{farm['id']}"
                    )

                    if response.status_code == 200:
                        st.success("शेतीची माहिती हटवली!")
                        st.rerun()
                    else:
                        st.error("शेती हटवता आली नाही.")

                st.divider()

        else:

            st.info(
                "अजून कोणतीही शेतीची माहिती उपलब्ध नाही."
            )

    else:

        st.error(
            "❌ शेतीची माहिती मिळवता आली नाही."
        )

if page == "🌱 पीक व्यवस्थापन":
    # =========================================================
    # CROP MANAGEMENT
    # =========================================================

    st.header("🌱 पिकांची माहिती")

    if farms:

        farm_options = {
            f"{farm['farm_name']} - {farm['location']}": farm["id"]
            for farm in farms
        }

        selected_farm = st.selectbox(
            "🌾 शेत निवडा",
            list(farm_options.keys()),
            key="crop_farm"
        )

        crop_name = st.text_input(
            "🌱 पिकाचे नाव",
            key="crop_name"
        )

        area_acres = st.number_input(
            "📐 पिकाचे क्षेत्रफळ (एकर)",
            min_value=0.0,
            step=0.5,
            key="crop_area"
        )

        sowing_date = st.text_input(
            "📅 पेरणीची तारीख",
            key="sowing_date"
        )

        season = st.selectbox(
            "🌦️ हंगाम",
            ["खरीप", "रब्बी", "उन्हाळी"],
            key="crop_season"
        )

        if st.button(
            "💾 पिकाची माहिती जतन करा",
            key="save_crop"
        ):

            if crop_name and area_acres > 0 and sowing_date:

                response = requests.post(
                    f"{API_URL}/crops",
                    params={
                        "crop_name": crop_name,
                        "area_acres": area_acres,
                        "sowing_date": sowing_date,
                        "season": season,
                        "farm_id": farm_options[selected_farm]
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "✅ पिकाची माहिती जतन झाली!"
                    )

                else:

                    st.error(
                        "❌ माहिती जतन करता आली नाही."
                    )

            else:

                st.warning(
                    "⚠️ कृपया सर्व माहिती भरा."
                )

    else:

        st.info(
            "⚠️ आधी शेतीची माहिती जोडा."
        )


    # =========================================================
    # SHOW CROPS
    # =========================================================

    st.divider()

    st.header("📋 माझी पिके")

    crop_response = requests.get(
        f"{API_URL}/crops"
    )

    if crop_response.status_code == 200:

        crops = crop_response.json()

        if crops:

            for crop in crops:

                farm_name_display = "माहिती उपलब्ध नाही"

                for farm in farms:

                    if farm["id"] == crop["farm_id"]:

                        farm_name_display = farm["farm_name"]

                        break

                st.write(
                    f"🌱 **पीक:** {crop['crop_name']}"
                )

                st.write(
                    f"📐 **क्षेत्रफळ:** {crop['area_acres']} एकर"
                )

                st.write(
                    f"📅 **पेरणी तारीख:** {crop['sowing_date']}"
                )

                st.write(
                    f"🌦️ **हंगाम:** {crop['season']}"
                )

                st.write(
                   f"🌾 **शेत:** {farm_name_display}"
              )

                if st.button(
                  "🗑️ पीक हटवा",
                   key=f"delete_crop_{crop['id']}"
                ):
                   response = requests.delete(
                   f"{API_URL}/crops/{crop['id']}"
               )

                   if response.status_code == 200:
                     st.success("पिकाची माहिती हटवली!")
                     st.rerun()
                   else:
                      st.error("पीक हटवता आले नाही.")

                      st.divider()
        else:

            st.info(
                "अजून कोणतीही पिकांची माहिती उपलब्ध नाही."
            )

    else:

        st.error(
            "❌ पिकांची माहिती मिळवता आली नाही."
        )
        



if page == "🐄 जनावरांचे व्यवस्थापन":
    # =========================================================
    # ANIMAL MANAGEMENT
    # =========================================================

    st.divider()

    st.header("🐄 जनावरांची माहिती")

    animal_name = st.text_input(
        "🐄 जनावराचे नाव",
        key="animal_name"
    )

    animal_type = st.selectbox(
        "🐮 जनावराचा प्रकार",
        ["गाय", "म्हैस"],
        key="animal_type"
    )

    breed = st.text_input(
        "🧬 जात",
        key="animal_breed"
    )

    age = st.number_input(
        "🎂 वय (वर्षे)",
        min_value=0.0,
        step=0.5,
        key="animal_age"
    )

    if st.button(
        "💾 जनावराची माहिती जतन करा",
        key="save_animal"
    ):

        if animal_name and breed and age > 0:

            response = requests.post(
                f"{API_URL}/animals",
                params={
                    "animal_name": animal_name,
                    "animal_type": animal_type,
                    "breed": breed,
                    "age": age,
                    "farm_id": 1
                }
            )

            if response.status_code == 200:

                st.success(
                    "✅ जनावराची माहिती जतन झाली!"
                )

            else:

                st.error(
                    "❌ माहिती जतन करता आली नाही."
                )

        else:

            st.warning(
                "⚠️ कृपया सर्व माहिती भरा."
            )


    # =========================================================
    # SHOW ANIMALS
    # =========================================================

    st.header("📋 माझी जनावरे")

    animal_response = requests.get(
        f"{API_URL}/animals"
    )

    if animal_response.status_code == 200:

        animals = animal_response.json()

        if animals:

            for animal in animals:

                st.write(
                    f"🐄 **नाव:** {animal['animal_name']}"
                )

                st.write(
                    f"🐮 **प्रकार:** {animal['animal_type']}"
                )

                st.write(
                    f"🧬 **जात:** {animal['breed']}"
                )

                st.write(
                   f"🎂 **वय:** {animal['age']} वर्षे"
                )

                if st.button(
                  "🗑️ जनावर हटवा",
                   key=f"delete_animal_{animal['id']}"
                ):
                   response = requests.delete(
                   f"{API_URL}/animals/{animal['id']}"
                )

                   if response.status_code == 200:
                      st.success("जनावराची माहिती हटवली!")
                      st.rerun()
                   elif response.status_code == 404:
                        st.error("जनावराची नोंद सापडली नाही.")
                   else:
                       st.error("जनावर हटवता आले नाही.")

                st.divider()

        else:

            st.info(
                "अजून कोणत्याही जनावराची माहिती उपलब्ध नाही."
            )

    else:

        st.error(
            "❌ जनावरांची माहिती मिळवता आली नाही."
        )

if page == "🥛 दूध नोंद":
    # =========================================================
    # MILK MANAGEMENT
    # =========================================================

    st.divider()

    st.header("🥛 दररोजच्या दुधाची नोंद")

    # Get animals
    animal_response = requests.get(
        f"{API_URL}/animals"
    )

    animals = []

    if animal_response.status_code == 200:
        animals = animal_response.json()

    if animals:

        animal_options = {
            f"{animal['animal_name']} - {animal['animal_type']}": animal["id"]
            for animal in animals
        }

        selected_animal = st.selectbox(
            "🐄 जनावर निवडा",
            list(animal_options.keys()),
            key="milk_animal"
        )

        milk_date = st.date_input(
            "📅 तारीख",
            key="milk_date"
        )

        morning_milk = st.number_input(
            "🌅 सकाळचे दूध (लिटर)",
            min_value=0.0,
            step=0.5,
            key="morning_milk"
        )

        evening_milk = st.number_input(
            "🌙 संध्याकाळचे दूध (लिटर)",
            min_value=0.0,
            step=0.5,
            key="evening_milk"
        )

        if st.button(
            "💾 दुधाची नोंद जतन करा",
            key="save_milk"
        ):

            if morning_milk > 0 or evening_milk > 0:

                response = requests.post(
                    f"{API_URL}/milk",
                    params={
                        "animal_id": animal_options[selected_animal],
                        "milk_date": str(milk_date),
                        "morning_milk": morning_milk,
                        "evening_milk": evening_milk
                    }
                )

                if response.status_code == 200:

                    total = morning_milk + evening_milk

                    st.success(
                        f"✅ दुधाची नोंद जतन झाली! एकूण दूध: {total} लिटर"
                    )

                else:

                    st.error(
                        "❌ दुधाची नोंद जतन करता आली नाही."
                    )

            else:

                st.warning(
                    "⚠️ कृपया सकाळचे किंवा संध्याकाळचे दूध भरा."
                )

    else:

        st.info(
            "⚠️ आधी जनावराची माहिती जोडा."
        )
        # =========================================================
    # SHOW MILK RECORDS
    # =========================================================

    st.divider()

    st.header("📋 दुधाच्या नोंदी")

    milk_response = requests.get(
        f"{API_URL}/milk"
    )

    if milk_response.status_code == 200:

        milk_records = milk_response.json()

        if milk_records:

            for record in milk_records:

                animal_name_display = "माहिती उपलब्ध नाही"

                for animal in animals:

                    if animal["id"] == record["animal_id"]:
                        animal_name_display = animal["animal_name"]
                        break

                st.write(
                    f"🐄 **जनावर:** {animal_name_display}"
                )

                st.write(
                    f"📅 **तारीख:** {record['milk_date']}"
                )

                st.write(
                    f"🌅 **सकाळचे दूध:** {record['morning_milk']} लिटर"
                )

                st.write(
                    f"🌙 **संध्याकाळचे दूध:** {record['evening_milk']} लिटर"
                )

                st.write(
                   f"🥛 **एकूण दूध:** {record['total_milk']} लिटर"
               )

                if st.button(
                   "🗑️ दूध नोंद हटवा",
                    key=f"delete_milk_{record['id']}"
                ):
                    response = requests.delete(
                        f"{API_URL}/milk/{record['id']}"
                   ) 

                    if response.status_code == 200:
                      st.success("दुधाची नोंद हटवली!")
                      st.rerun()
                    elif response.status_code == 404:
                     st.error("दुधाची नोंद सापडली नाही.")
                    else:
                     st.error("दुधाची नोंद हटवता आली नाही.")

                     st.divider()
            else:

              st.info(
                "अजून कोणतीही दुधाची नोंद उपलब्ध नाही."
            )

    else:

        st.error(
            "❌ दुधाच्या नोंदी मिळवता आल्या नाहीत."
        )
        # =========================================================
    # MILK SUMMARY
    # =========================================================

    st.divider()

    st.header("📊 दुधाचा सारांश")

    if milk_records:

        total_milk = sum(
            record["total_milk"]
            for record in milk_records
        )

        total_records = len(milk_records)

        average_milk = total_milk / total_records

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🥛 एकूण दूध",
                f"{total_milk:.1f} लिटर"
            )

        with col2:
            st.metric(
                "📋 एकूण नोंदी",
                total_records
            )

        with col3:
            st.metric(
                "📈 सरासरी दूध",
                f"{average_milk:.1f} लिटर"
            )

    else:

        st.info(
            "दुधाचा सारांश पाहण्यासाठी आधी दूधाची नोंद करा."
        )

if page == "👷 कामगार व्यवस्थापन":
    # =========================================================
    # WORKER MANAGEMENT
    # =========================================================

    st.divider()

    st.header("👷 कामगारांची माहिती")

    worker_name = st.text_input(
        "👷 कामगाराचे नाव",
        key="worker_name"
    )

    phone = st.text_input(
        "📱 मोबाईल नंबर",
        key="worker_phone"
    )

    work_type = st.text_input(
        "🔨 कामाचा प्रकार",
        key="worker_work_type"
    )

    work_date = st.date_input(
        "📅 कामाची तारीख",
        key="worker_work_date"
    )

    days_worked = st.number_input(
        "📆 काम केलेले दिवस",
        min_value=0.0,
        step=1.0,
        key="worker_days"
    )

    rate_per_day = st.number_input(
        "💰 दररोजची मजुरी (₹)",
        min_value=0.0,
        step=100.0,
        key="worker_rate"
    )

    payment_status = st.selectbox(
        "💳 पेमेंट स्थिती",
        ["बाकी", "पूर्ण झाले"],
        key="worker_payment_status"
    )

    if st.button(
        "💾 कामगाराची माहिती जतन करा",
        key="save_worker"
    ):

        if worker_name and work_type and days_worked > 0 and rate_per_day > 0:

            total_payment = days_worked * rate_per_day

            response = requests.post(
                f"{API_URL}/workers",
                params={
                    "worker_name": worker_name,
                    "phone": phone,
                    "work_type": work_type,
                    "work_date": str(work_date),
                    "days_worked": days_worked,
                    "rate_per_day": rate_per_day,
                    "payment_status": payment_status
                }
            )

            if response.status_code == 200:

                st.success(
                    f"✅ माहिती जतन झाली! एकूण मजुरी: ₹{total_payment:.2f}"
                )

            else:

                st.error(
                    "❌ कामगाराची माहिती जतन करता आली नाही."
                )

        else:

            st.warning(
                "⚠️ कृपया आवश्यक माहिती भरा."
            )
            # =========================================================
    # SHOW WORKERS
    # =========================================================

    st.divider()

    st.header("📋 कामगारांची नोंद")

    worker_response = requests.get(
        f"{API_URL}/workers"
    )

    if worker_response.status_code == 200:

        workers = worker_response.json()

        if workers:

            for worker in workers:

                st.write(
                    f"👷 **नाव:** {worker['worker_name']}"
                )

                st.write(
                    f"📱 **मोबाईल:** {worker['phone']}"
                )

                st.write(
                    f"🔨 **काम:** {worker['work_type']}"
                )

                st.write(
                    f"📅 **तारीख:** {worker['work_date']}"
                )

                st.write(
                    f"📆 **कामाचे दिवस:** {worker['days_worked']}"
                )

                st.write(
                    f"💰 **दररोजची मजुरी:** ₹{worker['rate_per_day']}"
                )

                st.write(
                    f"💵 **एकूण मजुरी:** ₹{worker['total_payment']}"
                )
                st.write(
                    f"💵 **आगाऊ रक्कम:** ₹{worker['advance_payment']}"
            )

                st.write(
                    f"💰 **बाकी रक्कम:** ₹{worker['remaining_payment']}"
        )

                st.write(
                    f"💳 **पेमेंट स्थिती:** {worker['payment_status']}"
                )

                if st.button(
                    "🗑️ कामगार नोंद हटवा",
                    key=f"delete_worker_{worker['id']}"
                ):
                    response = requests.delete(
                        f"{API_URL}/workers/{worker['id']}"
                    )

                    if response.status_code == 200:
                        st.success("कामगाराची नोंद हटवली!")
                        st.rerun()
                    elif response.status_code == 404:
                        st.error("कामगाराची नोंद सापडली नाही.")
                    else:
                        st.error("कामगाराची नोंद हटवता आली नाही.")

                st.divider()

        else:

            st.info(
                "अजून कोणत्याही कामगाराची नोंद उपलब्ध नाही."
            )

    else:

        st.error(
            "❌ कामगारांची माहिती मिळवता आली नाही."
        )


if page == "🏪 दुकान व्यवस्थापन":

    st.divider()
    st.header("🏪 दुकान व्यवस्थापन")
    st.write("दुकानातील विक्री आणि ग्राहकांच्या पेमेंटची नोंद")

    # ---------------- NEW SALE FORM ----------------
    st.subheader("📝 नवीन विक्रीची नोंद")

    with st.form("store_sale_form"):
        product_name = st.text_input("📦 उत्पादनाचे नाव")

        quantity = st.number_input(
            "🔢 प्रमाण",
            min_value=0.0,
            step=1.0
        )

        customer_name = st.text_input("👤 ग्राहकाचे नाव")

        total_amount = st.number_input(
            "💰 एकूण रक्कम (₹)",
            min_value=0.0,
            step=100.0
        )

        amount_paid = st.number_input(
            "✅ मिळालेली रक्कम (₹)",
            min_value=0.0,
            step=100.0
        )

        sale_date = st.date_input("📅 विक्रीची तारीख")

        submitted = st.form_submit_button("💾 विक्री जतन करा")

    # ---------------- SAVE SALE ----------------
    if submitted:

        if not product_name.strip() or not customer_name.strip():
            st.warning("कृपया उत्पादनाचे आणि ग्राहकाचे नाव भरा.")

        elif quantity <= 0 or total_amount <= 0:
            st.warning("प्रमाण आणि एकूण रक्कम शून्यापेक्षा जास्त असावी.")

        elif amount_paid > total_amount:
            st.warning("मिळालेली रक्कम एकूण रकमेपेक्षा जास्त असू शकत नाही.")

        else:
            try:
                response = requests.post(
                    f"{API_URL}/shop/sales",
                    json={
                        "product_name": product_name.strip(),
                        "quantity": quantity,
                        "total_amount": total_amount,
                        "customer_name": customer_name.strip(),
                        "sale_date": str(sale_date),
                        "amount_paid": amount_paid
                    },
                    timeout=10
                )

                if response.status_code in (200, 201):
                    st.success("विक्री यशस्वीरित्या जतन झाली!")
                    st.rerun()

                else:
                    st.error("विक्री जतन करता आली नाही.")
                    st.write("Backend status:", response.status_code)
                    st.write("Backend response:", response.text)

            except requests.RequestException as error:
                st.error(f"Backend शी संपर्क होत नाही: {error}")

    # ---------------- SAVED SALES ----------------
    st.divider()
    st.subheader("📋 जतन केलेल्या विक्री")

    try:
        sales_response = requests.get(
            f"{API_URL}/shop/sales",
            timeout=10
        )

        if sales_response.status_code == 200:
            sales = sales_response.json()

            if sales:
                for sale in sales:
                    st.markdown("---")

                    col1, col2, col3 = st.columns([2, 2, 1])

                    with col1:
                        st.write(f"🆔 विक्री क्रमांक: {sale['id']}")
                        st.write(f"📦 उत्पादन: {sale['product_name']}")
                        st.write(f"👤 ग्राहक: {sale['customer_name']}")
                        st.write(f"🔢 प्रमाण: {sale['quantity']}")
                        st.write(f"📅 तारीख: {sale['sale_date']}")

                    with col2:
                        st.write(
                            f"💰 एकूण: ₹{sale['total_amount']:.2f}"
                        )
                        st.write(
                            f"✅ मिळाले: ₹{sale['amount_paid']:.2f}"
                        )
                        st.write(
                            f"⏳ बाकी: ₹{sale['remaining_balance']:.2f}"
                        )

                    with col3:
                        if st.button(
                            "🗑️ Delete",
                            key=f"delete_sale_{sale['id']}"
                        ):
                            try:
                                delete_response = requests.delete(
                                    f"{API_URL}/shop/sales/{sale['id']}",
                                    timeout=10
                                )

                                if delete_response.status_code == 200:
                                    st.success("विक्री हटवली!")
                                    st.rerun()

                                else:
                                    st.error("विक्री हटवता आली नाही.")
                                    st.write(delete_response.text)

                            except requests.RequestException as error:
                                st.error(
                                    f"Backend शी संपर्क होत नाही: {error}"
                                )

            else:
                st.info("अजून कोणतीही विक्री जतन केलेली नाही.")

        else:
            st.error("विक्रीची माहिती मिळवता आली नाही.")
            st.write("Backend status:", sales_response.status_code)

    except requests.RequestException as error:
        st.error(f"Saved sales मिळवताना त्रुटी: {error}")




# =========================================================
# AI FARMING ASSISTANT - TEXT + VOICE INPUT + VOICE OUTPUT
# =========================================================

elif page == "🤖 शेती AI सहाय्यक":

    import io
    import hashlib
    from gtts import gTTS

    st.header("🤖 शेती AI सहाय्यक")

    st.write(
        "शेती, पिके, कीड, खते, पाणी आणि जनावरांबद्दल "
        "मराठीत किंवा इतर भाषेत प्रश्न विचारा."
    )

    st.info(
        "🌱 स्पष्ट प्रश्न विचारा. पिकाचे नाव, पेरणीची तारीख "
        "आणि दिसणारी लक्षणे सांगितल्यास अधिक योग्य सल्ला मिळेल."
    )

    # -----------------------------------------------------
    # SESSION STATE
    # -----------------------------------------------------

    if "farming_chat" not in st.session_state:
        st.session_state.farming_chat = []

    if "last_voice_id" not in st.session_state:
        st.session_state.last_voice_id = None

    if "farming_answer" not in st.session_state:
        st.session_state.farming_answer = None

    if "farming_audio" not in st.session_state:
        st.session_state.farming_audio = None

    if "recognized_question" not in st.session_state:
        st.session_state.recognized_question = ""

    if "voice_language" not in st.session_state:
        st.session_state.voice_language = "mr"

    # -----------------------------------------------------
    # ASK AI
    # -----------------------------------------------------

    def ask_farming_ai(question):

        question = question.strip()

        if not question:
            return

        # Clear audio belonging to the previous answer
        st.session_state.farming_audio = None
        st.session_state.farming_answer = None

        st.session_state.farming_chat.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("शेती AI उत्तर तयार करत आहे..."):

                try:
                    response = requests.post(
                        f"{API_URL}/ai/ask",
                        json={"question": question},
                        timeout=60
                    )

                    if response.status_code == 200:
                        answer = response.json().get(
                            "answer",
                            "माफ करा, उत्तर मिळाले नाही."
                        )
                    else:
                        answer = (
                            "AI कडून उत्तर मिळाले नाही. "
                            "कृपया पुन्हा प्रयत्न करा."
                        )

                    # Save answer so it survives Streamlit reruns
                    st.session_state.farming_answer = answer

                    st.write(answer)

                    st.session_state.farming_chat.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except requests.RequestException:
                    st.error(
                        "Backend शी संपर्क होत नाही. "
                        "FastAPI सर्व्हर सुरू आहे का ते तपासा."
                    )

    # -----------------------------------------------------
    # DISPLAY CHAT HISTORY
    # -----------------------------------------------------

    for message in st.session_state.farming_chat:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # -----------------------------------------------------
    # MARATHI VOICE OUTPUT
    # -----------------------------------------------------

    if st.session_state.farming_answer:

        st.subheader("🔊 AI उत्तर ऐका")

        if st.button(
            "🔊 उत्तर ऐका",
            key="listen_farming_answer"
        ):

            try:
                with st.spinner("आवाज तयार होत आहे..."):

                    audio_buffer = io.BytesIO()

                    tts = gTTS(
                        text=st.session_state.farming_answer,
                        lang="mr"
                    )

                    tts.write_to_fp(audio_buffer)

                    st.session_state.farming_audio = (
                        audio_buffer.getvalue()
                    )

            except Exception:
                st.session_state.farming_audio = None

                st.error(
                    "आवाज तयार झाला नाही. "
                    "इंटरनेट कनेक्शन तपासा आणि पुन्हा प्रयत्न करा."
                )

        if st.session_state.farming_audio:
            st.audio(
                st.session_state.farming_audio,
                format="audio/mp3"
            )

    # -----------------------------------------------------
    # VOICE INPUT
    # -----------------------------------------------------

    st.subheader("🎤 बोलून प्रश्न विचारा")

    st.caption(
        "तुम्ही कोणत्या भाषेत बोलणार आहात ते निवडा. "
        "रेकॉर्डिंगनंतर ओळखलेला प्रश्न तपासा."
    )

    voice_language = st.selectbox(
        "बोलण्याची भाषा",
        options=["मराठी", "हिंदी", "English"],
        index=0,
        key="farming_voice_language"
    )

    language_codes = {
        "मराठी": "mr",
        "हिंदी": "hi",
        "English": "en"
    }

    st.session_state.voice_language = language_codes[
        voice_language
    ]

    voice_audio = mic_recorder(
        start_prompt="🎤 बोलण्यासाठी दाबा",
        stop_prompt="⏹️ रेकॉर्डिंग थांबवा",
        key="farming_voice_recorder"
    )

    if voice_audio and voice_audio.get("bytes"):

        audio_bytes = voice_audio["bytes"]
        voice_id = hashlib.sha256(audio_bytes).hexdigest()

        # Process the same recording only once
        if voice_id != st.session_state.last_voice_id:

            st.session_state.last_voice_id = voice_id

            with st.spinner("तुमचा आवाज मजकुरात बदलत आहे..."):

                try:
                    
                    transcription_response = requests.post(
                        f"{API_URL}/ai/transcribe",
                        files={
                            "audio": (
                                "farming_question.wav",
                                audio_bytes,
                                "audio/wav"
                            )
                        },
                        data={
                            "language": st.session_state.voice_language
                        },
                        timeout=90
                    )


                    if transcription_response.status_code == 200:

                        recognized_text = (
                            transcription_response.json()
                            .get("text", "")
                            .strip()
                        )

                        if recognized_text:

                            st.session_state.recognized_question = (
                                recognized_text
                            )

                        else:
                            st.warning(
                                "आवाज समजला नाही. "
                                "कृपया हळू आणि स्पष्ट बोला."
                            )

                    else:
                        st.error(
                            "आवाज ओळखता आला नाही. "
                            "कृपया पुन्हा रेकॉर्ड करा."
                        )

                except requests.RequestException:
                    st.error(
                        "Backend शी संपर्क होत नाही. "
                        "FastAPI सर्व्हर सुरू आहे का ते तपासा."
                    )

    # -----------------------------------------------------
    # REVIEW AND SUBMIT RECOGNIZED QUESTION
    # -----------------------------------------------------

    if st.session_state.recognized_question:

        st.write("**🎧 आवाजातून ओळखलेला प्रश्न:**")

        corrected_question = st.text_area(
            "चुकीचा मजकूर असल्यास इथे दुरुस्त करा",
            value=st.session_state.recognized_question,
            key="corrected_farming_question"
        )

        if st.button(
            "✅ प्रश्न AI ला विचारा",
            key="submit_recognized_question"
        ):

            if corrected_question.strip():
                st.session_state.recognized_question = ""
                ask_farming_ai(corrected_question)
                st.rerun()

            else:
                st.warning("कृपया प्रश्न बोला किंवा लिहा.")

    # -----------------------------------------------------
    # TEXT INPUT
    # -----------------------------------------------------

    st.subheader("⌨️ किंवा प्रश्न टाइप करा")

    typed_question = st.chat_input(
        "तुमचा शेतीविषयक प्रश्न इथे लिहा..."
    )

    if typed_question:
        ask_farming_ai(typed_question)
        st.rerun()

    # -----------------------------------------------------
    # CLEAR CHAT
    # -----------------------------------------------------

    if st.button(
        "🗑️ संभाषण साफ करा",
        key="clear_farming_chat"
    ):
        st.session_state.farming_chat = []
        st.session_state.last_voice_id = None
        st.session_state.farming_answer = None
        st.session_state.farming_audio = None
        st.session_state.recognized_question = ""
        st.rerun()

elif page == "🌦️ हवामान व शेती सूचना":
    st.title("🌦️ हवामान व शेती सूचना")
    st.write("तुमच्या शेतासाठी हवामान आणि शेतीविषयक सूचना पाहा.")

    city = st.text_input(
        "गाव किंवा शहराचे नाव लिहा",
        value="Baramati",
        key="weather_city"
    )

    if st.button("🌤️ हवामान तपासा", key="check_weather"):
        if not city.strip():
            st.warning("कृपया गावाचे नाव लिहा.")
        else:
            try:
                with st.spinner("हवामानाची माहिती मिळवत आहे..."):
                    response = requests.get(
                        f"{API_URL}/weather/check",
                        params={"city": city.strip()},
                        timeout=30
                    )

                if response.status_code == 200:
                    data = response.json()
                    current = data["current"]
                    daily = data["daily"]

                    location = data["location"]
                    location_name = location["name"]

                    if location.get("admin1"):
                        location_name += ", " + location["admin1"]

                    # Location
                    st.subheader(f"📍 {location_name}")

                    # Current weather
                    st.markdown("### 🌡️ सध्याचे हवामान")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "तापमान",
                        f'{current["temperature_2m"]} °C'
                    )
                    col2.metric(
                        "आर्द्रता",
                        f'{current["relative_humidity_2m"]} %'
                    )
                    col3.metric(
                        "वाऱ्याचा वेग",
                        f'{current["wind_speed_10m"]} km/h'
                    )

                    st.write(
                        f'सध्याचा पाऊस: {current["precipitation"]} mm'
                    )

                    # Three-day forecast
                    st.markdown("### 📅 पुढील ३ दिवस")

                    for i, forecast_date in enumerate(daily["time"]):
                        with st.container(border=True):
                            st.markdown(f"**📆 {forecast_date}**")

                            c1, c2, c3 = st.columns(3)

                            c1.metric(
                                "कमाल तापमान",
                                f'{daily["temperature_2m_max"][i]} °C'
                            )
                            c2.metric(
                                "किमान तापमान",
                                f'{daily["temperature_2m_min"][i]} °C'
                            )
                            c3.metric(
                                "पावसाची शक्यता",
                                f'{daily["precipitation_probability_max"][i]} %'
                            )

                    # Farming alerts - outside the forecast loop
                    st.markdown("### 🚜 शेतीविषयक सूचना")

                    alerts_shown = 0

                    rain_probability = max(
                        daily["precipitation_probability_max"],
                        default=0
                    )

                    max_temperature = max(
                        daily["temperature_2m_max"],
                        default=0
                    )

                    if rain_probability >= 60:
                        st.warning(
                            "🌧️ पावसाची शक्यता जास्त आहे. "
                            "शेतातील कामांचे नियोजन करा आणि काढणी केलेल्या "
                            "मालासाठी सुरक्षित, झाकलेली जागा ठेवा."
                        )
                        alerts_shown += 1

                    if max_temperature >= 35:
                        st.warning(
                            "☀️ तापमान ३५°C किंवा त्यापेक्षा जास्त होण्याची "
                            "शक्यता आहे. पिकांतील ओलावा तपासा आणि "
                            "गरजेनुसार सिंचनाचे नियोजन करा."
                        )
                        alerts_shown += 1

                    if current["wind_speed_10m"] >= 30:
                        st.warning(
                            "💨 वाऱ्याचा वेग जास्त आहे. फवारणी करण्यापूर्वी "
                            "स्थानिक हवामान व उत्पादनाच्या सूचनांची तपासणी करा."
                        )
                        alerts_shown += 1

                    if alerts_shown == 0:
                        st.success(
                            "✅ या साध्या नियमांनुसार सध्या विशेष हवामान "
                            "सूचना नाही. शेतातील प्रत्यक्ष परिस्थितीही तपासा."
                        )

                    st.caption(
                        "स्रोत: Open-Meteo. हे सामान्य हवामान-आधारित "
                        "इशारे आहेत, पिकानुसार तज्ज्ञ सल्ला नाहीत. "
                        "हवामानाचा अंदाज बदलू शकतो."
                    )

                else:
                    try:
                        error_message = response.json().get(
                            "detail",
                            "हवामानाची माहिती मिळाली नाही."
                        )
                    except ValueError:
                        error_message = "हवामानाची माहिती मिळाली नाही."

                    st.error(error_message)

            except requests.RequestException:
                st.error(
                    "Backend शी संपर्क होत नाही. "
                    "FastAPI आणि इंटरनेट कनेक्शन तपासा."
                )
                
