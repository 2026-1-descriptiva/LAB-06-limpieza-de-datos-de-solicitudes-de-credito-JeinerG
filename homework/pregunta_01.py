"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import os
import pandas as pd

def limpiar_fecha_columna(fecha_str):
    """Parsea formatos mixtos basándose estrictamente en la posición del año."""
    if pd.isna(fecha_str):
        return pd.NaT

    fecha_str = str(fecha_str).strip()
    sep = "/" if "/" in fecha_str else "-"
    partes = fecha_str.split(sep)

    if len(partes) == 3:
        # Si el primer bloque tiene 4 caracteres, es formato Año-Mes-Día
        formato = f"%Y{sep}%m{sep}%d" if len(partes[0]) == 4 else f"%d{sep}%m{sep}%Y"
        try:
            return pd.to_datetime(fecha_str, format=formato)
        except Exception:
            return pd.NaT
    return pd.NaT


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    infile = "files/input/solicitudes_de_credito.csv"
    outfile = "files/output/solicitudes_de_credito.csv"
    os.makedirs(os.path.dirname(outfile), exist_ok=True)

    # 1. Cargar datos omitiendo el índice anónmo
    df = pd.read_csv(infile, sep=";", index_col=0)

    # 2. Limpieza uniforme de campos de texto
    text_cols = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "línea_credito"]
    df[text_cols] = df[text_cols].apply(
        lambda col: col.astype(str)
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
    )

    # 3. Limpieza y conversión del monto de crédito
    df["monto_del_credito"] = pd.to_numeric(
        df["monto_del_credito"]
        .astype(str)
        .str.replace(r"[\$\s,]", "", regex=True)
        .str.split(".")
        .str[0],
        errors="coerce",
    )

    # 4. Formateo seguro de fechas manteniendo el orden original
    df["fecha_de_beneficio"] = (
        df["fecha_de_beneficio"]
        .apply(limpiar_fecha_columna)
        .dt.strftime("%Y-%m-%d")
    )

    # 5. Remover registros vacíos, limpiar duplicados y exportar
    df.dropna().drop_duplicates().to_csv(outfile, sep=";", index=False)


if __name__ == "__main__":
    pregunta_01()