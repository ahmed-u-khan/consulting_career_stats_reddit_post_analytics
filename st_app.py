import streamlit as st
# from st_aggrid import AgGrid, GridOptionsBuilder
# from st_aggrid.shared import GridUpdateMode
import pandas as pd
import numpy as np
import re
import altair as alt

import streamlit_analytics

streamlit_analytics.start_tracking()


st.set_page_config(
	page_title="stats: r/Consulting salary thread"
	, page_icon=":bar_chart:"
	, layout="wide"
	, initial_sidebar_state="auto"
	, menu_items=None
	)




# def aggrid_interactive_table(df: pd.DataFrame):
#     """Creates an st-aggrid interactive table based on a dataframe.

#     Args:
#         df (pd.DataFrame]): Source dataframe

#     Returns:
#         dict: The selected row
#     """
#     options = GridOptionsBuilder.from_dataframe(
#         df, enableRowGroup=True, enableValue=True, enablePivot=True
#     )

#     options.configure_side_bar()

#     options.configure_selection("single")
#     selection = AgGrid(
#         df,
#         enable_enterprise_modules=True,
#         gridOptions=options.build(),
#         update_mode=GridUpdateMode.MODEL_CHANGED,
#         allow_unsafe_jscode=True,
#     )

#     return selection

df_comments = pd.read_csv (r'comments.csv')

st.markdown (
	"""
	# r/Consulting Canadian Salary Thread
	#### *Aggregating Carrer and Salary info*


	"""
)

df_comments_filtered = df_comments[['author_fullname','body']]

terms = ['1.', '2.', '3.', '4.', '5.', '6.']
df_comments_filtered = df_comments_filtered[df_comments_filtered['body'].str.contains('|'.join(map(re.escape, terms)))]
df_comments_filtered = df_comments_filtered.reset_index(drop=True)



df_comments_filtered[['false_positive_check','first']] = df_comments_filtered['body'].str.split("1.",1,expand=True)
df_comments_filtered[['first','second']] = df_comments_filtered['first'].str.split("2.",1,expand=True)
df_comments_filtered[['second','third']] = df_comments_filtered['second'].str.split("3.",1,expand=True)
df_comments_filtered[['third','fourth']] = df_comments_filtered['third'].str.split("4.",1,expand=True)
df_comments_filtered[['fourth','fifth']] = df_comments_filtered['fourth'].str.split("5.",1,expand=True)
df_comments_filtered[['fifth','sixth']] = df_comments_filtered['fifth'].str.split("6.",1,expand=True)

df_comments_filtered = df_comments_filtered.rename(
	columns=
		{
		  "first": "Firm_Type"
		, "second": "COL_Location"
		, "third": "LOS_Vertical_Practice"
		, "fourth": "Level_at_Firm"
		, "fifth": "Compensation_CAD"
		, "sixth": "Additional_Comments"
		}
	)


df_comments_filtered['false_positive_check']=df_comments_filtered['false_positive_check'].str.strip().replace('',np.nan)
df_comments_filtered = df_comments_filtered[df_comments_filtered['false_positive_check'].isnull()]
df_comments_filtered = df_comments_filtered.reset_index(drop=True)






# df_comments_filtered[['one','two']] = df_comments_filtered['Compensation_CAD'].str.split(";|\+|,|.",1,expand=True)
df_comments_filtered[['Base_Compensation_CAD','Compensation_Bonus_and_Benefits']] = df_comments_filtered['Compensation_CAD'].str.split(",|;|\.|\+",1,expand=True)


# df_comments_filtered['Base_Compensation_CAD'] = df_comments_filtered['Base_Compensation_CAD'].str.extract('(d+)', expand=False)
df_comments_filtered['Base_Compensation_CAD'] = df_comments_filtered.Base_Compensation_CAD.str.replace(r'[^0-9]+', '')
df_comments_filtered['Base_Compensation_CAD'] = df_comments_filtered['Base_Compensation_CAD'].astype(int)

















# cleaning up the filtered dataframe

df_comments_filtered_and_cleaned = pd.DataFrame()

