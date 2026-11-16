---
name: agendar-reunion
description: Agenda reuniones y bloqueos en el calendario de Outlook (fernanda@svatek.co) de forma rápida y segura, con nombre, invitados y modalidad (presencial o Zoom). Revisa conflictos en Outlook y en Google Calendar antes de agendar, y verifica que el evento realmente quedó en el calendario. Nunca usa Teams ni Google Meet. Úsalo cuando la usuaria diga "agenda", "agéndame", "pon en mi calendario", "bloquea", "programa una reunión", "cita con...", "junta con...", "zoom con...", y también cuando en la conversación aparezca un compromiso con fecha y hora que todavía no esté en el calendario.
---

# Agendar reunión

Dos principios mandan sobre todo lo demás:

1. **Si no está en el calendario, no existe.** Nunca digas "agendado" si no comprobaste que el evento existe en Outlook.
2. **Ninguna fecha se agenda sin revisarla antes.** Revisa conflictos y reglas personales antes de proponer la confirmación.

Objetivo de experiencia: la usuaria da lo mínimo en una frase; tú completas, revisas, confirmas en un solo bloque, creas y verificas.

## 0. Calendarios

| Calendario | Cuenta | Uso |
|---|---|---|
| **Outlook (principal)** | fernanda@svatek.co | Aquí se crea todo: reuniones y bloqueos personales |
| Google Calendar ("Fer personal") | cuenta personal de Gmail | Solo se consulta para detectar conflictos. Se escribe aquí únicamente si la usuaria lo pide |

Herramientas: `mcp__Microsoft_365__outlook_calendar_search`, `outlook_create_event`, `outlook_update_event`, y `mcp__Google_Calendar__list_events` para la consulta personal.

## 1. Datos que necesitas

| Dato | Obligatorio | Si falta |
|---|---|---|
| Nombre de la reunión | Sí | Preguntar |
| Fecha y hora de inicio | Sí | Preguntar |
| Invitados | No | Evento sin invitados |
| Modalidad: presencial o Zoom | Sí, si hay invitados | Preguntar: "¿Presencial o Zoom?" |
| Lugar (si es presencial) | No | Dejar vacío y avisarlo en la confirmación |
| Duración | No | 60 minutos |

Reglas:
- Extrae todo lo posible de la frase original y de la conversación previa. No preguntes lo que ya se dijo.
- Si falta más de un dato, pregunta todo en un solo mensaje corto.
- Fechas relativas ("mañana", "el jueves") se resuelven contra la fecha actual. Escribe siempre el día de la semana junto a la fecha.
- Zona horaria por defecto: `America/Mexico_City`, salvo que la usuaria indique otra.
- Nunca inventes título, hora ni correos.

**Bloqueos personales** (niños, médico, trámites, traslados): no llevan invitados ni modalidad. Se crean con `showAs: busy` y `sensitivity: private` para que el equipo vea "ocupado" sin ver el detalle.

## 2. Captura: que nada se quede fuera

- Si en cualquier conversación aparece un compromiso con fecha (cita, entrega, visita, llamada) y no se pidió agendarlo, pregunta: "¿Lo agendo?".
- Antes de ofrecerlo, busca en Outlook si ya existe, para no duplicarlo.
- Una reunión de Zoom nunca debe existir sin su evento en Outlook.

## 3. Revisión de la fecha (antes de confirmar)

Haz esto siempre, sin que te lo pidan:

1. Consulta el día completo en **ambos** calendarios:
   - Outlook: `outlook_calendar_search` con `query: "*"`, `afterDateTime` y `beforeDateTime` del día, `order: "oldest"`.
   - Google: `list_events` del mismo día.
2. Evalúa:
   - **Empalme:** cualquier evento que se cruce con el horario propuesto, incluidos los marcados como "tentative" (se reportan, aunque sean tentativos).
   - **Sin margen:** un evento que termina o empieza a menos de 15 minutos. Si es presencial, el margen mínimo es de 45 minutos para traslado.
   - **Bloqueos:** eventos de todo el día, eventos con `showAs: busy` u `oof`, o con palabras como "Bloqueado", "No agendar", "Vacaciones", "Viaje", "Personal", "Familia", "Escuela", "Niños".
   - **Reglas personales:** las de la sección 4.
   - Ignora eventos marcados como libres/transparentes (por ejemplo, estancias de hospedaje).
3. Resultado:
   - Si no hay nada, en la confirmación pon `Revisión: sin conflictos (Outlook y Google)`.
   - Si hay empalme, bloqueo o regla rota, dilo primero, en una línea clara, y ofrece de 2 a 3 horarios libres cercanos.
   - Solo agenda en una fecha con conflicto si la usuaria dice explícitamente "agéndalo de todos modos". Excepción: un bloqueo personal obligatorio (niños, salud) se crea igual y se reporta el conflicto para que ella decida qué mover.

## 4. Reglas personales (fechas y horarios que no se agendan)

