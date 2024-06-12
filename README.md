# SusGPT: Where Sustainability is Answered

The idea of SusGPT is to be the source of answers for the sustainability landscape in India. It draws on the database of climate action startups and functions like ChatGPT on climate steroids to build insights.

### Demo Video to Run
Since this is not hosted on any platform right now, we have developed this in local host. 
You can follow the demo video to run and use this : 
And the steps are given below as well!

### Steps to Run:

1. Clone Repository from Github in an IDE : https://github.com/YashKandoi/susgpt.git

2. Adding API tokens from Hugging Face (it's free) [Get it here: https://huggingface.co/settings/tokens]
    1. Generate a write token
    2. Go to susgpt/susgpt/hf_inference_api_key.txt
    3. Paste this API token here

3. Adding API tokens from JINA Embeddings (it's free) [Scroll down in this page and get it here: https://jina.ai/embeddings/]
    1. Copy this token
    2. Go to susgpt/susgpt/jina_emb_api_key.txt
    3. Paste this API token here

4. Now open Termninal and run this:
     ```pip install -r requirements.txt```
    This will take sometime and install all required libraries.

    Next step is to run:
    ```python3 manage.py runserver```
    This will start the backend server

5. Now open another terminal and run this:

    ```streamlit run frontend/Home.py ```
    This will start the frontend server and will open up SusGPT.


