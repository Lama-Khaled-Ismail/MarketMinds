from collections import defaultdict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from mongo.database import english_collection, ar_collection
import oauth2
from postgres import models, schemas
from postgres.database import get_db
import pandas as pd
from lifespan import ml_models
from sqlalchemy.orm import Session
from mongo import models as mongo_models
from word_count import extract_top_adjectives, format_result





router = APIRouter(
    prefix="/predict",
    tags=["prediction"],
)

features = ['text']


@router.get("/en")
def predict():
    
    # Predict the sentiment
    prediction = ml_models["en"].predict(["The pizza was very cold"])

    # Print the sentiment
    sentiment_label = "positive" if prediction[0] == 1 else "negative"
    
    
    return{"score":sentiment_label}


@router.post("/{lang}/{brand_name}/{platform}", status_code=status.HTTP_201_CREATED, response_model=schemas.AnalysisOut)
def predict_en(lang: str, brand_name: str, platform: str, db:Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):

        
        brand = db.query(models.Brand).filter(models.Brand.name==brand_name).first()
        if not brand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
        
        if brand.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        if lang == 'en':
            collection = english_collection
        elif lang == 'ar':
            collection = ar_collection
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported language")
        # Fetch data from MongoDB
        
        documents = list(collection.find({ 'brand_id': brand.id ,'platform': platform},{'_id': 1,'text': 1}))
        
        if not documents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found ")

        # Convert MongoDB documents to DataFrame
        df = pd.DataFrame(documents)
        
        # Ensure the DataFrame has the required features
        if not all(feature in df.columns for feature in features):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Input data must contain the following features: {features}")

        # Prepare the data for prediction
        X_batch = df['text']
        #print(X_batch.shape)
        #print(type(X_batch))

        # Make predictions
        predictions = ml_models[lang].predict(X_batch)
        
        positive = 0
        negative = 0 
        num_reviews = X_batch.shape[0]
        
        count_sample_negative = 0
        count_sample_positive = 0
        sample_reviews = []
        # Update MongoDB documents with predictions
        for doc, prediction in zip(documents, predictions):
            if prediction == 1:
                positive += 1
                if count_sample_positive < 5 :
                    sample_reviews.append(
                        models.Review(text=doc['text'],score=prediction)
                    )
                    count_sample_positive += 1
                
                
            else:
                negative += 1
                if count_sample_negative < 5 :
                    sample_reviews.append(
                        models.Review(text=doc['text'],score=prediction)
                    )
                    count_sample_negative += 1
                
            collection.update_one({'_id':  doc['_id']}, {'$set': {'score': int(prediction)}})
            
        # add analysis to db
        new_analysis = models.Analysis(
            brand_id=brand.id,
            positive=positive,
            negative=negative,
            num_reviews=num_reviews,
            platform=platform,
            language=lang
        )
        
        new_analysis.reviews.extend(sample_reviews)
        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)
        return new_analysis

    
@router.get("/associated-words/{lang}/{brand_name}")
def associated_words(lang: str,brand_name: str, db:Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
   
        brand = db.query(models.Brand).filter(models.Brand.name==brand_name).first()
        
        if not brand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
        
        if brand.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
        if lang == 'en':
            collection = english_collection
        elif lang == 'ar':
            collection = ar_collection
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported language")
          
        reviews = list(collection.find({ 'brand_id': brand.id},{'text': 1,'platform': 1}))
        reviews_by_platform = reviews_by_platform = {platform.value: [] for platform in mongo_models.Platform}
        
        for review in reviews:
            platform = review['platform']
            text = review['text']
        
            reviews_by_platform[platform].append(text)
        
        top_adjectives, review_dict = extract_top_adjectives(reviews_by_platform)
        formatted_result = format_result(top_adjectives, review_dict)
        return formatted_result
   
    


@router.get("/{lang}/{brand_name}/{platform}")
def analysis_by_month(lang: str, brand_name: str, platform: str, db:Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    
        brand = db.query(models.Brand).filter(models.Brand.name==brand_name).first()
        if not brand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
        
        if brand.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        # Fetch data from MongoDB
        if lang == 'en':
            collection = english_collection
        elif lang == 'ar':
            collection = ar_collection
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported language")
            
        documents = list(collection.find({ 'brand_id': brand.id ,'platform': platform},{'_id': 1,'text': 1, 'time': 1}))
        
        if not documents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found ")

        # Convert MongoDB documents to DataFrame
        df = pd.DataFrame(documents)
        
        # Ensure the DataFrame has the required features
        if not all(feature in df.columns for feature in features):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Input data must contain the following features: {features}")


        # Prepare the data for prediction
        X_batch = df['text']
       

        # Make predictions
        predictions = ml_models[lang].predict(X_batch)
        
        monthly_summary = defaultdict(lambda: {"positive": 0, "negative": 0})
        # Update MongoDB documents with predictions
        for doc, prediction in zip(documents, predictions):
            date_obj = datetime.strptime(doc["time"], "%d %B %Y")
            month_str = date_obj.strftime("%B")
            
            if prediction == 1:
                monthly_summary[month_str]["positive"] += 1
            else:
                monthly_summary[month_str]["negative"] += 1
               
                
            collection.update_one({'_id':  doc['_id']}, {'$set': {'score': int(prediction)}})
            
        return monthly_summary
    
 


    