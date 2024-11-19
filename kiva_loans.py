import pandas as pd
import sweetviz as sv
import seaborn as sns
import dtale
import matplotlib as plt
import numpy as np


kiva_loans_data = pd.read_csv("C:/Users/Shuhrat/VsCode/ISA_Python/assigment3/DataRaw/kiva_loans.csv")
print(kiva_loans_data.info())

# Initial inspect kiva_loans.scv dataset with Sweetviz, view feature properties, 
# perform numerical and statistical single-factor analysis, and so on.
report_sv = sv.analyze(kiva_loans_data)
report_sv.show_html()

# Filter the data for 'agriculture' sector
agriculture_data = kiva_loans_data[kiva_loans_data["sector"].str.contains('Agriculture', case=False, na=False)]

agriculture_data = pd.read_csv("C:/Users/Shuhrat/VsCode/ISA_Python/agriculture_data.csv")


# Initial inspect kiva_loans.scv dataset with Sweetviz, view feature properties, 
# perform numerical and statistical single-factor analysis, and so on.
#report_sv = sv.analyze(agriculture_data)
#report_sv.show_html()

# Extract the first gender
agriculture_data['first_gender'] = agriculture_data['borrower_genders'].str.split(',').str[0].str.strip()

# Count the number of words in the 'borrower_genders' column
agriculture_data['gender_word_count'] = agriculture_data['borrower_genders'].str.split(',').apply(
    lambda x: len(x) if isinstance(x, list) else 0
)

# Convert 'male' to 0 and 'female' to 1 in the 'first_gender' column
agriculture_data['gender_indicator'] = agriculture_data['first_gender'].map({'male': 0, 'female': 1})

# Drop unnecessary columns
agriculture_data = agriculture_data.drop(columns=['borrower_genders', 'first_gender'])

agriculture_data['gender_indicator'] = agriculture_data['gender_indicator'].fillna(-1).astype(int)

data = agriculture_data.dropna(subset=['gender_indicator'])

print(agriculture_data['gender_indicator'].isnull().sum())

# 
agriculture_data['gender_indicator'] = agriculture_data['gender_indicator'].astype(int)
date_columns = ['posted_time', 'disbursed_time', 'funded_time', 'date']
for col in date_columns:
    agriculture_data[col] = pd.to_datetime(agriculture_data[col], errors='coerce')


# Fill missing values
agriculture_data['tags'] = agriculture_data['tags'].fillna('No Tags')  # Replace missing tags
agriculture_data['tags'] = agriculture_data['tags'].replace('No Tags', np.nan)
agriculture_data['partner_id'] = agriculture_data['partner_id'].fillna(0)  # Replace missing partner_id with 0

# Normalize text columns
agriculture_data['activity'] = agriculture_data['activity'].str.strip()
agriculture_data['sector'] = agriculture_data['sector'].str.strip()

# Convert date columns to datetime
date_columns = ['posted_time', 'disbursed_time', 'funded_time', 'date']
for col in date_columns:
    agriculture_data[col] = pd.to_datetime(agriculture_data[col], errors='coerce')

# Add derived columns
# Calculate time to funding (days)
agriculture_data['time_to_funding'] = (agriculture_data['funded_time'] - agriculture_data['posted_time']).dt.days

# Add a loan amount category
agriculture_data['loan_category'] = agriculture_data['loan_amount'].apply(
    lambda x: 'Low' if x <= 200 else 'Medium' if x <= 500 else 'High'
)
# Funding Speed: Days between posted_time and funded_time.Loan and term in years.
agriculture_data['funding_speed'] = (agriculture_data['funded_time'] - agriculture_data['posted_time']).dt.days
agriculture_data['loan_term_years'] = agriculture_data['term_in_months'] / 12

# 5. Remove duplicate rows
agriculture_data = agriculture_data.drop_duplicates()
agriculture_data = agriculture_data.drop(columns=['Unnamed: 0'])
# 6. Check data types and fix any issues
print(agriculture_data.info())

# 7. Save the cleaned data
cleaned_file_path = 'cleaned_dataset.csv'
agriculture_data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned dataset saved to {cleaned_file_path}")

cleaned_data = pd.read_csv('cleaned_dataset.csv')
cleaned_data.head()
