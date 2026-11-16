---
name: agendar-reunion
description: Agenda reuniones en Google Calendar de forma rápida, con nombre, invitados y modalidad (presencial o Zoom). Si es Zoom, crea la liga de Zoom y la pone en el evento. Nunca usa Teams ni Google Meet. Úsalo cuando la usuaria diga "agenda", "agéndame", "pon en mi calendario", "programa una reunión", "cita con...", "junta con...", "zoom con...", o mencione una reunión con fecha y hora aunque no pida explícitamente agendarla.
---

# Agendar reunión

Objetivo: que agendar sea casi sin fricción. La usuaria da lo mínimo en una frase; tú completas el resto, confirmas en un solo bloque y creas el evento.

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
- Si falta más de un dato, pregunta todo en un solo mensaje corto, no uno por uno.
- Fechas relativas ("mañana", "el jueves", "la próxima semana") se resuelven contra la fecha actual. Si "el jueves" es ambiguo, toma el próximo jueves.
- Nunca inventes título, hora ni correos.

## 2. Modalidades

Solo existen dos. **Nunca uses Microsoft Teams ni Google Meet**, aunque la herramienta lo ofrezca.

- **Presencial**: evento en Google Calendar con `location` = dirección o lugar indicado.
- **Zoom**: primero crear la reunión en Zoom, luego el evento en Google Calendar con la liga.

Palabras que significan Zoom: "zoom", "virtual", "en línea", "online", "videollamada", "remota". Palabras que significan presencial: "presencial", "en persona", "en la oficina", "en obra", "en sitio", o cuando se menciona una dirección o lugar físico.

## 3. Invitados

- Si te dan correos, úsalos tal cual.
- Si te dan solo nombres, busca el correo en reuniones anteriores (`search_events` de Google Calendar) o en Gmail (`search_threads` con el nombre). Si hay un único resultado claro, úsalo. Si hay varios o ninguno, pregunta el correo.
- Muestra siempre en la confirmación el correo que vas a usar para cada persona.

## 4. Confirmación (un solo bloque)

Antes de crear nada, muestra esto y espera un "sí" (o correcciones):

```
Reunión:   [nombre]
Fecha:     [día de la semana, fecha] de [hora inicio] a [hora fin]
Modalidad: Zoom | Presencial – [lugar o "sin lugar definido"]
Invitados: [Nombre <correo>], ...
```

Si la usuaria corrige algo, ajusta y crea directamente, sin volver a confirmar.

## 5. Creación

### Zoom
1. `mcp__Zoom_for_Claude__meeting_create`:
   - `userId`: "me"
   - `topic`: nombre de la reunión
   - `type`: 2
   - `start_time`: hora local sin "Z" (ej. `2026-11-18T10:00:00`)
   - `duration`: minutos
   - `timezone`: solo si la usuaria indicó zona horaria; si no, omitir (Zoom usa la de su cuenta)
   - `settings.meeting_invitees`: correos de los invitados
2. `mcp__Google_Calendar__create_event`:
   - `summary`: nombre de la reunión
   - `startTime` / `endTime`: hora local sin offset
   - `attendees`: invitados
   - `location`: `join_url` de Zoom
   - `description`: liga de Zoom, ID de reunión y código de acceso
   - `addGoogleMeetUrl`: false
3. Nunca compartas el `start_url` de Zoom.

### Presencial
1. `mcp__Google_Calendar__create_event`:
   - `summary`, `startTime`, `endTime`, `attendees`
   - `location`: lugar indicado
   - `addGoogleMeetUrl`: false

En ambos casos, no pongas `timeZone` salvo que la usuaria lo indique.

## 6. Cierre

Responde en dos o tres líneas:
- "Agendado: [nombre], [día] [hora]."
- Si es Zoom: la liga de Zoom.
- Si algo quedó pendiente (lugar sin definir, invitado sin correo), menciónalo en una línea.

Si falla la creación en Zoom, no crees el evento en Calendar; explica el error y ofrece agendarlo como presencial o reintentar. Si Zoom se creó pero Calendar falló, entrega la liga de Zoom y ofrece reintentar el evento.

## Ejemplos

**Entrada:** "Agéndame zoom con Laura y Pedro el jueves a las 10, revisión de planos"
**Acción:** buscar correos de Laura y Pedro, confirmar en un bloque, crear Zoom + evento.

**Entrada:** "Junta presencial mañana 4pm en obra Polanco, arranque de proyecto"
**Acción:** sin invitados; confirmar, crear evento con location "Obra Polanco".

**Entrada:** "Pon reunión con el cliente el lunes"
**Acción:** preguntar en un mensaje: hora, presencial o Zoom, y correo del cliente.
