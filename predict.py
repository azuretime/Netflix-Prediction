from PIL import Image
import numpy as np 
import pandas as pd 
from keras.applications.inception_v3 import preprocess_input
import pickle
import xgboost as xgb
import numpy as np
import yaml
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

config = read_params(params_path)

def url_to_array(file_path): 
    img = Image.open(file_path)
    new_size = (160,240)
    img = img.resize(new_size)
    img_arr = np.asarray(img,dtype="uint8")

    return img_arr

def img_to_embedding(image,model):
    try:
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        img_preprocessed = preprocess_input(image)
        features = model.predict(img_preprocessed)
    except Exception as error: 
        print("An exception occurred")
        print(error)
  
    return features


def getImgFeatures(file_path):
    img_arr = url_to_array(file_path)
    model_path = config["model_webapp_dir"]['image']
    with open(model_path, "rb") as f:
        loaded_model = pickle.load(f)
    features = img_to_embedding(img_arr, loaded_model)
    # Convert array to dataframe and assign column names
    col_name = ['poster_'+str(i+1) for i in range(features.shape[1])]
    features_df = pd.DataFrame(features,columns=col_name)
    # Trim features for popularity task 
    selected_cols_popularity = ['poster_1179','poster_1057','poster_278','poster_1911','poster_711','poster_1074','poster_197','poster_856','poster_1876','poster_236']
    df_popularity = features_df[selected_cols_popularity]
    # Trim features for quality task
    selected_cols_quality = ['poster_1653','poster_143','poster_1594','poster_1592','poster_1070','poster_1623','poster_1011','poster_23','poster_1587','poster_451','poster_1586']
    df_quality = features_df[selected_cols_quality]
    
    return df_popularity,df_quality

def predict_votes(input_list,poster_features): 
    # input_list example: ['Movie', 'Action', 'G', 'director', 'writer', '4', '2'] type, genre, rating , 'director', 'writer', awards received, nominated, poster
    # Load the fitted LabelEncoder
    with open(config["encoder"]['type'], 'rb') as f:
        series_movie_encoder = pickle.load(f)

    with open(config["encoder"]['director'], 'rb') as f:
        director_encoder = pickle.load(f)

    with open(config["encoder"]['rating'], 'rb') as f:
        view_rating_encoder = pickle.load(f)

    with open(config["encoder"]['writer'], 'rb') as f:
        writer_encoder = pickle.load(f)

    series_movie=series_movie_encoder.transform([input_list[0]]).item()
    Awards_nominated_for=int(input_list[6])
    Awards_received=int(input_list[5])
    Director=director_encoder.transform([input_list[3]]).item()
    View_rating=view_rating_encoder.transform([input_list[2]]).item()
    Writer=writer_encoder.transform([input_list[4]]).item()

    Genre_Family = 0
    Genre_Documentary = 0
    Genre_Horror = 0
    Genre_Drama = 0
    Genre_Animation = 0
    Genre_Action=0
    Genre_Comedy=0
    Genre_Thriller=0

    input_genre=input_list[2]
    if input_genre == "Family":
        Genre_Family = 1
    elif input_genre == "Documentary":
        Genre_Documentary = 1
    elif input_genre == "Horror":
        Genre_Horror = 1
    elif input_genre == "Drama":
        Genre_Drama = 1
    elif input_genre == "Animation":
        Genre_Animation = 1
    elif input_genre == "Action":
        Genre_Action = 1
    elif input_genre == "Comedy":
        Genre_Comedy = 1  
    elif input_genre == "Thriller":
        Genre_Thriller = 1  

    input_instance = [None]*20
    input_instance[0]=series_movie
    input_instance[1]=View_rating
    input_instance[2]=Awards_nominated_for
    input_instance[3]=Awards_received
    input_instance[4]=Writer
    input_instance[5]=Director
    input_instance[6]=Genre_Documentary
    input_instance[7]=Genre_Action
    input_instance[8]=Genre_Comedy
    input_instance[9]=Genre_Thriller
    input_instance[10]=poster_features['poster_1179'].values[0]
    input_instance[11]=poster_features['poster_1057'].values[0]
    input_instance[12]=poster_features['poster_278'].values[0]
    input_instance[13]=poster_features['poster_1911'].values[0]
    input_instance[14]=poster_features['poster_711'].values[0]
    input_instance[15]=poster_features['poster_1074'].values[0]
    input_instance[16]=poster_features['poster_197'].values[0]
    input_instance[17]=poster_features['poster_856'].values[0]
    input_instance[18]=poster_features['poster_1876'].values[0]
    input_instance[19]=poster_features['poster_236'].values[0]

  # Standardize data
    with open(config["scaler"]['popularity'], 'rb') as f:
        loaded_scaler = pickle.load(f)

    input_array = np.array(input_instance).reshape(1, -1)
    scaled_new_row = loaded_scaler.transform(input_array)

  # Load model
    loaded_model = xgb.Booster()
    loaded_model.load_model(config["model_webapp_dir"]['popularity'])
    
    dtest = xgb.DMatrix(scaled_new_row)
    predictions = loaded_model.predict(dtest)
    highest_value_index = np.argmax(predictions)

    if highest_value_index==0:
        return "High"
    elif highest_value_index==1:
        return "Low"
    elif highest_value_index==2:
        return "Medium"
    

