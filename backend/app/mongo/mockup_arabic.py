import pandas as pd
from database import ar_collection
from models import Review, Platform


df = pd.read_csv('D:/Graduation Project/GP/Web Scrapper/ar_reviews.csv')



data = []
for index, row in df.iterrows():
    restuarnt_name = row.get('Restaurant')
    if restuarnt_name == 'El Haty':
        # Extract the value from 'feature1' column
        feature1_value = row.get('Review')
        feature2_value = row.get('Date')

        # Create an instance of YourModel with feature1 and defaults
        instance = Review(text=feature1_value,brand_id=6,platform=Platform.TWITTER.value,time=feature2_value)
        
        document = instance.model_dump()

        # Convert Pydantic model to dictionary and insert into MongoDB
    
        data.append(document)
    
ar_collection.insert_many(data)   

print("Insertion complete.")
    
    
