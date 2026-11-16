---
name: agendar-reunion
description: Agenda reuniones en Google Calendar de forma rápida y segura, con nombre, invitados y modalidad (presencial o Zoom). Revisa conflictos y fechas bloqueadas antes de agendar, y verifica que el evento realmente quedó en el calendario. Nunca usa Teams ni Google Meet. Úsalo cuando la usuaria diga "agenda", "agéndame", "pon en mi calendario", "programa una reunión", "cita con...", "junta con...", "zoom con...", y también cuando en la conversación aparezca un compromiso con fecha y hora que todavía no esté en el calendario.
---

# Agendar reunión

Dos principios mandan sobre todo lo demás:

1. **Si no está en el calendario, no existe.** Nunca digas "agendado" si no comprobaste que el evento existe en Google Calendar.
2. **Ninguna fecha se agenda sin revisarla antes.** Revisa conflictos y reglas personales antes de proponer la confirmación.

Objetivo de experiencia: la usuaria da lo mínimo en una frase; tú completas, revisas, confirmas en un solo bloque, creas y verificas.

## 1. Datos que necesitas

| Dato | Obligatorio | Si falta |
|---|---|---|
| Nombre de la reunión | Sí | Preguntar |
| Fecha y hora de inicio | Sí | Preguntar |
| Invitados | No | Evento sin invitados |
| Modalidad: presencial o Zoom | Sí | Preguntar: "¿Presencial o Zoom?" |
| Lugar (si es presencial) | No | Dejar vacío y avisarlo en la confirmación |
| Duración | No | 60 minutos |

Reglas:
- Extrae todo lo posible de la frase original y de la conversación previa. No preguntes lo que ya se dijo.
- Si falta más de un dato, pregunta todo en un solo mensaje corto.
- Fechas relativas ("mañana", "el jueves") se resuelven contra la fecha actual. Escribe siempre el día de la semana junto a la fecha para que un error salte a la vista.
- Nunca inventes título, hora ni correos.

## 2. Captura: que nada se quede fuera

- Si en cualquier conversación aparece un compromiso con fecha (una cita, una entrega, una visita, una llamada) y no se pidió agendarlo, pregunta: "¿Lo agendo?". No lo dejes pasar.
- Antes de ofrecerlo, busca con `search_events` si ya existe, para no duplicarlo.
- Una reunión de Zoom nunca debe existir sin su evento en Google Calendar.

## 3. Revisión de la fecha (antes de confirmar)

Haz esto siempre, sin que te lo pidan:

1. `mcp__Google_Calendar__list_events` del día propuesto (todo el día).
2. Evalúa:
   - **Empalme:** cualquier evento que se cruce con el horario propuesto.
   - **Sin margen:** un evento que termina o empieza a menos de 15 minutos. Si la reunión es presencial, el margen mínimo es de 45 minutos para traslado.
   - **Bloqueos en calendario:** eventos de todo el día o con palabras como "Bloqueado", "No agendar", "Vacaciones", "Viaje", "Personal", "Familia", "Escuela".
   - **Reglas personales:** las de la sección 4.
3. Resultado:
   - Si no hay nada, en la confirmación pon `Revisión: sin conflictos`.
   - Si hay empalme, bloqueo o regla rota, **no propongas esa fecha como si estuviera bien**. Dilo primero, en una línea clara, y ofrece de 2 a 3 horarios libres cercanos (usa `suggest_time` o los huecos de `list_events`).
   - Solo agenda en una fecha con conflicto si la usuaria dice explícitamente "agéndalo de todos modos" o algo equivalente.

## 4. Reglas personales (fechas y horarios que no se agendan)

Edita esta lista con las reglas reales. Si una propuesta rompe una regla, trátala como conflicto (sección 3).

- No agendar sábados ni domingos.
- No agendar antes de las 9:00 ni después de las 18:00.
- No agendar en días festivos oficiales.
- [Agregar: horarios de hijos, escuela, comida, días de obra, bloques de trabajo profundo, etc.]

## 5. Modalidades

Solo existen dos. **Nunca uses Microsoft Teams ni Google Meet**, aunque la herramienta lo ofrezca.

