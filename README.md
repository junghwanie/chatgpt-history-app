## ChatGPT history interface

#### Install
```
pip install streamlit langchain-core langchain-community langchain-openai
```

#### Run
```
streamlit run app.py --server.address 0.0.0.0 --server.port [your port]
# http://0.0.0.0:[your port]
```

#### Docker used
```
docker build -t chatgpt-history-app .
docker run -p 8501:8501 chatgpt-history-app
```