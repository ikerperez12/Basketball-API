Nombre Proyecto:aplicacion_django-gomez_perez <https://github.com/GEI-PI-614G010492223/aplicacion_django-gomez_perez>
----------------

Breve descripción de la aplicación, y un listado de las funcionalidades más relevantes:
  Nuestra app es una web de estadisticas de la NBA.Realiza consultas a API-NBA para obtener estadisticas,jugadores y equipos. BingSearchImages para obtener imagenes
  para toda nuestra página web y Google Calendar API para guardar eventos relevantes

  En nuestra primera iteración, la version 0.1 implementa la vista PLAYERS:
  * Gestion de usuarios, para acceder a la página se necesita crear un usuario válido.
  * Se despliega una pagina home funcional, con barras de navegacion y footers comunes.
  * Si pulsamos en la pestaña players, podremos buscar un jugador por su nombre.Un ejemplo "Curry" y nos devolvera estadisticas del mismo.
  * Entre esas estadisticas, algunas como PER, se calculan con pandas, al igual que filtrado de columnas para borrar las no relevantes, limpiar datos para evitar
    nulos y calculo de medias.
  * Tambien se hace una llamada al API de Bing para obtener una imagen del jugador en cuestion
  * Matplotlib nos genera una grafica para las estadisticas, en estos momentos solo para los puntos por partido.

  Ademas, todas las otras vistas tienen funcionalidades basicas implementas:
  
  * Rankings devuelve una clasificación general y las clasificaciones por conferencias, correctamente ordenadas con pandas
  * Teams nos da una lista con todos los equipos actualmente activos en la NBA
  * Busqueda de Equipo nos permite buscar un equipo por su nombre o sus siglas, ej Boston o BOS y nos imprime su logo y los jugadores que conforman su plantilla  en la temporada actual.Se muestran como links, que deberian llevarnos a PLAYERS y ver las estadisticas de ese jugador, pero actualmente no está implementado esto

Integrantes Grupo:
------------------

  * Brais Gómez Espiñeira brais.gomez2@udc.es <brais.gomez2@udc.es>
  * Iker Pérez García <iker.perez@udc.es>
  * Rubén Cambeiro Oreiro <ruben.cambeiro.oreiro@udc.es>
  ...
  
Cómo ejecutar:
--------------

Secuencia de comandos (docker) para descargar y lanzar la aplicación:

1.-docker build -t proyect:prueba1 .
2.-docker run -p 8000:8000 proyect:prueba1
3.-http://localhost:8000
4.-Registrar un usuario
5.-Acceder a la vista PLAYERS que es la mas funcional

Funcionalidades de las diferentes vistas de la aplicación:
--------------
  HOME: Vista principal de la aplicación desde donde se podrá acceder a las demás vistas y funcionalidades
  LOGIN: El usuario podrá acceder a la aplicación, en caso de haberse registrado previamente, introduciendo su usuario y contraseña
  REGISTRO: El usuario podrá registrarse en la aplicación introduciendo un nombre de usuario, contraseña y confirmando la contraseña
  PLAYERS: El usuario introducirá un nombre y apellidos de un jugador, se le mostrará una serie de opciones que coincidan con su búsqueda, podrá seleccionar una y acceder a las estadísticas de ese jugador
  TEAMS: El usuario obtendrá una vista de todos los equipos de la NBA
  RANKING: El usuario podrá acceder a la clasificación tanto general como por conferencia
  BÚSQUEDA EQUIPO: El usuario podrá buscar un equipo por su nombre y acceder su lista de jugadores, a mayores se le mostrará el escudo de la franquicia y tendrá la opción de buscar donde está localizado su estadio

Problemas conocidos:
--------------------

Lista con los problemas conocidos si los hubiere:
  
  Version 0.1:
  * Buscar un jugador que no exista,o un nombre que no sea el apellido dara un error no controlado.Enviar el formulario en blanco tambien.
  * Las excepciones no estan debidamente gestionadas, pero esto es debido a que para implementar todo, estos errores eran muy útiles.
  * Alguna pestaña tiene fallos de CSS no corregidos