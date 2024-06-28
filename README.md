## Turtles

You can chat with AI and ask about turtles.

## Methodology

Here are the framework and models used in the project. 

- **Framework** - Langchain, Langchain-huggingface
- **Model** - Meta-Llama-3-8B-Instruct

## Docker 

Clone this repo. Create .env file in the project folder. Add

```
HF_TOKEN=your_huggingface_token
```

Then, build docker image.

```
docker build -t about_turtles .
```

And, run docker file.
```
docker run --rm -it --env-file .env -p 8501:8501 about_turtles
```

Or you can simply run the application with `streamlit run main.py`
