def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    import os
    import pandas as pd

    base = os.path.join(os.path.dirname(__file__), '..')
    data_dir = os.path.join(base, 'data')
    salida = os.path.join(base, 'submission')

    os.makedirs(salida, exist_ok=True)

    for division in ["train", "test"]:
        registros = []

        for sentimiento in sorted(os.listdir(os.path.join(data_dir, division))):
            carpeta = os.path.join(data_dir, division, sentimiento)
            if not os.path.isdir(carpeta):
                continue

            for nombre in sorted(os.listdir(carpeta)):
                if not nombre.endswith(".txt"):
                    continue

                with open(
                    os.path.join(carpeta, nombre), encoding="utf-8"
                ) as archivo:
                    frase = archivo.read().strip()

                registros.append({"phrase": frase, "target": sentimiento})

        df = pd.DataFrame(registros, columns=["phrase", "target"])
        df.to_csv(
            os.path.join(salida, f"{division}_dataset.csv"),
            index=False,
        )
