from google_play_scraper import app, reviews #package library untuk scarape data review
import pandas as pd #mengolah data
from textblob import TextBlob #untuk Mengolahkata

# Download the NLTK corpora untuk menganalisis Sentiment dan support Textblob
import nltk
nltk.download('punkt')

# Specify the app package name
app_package = 'com.zhiliaoapp.musically' # untuk mendapatkan package namenya ikutilah ling berikut ini
# https://www.techmesto.com/find-android-app-package-name/

# Get app details
app_info = app(app_package)

# Get reviews for the app
result, continuation_token = reviews(
    app_package,
    lang='en',
    country='us',
    count=100,
)

# Create a DataFrame to store the reviews
columns = ['Rating', 'Review', 'Author', 'Date', 'Sentiment']
data = []

# Populate the DataFrame with review data and sentiment analysis
for review in result:
    # Perform sentiment analysis using TextBlob
    analysis = TextBlob(review['content'])
    sentiment = 'Positive' if analysis.sentiment.polarity > 0 else 'Negative' if analysis.sentiment.polarity < 0 else 'Neutral'

    row_data = [
        review['score'],
        review['content'],
        review['userName'],
        review['at'],
        sentiment,
    ]
    data.append(row_data)

df = pd.DataFrame(data, columns=columns)

# Save the DataFrame to a CSV file
csv_filename = f'{app_info["title"]}_reviews_with_sentiment.csv'
df.to_csv(csv_filename, index=False)

print(f'DataFrame with sentiment analysis saved to {csv_filename}')
