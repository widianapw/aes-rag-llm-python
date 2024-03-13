## Setup
- Run pip install to install all the required packages
```bash
pip install -r requirements.txt
```
- Download the ollama platform from https://ollama.com/
- pull the model 
```bash
  ollama pull mistral
  ollama pull llama2:7b
  ollama pull gemma
  ```

## Usage File
Preprocess:
- preprocessing/kuis.py
- preprocessing/uas.py

Answering:
- answering/kuis_translate.py

scoring:
- scoring/kuis_mistral.py