Netflix Prediction
==============================

A python Flask web app that allows uploading a poster, entering the type of production, genre, rating, director, writer, awards received and nominated for to predict the popularity and quality of the movies and TV series. We deploy the prediction model as a real-time API service.

1. Install packages: `pip install -r /path/to/requirements.txt`

2. Run app: `python3 app.py`

3. Open `http://localhost:5001` in your browser

Important Files
------------

1. webapp folder

    The folder contains frontend design and supporting files

    a. model_webapp_dir: keep the model file
    b. static: keep css, js, images files
    c. template: contain html files

2. app.py and predict.py

   It implements the main backend logic
   
3. notebooks 

   It contains Jupyter notebooks used to analyze the data.



Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── app.py             <- Implements the main backend logic
    ├── predict.py         <- Implements the main backend logic
    └──  webapp             <- The folder contains frontend design and supporting files



--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