def predict_score(input_list,features_quality): 
  # input_list example: ['Movie', 'Action', 'G', 'director', 'writer', '4', '2'] type, genre, rating , 'director', 'writer', awards received, nominated, poster
  # Load the fitted LabelEncoder
    config = read_params(params_path)
    with open(config["encoder"]['type'], 'rb') as f:
        series_movie_encoder = pickle.load(f)

    with open(config["encoder"]['director'], 'rb') as f:
        director_encoder = pickle.load(f)

    series_movie=series_movie_encoder.transform([input_list[0]]).item()
    Awards_nominated_for=int(input_list[6])
    Awards_received=int(input_list[5])
    Director=director_encoder.transform([input_list[3]]).item()

    Genre_Family = 0
    Genre_Documentary = 0
    Genre_Horror = 0
    Genre_Drama = 0
    Genre_Animation = 0

    input_genre=input_list[2]
    if input_genre == "Family":
        Genre_Family = 1
    elif input_genre == "Documentary":
        Genre_Documentary = 1
    elif input_genre == "Horror":
        Genre_Horror = 1
    elif input_genre == "Drama":
        Genre_Drama = 1
    elif input_genre == "Animation":
        Genre_Animation = 1

    input_instance = [None]*20
    input_instance[0]=series_movie
    input_instance[1]=Awards_nominated_for
    input_instance[2]=Awards_received
    input_instance[3]=Director
    input_instance[4]=Genre_Family
    input_instance[5]=Genre_Documentary
    input_instance[6]=Genre_Horror
    input_instance[7]=Genre_Drama
    input_instance[8]=Genre_Animation
    input_instance[9]=features_quality['poster_1653'].values[0]
    input_instance[10]=features_quality['poster_143'].values[0]
    input_instance[11]=features_quality['poster_1594'].values[0]
    input_instance[12]=features_quality['poster_1592'].values[0]
    input_instance[13]=features_quality['poster_1070'].values[0]
    input_instance[14]=features_quality['poster_1623'].values[0]
    input_instance[15]=features_quality['poster_1011'].values[0]
    input_instance[16]=features_quality['poster_23'].values[0]
    input_instance[17]=features_quality['poster_1587'].values[0]
    input_instance[18]=features_quality['poster_451'].values[0]
    input_instance[19]=features_quality['poster_1586'].values[0]

  # Standardize data
    with open(config["scaler"]['quality'], 'rb') as f:
        loaded_scaler = pickle.load(f)

    input_array = np.array(input_instance).reshape(1, -1)
    scaled_new_row = loaded_scaler.transform(input_array)

  # Load model
    loaded_model = xgb.Booster()
    loaded_model.load_model(config["model_webapp_dir"]['quality'])
    
    dtest = xgb.DMatrix(scaled_new_row)
    predictions = loaded_model.predict(dtest)
    highest_value_index = np.argmax(predictions)

    if highest_value_index==0:
        return "High"
    elif highest_value_index==1:
        return "Low"
    elif highest_value_index==2:
        return "Medium"
