# 2020 population estimates https://uidai.gov.in/images/state-wise-aadhaar-saturation.pdf
# violent crime stats https://ncrb.gov.in/sites/default/files/crime_in_india_table_additional_table_chapter_reports/TABLE%201C.2.pdf
import streamlit as st
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt

df = pd.read_excel(r"data.xlsx")

india = gp.read_file("India_State_Boundary.shp")

india.replace({
    "Andaman & Nicobar": "A&N Islands",
    "Jammu and Kashmir": "Jammu & Kashmir",
    "Telengana": "Telangana",
    "Tamilnadu": "Tamil Nadu",
    "Chhattishgarh": "Chhattisgarh"
}, inplace = True)

india.rename(columns = {
    "Name": "feature.id"
}, inplace = True)

df.rename(columns = {
    "State/UT": "feature.id"
}, inplace = True)

headers = list(df.columns[1:-1])
states = df.iloc[:, 0]

combo_df = pd.merge(india, df, left_on = "feature.id", right_on = "feature.id")
combo_df = combo_df.drop(['Type'], axis = 1)
combo_df = combo_df.set_index('feature.id')

with st.sidebar:
    st.title("India Violent Crimes 2020")
    header = st.selectbox('Select Crime', headers)
    chart_type = st.selectbox('Incidence Rate or Absolute', ['Absolute', 'Incidence'])
    status = st.button("Draw Chart")
    st.markdown("The crime data has been obtained from [National Crime Records Bureau](https://ncrb.gov.in/sites/default/files/crime_in_india_table_additional_table_chapter_reports/TABLE%201C.2.pdf) and the population figures of 2020 has been estimated from [UIDAI data](https://uidai.gov.in/images/state-wise-aadhaar-saturation.pdf) from their official website.")
    st.markdown("The absolute number indicates the total number of crimes committed in a particular state, whereas the incidence rate shows the number of crimes committed per 10,000 people in that particular state.")

if status:
    if chart_type == "Absolute":
        st.header("Absolute Number of Crimes Committed")
        col1, col2 = st.columns([7, 5])
        
        with col1:
            st.subheader("Map of India")
            fig, ax = plt.subplots(1)
            combo_df.plot(column=header, cmap='RdYlGn_r', linewidth=1, ax=ax, edgecolor='0.9', legend = True)
            ax.axis('off')
            st.pyplot(fig)
        
        with col2:
            st.subheader("Top 5 States")
            top_5 = combo_df[header].nlargest(5)
            tdf = pd.DataFrame({'State':top_5.index, 'Count':top_5.values})
            tdf.index += 1
            st.dataframe(tdf)

            st.subheader("Bottom 5 States")
            bottom_5 = combo_df[header].nsmallest(5)
            tdf = pd.DataFrame({'State':bottom_5.index, 'Count':bottom_5.values})
            tdf.index += 1
            st.dataframe(tdf)
    
    elif chart_type == "Incidence":
        st.header("Incidence Rate per 10,000 people")
        col1, col2 = st.columns([7, 5])
        
        combo_df = combo_df.iloc[:, 1:-1].divide(combo_df.iloc[:,-1], axis = 'rows')*10000
        com_df = pd.merge(india, combo_df, left_on = "feature.id", right_on = "feature.id")
        com_df = com_df.drop(['Type'], axis = 1)
        com_df = com_df.set_index('feature.id')

        with col1:
            st.subheader("Map of India")
            fig, ax = plt.subplots(1)
            com_df.plot(column=header, cmap='RdYlGn_r', linewidth=1, ax=ax, edgecolor='0.9', legend = True)
            ax.axis('off')
            st.pyplot(fig)
        
        with col2:
            st.subheader("Top 5 States")
            top_5 = com_df[header].nlargest(5)
            tdf = pd.DataFrame({'State':top_5.index, 'Rate':top_5.values})
            tdf.index += 1
            st.dataframe(tdf)

            st.subheader("Bottom 5 States")
            bottom_5 = com_df[header].nsmallest(5)
            tdf = pd.DataFrame({'State':bottom_5.index, 'Rate':bottom_5.values})
            tdf.index += 1
            st.dataframe(tdf)        