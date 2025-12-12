package modelo;

import java.io.Serializable;

public class Taller implements Serializable {
    private static final long serialVersionUID = 2L;

    private int id;
    private String nombre;
    private String descripcion;
    private int cuposTotal;
    private String horario;
    private String instructor; // NUEVO

    public Taller(int id, String nombre, String descripcion, int cuposTotal, String horario, String instructor) {
        setId(id);
        setNombre(nombre);
        setDescripcion(descripcion);
        setCuposTotal(cuposTotal);
        setHorario(horario);
        setInstructor(instructor);
    }

    public int getId() { return id; }
    public void setId(int id) {
        if (id <= 0) throw new IllegalArgumentException("ID inválido");
        this.id = id;
    }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) {
        if (nombre == null || nombre.trim().isEmpty()) throw new IllegalArgumentException("Nombre vacío");
        this.nombre = nombre.trim();
    }

    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) {
        if (descripcion == null || descripcion.trim().isEmpty()) throw new IllegalArgumentException("Descripción vacía");
        this.descripcion = descripcion.trim();
    }

    public int getCuposTotal() { return cuposTotal; }
    public void setCuposTotal(int cuposTotal) {
        if (cuposTotal <= 0) throw new IllegalArgumentException("Cupos deben ser > 0");
        this.cuposTotal = cuposTotal;
    }

    public String getHorario() { return horario; }
    public void setHorario(String horario) {
        if (horario == null || horario.trim().isEmpty()) throw new IllegalArgumentException("Horario vacío");
        this.horario = horario.trim();
    }

    public String getInstructor() { return instructor; }
    public void setInstructor(String instructor) {
        if (instructor == null || instructor.trim().isEmpty()) throw new IllegalArgumentException("Instructor vacío");
        this.instructor = instructor.trim();
    }
}
