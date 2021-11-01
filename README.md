# AIOCR_streamlit

Run OCR with Azure cognitive service and visualize with streamlit.

## demo

https://share.streamlit.io/otufor/aiocr_streamlit/AIOCR_streamlit.py

## How to use it locally

0. Prepare the Azure computer vision resource

1. git clone this repository

``` bash
git clone https://github.com/otufor/AIOCR_streamlit.git
```

2. Create a .streamlit/secret.toml in the repository directory

``` bash
cd AIOCR_streamlit/
mkdir .streamlit
touch .streamlit/secret.toml
```

3. Add Azure key and endpoint to .streamlit/secret.toml

* Open with vi

``` bash
vi .streamlit/secret.toml
```

* AND Copy from your Azure computer vision resource

``` toml
subscription_key = "[subscription_key]"
endpoint = "[endpoint]"
```

4. pip install

``` bash
pip install -r requirements.txt
```

5. Run

``` bash
streamlit run AIOCR_streamlit.py
```

6. Open the URL in a web browser and try it!

http://localhost:8501/
