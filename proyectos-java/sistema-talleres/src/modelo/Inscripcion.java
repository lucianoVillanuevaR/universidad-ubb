package modelo;

import java.io.Serializable;

public class Inscripcion implements Serializable {
    private static final long serialVersionUID = 2L;

    public enum Estado { INSCRITO, EN_ESPERA }

    private final int id;
    private final int tallerId;
    private final String nombrePersona;
    private final Estado estado;
    private boolean asistio = false;
    private final long fechaEpochMs;

    public Inscripcion(int id, int tallerId, String nombrePersona, Estado estado) {
        this.id = id;
        this.tallerId = tallerId;
        this.nombrePersona = nombrePersona;
        this.estado = estado;
        this.fechaEpochMs = System.currentTimeMillis();
    }

    public int getId() { return id; }
    public int getTallerId() { return tallerId; }
    public String getNombrePersona() { return nombrePersona; }
    public Estado getEstado() { return estado; }

    public boolean isAsistio() { return asistio; }
    public void setAsistio(boolean asistio) { this.asistio = asistio; }

    public long getFechaEpochMs() { return fechaEpochMs; }
}
