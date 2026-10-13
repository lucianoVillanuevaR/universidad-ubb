package modelo;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class TallerDAO {
    private final Persistencia persistencia;
    private final DataStore data;

    public TallerDAO(Persistencia persistencia) {
        this.persistencia = persistencia;
        this.data = persistencia.cargar();
    }

    // talleres
    public Taller crearTaller(String nombre, String descripcion, int cuposTotal, String horario, String instructor) {
        data.ultimoTallerId++;
        Taller t = new Taller(data.ultimoTallerId, nombre, descripcion, cuposTotal, horario, instructor);
        data.talleres.add(t);
        persistencia.guardar(data);
        return t;
    }

    public boolean actualizarTaller(int id, String nombre, String descripcion, int cuposTotal, String horario, String instructor) {
        Taller t = buscarPorId(id);
        if (t == null) return false;

        String horarioAnterior = t.getHorario();
        int cuposAnterior = t.getCuposTotal();

        t.setNombre(nombre);
        t.setDescripcion(descripcion);
        t.setCuposTotal(cuposTotal);
        t.setHorario(horario);
        t.setInstructor(instructor);

        // Notificaciones mínimas (historial)
        if (!horarioAnterior.equals(t.getHorario())) {
            registrarNotificacion(id, "Cambio de horario: '" + horarioAnterior + "' -> '" + t.getHorario() + "'");
        }
        if (cuposAnterior != t.getCuposTotal()) {
            registrarNotificacion(id, "Cambio de cupos: " + cuposAnterior + " -> " + t.getCuposTotal());
        }

        persistencia.guardar(data);
        return true;
    }

    public boolean eliminarPorId(int id) {
        boolean ok = data.talleres.removeIf(t -> t.getId() == id);
        if (ok) {
            data.inscripciones.removeIf(i -> i.getTallerId() == id);
            registrarNotificacion(id, "Taller eliminado.");
            persistencia.guardar(data);
        }
        return ok;
    }

    public List<Taller> obtenerTodos() {
        return new ArrayList<>(data.talleres);
    }
    public Taller buscarPorId(int id) {
        for (Taller t : data.talleres) if (t.getId() == id) return t;
        return null;
    }
    public List<Taller> buscar(String texto) {
        String q = (texto == null) ? "" : texto.trim().toLowerCase();
        if (q.isEmpty()) return obtenerTodos();
        return data.talleres.stream()
                .filter(t ->
                        t.getNombre().toLowerCase().contains(q) ||
                        t.getHorario().toLowerCase().contains(q) ||
                        t.getInstructor().toLowerCase().contains(q)
                )
                .collect(Collectors.toList());
    }

    // inscipciones 

    public int cuposOcupados(int tallerId) {
        int count = 0;
        for (Inscripcion i : data.inscripciones) {
            if (i.getTallerId() == tallerId && i.getEstado() == Inscripcion.Estado.INSCRITO) count++;
        }
        return count;
    }

    public int enEspera(int tallerId) {
        int count = 0;
        for (Inscripcion i : data.inscripciones) {
            if (i.getTallerId() == tallerId && i.getEstado() == Inscripcion.Estado.EN_ESPERA) count++;
        }
        return count;
    }

    public boolean yaInscrito(int tallerId, String nombrePersona) {
        String n = nombrePersona.trim().toLowerCase();
        for (Inscripcion i : data.inscripciones) {
            if (i.getTallerId() == tallerId && i.getNombrePersona().trim().toLowerCase().equals(n)) return true;
        }
        return false;
    }

    public Inscripcion inscribir(int tallerId, String nombrePersona) {
        Taller t = buscarPorId(tallerId);
        if (t == null) throw new IllegalArgumentException("Taller no existe");

        if (yaInscrito(tallerId, nombrePersona)) {
            throw new IllegalArgumentException("La persona ya está inscrita o en espera en este taller.");
        }

        data.ultimoInscripcionId++;
        int ocupados = cuposOcupados(tallerId);

        Inscripcion.Estado estado = (ocupados < t.getCuposTotal())
                ? Inscripcion.Estado.INSCRITO
                : Inscripcion.Estado.EN_ESPERA;

        Inscripcion ins = new Inscripcion(data.ultimoInscripcionId, tallerId, nombrePersona, estado);
        data.inscripciones.add(ins);

        registrarNotificacion(tallerId, "Nueva inscripción: " + nombrePersona + " (" + estado + ")");
        persistencia.guardar(data);
        return ins;
    }
    public List<Inscripcion> obtenerInscripciones() {
        return new ArrayList<>(data.inscripciones);
    }
    public List<Inscripcion> obtenerInscripcionesDeTaller(int tallerId) {
        return data.inscripciones.stream().filter(i -> i.getTallerId() == tallerId).collect(Collectors.toList());
    }

    public Inscripcion buscarInscripcionPorId(int idIns) {
        for (Inscripcion i : data.inscripciones) if (i.getId() == idIns) return i;
        return null;
    }

    public boolean marcarAsistencia(int idInscripcion, boolean asistio) {
        Inscripcion i = buscarInscripcionPorId(idInscripcion);
        if (i == null) return false;
        i.setAsistio(asistio);
        persistencia.guardar(data);
        return true;
    }
    private void registrarNotificacion(int tallerId, String mensaje) {
        data.ultimoNotificacionId++;
        data.notificaciones.add(new Notificacion(
                data.ultimoNotificacionId,
                tallerId,
                mensaje,
                System.currentTimeMillis()
        ));
    }
    public List<Notificacion> obtenerNotificaciones() {
        return new ArrayList<>(data.notificaciones);
    }
    public DataStore getDataStore() { return data; }
}