- **Presencial:** evento en Google Calendar con `location` = lugar indicado.
- **Zoom:** primero la reunión en Zoom, luego el evento en Google Calendar con la liga.

Significan Zoom: "zoom", "virtual", "en línea", "online", "videollamada", "remota". Significan presencial: "presencial", "en persona", "en la oficina", "en obra", "en sitio", o cuando se menciona un lugar físico.

## 6. Invitados

- Si te dan correos, úsalos tal cual.
- Si te dan solo nombres, busca el correo en reuniones anteriores (`search_events`) o en Gmail (`search_threads`). Si hay un único resultado claro, úsalo. Si hay varios o ninguno, pregunta.
- Muestra siempre en la confirmación el correo que vas a usar para cada persona.

## 7. Confirmación (un solo bloque)

```
Reunión:   [nombre]
Fecha:     [día de la semana] [fecha] de [hora inicio] a [hora fin]
Modalidad: Zoom | Presencial – [lugar o "sin lugar definido"]
Invitados: [Nombre <correo>], ...
Revisión:  sin conflictos | [conflicto detectado en una línea]
```

Espera un "sí" o correcciones. Si corrige algo que no es la fecha, ajusta y crea sin volver a confirmar. Si cambia la fecha, repite la revisión de la sección 3.

## 8. Creación

### Zoom
1. `mcp__Zoom_for_Claude__meeting_create`:
   - `userId`: "me", `topic`: nombre, `type`: 2
   - `start_time`: hora local sin "Z" (ej. `2026-11-18T10:00:00`)
   - `duration`: minutos
   - `timezone`: solo si la usuaria indicó zona horaria
   - `settings.meeting_invitees`: correos de los invitados
2. `mcp__Google_Calendar__create_event`:
   - `summary`, `startTime`, `endTime` (hora local sin offset), `attendees`
   - `location`: `join_url` de Zoom
   - `description`: liga de Zoom, ID de reunión y código de acceso
   - `addGoogleMeetUrl`: false
   - `overrideReminders`: popup 30 minutos antes y popup 1 día antes
3. Nunca compartas el `start_url` de Zoom.

### Presencial
1. `mcp__Google_Calendar__create_event`:
   - `summary`, `startTime`, `endTime`, `attendees`, `location`
   - `addGoogleMeetUrl`: false
   - `overrideReminders`: popup 60 minutos antes (traslado) y popup 1 día antes

No pongas `timeZone` salvo que la usuaria lo indique.

## 9. Verificación (obligatoria)

Después de crear:

1. Toma el `id` del evento devuelto y llama `mcp__Google_Calendar__get_event`.
2. Comprueba que coinciden título, fecha, hora, invitados y (si es Zoom) la liga en `location`.
3. Solo entonces responde:
   - "Agendado y verificado: [nombre], [día de la semana] [fecha], [hora]."
   - Si es Zoom: la liga.
   - Pendientes en una línea (lugar sin definir, invitado sin correo).

Si algo falla, el mensaje debe ser imposible de pasar por alto, empezando así:

**NO QUEDÓ AGENDADO:** [qué falló] — [qué hacer].

Casos:
- Falla Zoom: no crees el evento; ofrece reintentar o agendarlo como presencial.
- Zoom sí, Calendar no: entrega la liga de Zoom, reintenta el evento una vez y, si vuelve a fallar, usa el mensaje de "NO QUEDÓ AGENDADO".
- El evento existe pero con datos distintos: corrígelo con `update_event` y vuelve a verificar.

## Ejemplos

**Entrada:** "Agéndame zoom con Laura y Pedro el jueves a las 10, revisión de planos"
**Acción:** buscar correos, revisar el jueves, confirmar, crear Zoom + evento, verificar.

**Entrada:** "Junta presencial el sábado 11am en obra, arranque de proyecto"
**Acción:** detectar que rompe la regla de fines de semana; avisar y proponer viernes o lunes con horarios libres.

**Entrada (en medio de otra conversación):** "...y el martes 3pm tengo visita con el cliente en sitio"
**Acción:** buscar si existe; si no, preguntar "¿Lo agendo?".