Pendiente de confirmar con la usuaria. Si una propuesta rompe una regla, trátala como conflicto.

- No agendar sábados ni domingos.
- No agendar antes de las 9:00 ni después de las 18:00.
- No agendar en días festivos oficiales.
- [Agregar: horarios de hijos, escuela, comida, días de obra, bloques de trabajo profundo, etc.]

## 5. Modalidades

Solo existen dos. **Nunca uses Microsoft Teams ni Google Meet.**

- En `outlook_create_event`, **siempre** `isOnlineMeeting: false`. Si se pone en `true` crea un Teams que no se puede quitar.
- **Presencial:** `location` = lugar indicado.
- **Zoom:** primero la reunión en Zoom, luego el evento en Outlook con la liga.

Significan Zoom: "zoom", "virtual", "en línea", "online", "videollamada", "remota". Significan presencial: "presencial", "en persona", "en la oficina", "en obra", "en sitio", o cuando se menciona un lugar físico.

## 6. Invitados

- Si te dan correos, úsalos tal cual.
- Si te dan solo nombres, busca el correo en reuniones anteriores de Outlook (`outlook_calendar_search` con `attendee`) o en el correo (`mcp__Microsoft_365__search_people`). Si hay un único resultado claro, úsalo. Si hay varios o ninguno, pregunta.
- Muestra siempre en la confirmación el correo que vas a usar para cada persona.

## 7. Confirmación (un solo bloque)

```
Reunión:   [nombre]
Fecha:     [día de la semana] [fecha] de [hora inicio] a [hora fin]
Modalidad: Zoom | Presencial – [lugar o "sin lugar definido"] | Bloqueo personal
Invitados: [Nombre <correo>], ...
Revisión:  sin conflictos (Outlook y Google) | [conflicto detectado en una línea]
```

Espera un "sí" o correcciones. Si corrige algo que no es la fecha, ajusta y crea sin volver a confirmar. Si cambia la fecha, repite la revisión.

Los bloqueos personales sin invitados que la usuaria pide de forma directa ("agéndame X el viernes de 2:30 a 8") se pueden crear sin confirmación previa, siempre que se reporten los conflictos al terminar.

## 8. Creación

### Zoom
1. `mcp__Zoom_for_Claude__meeting_create`:
   - `userId`: "me", `topic`: nombre, `type`: 2
   - `start_time`: hora local sin "Z" (ej. `2026-11-18T10:00:00`)
   - `timezone`: `America/Mexico_City` (o la que indique la usuaria)
   - `duration`: minutos
   - `settings.meeting_invitees`: correos de los invitados
2. `mcp__Microsoft_365__outlook_create_event`:
   - `subject`, `start` y `end` como `{dateTime, timeZone: "America/Mexico_City"}`
   - `attendees`: invitados
   - `location`: "Zoom"
   - `body`: liga de Zoom, ID de reunión y código de acceso
   - `isOnlineMeeting`: false
   - `showAs`: busy
3. Nunca compartas el `start_url` de Zoom.

### Presencial
1. `outlook_create_event` con `subject`, `start`, `end`, `attendees`, `location`, `isOnlineMeeting: false`, `showAs: busy`.

### Bloqueo personal
1. `outlook_create_event` con `subject`, `start`, `end`, `body` breve, `showAs: busy`, `sensitivity: private`, `isOnlineMeeting: false`.

## 9. Verificación (obligatoria)

Después de crear:

1. Busca el evento en Outlook con `outlook_calendar_search` (por título y fecha).
2. Comprueba que coinciden título, fecha, hora, invitados y (si es Zoom) la liga en el cuerpo.
3. Solo entonces responde:
   - "Agendado y verificado en Outlook: [nombre], [día de la semana] [fecha], [hora]."
   - Si es Zoom: la liga.
   - Conflictos o pendientes en una línea cada uno.

Si algo falla, el mensaje debe empezar así:

**NO QUEDÓ AGENDADO:** [qué falló] — [qué hacer].

Casos:
- Falla Zoom: no crees el evento; ofrece reintentar o agendarlo como presencial.
- Zoom sí, Outlook no: entrega la liga, reintenta el evento una vez y, si vuelve a fallar, usa el mensaje de "NO QUEDÓ AGENDADO".
- El evento existe pero con datos distintos: corrígelo con `outlook_update_event` y vuelve a verificar.

## Ejemplos

**Entrada:** "Agéndame zoom con Laura y Pedro el jueves a las 10, revisión de planos"
**Acción:** buscar correos, revisar el jueves en ambos calendarios, confirmar, crear Zoom + evento en Outlook, verificar.

**Entrada:** "Junta presencial el sábado 11am en obra, arranque de proyecto"
**Acción:** detectar que rompe la regla de fines de semana; avisar y proponer viernes o lunes con horarios libres.

**Entrada:** "Agéndame el viernes de 2:30 a 8, recojo a los niños"
**Acción:** bloqueo personal; crear en Outlook (privado, ocupado), verificar y reportar cualquier empalme.
