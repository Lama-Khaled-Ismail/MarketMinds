from needed_ar import clean_arabic_text
import dill

with open('ar_model.pkl', 'rb') as file:
    model = dill.load(file)


# Predict the sentiment
prediction = model.predict(["اول مرة يطلع ورق العنب فوق الممتاز وملفوف بشكل كويس ومهندم كل مرة بيبقي مبهدل ومفكوك"])

# Print the sentiment
sentiment_label = "positive" if prediction[0] == 1 else "negative"
print(f"The sentiment of the text is: {sentiment_label}")