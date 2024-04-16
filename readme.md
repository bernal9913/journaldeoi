## proyecto idk de journals

Realizar una página web en Python + Flask que permita explorar o buscar en el catálogo de revistas.
La idea es poder encontrar revistas, ya sea explorando o mediante una búsqueda de texto, y desplegar al catálogo que pertenecen, así como su Factor de Impacto, Cuartil al que pertenecen (Q), y número de citas totales de acuerdo al sitio scimagojr.com
El sitio debe tener una vista profesional y utilizar los colores institucionales de la Universidad de Sonora.

* Sitio principal (Inicio):
* Barra de menú con logotipo de la Universidad
* Inicio
* Explorar
* Barra de Búsqueda
* Créditos
* Breve introducción al sitio
* Explorar
* Mostrar un abecedario con hipervínculos, que lleven a una sección con palabras que inicien con la letra seleccionada (las palabras provienen de los títulos de las revistas). Al dar click en una palabra, que muestre una nueva página que lista una tabla de revistas que contengan esa palabra. En el listado deben aparecer el título de la revista, así como los catálogos a los que pertenece y al menos su Factor de impacto. Al dar click en el nombre de la revista, deberá mostrar toda la información relacionada a ella.

* Búsqueda
* Mostrar una página con una tabla que liste todas las revistas que contengan las palabras buscadas (una operación de UNIÓN). En el listado deben aparecer el título de la revista, así como los catálogos a los que pertenece y al menos su Factor de impacto. Al dar click en el nombre de la revista, deberá mostrar toda la información relacionada a ella.

* Créditos
* Nombre de los alumnos que desarrollaron el sistema (y fotos tipo credencial sí así lo desean).

### Nota: Es necesario desarrollar un programa tipo web scrapper que visite el sitio de scimagojr.com, obtenga la información de las revistas en el catálogo general y guarde los datos en un archivo csv, el cual el sistema basado en Flask leerá para poder realizar las exploraciones. Una vez obtenida la información de una revista, no se debe volver a visitar (probar si existe la información en nuestro catálogo antes de visitar scimagojr.com). Pueden utilizar los programas catalogo y  dolar scrapper que desarrollamos en clase como base.


### Puntos extra:
* Mostrar un logotipo que personalice el sitio (además del logo de la universidad)
* Mostar más información sobre la revista (1 punto por elemento)
* Sitio web
* Subject Area and category
* Publisher
* ISSN
* Widget
* My work