import streamlit as st
import json
import csv
import pandas as pd
from PIL import Image
import numpy as np
import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit.components.v1 import html
import matplotlib.pyplot as plt


filename = "registered_users.csv"
data_feedback = pd.read_csv("Feedback Formular.csv",encoding='utf-8-sig')




# CSV-Datei im Lese-Modus öffnen
with open('Parameter_test.csv', 'r') as f:
    reader = csv.reader(f,delimiter=';')
    data = [row for row in reader]
    


        
#Json-Datei im Lese-Modus öffnen
#with open('data.json', 'r') as f:
 #   data = json.load(f)

# json-Datei im Lese-Modus öffnen
#with open('Parameter_test.json', 'r') as f:
 #   reader = csv.reader(f, delimiter=';')
  #  data = [row for row in reader]

# CSS-Code für die Farbe
css = """
<style>
body {
    background-color: #F5DEED; /* Hintergrundfarbe */
}

h1 {
    color: #d1b8c8; /* Textfarbe */
}
</style>
"""

global username
# CSS-Code in der Streamlit-App anzeigen
st.markdown(css, unsafe_allow_html=True)

# Benutzername und Passwort erstellen
correct_username = {"zhaw": "1234", "adrian": "aaaa", "samuel": "ssss", "sangi": "1111", "achu": "4444"}


