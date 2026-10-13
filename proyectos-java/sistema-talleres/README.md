# SistemaTalleresMVC

Aplicacion de escritorio (Swing, MVC) para gestionar talleres con inscripciones, lista de espera y reportes.

## Requisitos
- Java 17
- Apache Ant (o NetBeans con soporte Ant)

## Como ejecutar (CLI)
1. Ubicate en la raiz del proyecto:
   ```
   cd SistemaTalleresMVC
   ```
2. Construir y ejecutar:
   ```
   ant clean run
   ```
   Esto usa el main `sistematalleresmvc.SistemaTalleresMVC` configurado por NetBeans.

Para generar el JAR ejecutable:
```
ant clean jar
java -jar dist/SistemaTalleresMVC.jar
```

## Ejecucion en NetBeans
1. Abrir el proyecto existente (build.xml y nbproject ya incluidos).
2. Elegir Java 17 como plataforma.
3. Run Project.

## Roles y acceso
- Administrador: elegir "Administrador" en el login y usar clave `admin`.
- Usuario: elegir "Usuario". Acceso solo lectura y sin marcar asistencia.

## Funcionalidades principales
- CRUD de talleres (nombre, descripcion, cupos, horario, instructor).
- Busqueda y exportacion a CSV de la tabla de talleres.
- Inscripcion a talleres con control de cupos y lista de espera, notificaciones de cambios.
- Reportes: resumen de cupos, inscripciones, historial de notificaciones; marcado de asistencia (solo admin).

## Persistencia de datos
- Los datos se guardan en `datos_talleres.dat` en la raiz del proyecto (excluido en .gitignore). Se crea automaticamente al ejecutar.

## Estructura
- `src/sistematalleresmvc/` main y arranque.
- `src/modelo/` entidades, DAO y persistencia.
- `src/controlador/` logica de UI.
- `src/vista/` ventanas Swing.

## Notas
- Finales de linea: Git puede convertir LF/CRLF automaticamente en Windows; los avisos son informativos.
