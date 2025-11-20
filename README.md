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
  8. 
       kedro run --params autogluon.time_limit=60
     
       kedro run --params autogluon.time_limit=120
     
       kedro run --params autogluon.presets=best_quality,autogluon.time_limit=60

<img width="372" height="922" alt="image" src="https://github.com/user-attachments/assets/bd8a62e7-3509-4a4a-914a-7496292aff10" />


# Tabela runów
<img width="1112" height="219" alt="image" src="https://github.com/user-attachments/assets/8234949b-df94-4699-be7c-96a123297986" />
