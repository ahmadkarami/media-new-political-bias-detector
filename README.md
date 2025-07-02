# Political Bias & Fake News Detection from Multi-Source News

## Project Overview

This project aims to collect the same news from multiple media outlets and compare the language, content, and tone to:

- Detect **fake or manipulated news**
- Analyze the **political bias** of each source
- Help users identify **neutral and reliable** news providers

Using Natural Language Processing (NLP), we extract and analyze news from various media (left-wing, right-wing, and neutral), and provide users with a summary comparison of how each source reports the same event.

---

## Key Features

-  Web scraping from multiple real-time news sources  
-  NLP-based summarization of each article  
-  Semantic comparison of articles on the same topic  
-  Tone and sentiment analysis  
-  Fake news likelihood estimation (based on semantic conflict and exaggeration)  
-  Media bias profiling based on language and framing

---

##  Tech Stack

- **Python**  
- `BeautifulSoup`, `requests`, `newspaper3k` – Web scraping  
- `transformers`, `T5`, `BERT`, `GPT` – NLP models  
- `nltk`, `spacy`, `textblob` – sentiment & tone analysis  
- `scikit-learn` – basic ML for classification  
- `Flask` or `Streamlit` – user interface  

---

##  Example Use Case

> When a user selects a breaking news headline (e.g. "Election Results 2025"),  
> the system collects the same headline from various sources (CNN, Fox News, BBC, etc.)  
> Then it summarizes and compares the articles, and highlights bias (e.g. exaggeration, emotional tone, focus shift).  
> It may also flag if any version contains potential misinformation.

---

##  Future Plans

- Integrate real-time Twitter comparison  
- Add media profile dashboard per outlet  
- Fake news detection using fine-tuned transformer models  
- Visual representation of political lean (left / center / right)

---

##  Author

Ahmad Karami – [ahmadkarami73@gmail.com]  
Feel free to contribute or reach out!