df_comments_filtered_and_cleaned['Firm_Type'] = df_comments_filtered['Firm_Type'].str.upper()
df_comments_filtered_and_cleaned['COL_Location'] = df_comments_filtered['COL_Location'].str.upper()
df_comments_filtered_and_cleaned['LOS_Vertical_Practice'] = df_comments_filtered['LOS_Vertical_Practice'].str.upper()
df_comments_filtered_and_cleaned['Level_at_Firm'] = df_comments_filtered['Level_at_Firm'].str.upper()
df_comments_filtered_and_cleaned['Base_Compensation_CAD'] = df_comments_filtered['Base_Compensation_CAD']


df_comments_filtered_and_cleaned['Firm_Type'] = df_comments_filtered_and_cleaned['Firm_Type'].str.strip()
df_comments_filtered_and_cleaned['COL_Location'] = df_comments_filtered_and_cleaned['COL_Location'].str.strip()
df_comments_filtered_and_cleaned['LOS_Vertical_Practice'] = df_comments_filtered_and_cleaned['LOS_Vertical_Practice'].str.strip()
df_comments_filtered_and_cleaned['Level_at_Firm'] = df_comments_filtered_and_cleaned['Level_at_Firm'].str.strip()


df_comments_filtered_and_cleaned['Firm_Type'][df_comments_filtered_and_cleaned['Firm_Type'].str.contains("BIG")] = "BIG 4"




df_comments_filtered_and_cleaned['Firm_Type'] = df_comments_filtered_and_cleaned['Firm_Type'].str.replace(" ", "_")
df_comments_filtered_and_cleaned['COL_Location'] = df_comments_filtered_and_cleaned['COL_Location'].str.replace(" ", "_")
df_comments_filtered_and_cleaned['LOS_Vertical_Practice'] = df_comments_filtered_and_cleaned['LOS_Vertical_Practice'].str.replace(" ", "_")
df_comments_filtered_and_cleaned['Level_at_Firm'] = df_comments_filtered_and_cleaned['Level_at_Firm'].str.replace(" ", "_")















# making charts 


st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")




col1, col2 = st.columns(2)






with col1:
    st.write("Average per Firm_Type - Table")
    avg_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='Firm_Type', values='Base_Compensation_CAD', aggfunc='mean')
    median_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='Firm_Type', values='Base_Compensation_CAD', aggfunc='median')
    cnt_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='Firm_Type', values='Base_Compensation_CAD', aggfunc='count')
    resultant_one_df = pd.merge(avg_bar_chart_df, cnt_bar_chart_df, on='Firm_Type', how='outer')
    resultant_df = pd.merge(resultant_one_df, median_bar_chart_df, on='Firm_Type', how='outer')
    resultant_df = resultant_df.rename(
	columns=
		{
		  "Base_Compensation_CAD_x": "AVG_Base_Compensation_CAD"
		, "Base_Compensation_CAD_y": "Number_of_Responses"
		, "Base_Compensation_CAD": "MEDIAN_Base_Compensation_CAD"
		}
	)
    # resultant_df = resultant_df.reset_index(level=0)
    # selection = aggrid_interactive_table(df=resultant_df)
    st.dataframe(resultant_df)



with col2:
    st.write("Average per Firm_Type - Chart")
    avg_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='Firm_Type', values='Base_Compensation_CAD', aggfunc='mean').sort_values(by=['Base_Compensation_CAD'], ascending=False)
    st.bar_chart(avg_bar_chart_df)









st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")




col1, col2 = st.columns(2)






with col1:
    st.write("Average per COL_Location - Table")
    avg_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='COL_Location', values='Base_Compensation_CAD', aggfunc='mean')
    median_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='COL_Location', values='Base_Compensation_CAD', aggfunc='median')
    cnt_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='COL_Location', values='Base_Compensation_CAD', aggfunc='count')
    resultant_one_df = pd.merge(avg_bar_chart_df, cnt_bar_chart_df, on='COL_Location', how='outer')
    resultant_df = pd.merge(resultant_one_df, median_bar_chart_df, on='COL_Location', how='outer')
    resultant_df = resultant_df.rename(
	columns=
		{
		  "Base_Compensation_CAD_x": "AVG_Base_Compensation_CAD"
		, "Base_Compensation_CAD_y": "Number_of_Responses"
		, "Base_Compensation_CAD": "MEDIAN_Base_Compensation_CAD"
		}
	)
    # resultant_df = resultant_df.reset_index(level=0)
    # selection = aggrid_interactive_table(df=resultant_df)
    st.dataframe(resultant_df)
    

