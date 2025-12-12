package modelo;

import java.io.Serializable;

public class Notificacion implements Serializable {
    private static final long serialVersionUID = 1L;

    private final int id;
    private final int tallerId;
    private final String mensaje;
    private final long fechaEpochMs;

    public Notificacion(int id, int tallerId, String mensaje, long fechaEpochMs) {
        this.id = id;
        this.tallerId = tallerId;
        this.mensaje = mensaje;
        this.fechaEpochMs = fechaEpochMs;
    }

    public int getId() { return id; }
    public int getTallerId() { return tallerId; }
    public String getMensaje() { return mensaje; }
    public long getFechaEpochMs() { return fechaEpochMs; }
}
