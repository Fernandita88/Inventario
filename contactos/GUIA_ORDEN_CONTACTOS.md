# Orden de contactos, calendarios y archivos

## 1. Decisión de arquitectura (lo que se define una sola vez)

| Elemento | Dónde vive |
|---|---|
| Todos los contactos (personales, comunidades y trabajo) | Cuenta personal de Google |
| Contactos de trabajo | Misma cuenta, con etiqueta `Chamba` |
| Outlook | Solo consulta; no se capturan contactos ahí |

Reglas:

1. **Una sola fuente de verdad.** Nada en la memoria del teléfono, la SIM ni Outlook.
2. **La red es de la persona, no de la empresa.** Por eso todo vive en la cuenta personal.
3. **Outlook no es fuente.** Guarda "contactos sugeridos" solo con nombre y correo.

## 2. Formato estándar: tres tipos de contacto

Regla general: **Empresa = el grupo con el que ubicas a la persona.**

| Tipo | Empresa | Puesto | Departamento | Relación |
|---|---|---|---|---|
| 1. Escuela de los hijos | Escuela | Hijo o hija con quien se relaciona | Vínculo (Mamá de Tian) | Tian, tipo Hijo |
| 2. Comunidades (programas, generaciones, deportes, vecinos) | Grupo + generación (Medex 19-21) | Su cargo y empresa real | Subgrupo (Equipo 4) | Si aplica |
| 3. Trabajo y servicios | Su empresa real | Cargo o rol | Vínculo contigo | Si aplica |

- **Notas:** `Origen:` cómo llegó + fecha. Sin rastros automáticos de WhatsApp.
- **Relación:** acepta cualquier nombre, aunque no sea contacto. Sirve para "de quién viene" (primo de, esposa de, mamá de).
- **Etiquetas (para filtrar):** una por hijo o hija, `Medex`, `Medex Girl`, `Chamba`. No crear más sin necesidad.
- Android busca en todos los campos, así que cualquier dato de los anteriores sirve para encontrar a alguien.

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
- App Contactos → Ajustes → Cuenta predeterminada para contactos nuevos → **personal** (ahí vive todo).
- Importar el .vcf del dispositivo al lugar que corresponda y borrar los del dispositivo/SIM.

**iPhone**
- Ajustes → Contactos → Cuentas: agregar ambas cuentas de Gmail con Contactos activado.
- Ajustes → Contactos → Cuenta predeterminada → la **personal**.
- Desactivar Contactos en iCloud (si no, se vuelve una tercera fuente de caos).

### Bloque F — Outlook
- Outlook (web o nuevo Outlook) → Agregar cuenta → conectar la cuenta personal de Google: los contactos de Google aparecen al redactar.
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
