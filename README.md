**Link do źródła**: https://archive.ics.uci.edu/dataset/73/mushroom
**Nazwa licencji**: Creative Commons Attribution 4.0 International (CC BY 4.0) license, https://creativecommons.org/licenses/by/4.0/
**Data pobrania**: 15.10.2025
**Metryka**: F1-score dla klasy „poisonous”
**Uzasadnienie**: Błąd polegający na sklasyfikowaniu trującego grzyba jako jadalny jest krytyczny, dlatego metryka F1-score pozwala zbalansować precyzję i recall dla klasy trujących grzybów.

W&B: https://wandb.ai/s25983-pjatk/mushrooms?nw=nwusers25983

Uruchom:
  
  Wymagania: Git, Conda / Miniconda, Python 3.9–3.11

  1. Sklonuj repozytorium:
       git clone https://github.com/<twoje_repo>/ASI-Project.git
       cd ASI-Project
  2. Utwórz środowisko Conda:
       conda env create -f environment.yml
       conda activate asi-ml
  3. Zainstaluj projekt:
       pip install -e .
  4. Pobierz pełny zestaw danych z 1 linijki tego pliku oraz umieść go w data/01_raw pod nazwą mushrooms.csv
  5. Uruchom pipeline kedro:
       kedro run --pipeline asi

<img width="372" height="922" alt="image" src="https://github.com/user-attachments/assets/bd8a62e7-3509-4a4a-914a-7496292aff10" />
