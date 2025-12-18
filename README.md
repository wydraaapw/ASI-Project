## Źródła

- **Dataset**: https://archive.ics.uci.edu/dataset/73/mushroom
- **Licencja**: Creative Commons Attribution 4.0 International (CC BY 4.0) license, https://creativecommons.org/licenses/by/4.0/
- **Data pobrania**: 15.10.2025

---

## Metryka ewaluacji

- **Metryka**: F1-score dla klasy „poisonous”
- **Uzasadnienie**: Błąd polegający na sklasyfikowaniu trującego grzyba jako jadalny jest krytyczny, dlatego metryka F1-score pozwala zbalansować precyzję i recall dla klasy trujących grzybów.

---

## Weights & Biases

- **W&B**: https://wandb.ai/s25983-pjatk/mushrooms?nw=nwusers25983

---

## Wymagania

- **Git**
- **Conda / Miniconda**
- **Python 3.9–3.11**

---

## Uruchom:

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/wydraaapw/ASI-Project.git
   ```
   ```bash
   cd ASI-Project
   ```
3. Utwórz środowisko Conda:
   ```bash
   conda env create -f environment.yml
   ```
   ```bash
   conda activate asi-ml
   ```
4. Zainstaluj projekt:
   ```bash
   pip install -e .
   ```
5. Pobierz pełny zestaw danych z 1 linijki tego pliku, rozpakuj archiwum oraz umieść plik agaricus-lepiota.data w data/01_raw pod nazwą mushrooms.csv

6. Uruchom eksperymenty kedro z różnymi parametrami:
   ```bash
   kedro run --params autogluon.time_limit=60
   ```
   ```bash
   kedro run --params autogluon.time_limit=120
   ```
   ```bash
   kedro run --params autogluon.presets=best_quality,autogluon.time_limit=60
   ```
### Kedro pipeline
<img width="372" height="922" alt="image" src="https://github.com/user-attachments/assets/bd8a62e7-3509-4a4a-914a-7496292aff10" />

### Tabela runów
<img width="1112" height="219" alt="image" src="https://github.com/user-attachments/assets/8234949b-df94-4699-be7c-96a123297986" />

### Walidacja API
```bash
uvicorn src.api.main:app --reload --port 8000
```
```bash
curl http://127.0.0.1:8000/healthz
```
```bash
curl -X POST http://127.0.0.1:8000/predict \
-H "Content-Type: application/json" \
-d '{
"cap-shape": "x",
"cap-surface": "s",
"cap-color": "n",
"bruises": "t",
"odor": "p",
"gill-attachment": "f",
"gill-spacing": "c",
"gill-size": "b",
"gill-color": "k",
"stalk-shape": "e",
"stalk-root": "b",
"stalk-surface-above-ring": "s",
"stalk-surface-below-ring": "s",
"stalk-color-above-ring": "w",
"stalk-color-below-ring": "w",
"veil-type": "p",
"veil-color": "w",
"ring-number": "o",
"ring-type": "p",
"spore-print-color": "k",
"population": "v",
"habitat": "d"
}'
```

<!-- Previous README version
**Link do źródła**: https://archive.ics.uci.edu/dataset/73/mushroom
**Nazwa licencji**: Creative Commons Attribution 4.0 International (CC BY 4.0) license, https://creativecommons.org/licenses/by/4.0/
**Data pobrania**: 15.10.2025
**Metryka**: F1-score dla klasy „poisonous”
**Uzasadnienie**: Błąd polegający na sklasyfikowaniu trującego grzyba jako jadalny jest krytyczny, dlatego metryka F1-score pozwala zbalansować precyzję i recall dla klasy trujących grzybów.

W&B: https://wandb.ai/s25983-pjatk/mushrooms?nw=nwusers25983

Uruchom:

  Wymagania: Git, Conda / Miniconda, Python 3.9–3.11

  1. Sklonuj repozytorium:

     git clone https://github.com/wydraaapw/ASI-Project.git

     cd ASI-Project
  3. Utwórz środowisko Conda:

       conda env create -f environment.yml

       conda activate asi-ml
  5. Zainstaluj projekt:
       pip install -e .
  6. Pobierz pełny zestaw danych z 1 linijki tego pliku, rozpakuj archiwum oraz umieść plik agaricus-lepiota.data w data/01_raw pod nazwą mushrooms.csv

  7. Uruchom eksperymenty kedro z różnymi parametrami:


       kedro run --params autogluon.time_limit=60

       kedro run --params autogluon.time_limit=120

       kedro run --params autogluon.presets=best_quality,autogluon.time_limit=60

<img width="372" height="922" alt="image" src="https://github.com/user-attachments/assets/bd8a62e7-3509-4a4a-914a-7496292aff10" />


# Tabela runów
<img width="1112" height="219" alt="image" src="https://github.com/user-attachments/assets/8234949b-df94-4699-be7c-96a123297986" />

#Walidacja API

uruchom: 
  1. uvicorn src.api.main:app --reload --port 8000
     
  2. curl http://127.0.0.1:8000/healthz
     
  3. curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cap-shape": "x",
    "cap-surface": "s",
    "cap-color": "n",
    "bruises": "t",
    "odor": "p",
    "gill-attachment": "f",
    "gill-spacing": "c",
    "gill-size": "b",
    "gill-color": "k",
    "stalk-shape": "e",
    "stalk-root": "b",
    "stalk-surface-above-ring": "s",
    "stalk-surface-below-ring": "s",
    "stalk-color-above-ring": "w",
    "stalk-color-below-ring": "w",
    "veil-type": "p",
    "veil-color": "w",
    "ring-number": "o",
    "ring-type": "p",
    "spore-print-color": "k",
    "population": "v",
    "habitat": "d"

  }'
-->
