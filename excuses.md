## Lectura opcional

A continuación, voy a enumerar una serie de ítems que deberían responder a algunas preguntas de tipo **“¿Qué?”, “¿Por qué?” y “¿Por qué hizo eso? 😱”**

---

### ¿Por qué definí un archivo de "routes"?

Al comienzo del proyecto esperaba poder incluir una conexión a la base de datos, pensando que en un proyecto real todos los datos que iba a usar se tendrían que leer de una db. Pero luego de empezar con la lógica de los endpoints, me di cuenta de que me iba a tomar demasiado tiempo aprender:

- A usar Python
- A usar Pydantic
- A usar Flask
- A usar Langchain
- A usar Twilio
- A resolver cualquier problema con la lógica
- etc.

Por lo que decidí usar el `.csv` como base de datos, pero al final creo que hubiese sido mejor intentar investigar un poco… Me hubiese traído menos problemas relacionados al tipado y a leer los archivos 😅

---

### ¿Por qué la data de los usuarios se guarda en un JSON?

Por la misma razón: creí que sería más fácil que aprender a usar un ORM y linkearlo al proyecto. Pero esto lo decidí más sobre la hora porque ya no me daba el tiempo.  
Usar los JSONs no es la mejor decisión, pero tampoco me quejo a esta altura del test.

---

### ¿Por qué solo hay 2 modelos definidos?

Al principio decidí ser prolija y escribir clases con Pydantic para cada entidad… Hubo otras prioridades en el camino y ya no lo hice.

---