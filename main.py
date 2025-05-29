import streamlit as st
import pandas as pd
import os

# ประกาศตัวแปร
sex = ""
age = ""
ages = ""
freq = ""
p1 = []
reason = ""
rank = ""
know=[]
alw=""

st.set_page_config(page_title="แบบสอบถาม", layout="centered")

st.title("แบบสอบถามพฤติกรรมการบริโภค")

st.write("คุณสมบัติของกลุ่มตัวอย่าง")
st.warning("เพศชาย / หญิง อายุ 22 - 60 ปี กินมากว่า 1 ครั้ง / เดือน จำนวน 300 ชุด")
st.markdown("---")

#ข้อ 1
st.subheader("ข้อ 1 : เพศ")
sex = st.radio("กรุณาเลือกเพศ", ("ชาย", "หญิง"))
#ข้อ 2
st.subheader("ข้อ 2 : อายุ")
age_input = st.text_input("ระบุอายุ : ")

if age_input.isdigit():
    age = int(age_input)

    if 22 <= age <= 31:
        ages = "22 - 31"
    elif 32 <= age <= 41: 
        ages = "32 - 41"
    elif 42 <= age <= 51: 
        ages = "42 - 51"
    elif 52 <= age <= 60:
        ages = "52 - 60"
    elif not age.isdigit() :
        e = Error("กรุณาระบุเป็นตัวเลข")
        st.exception(e)
    else : 
        st.warning("ไม่ผ่านเงื่อนไข ปิดจบแบบสัมภาษณ์")
        if st.button("ส่งแบบสอบถาม"):
            st.success("ส่งข้อมูลเรียบร้อย")
            st.stop()
    st.success(f"คุณอยู่ในช่วงอายุ: {ages}")
    st.success("ไปยังข้อ 3")
#ข้อ 3
if age != "" and ages != "":
    st.subheader("ข้อ 3: คุณบริโภคบ่อยแค่ไหน?")
    freq = st.radio("กรุณาเลือกคำตอบ", (
        "ทุกสัปดาห์",
        "กิน 4-6 ครั้งต่อเดือน",
        "กิน 2-3 ครั้ง / เดือน",
        "กิน 1 ครั้ง / เดือน"))
    if freq == "กิน 1 ครั้ง / เดือน":
        st.warning("ไม่ผ่านเงื่อนไข ปิดจบแบบสัมภาษณ์")
        if st.button("ส่งแบบสอบถาม"):
            st.success("ส่งข้อมูลเรียบร้อย")
        st.stop()
    elif freq in ("ทุกสัปดาห์", "กิน 4-6 ครั้งต่อเดือน"):
        st.success("ไปยังข้อ 4")
        st.subheader("ข้อ 4: คุณซื้อผลิตภัณฑ์จากที่ไหน? " )
        place = {"Tops","Big C","Lotus","Maxvalu","7-Eleven"}
        p1 = st.segmented_control("สถานที่ซื้อผลิตภัณฑ์ (เลือกได้หลายคำตอบ)", 
                                  place ,
                                  selection_mode="multi")
    
    
    elif freq == "กิน 2-3 ครั้ง / เดือน":
        st.success("ไปยังข้อ 5 ")
        st.subheader("ข้อ 5 : ทำไมคุณถึงกินน้อยลง?")
        reason = st.text_area("ระบุเหตุผล")

if sex == "หญิง" and freq == "กิน 2-3 ครั้ง / เดือน" and reason != "" :
    st.subheader("ข้อ 6 : คุณจัดระดับความชอบ?")
    rank = st.select_slider("ระดับความชอบเต็ม 10 ",
                             options=[str(i) for i in range(1, 11)])

brand = {"ยี่ห้อ A","ยี่ห้อ B","ยี่ห้อ C","ยี่ห้อ D","ยี่ห้อ E","ยี่ห้อ F"}

#ข้อ 7
if freq and (p1 or reason):
    st.subheader("ข้อ 7 : คุณเคยบริโภคยี่ห้ออะไรบ้าง")
    know = st.multiselect(label="ยี่ห้อที่รู้จัก (หลายคำตอบ)",
                      options=list(brand),
                      format_func=lambda x: x)
                      


#ข้อ 8
if know :
    st.subheader("ข้อ 8 : ยี่ห้อที่บริโภคเป็นประจำ")
    alw = st.pills(label="ยี่ห้อเคยกิน (ตอบได้คำตอบเดียว)",
                           options=know,
                           selection_mode="single",
                           format_func=lambda x: x)
    if st.button("ส่งแบบสอบถาม") :
        data = {
            "เพศ" : sex,
            "อายุ": age,
            "ช่วงอายุ": ages,
            "ความถี่": freq,
            "สถานที่ซื้อ": ', '.join(p1),
            "เหตุผล": reason,
            "ความชอบ": rank ,
            "ยี่ห้อที่รู้จัก" :', '.join(know),
            "ยี่ห้อที่ทานประจำ" :alw
        }
        new = pd.DataFrame([data]) 
        csv = "jobtest.csv"
        
        if os.path.exists(csv):
            exist_data = pd.read_csv(csv )
            all_data = pd.concat([exist_data, new], ignore_index=True)
        else:
            all_data = new

        all_data.to_csv(csv, index=False)
    
        if os.path.exists(csv):
            df = pd.read_csv(csv)
            st.info(f"มีผู้ส่งแบบสอบถามแล้วทั้งหมด: **{len(df)}** ครั้ง")

        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label=" ดาวน์โหลดข้อมูล(CSV)",
            data=csv,
            file_name="jobtest.csv",
            mime="text/csv",
        )
