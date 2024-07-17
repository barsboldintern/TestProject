from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

# Load the trained model
model = joblib.load('../scraping/model.pkl')

# Load the encoders from the files
ordencode = joblib.load('../scraping//ordinal_encoder.pkl')

app = Flask(__name__)

categorization_df = pd.read_csv('../scraping/datas/categorization.csv')

expected_columns = ['Тагт', 'Гараж', 'Талбай', 'Хэдэн давхарт', 'Лизингээр авах боломж',
                    'Цонхны тоо', 'Барилгын явц', 'Цонх-Бусад', 'Цонх-Вакум',
                    'Дүүрэг-УБ  Багануур', 'Дүүрэг-УБ  Баянгол', 'Дүүрэг-УБ  Баянзүрх',
                    'Дүүрэг-УБ  Налайх', 'Дүүрэг-УБ  Сонгинохайрхан',
                    'Дүүрэг-УБ  Сүхбаатар', 'Дүүрэг-УБ  Хан-Уул', 'Дүүрэг-УБ  Чингэлтэй',
                    'Хаалга-Бусад', 'Хаалга-Бүргэд', 'Хаалга-Төмөр', 'Шал-Бусад',
                    'Шал-Паркет', 'Category-High', 'Category-Low', 'Category-Medium',
                    'totalfloorlog', 'agelog', 'Specific_Location_Encoded']

@app.route('/')
def home():
    return render_template('web.html')

@app.route('/predict', methods=['POST'])
def pred():
    data = request.json
    print('Received data:', data)
    data['Барилгын_давхар'] = pd.to_numeric(data['Барилгын_давхар'], errors='coerce')
    data['Нас'] = pd.to_numeric(data['Нас'], errors='coerce')


    # Categorize district based on the precomputed categories
    hayag = data['Хаяг']


    # Categorize district based on the precomputed categories
    category_row = categorization_df[categorization_df['хаяг'] == hayag]
    
    if category_row.empty:
        return jsonify({'error': 'No category found for the specified хаяг'}), 400
    
    category = category_row['Category'].values[0]

    # Mapping dictionary for yes/no values
    yes_no_mapping = {'yes': 1, 'no': 0}
    
    # Convert yes/no values to 0/1
    tagt_value = yes_no_mapping[data['тагт'].lower()]
    garaj_value = yes_no_mapping[data['гараж'].lower()]
    lizing_value = yes_no_mapping[data['Лизинг'].lower()]
    yvts_value = yes_no_mapping[data['Барилгын_явц'].lower()]
    
    input_data = pd.DataFrame([{
        'Тагт': tagt_value,
        'Гараж': garaj_value,
        'Талбай': data['Талбай'],
        'Хэдэн давхарт': data['Хэдэн_давхарт'],
        'Лизингээр авах боломж': lizing_value,
        'Цонхны тоо': data['Цонхны_тоо'],
        'Барилгын давхар': data['Барилгын_давхар'],
        'Цонх': data['Цонх'],
        'Дүүрэг': data['Дүүрэг'],
        'Хаалга': data['Хаалга'],
        'Шал': data['Шал'],
        'Category': category,
        'totalfloorlog': np.log(data['Барилгын_давхар']),
        'agelog': np.log(data['Нас'] + 2),
        'Барилгын явц': yvts_value,
        'Specific_Location_Encoded': ordencode.transform([[data['Хаяг']]])[0][0]
    }])
    print(input_data)
    # One-hot encode the categorical features
    input_data_encoded = pd.get_dummies(input_data, columns=['Цонх', 'Дүүрэг', 'Хаалга', 'Шал', 'Category'])

    # Ensure all expected columns are present
    for col in expected_columns:
        if col not in input_data_encoded.columns:
            input_data_encoded[col] = 0

    # Reorder the columns to match the training data
    input_data_encoded = input_data_encoded[expected_columns]

    # Make a prediction
    prediction = model.predict(input_data_encoded)

    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
