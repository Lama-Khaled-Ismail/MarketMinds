import dill
from needed_fucntions import text_data_cleaning


with open('model.pkl', 'rb') as file:
    model = dill.load(file)


# Predict the sentiment
prediction = model.predict(["The pizza was very cold"])

# Print the sentiment
sentiment_label = "positive" if prediction[0] == 1 else "negative"
print(f"The sentiment of the text is: {sentiment_label}")