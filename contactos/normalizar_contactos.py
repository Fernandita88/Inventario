"""Une, limpia y separa contactos exportados de Google Contacts y Outlook.

Uso:
  python3 normalizar_contactos.py revisar archivo1.csv [archivo2.csv ...] -o revision.csv
  python3 normalizar_contactos.py exportar revision.csv

Paso 1 (revisar): une todos los CSV, normaliza y quita duplicados.
  Llena a mano la columna "Cuenta" con P (personal), E (empresa) o X (descartar).
Paso 2 (exportar): genera importar_personal.csv e importar_empresa.csv
  en formato de importación de Google Contacts.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

# Nombres de columna posibles en exportaciones de Google (nueva y antigua) y Outlook.
ALIAS = {
    "nombre": ["First Name", "Given Name", "Nombre"],
    "segundo": ["Middle Name", "Additional Name", "Segundo nombre"],
    "apellidos": ["Last Name", "Family Name", "Apellidos"],
    "empresa": ["Organization Name", "Organization 1 - Name", "Company", "Empresa", "Compañía"],
    "puesto": ["Organization Title", "Organization 1 - Title", "Job Title", "Puesto"],
    "etiquetas": ["Labels", "Group Membership", "Categories", "Categorías", "Etiquetas"],
    "notas": ["Notes", "Notas"],
}
CORREO_COLS = re.compile(r"^(E-mail( \d+)? - Value|E-mail( \d)? ?Address|Correo.*)$", re.I)
TEL_COLS = re.compile(r"^(Phone \d+ - Value|.*Phone.*|Teléfono.*|Móvil|Celular)$", re.I)

SALIDA = ["Cuenta", "Faltantes", "Nombre", "Apellidos", "Empresa", "Puesto",
          "Correos", "Teléfonos", "Etiquetas", "Notas", "Fuente"]

MINUSCULAS = {"de", "del", "la", "las", "los", "y", "van", "von"}


def primero(fila, claves):
    for c in claves:
        v = (fila.get(c) or "").strip()
        if v:
            return v
    return ""


def nombre_propio(texto):
    if not texto or not (texto.isupper() or texto.islower()):
        return texto.strip()  # respeta capitalización mixta ya escrita a mano
    palabras = texto.strip().lower().split()
    return " ".join(p if i and p in MINUSCULAS else p.capitalize() for i, p in enumerate(palabras))


def telefono(t):
    digitos = re.sub(r"\D", "", t)
    if not digitos:
        return ""
    if len(digitos) == 10:  # número mexicano sin lada de país
        digitos = "52" + digitos
    if len(digitos) == 13 and digitos.startswith("521"):  # formato antiguo de celular
        digitos = "52" + digitos[3:]
    if len(digitos) == 12 and digitos.startswith("52"):
        return f"+52 {digitos[2:4]} {digitos[4:8]} {digitos[8:]}"
    return "+" + digitos


def separar(valor):
    # Google usa " ::: " para varios valores en una celda.
    return [v.strip() for v in re.split(r":::|;", valor) if v.strip()]


def leer(ruta):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        for fila in csv.DictReader(f):
            c = {k: nombre_propio(primero(fila, v)) if k in ("nombre", "segundo", "apellidos")
                 else primero(fila, v) for k, v in ALIAS.items()}
            if c["segundo"]:
                c["nombre"] = f'{c["nombre"]} {c["segundo"]}'.strip()
            correos, tels = [], []
            for col, val in fila.items():
                if not col or not val:
                    continue
                if CORREO_COLS.match(col):
                    correos += [e.lower() for e in separar(val) if "@" in e]
                elif TEL_COLS.match(col) and "Label" not in col and "Type" not in col:
                    tels += [telefono(t) for t in separar(val)]
            etiquetas = [e.replace("* ", "") for e in separar(c["etiquetas"].replace(" ::: ", ";"))
                         if e not in ("* myContacts", "myContacts", "* starred")]
            if not (c["nombre"] or c["apellidos"] or correos or tels):
                continue
            yield {
                "Nombre": c["nombre"], "Apellidos": c["apellidos"],
                "Empresa": c["empresa"], "Puesto": c["puesto"],
                "Correos": list(dict.fromkeys(correos)),
                "Teléfonos": list(dict.fromkeys(t for t in tels if t)),
                "Etiquetas": etiquetas, "Notas": c["notas"],
                "Fuente": [Path(ruta).stem],
            }


def combinar(a, b):
    for campo in ("Nombre", "Apellidos", "Empresa", "Puesto"):
        if len(b[campo]) > len(a[campo]):
            a[campo] = b[campo]
    for campo in ("Correos", "Teléfonos", "Etiquetas", "Fuente"):
        a[campo] = list(dict.fromkeys(a[campo] + b[campo]))
    if b["Notas"] and b["Notas"] not in a["Notas"]:
        a["Notas"] = f'{a["Notas"]}\n{b["Notas"]}'.strip()


def revisar(archivos, salida):
    contactos, indice = [], {}
    for ruta in archivos:
        for c in leer(ruta):
            claves = c["Correos"] + c["Teléfonos"]
            existente = next((indice[k] for k in claves if k in indice), None)
            if existente is None:
                contactos.append(c)
                existente = c
            else:
                combinar(existente, c)
            for k in existente["Correos"] + existente["Teléfonos"]:
                indice[k] = existente

    with open(salida, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=SALIDA)
        w.writeheader()
        for c in sorted(contactos, key=lambda c: (c["Apellidos"] or c["Nombre"]).lower()):
            faltan = [n for n, ok in (("apellido", c["Apellidos"]), ("correo", c["Correos"]),
                                      ("teléfono", c["Teléfonos"]), ("empresa", c["Empresa"]),
                                      ("origen", "origen" in c["Notas"].lower())) if not ok]
            w.writerow({**c, "Cuenta": "", "Faltantes": ", ".join(faltan),
                        **{k: " ; ".join(c[k]) for k in ("Correos", "Teléfonos", "Etiquetas", "Fuente")}})
    print(f"{len(contactos)} contactos únicos en {salida}. Llena la columna 'Cuenta' con P, E o X.")


def exportar(revision):
    cols = ["First Name", "Last Name", "Organization Name", "Organization Title", "Labels", "Notes"]
    with open(revision, newline="", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    max_c = max([len(separar(r["Correos"])) for r in filas] + [1])
    max_t = max([len(separar(r["Teléfonos"])) for r in filas] + [1])
    cols += [f"E-mail {i} - Value" for i in range(1, max_c + 1)]
    cols += [f"Phone {i} - Value" for i in range(1, max_t + 1)]

    destinos = {"P": "importar_personal.csv", "E": "importar_empresa.csv"}
    escritores, sin_cuenta = {}, 0
    for r in filas:
        cuenta = r["Cuenta"].strip().upper()[:1]
        if cuenta == "X":
            continue
        if cuenta not in destinos:
            sin_cuenta += 1
            continue
        if cuenta not in escritores:
            f = open(Path(revision).parent / destinos[cuenta], "w", newline="", encoding="utf-8")
            escritores[cuenta] = (f, csv.DictWriter(f, fieldnames=cols))
            escritores[cuenta][1].writeheader()
        fila = {"First Name": r["Nombre"], "Last Name": r["Apellidos"],
                "Organization Name": r["Empresa"], "Organization Title": r["Puesto"],
                "Labels": " ::: ".join(separar(r["Etiquetas"])), "Notes": r["Notas"]}
        fila.update({f"E-mail {i} - Value": v for i, v in enumerate(separar(r["Correos"]), 1)})
        fila.update({f"Phone {i} - Value": v for i, v in enumerate(separar(r["Teléfonos"]), 1)})
        escritores[cuenta][1].writerow(fila)
    for f, _ in escritores.values():
        f.close()
    print("Generados:", ", ".join(destinos[k] for k in escritores) or "ninguno")
    if sin_cuenta:
        print(f"Aviso: {sin_cuenta} contactos sin 'Cuenta' asignada no se exportaron.", file=sys.stderr)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="modo", required=True)
    r = sub.add_parser("revisar")
    r.add_argument("archivos", nargs="+")
    r.add_argument("-o", "--salida", default="revision.csv")
    e = sub.add_parser("exportar")
    e.add_argument("revision")
    a = p.parse_args()
    revisar(a.archivos, a.salida) if a.modo == "revisar" else exportar(a.revision)
