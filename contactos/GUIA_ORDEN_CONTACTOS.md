# Orden de contactos, calendarios y archivos

## 1. Decisión de arquitectura (lo que se define una sola vez)

| Esfera | Cuenta dueña | Qué vive ahí |
|---|---|---|
| Personal | fernandita.gonzalez@gmail.com | Familia, amistades, escuela de los hijos, médicos, servicios del hogar |
| Empresa | fernanda.gonzalvarez@gmail.com | Clientes, proveedores, contratistas, equipo, prospectos |
| Outlook | Solo lectura / consulta | No se capturan contactos aquí; se alimenta desde Google |

Reglas:

1. **Una sola fuente de verdad por esfera.** Cada contacto vive en una sola cuenta de Google. Nunca en la memoria del teléfono ni en la SIM.
2. **Outlook no es fuente.** Outlook guarda "contactos sugeridos" (solo nombre y correo) automáticamente; por eso aparecen incompletos. Se capturan en Google y Outlook solo consulta.
3. **Si alguien es mixto** (amiga que además es proveedora): va en Empresa, con la etiqueta `Personal` adicional.

## 2. Formato estándar de cada contacto

| Campo | Regla | Ejemplo |
|---|---|---|
| Nombre | Nombre de pila | Ana Lucía |
| Apellidos | Ambos si se conocen | Martínez Ruiz |
| Empresa | **Siempre lleno.** En personales, el contexto | Svatek / Escuela Sofía / Familia |
| Puesto | Rol o relación | Gerente de proyecto / Mamá de Diego |
| Correo | En minúsculas | ana.martinez@empresa.com |
| Teléfono | Formato internacional | +52 55 1234 5678 |
| Etiquetas | 1 a 3 (ver catálogo) | Cliente, Obra Polanco |
| Notas | `Origen:` cómo llegó + fecha | Origen: Junta de arranque obra Polanco, oct 2026. La presentó Jorge. |

**Por qué Empresa siempre lleno:** el buscador del teléfono (iPhone y Android) busca por nombre y empresa, pero no siempre por notas. Si no recuerdas el nombre, escribes "Polanco" o "Escuela" y aparece.

### Catálogo de etiquetas (máximo 10, no inventar más)

- Empresa: `Cliente`, `Proveedor`, `Contratista`, `Equipo`, `Prospecto`, `Obra <nombre>`
- Personal: `Familia`, `Amistades`, `Hijos-Escuela`, `Hogar-Servicios`, `Salud`

## 3. Plan de ejecución (bloques cortos)

### Bloque A — Respaldo (15 min). EMPEZAR AQUÍ.
1. contacts.google.com con cuenta personal → Exportar → CSV de Google.
2. Lo mismo con la cuenta de empresa.
3. Outlook → Personas → Administrar contactos → Exportar → CSV.
4. En el teléfono: exportar contactos guardados "en el dispositivo" / SIM a un .vcf.

Nada se borra hasta tener los cuatro archivos.

### Bloque B — Limpieza con el script (30 min)
```bash
python3 contactos/normalizar_contactos.py revisar google_personal.csv google_empresa.csv outlook.csv -o revision.csv
```
El script:
- Une todo, quita duplicados (por correo o teléfono) y combina sus datos.
- Normaliza nombres, correos y teléfonos (+52).
- Agrega columnas `Cuenta` (vacía) y `Faltantes` (qué datos le faltan a cada uno).

Abre `revision.csv` en Excel/Sheets y llena `Cuenta` con `P` (personal), `E` (empresa) o `X` (borrar). Ordena por `Faltantes` y completa lo que sepas; lo que no, se queda.

Tip: no tienes que revisar todo de una vez. Haz 50 por sesión.

### Bloque C — Generar archivos de importación (5 min)
```bash
python3 contactos/normalizar_contactos.py exportar revision.csv
```
Genera `importar_personal.csv` e `importar_empresa.csv` en formato de Google Contacts.

### Bloque D — Cargar y depurar (20 min)
1. En cada cuenta de Google: borrar contactos actuales (ya respaldados) → Importar el CSV correspondiente.
2. Google Contacts → "Combinar y corregir" para los duplicados que quedaron.

### Bloque E — Configurar el teléfono (15 min)
**Android**
- Ajustes → Cuentas: ambas cuentas de Google con Contactos y Calendario activados.
- App Contactos → Ajustes → Cuenta predeterminada para contactos nuevos → **empresa** (el volumen nuevo vendrá de ahí).
- Importar el .vcf del dispositivo al lugar que corresponda y borrar los del dispositivo/SIM.

**iPhone**
- Ajustes → Contactos → Cuentas: agregar ambas cuentas de Gmail con Contactos activado.
- Ajustes → Contactos → Cuenta predeterminada → la de **empresa**.
- Desactivar Contactos en iCloud (si no, se vuelve una tercera fuente de caos).

### Bloque F — Outlook
- Outlook (web o nuevo Outlook) → Agregar cuenta → conectar la cuenta de Google de empresa: los contactos de Google aparecen al redactar.
- Desactivar el guardado automático de contactos sugeridos, si tu versión lo permite.
- En Outlook móvil: Ajustes → cuenta → "Sincronizar contactos" solo si quieres verlos en el teléfono; si ya están en Google, dejarlo apagado para no duplicar.

## 4. Calendarios y archivos (misma lógica)

| Elemento | Personal | Empresa |
|---|---|---|
| Calendario | Hogar, hijos, salud | Juntas, obras, entregas |
| Drive | Documentos familiares | Proyectos y entregables |

- Comparte el calendario personal con la cuenta de empresa en modo "solo ver disponible/ocupado": así no te agendan sobre la junta de la escuela.
- En el teléfono, ponle un color distinto a cada calendario.
- Archivos: nada se guarda en "Descargas" del teléfono; se sube a la Drive de la esfera correspondiente.

## 5. Mantenimiento (regla, no fuerza de voluntad)

1. **Al guardar un contacto nuevo:** nombre, apellido, empresa y una línea de `Origen:`. Toma 20 segundos.
2. **Viernes, 10 minutos:** revisar contactos de la semana sin empresa u origen.
3. **Cada trimestre:** correr el script con exportaciones nuevas para detectar duplicados.
