package modelo;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class DataStore implements Serializable {
    private static final long serialVersionUID = 2L;

    public int ultimoTallerId = 0;
    public int ultimoInscripcionId = 0;

    // notificaciones
    public int ultimoNotificacionId = 0;
    public List<Taller> talleres = new ArrayList<>();
    public List<Inscripcion> inscripciones = new ArrayList<>();
    // notificaciones
    public List<Notificacion> notificaciones = new ArrayList<>();
}