# Login Seite
def login():
    global username 
    
    st.write("# Q-Check")
    st.write(
    "<span style='color: grey'><i>discovering solutions, delivering results</i></span>",
    unsafe_allow_html=True,
    )

    login_option = st.radio("", ("Login", "Sign up"))

 

    if login_option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        
        if login_button:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username:
                        if row[1] == password:
                            st.success("Login successful!")
                            st.session_state["logged_in"] = True
                            welcome(username) 
                            st.experimental_rerun()
                        else:
                            st.error("Incorrect password")
                        break


    elif login_option == "Sign up":
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        signup_button = st.button("Sign up")
        if signup_button:
            if new_password == confirm_password:
                st.success("Sign up successful! Please log in.")
                correct_username[new_username] = new_password
                with open(filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([new_username, new_password])
            else:
                st.error("Passwords do not match")
 


# Seite für Willkommensnachricht nach erfolgreicher Anmeldung
def welcome(username):
    
    # Sidebar mit Optionen
    st.sidebar.write("## Menu")
    options = ["Analytics", "Videos", "Feedback", "About Us"]
    choice = st.sidebar.selectbox("Select Option", options)
    
    # Logout-Button
    logout_button = st.sidebar.button("Logout")

    if logout_button:
        st.session_state["logged_in"] = False
        st.experimental_rerun()
    
    
    # Willkommensnachricht anzeigen
    if "username" in st.session_state:
        st.write("Hello ", st.session_state['username'], "!")
    else:
        st.write("Hello!")
        
        

    if choice == "Analytics":
        
        st.write("# Welcome to Q-Check!")
        #Schriftart, erstes Wort krusiv
        st.markdown(""" <h2 style='font-size: 20px;'><em>Qualitycheck</em> is an open-source app framework built specifically to check quality control range in your laboratory.</h2> """, unsafe_allow_html=True)

        #verschiedene Tabs horizontal
        tab1, tab2, tab3 = st.tabs(["Hematogram II", "Hematogram V", "Shortcut & Definitions"])

        with tab1:
            st.header("Hematogram II")
            st.write("""<h2 style='font-size: 20px;'>Calculations for Quality Control</h2>
                        """, unsafe_allow_html=True)
            st.markdown("<p style='text-align: justify;'><em>Indication:</em> Anemia, infections, intoxications, collagenosis, leukemia and other systemic hematological diseases, malignant tumors, control of therapies, bone marrow depression (radiation, chemotherapy, immunosuppression).</p>", unsafe_allow_html=True)

            # Parameter erstellt
            st.write("Enter values:")
            parameter_options = ['RBC', 'HGB', 'HCT', 'WBC', 'MCH', 'MCHC', 'MCV', 'PLT']
            input1 = st.selectbox("parameter hematogram II", parameter_options, index=0)
            var_mean_val =0.001 #variablen definiert
            var_low_val =0.001
            var_max_val =0.001
            
            search_string = input1
            for item in data:
               if search_string in item[0]: #output (String vergleichen mit array)
                   var_max_val=float((item[1]))
                   var_low_val=float((item[2]))
                   var_mean_val=float((item[3]))
             
            #Print mit 3 Dezimalstellen
            mean_val = st.number_input("company mean hematogram II", value=var_mean_val, step=0.001, format="%.3f")
            low_val = st.number_input("company range low hematogram II", value=var_low_val, step=0.001, format="%.3f")
            max_val = st.number_input("company range high hematogram II", value=var_max_val, step=0.001, format="%.3f")
            
    
            # Calculate the coefficient of variation
            def calculate_value(mean, low):
                result = (mean - low) / 3
                return result

            #Klick Button mit 2 Stellen nach Komma
            if st.button("calculation for Hematogram II"):
                result = calculate_value(mean_val, low_val)
                st.write("The calculated 1s value is:", format(result,".3f"))
                coefficient_of_variation = result / mean_val *100
                st.write("The calculated coefficient of variation is:", format(coefficient_of_variation,".2f") ,"%")
               
            #Bild1 hinzugefügt mit Spruch
            imageDrops = Image.open('bilder/drops.jpg')
            st.image(imageDrops, caption='"Good quality is not what we put into it. It is what the client or customer gets out of it." - Peter Drucker', use_column_width=True)


        with tab2:
            st.header("Hematogram V")
            st.write("""<h2 style='font-size: 20px;'>Calculations for Quality Control</h2>
                       """, unsafe_allow_html=True)
            
            st.markdown("<p style='text-align: justify;'><em>Indication:</em> Anemia, infections, intoxications, collagenosis, leukemia and other systemic hematological diseases, malignant tumors, control of therapies, bone marrow depression (radiation, chemotherapy, immunosuppression).</p>", unsafe_allow_html=True)

            #Paramter erstellt für tab 2
            st.write("Enter values:")
            parameter_options = ['RBC', 'EO', 'HGB', 'HCT', 'WBC', 'MCH', 'MCHC', 'MCV', 'MONO', 'NEUT', 'PLT']
            input2 = st.selectbox("parameter hematogram V ", parameter_options, index=0)
            var_mean_val =0.001 #variablen definiert 
            var_low_val =0.001
            var_max_val =0.001
            
            search_string = input2
            for item in data:
               if search_string in item[0]: #output (String vergleichen mit array)
                   var_max_val=float((item[1]))
                   var_low_val=float((item[2]))
                   var_mean_val=float((item[3]))
            #Print
            mean_val2 = st.number_input("company mean hematogram V", value=var_mean_val, step=0.001, format="%.3f")
            low_val2 = st.number_input("company range low hematogram V", value=var_low_val, step=0.001, format="%.3f")
            input4 = st.number_input("company range high hematogram V", value=var_max_val, step=0.001, format="%.3f")
            
            # Calculate the coefficient of variation 
          
            def calculate_value(mean, low):
                result = (mean - low) / 3
                return result
            
            #Klick button
            if st.button("calculation for Hematogram V"):
                result = calculate_value(mean_val2, low_val2)
                st.write("The calculated 1s value is:", format(result,".3f"))
                coefficient_of_variation = result / mean_val2 *100
                st.write("The calculated coefficient of variation is:", format(coefficient_of_variation,".2f") ,"%")
                
            #Bild 2 hinzugefügt
            imageRed = Image.open('bilder/red.jpg')
            st.image(imageRed, caption='"Quality control is not a department, it is everyones job." - W. Edwards Deming', use_column_width=True)
            
            
        
        #defintion tab
        with tab3:
           st.write('<style>h2 {font-size: 28px; font-weight: bold, sans-serif;}</style>', unsafe_allow_html=True)
           st.header('Shortcuts & Definitions')
           
           # Pandas DataFrame für die Definitionen erstellt -> Tabelle
           df_definitions = pd.DataFrame({
               'Shortcut': ['BASO', 'RBC', 'EO', 'HGB', 'HCT', 'WBC', 'LYMPH', 'MCH', 'MCHC', 'MCV', 'MONO', 'NEUT', 'PLT'],
               'Full Name': ['Basophils', 'Red Blood Cells', 'Eosinophils', 'Hemoglobin', 'Hematocrit', 'White Blood Cells', 'Lymphocytes', 'Mean Corpuscular Hemoglobin', 'Mean Corpuscular Hemoglobin Concentration', 'Mean Corpuscular Volume', 'Monocytes', 'Neutrophils', 'Platelets'],
               'Definition': [
                   'Basophils are a type of white blood cell that works closely with your immune system to defend your body from allergens, pathogens and parasites. Basophils release enzymes to improve blood flow and prevent blood clots.',
                   'A type of blood cell that is made in the bone marrow and found in the blood. Red blood cells contain a protein called hemoglobin, which carries oxygen from the lungs to all parts of the body.',
                   'Eosinophils are one of several white blood cells that support your immune system. Sometimes, certain medical conditions and medications cause high eosinophil levels.',
                   'Hemoglobin is the iron containing oxygen-transport metalloprotein present in red blood cells of almost all vertebrates as well as the tissues of some invertebrates.',
                   'The amount of whole blood that is made up of red blood cells.',
                   'White blood cells are part of the body\'s immune system. They help the body fight infection and other diseases. Types of white blood cells are granulocytes (neutrophils, eosinophils, and basophils), monocytes, and lymphocytes (T cells and B cells).',
                   'Lymphocytes are a type of white blood cell. They help your body\'s immune system fight cancer and foreign viruses and bacteria.',
                   'Mean Corpuscular Hemoglobin is a calculation of the average amount of hemoglobin contained in each of a person\'s red blood cells.',
                   'Mean corpuscular hemoglobin concentration is a measurement of the average amount of hemoglobin in a single red blood cell as it relates to the volume of the cell.',
                   'A mean erythrocyte single-volume blood test measures the average size of your red blood cells.',
                   'Monocytes are a type of white blood cell in your immune system. Monocytes turn into macrophage or dendritic cells when an invading germ or bacteria enters your body. The cells either kill the invader or alert other blood cells to help destroy it and prevent infection.',
                   'Neutrophils help your immune system fight infections and heal injuries. Neutrophils are the most common type of white blood cell in your body.',
                   'Platelets are the smallest component of your blood that control bleeding. Platelets cluster together to form a clot and prevent bleeding at the site of an injury.'
            
        ]
               
               
    })
    
           def format_definition(definition):
                 return f"<p style='font-size: 16px; text-align: justify;'>{definition}</p>"

           df_definitions['Definition'] = df_definitions['Definition'].apply(format_definition)

           st.write(df_definitions.to_html(escape=False, index=False), unsafe_allow_html=True)       
          
         

    #Videos tab, Schriftart und Grösse definiert
    if choice == "Videos":
    
        st.write('<style>h1{font-size: 36px; font-weight: bold;}</style>', unsafe_allow_html=True)
        st.title('Videos')
       
        # Spalten erstellen
        col1, col2 = st.columns([2, 1])

  # Text in erster Spalte
        with col1:
                st.markdown(
    """
    <p style='font-size: 18px; text-align: justify;'>Here you will find a vast collection of instructional videos to help you acquire new skills and expand your knowledge in various areas. 
    Our goal is to make education accessible and enjoyable. We believe in lifelong learning for all, regardless of constraints like time, location, or financial resources.
    With our videos, you can learn at your own pace and choose topics that interest you. Our content is created by experienced professionals and experts, ensuring 
    high-quality and easy-to-understand material. Whether you want to enhance your professional skills, explore new hobbies, or broaden your knowledge, we offer a 
    diverse range of topics. Our user-friendly interface allows you to browse videos by category or search for specific topics. We regularly update our content to 
    keep you informed with the latest knowledge. Learning should be informative and entertaining, so we focus on engaging presentation and interactive elements. 
    Join us in this exciting educational journey to discover new horizons, expand your knowledge, and ignite your passions. The possibilities are limitless, and
    we are here to support you. Ready to get started?
    </p>
    """, unsafe_allow_html=True)

  # Bild in zweiter Spalte
        with col2:
      # Bild3 hinzugefügt mit Spruch
              imageLab = Image.open('bilder/lab.jpg')
              st.image(imageLab, caption='"Learning never exhausts the mind." - Leonardo da Vinci', use_column_width=True)

        # Read more Button erstellt
        read_more = st.button('VIDEOS...')

        if read_more:
            # ganzer Text wird angezeigt, wenn man es klickt
            st.write()
            
            # Pfad zum vorhandenen Video
            video_path = "videos/CRP.mp4"
            video_file = open(video_path, "rb")
            save_bytes = video_file.read()
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)
           
            # Pfad zum vorhandenen Video
            video_path = "videos/hematology.mp4"
            video_file = open(video_path, "rb")
            save_bytes = video_file.read()
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)

            
#Feedback tab, Schriftart und Grösse definiert
    if choice == "Feedback":
        tab1, tab2 = st.tabs(["Feedback", "Feedback Graphic"])
        
        with tab1:

            st.write('<style>h1{font-size: 36px; font-weight: bold;}</style>', unsafe_allow_html=True)
            st.title('Feedback')
            st.write("<p style='font-size: 30px; color: grey; text-decoration: none;'>Welcome to our feedback page!</p>", unsafe_allow_html=True)
            st.markdown(
    """
    <p style='font-size: 20px; text-align: justify;'>
    We are delighted to have you here and appreciate your valuable feedback. Your opinion is of great importance to us as it helps us continuously improve our services to meet your expectations.
    This feedback page provides you with an opportunity to share your thoughts, suggestions, and comments with us. Whether you have praise, constructive criticism, improvement ideas, or questions, we are eager to hear your feedback.
    We firmly believe that feedback is a crucial component of our growth. It enables us to address the needs and desires of our customers and enhance your experiences with our services.
    Your feedback is not only welcome but also taken seriously. We will carefully review each response and utilize them to implement positive changes and enhance our performance.
    We would like to express our sincere gratitude for taking the time to share your feedback with us. Together, we can contribute to making your experiences with our company even better.
    We look forward to receiving your feedback and are excited to hear your impressions! 
    Yours sincerely, Q-Check Team
    </p>
    """, unsafe_allow_html=True)



        #Bild3 hinzugefügt mit Spruch
            imageabout = Image.open('bilder/feedback.jpg')
            st.image(imageabout, caption='"Feedback is the breakfast of champions."', use_column_width=True)

            st.write("""<h2 style='font-size: 20px; color: grey;'>This section is still in progress!</h2>
                   """, unsafe_allow_html=True)
            st.write("""<h2 style='font-size: 20px; color: #d1b8c8; font-style: italic;'>-Team Q-Check </h2>
                          """, unsafe_allow_html=True)

            email = st.text_input("Please enter your email address:")
            feedback = st.text_area("Please enter your feedback:", "")

            if st.button("Submit Feedback"):
        # E-Mail-Einstellungen
                # E-Mail settings
                sender_email = email
                sender_password = 'qcheckHAM'
                receiver_email = 'qcheck.labham@gmail.com'

            # Send the email
                success = send_email(sender_email, sender_password, receiver_email, "Feedback", feedback)

                if success:
                    st.write("Thank you for your feedback! Your feedback has been successfully submitted.")

        with tab2:
            st.title('Feedback Graphic')
            st.write("""<h2 style='font-size: 20px; color: grey;'>This page is temporarly progress, we will be back soon!</h2>
                   """, unsafe_allow_html=True)
            st.write("""<h2 style='font-size: 20px; color: #d1b8c8; font-style: italic;'>-Team Q-Check </h2>
                          """, unsafe_allow_html=True)
        
            
            # Balkendiagramm erstellen
            fig, ax = plt.subplots(figsize=(8, 6))
            #data_feedback["Wie leicht war es für Sie, sich mit der App vertraut zu machen?"].value_counts().sort_index().plot(kind="bar", ax=ax)

            # Diagramm beschriften
            plt.title("Benutzerfreundlichkeit der App")
            plt.xlabel("Bewertung")
            plt.ylabel("Anzahl der Bewertungen")

            # Diagramm im Streamlit anzeigen
            st.pyplot(fig)
        
            x = ['A', 'B', 'C', 'D', 'E']
            y = [10, 7, 5, 3, 1]

        
        




    #About us tab, Schriftart und Grösse definiert
    if choice == "About Us":
        tab1, tab2, tab3 = st.tabs(["About Us", "Web Developer", "Contact"])

        with tab1:
            
            st.write('<style>h1{font-size: 36px; font-weight: bold;}</style>', unsafe_allow_html=True)
            st.title('Who are we?')
            st.write("<p style='font-size: 30px; color: grey; text-decoration: none; text-align: justify;'>discovering solutions, delivering results</p>", unsafe_allow_html=True)

            st.markdown(
 """
<p style='font-size: 20px; text-align: justify;'>Welcome to our hematology quality control website, where we provide comprehensive solutions for ensuring accurate and reliable results in your hematology laboratory. 
Our team of experts has years of experience in the field, and we understand the importance of quality control in providing the best possible care to patients. 
We offer a range of products and services, including proficiency testing, validation, and training, all designed to help you achieve and maintain the highest standards of quality control in hematology. 
Our focus on quality control means that you can trust in the accuracy and precision of your results, enabling you to provide the highest standard of care to your patients.
</p>
<p style='font-size: 20px; text-align: justify;'>Visit our website to learn more about our services, and let us help you optimize your hematology laboratory's performance. Our team is here to support you with any additional information or help you require.</p>
""", unsafe_allow_html=True)


            #Bild3 hinzugefügt mit Spruch
            imageabout = Image.open('bilder/about.jpg')
            st.image(imageabout, caption='"The science of today is the technology of tomorrow." - Edward Teller', use_column_width=True)
    

            # Text Personas
            long_text = """
        The app was created for Nila Walker. Nila is a 32-year-old woman and works as a biomedical laboratory 
        diagnostician at Roche. Nila has a lot of responsibilities in the company, so she doesn't have time to recalculate 
        the range of norm values ​​for the controls with each new lot number. Due to the stress, it has also happened that she entered the range 
        values ​​incorrectly. This was discovered when the controls were repeatedly out of the norm.
        That's why we decided to make Nila's everyday work a little easier and design an app that 
        calculates the standard values ​​​​for quality control.
        """
        
            # Read more Button erstellt
            read_more = st.button('How it all started...')

            if read_more:
    # ganzer Text wird angezeigt, wenn man es klickt
                st.markdown(f"<p style='text-align: justify;'>{long_text}</p>", unsafe_allow_html=True)
            else:
    # wir wollten nicht, dass schon gewisse Wörter vorher erscheinen, deshalb 0
                st.markdown(f"<p style='text-align: justify;'>{long_text[:0]}</p>", unsafe_allow_html=True)

        with tab2:
            
            st.write('<style>h1{font-size: 36px; font-weight: bold;}</style>', unsafe_allow_html=True)
            st.title('Web Developer')
   
            st.markdown(
 """
<p style='font-size: 20px; text-align: justify;'>
Step into the world of web development and unlock limitless possibilities. Our team of skilled web developers is dedicated to creating stunning and functional websites. We specialize in crafting customized web solutions tailored to your unique business needs. From responsive designs to seamless navigation, we ensure an exceptional user experience. Let us bring your vision to life and help you establish a strong online presence. 
</p>
""", unsafe_allow_html=True)


             # Shankavie hinzugefügt mit Spruch
            col1, col2 = st.columns(2)

            with col1:
                image_about = Image.open('bilder/shankavie.jpg')
                st.image(image_about, caption='Shankavie Jeyanathan - Studierende BMLD an der ZHAW Wädenswil', use_column_width=True)

    # Akkshayaa hinzugefügt mit Spruch
            with col2:
                image_about = Image.open('bilder/akkshayaa.jpg')
                st.image(image_about, caption='Akkshayaa Rukunakumar - Studierende BMLD an der ZHAW Wädenswil', use_column_width=True)

        with tab3:
            st.write('<style>h1{font-size: 36px; font-weight: bold;}</style>', unsafe_allow_html=True)
            st.title('Contacts')
            st.markdown(
 """
Thank you for visiting our website! We value your interest and would be delighted to hear from you. Please feel free to get in touch with us using any of the contact methods below:

**Phone:** 

+41 79 726 71 47

**Email:**

jeyansha@students.zhaw.ch

rukunakk@students.zhaw.ch

**Address:**

ZHAW Campus Reidbach (RT), School of Life Sciences und Facility Management<br>
Einsiedlerstrasse 31<br>
8820 Wädenswil

ZHAW Departement Gesundheit<br>
Katharina-Sulzer-Platz 9<br>
8400 Winterthur

""", 
unsafe_allow_html=True)
                


            # Koordinaten für die beiden Punkte
            latitude1 = 47.22714
            longitude1 = 8.66952
            latitude2 = 47.499642
            longitude2 = 8.725621

            # DataFrame mit den beiden Punkten erstellen
            df = pd.DataFrame({'lat': [latitude1, latitude2], 'lon': [longitude1, longitude2]})

            # Schweizer Karte anzeigen und beide Punkte markieren
            st.map(df, zoom=9)

     

        

# Haupt App
def app():
    global username
        
     # abrufen, ob User eingeloggt ist, wenn nicht..
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # User nicht eingeloggt, dann erscheint ->login page
    if not st.session_state["logged_in"]:
        login()
    else:
        # welcome Seite nach erfolgreiche Login 
        username = st.session_state.get("username")  # Get the username from the session state
        welcome(username)
 

def send_email(sender_email, sender_password, receiver_email, subject, message):
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to the email account
        server.login(sender_email, sender_password)

        # Compose the email
        email_message = f"Subject: {subject}\n\n{message}"

        # Send the email
        server.sendmail(sender_email, receiver_email, email_message)

        # Close the connection
        server.quit()

        return True
    except Exception as e:
        #st.error(f"An error occurred while sending the email: {e}")
        return True

# app laufen lassen
if __name__ == '__main__':
	app()

