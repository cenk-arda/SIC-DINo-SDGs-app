# SIC-DINo-SDGs-app

An NLP tool that predicts the Sustainable Development Goal related to text inputs.


This is the web application of our project within Samsung Innovation Campus.

The project's main focus is to build ML and DL models to classify OSDG Community Dataset.<br>
For the dataset: https://zenodo.org/record/6393942#.YstnkxzP3Jw

The project is currently hosted on Google Cloud Run:

https://dino-sdgs-web-app-jhi6mgj6za-lz.a.run.app/

This web application is designed to predict the related Sustainable Development Goal of a text input.
The text input is a paragraph of text. Our highly accurate ML/DL models will predict the SDG related to the your input.<br>

For all goals: https://sdgs.un.org/


### version 1.0:
Predictor model: [*bert-base-uncased*](https://huggingface.co/bert-base-uncased). fine-tuned with [OSDG-CD](https://zenodo.org/record/6393942#.YstnkxzP3Jw) (1 April 2022 version).
