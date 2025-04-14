# CPE490590hw05
# CNN trained on MNIST Classifier Web app
This web app was made to classify uploaded images if hand drawn numbers specificaslly trained on the MNIST dataset using a CNN model. The model was incorporated into the webapp using onnx for efficiency. Example datasets are included and were sourced from kaggle's MNIST dataset (https://www.kaggle.com/datasets/scolianni/mnistasjpg) in the jpg format. 

# Step 1: Environment setup
Python was used to set up the virtual environment to run the web app and avoid potential conflicts with existing libraries. 

Conda was used to activate the environment but powershell or similar can be utilized as well.

Installing uv (https://docs.astral.sh/uv/getting-started/installation/#installation-methods):

```python
1 powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" (Windows)
2 pip install uv (alternative method)
3 uv venv
4 .venv\Scripts\activate
```

# Step 2: Install dependencies

```python
1 pip install Flask onnx onnxruntime numpy Pillow Werkzeug
```
requirements.txt can also be referenced for additonal libraries.

# Step 3: Gather required files
The source code is available in the github (https://github.com/uahuser00000/CPE490590hw05.git).
It is important to navigate or create an easily accessible directory before activating the web app. 

```python
1 mkdir hello (example)
2 cd hello
```

# Step 4: Activate the Web App
The web app can be activated with flask as follows:
```python
1 flask --app hello run (example)
2 flask run (if named app.py)
```
The generated html can then be entered in the browser and web app can be used. If desired, more example data can be used in the MNIST_samples folder.
More information can be found on their quickstart guide: (https://flask.palletsprojects.com/en/stable/quickstart/)

# Step 5: Running the Web App
In the webpage, an image can be uploaded and the "Upload" Button should then be selected. The image preview should then be seen and the "Predict" button can then be selected to view the probabilities and predicted digit. In the lower half of the webpage, example data can also be tested by clicking on their associated button.
