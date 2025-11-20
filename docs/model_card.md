Problem & Intended Use

Problem: Rozróżnianie grzybów jadalnych (edible) od trujących (poisonous) na podstawie ich cech morfologicznych (np. kształt kapelusza, zapach, kolor blaszek).
Po co: Stworzenie modelu wspierającego identyfikację grzybów, który minimalizuje ryzyko błędnej klasyfikacji grzyba trującego jako jadalnego (False Negative).
Użytkownicy: Aplikacje mobilne dla grzybiarzy, systemy edukacyjne.

Data

Źródło: UCI Machine Learning Repository (Mushroom Data Set).
Wielkość: 8124 instancje, 22 cechy kategoryczne.
Preprocessing: - Usunięcie braków danych (dropna).

Kodowanie etykiet (Label Encoding) dla cech kategorycznych.

Podział Train/Test: 80/20.
Prywatność: Dane nie zawierają danych osobowych (PII).

Metrics

Główna metryka: F1-score (weighted). Wybrano F1, aby zachować balans między Precyzją a Czułością w niezbalansowanym problemie.
Metryki pomocnicze: Accuracy, Feature Importance (AutoGluon).

Wyniki modelu produkcyjnego:

F1 Score: 1


Limitations & Risks

Zasięg danych: Zbiór pochodzi z 1981 roku i dotyczy konkretnych gatunków (Agaricus, Lepiota). Model nie zadziała na grzybach spoza tego zakresu.

Ryzyko zdrowotne: Błędna klasyfikacja (False Negative) może prowadzić do zatrucia. Model nie może być jedynym wyznacznikiem jadalności.

Wymagane cechy: Model wymaga podania wszystkich cech fizycznych, co może być trudne dla amatora (np. ocena zapachu).

Versioning

Szczegóły wybranego modelu:

W&B Project: https://wandb.ai/s25983-pjatk/mushrooms/runs/fk2k69nm?nw=nwusers25983

Production Artifact: s25983-pjatk/mushrooms/ag_model_fk2k69nm:v0 
https://wandb.ai/s25983-pjatk/mushrooms/artifacts/model/ag_model_fk2k69nm/latest/overview

Run ID: fk2k69nm

Data Version: clean_data 

Environment: Python 3.10+, AutoGluon 1.1, Kedro 0.19.x
