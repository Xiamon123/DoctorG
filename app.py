import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import streamlit.components.v1 as components

# Load the doctor dataset from CSV
doctors_df = pd.read_csv('doctors.csv')

# Load the symptoms and specialist dataset from CSV
symptoms_specialist_df = pd.read_csv('symptoms_specialist.csv')

# Application Frontend
st.title('Doctor Recommendation System')

# Collect user symptoms
selected_symptoms = st.multiselect('Select your symptoms:', symptoms_specialist_df['symptoms'].unique())

# Filter specialist based on selected symptoms
filtered_specialist = symptoms_specialist_df[symptoms_specialist_df['symptoms'].isin(selected_symptoms)]

if filtered_specialist['specialist'].nunique() < 2:
    st.write('Insufficient data to make a recommendation.')
else:
    # Train the classifier
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(filtered_specialist['symptoms'])
    y = filtered_specialist['specialist']
    classifier = LinearSVC()
    classifier.fit(X, y)

    # Predict specialist for the selected symptoms
    X_user = vectorizer.transform(selected_symptoms)
    predicted_specialist = classifier.predict(X_user)

    # Filter doctors based on predicted specialist
    filtered_doctors = doctors_df[doctors_df['Specialty'].isin(predicted_specialist)]

    # Display recommended doctors
    if not filtered_doctors.empty:
        st.subheader('Recommended Doctors:')
        for index, row in filtered_doctors.iterrows():
            st.write(f"### {row['Name']}")
            st.write(f"**Specialty:** {row['Specialty']}")
            st.write(f"**Location:** {row['Location']}")
            st.write(f"**Experience:** {row['Experience']} years")
            st.write("---")
    else:
        st.write('No doctors found for the selected symptoms.')

# Add CSS for styling
components.html('''
<style>
h1, h2, h3, h4, h5, h6 {
    color: #303f9f !important;
    font-family: 'Arial', sans-serif;
}

body {
    padding: 20px;
}

.card {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
}

.card-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}

.card-content {
    font-size: 16px;
    margin-bottom: 10px;
}

hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 20px 0;
}

</style>
''')
