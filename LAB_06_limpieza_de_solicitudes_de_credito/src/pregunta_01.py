def pregunta_01():
    """
    Limpia `data/solicitudes_de_credito.csv.gz` y guarda el resultado en
    `submission/solicitudes_de_credito.csv` (separador `;`, sin índice).
    """

    import os
    import re
    import pandas as pd

    base = os.path.join(os.path.dirname(__file__), '..')
    ruta = os.path.join(base, 'data', 'solicitudes_de_credito.csv.gz')

    columnas = [
        "sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio",
        "estrato", "comuna_ciudadano", "fecha_de_beneficio",
        "monto_del_credito", "línea_credito",
    ]
    texto = [
        "sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio",
        "línea_credito",
    ]

    df = pd.read_csv(ruta, sep=";", dtype=str, encoding="utf-8-sig")

    df.columns = [c.replace("\ufeff", "").strip().lower() for c in df.columns]
    df = df[columnas].copy()

    for col in texto:
        df[col] = (
            df[col]
            .str.lower()
            .str.replace(r"[_\-]+", " ", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    df["estrato"] = df["estrato"].str.extract(r"(\d+)", expand=False)

    def limpiar_monto(valor):
        if pd.isna(valor):
            return pd.NA
        v = valor.strip().replace("$", "").replace(" ", "")
        v = re.sub(r"[.,]\d{1,2}$", "", v)   # parte decimal
        v = re.sub(r"\D", "", v)             # separadores de miles
        return v if v else pd.NA

    df["monto_del_credito"] = df["monto_del_credito"].map(limpiar_monto)

    def limpiar_fecha(valor):
        if pd.isna(valor):
            return pd.NA
        v = valor.strip().replace("/", "-")
        if not v:
            return pd.NA
        primero_anio = re.match(r"^\d{4}", v) is not None
        fecha = pd.to_datetime(
            v, dayfirst=not primero_anio, yearfirst=primero_anio,
            errors="coerce",
        )
        return pd.NA if pd.isna(fecha) else fecha.strftime("%Y-%m-%d")

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].map(limpiar_fecha)

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    obligatorias = [c for c in columnas if c != "comuna_ciudadano"]
    df = df.dropna(subset=obligatorias)

    df["estrato"] = df["estrato"].astype(int)
    df["monto_del_credito"] = df["monto_del_credito"].astype(int)

    df = df.drop_duplicates().reset_index(drop=True)

    salida = os.path.join(base, 'submission')
    os.makedirs(salida, exist_ok=True)
    df.to_csv(
        os.path.join(salida, 'solicitudes_de_credito.csv'),
        sep=";",
        index=False,
    )