with col2:
    st.write("Average per COL_Location - Chart")
    avg_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='COL_Location', values='Base_Compensation_CAD', aggfunc='mean').sort_values(by=['Base_Compensation_CAD'], ascending=False)
    st.bar_chart(avg_bar_chart_df)








st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")




col1, col2 = st.columns(2)






with col1:
    st.write("Average per LOS_Vertical_Practice - Table")
    avg_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='LOS_Vertical_Practice', values='Base_Compensation_CAD', aggfunc='mean')
    median_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='LOS_Vertical_Practice', values='Base_Compensation_CAD', aggfunc='median')
    cnt_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='LOS_Vertical_Practice', values='Base_Compensation_CAD', aggfunc='count')
    resultant_one_df = pd.merge(avg_bar_chart_df, cnt_bar_chart_df, on='LOS_Vertical_Practice', how='outer')
    resultant_df = pd.merge(resultant_one_df, median_bar_chart_df, on='LOS_Vertical_Practice', how='outer')
    resultant_df = resultant_df.rename(
	columns=
		{
		  "Base_Compensation_CAD_x": "AVG_Base_Compensation_CAD"
		, "Base_Compensation_CAD_y": "Number_of_Responses"
		, "Base_Compensation_CAD": "MEDIAN_Base_Compensation_CAD"
		}
	)
    # resultant_df = resultant_df.reset_index(level=0)
    # selection = aggrid_interactive_table(df=resultant_df)
    st.dataframe(resultant_df)
    

with col2:
    st.write("Average per LOS_Vertical_Practice - Chart")
    avg_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='LOS_Vertical_Practice', values='Base_Compensation_CAD', aggfunc='mean').sort_values(by=['Base_Compensation_CAD'], ascending=False)
    st.bar_chart(avg_bar_chart_df)









st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")




col1, col2 = st.columns(2)






with col1:
    st.write("Average per Level_at_Firm - Table")
    avg_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='Level_at_Firm', values='Base_Compensation_CAD', aggfunc='mean')
    median_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='Level_at_Firm', values='Base_Compensation_CAD', aggfunc='median')
    cnt_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='Level_at_Firm', values='Base_Compensation_CAD', aggfunc='count')
    resultant_one_df = pd.merge(avg_bar_chart_df, cnt_bar_chart_df, on='Level_at_Firm', how='outer')
    resultant_df = pd.merge(resultant_one_df, median_bar_chart_df, on='Level_at_Firm', how='outer')
    resultant_df = resultant_df.rename(
    columns=
        {
          "Base_Compensation_CAD_x": "AVG_Base_Compensation_CAD"
        , "Base_Compensation_CAD_y": "Number_of_Responses"
        , "Base_Compensation_CAD": "MEDIAN_Base_Compensation_CAD"
        }
    )
    # resultant_df = resultant_df.reset_index(level=0)
    # selection = aggrid_interactive_table(df=resultant_df)
    st.dataframe(resultant_df)
    

with col2:
    st.write("Average per Level_at_Firm - Chart")
    avg_bar_chart_df = df_comments_filtered_and_cleaned.pivot_table(index='Level_at_Firm', values='Base_Compensation_CAD', aggfunc='mean').sort_values(by=['Base_Compensation_CAD'], ascending=False)
    st.bar_chart(avg_bar_chart_df)





st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.caption("cleaned and normalized data")
st.dataframe(df_comments_filtered_and_cleaned)
# selection = aggrid_interactive_table(df=df_comments_filtered_and_cleaned)


st.write("")
st.caption("filtered data")
st.dataframe(df_comments_filtered)
# selection = aggrid_interactive_table(df=df_comments_filtered)


st.write("")
st.caption("Raw Data || Datasource: [link](https://www.reddit.com/r/consulting/comments/wzsuz2/faang_top_tech_mbb_big4_canadian_salary_thread/)")
# selection = aggrid_interactive_table(df=df_comments)
st.dataframe(df_comments)

 

 streamlit_analytics.stop_tracking()
