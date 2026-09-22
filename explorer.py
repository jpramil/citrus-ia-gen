"""Cellules d'exploration interactives — à exécuter une par une dans VS Code.

Séparé de `bourrin.py` pour que le module reste importable : du code au niveau
module s'exécuterait à chaque `import bourrin`, y compris les appels réseau et
les appels LLM.

Kernel : citrus (uv .venv).
"""
# %%
from pprint import pprint

import polars as pl
from dotenv import load_dotenv

load_dotenv(override=True)

from bourrin import (
    COMPARED_READING,
    afficher_annonce,
    annotation_for,
    format_annonce,
    format_comparison,
    format_result,
    load_annotations,
    describe_annotations,
    run_bourrin,
)
from src.bodacc.api import bodacc_api

pl.Config.set_tbl_cols(-1)
annotations = load_annotations()
print(describe_annotations(annotations))

# %% une annonce de bout en bout
res = run_bourrin("A20230147853")
print(format_result(res))

# %% la réponse normalisée, et le raccourci de confort
res["envelope"]
res["prediction"]
pprint(res["payload"])

# %% confronter à la référence annotée
print(format_comparison(
    res["envelope"][COMPARED_READING]["operations"],
    annotation_for(annotations, "A20230147853"),
))

# %% inspecter une annonce sans appeler le LLM
afficher_annonce("A202302002243")
annotation_for(annotations, "A202302002243")
annotations.filter(pl.col("ref_annonce_complet") == "A202302002243")

# %% le payload brut
pprint(bodacc_api().fetch_annonce_json("A202302002243"))
