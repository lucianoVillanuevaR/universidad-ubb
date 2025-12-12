package modelo;

import java.io.*;

public class Persistencia {
    private final File archivo;
    public Persistencia(String nombreArchivo) {
        this.archivo = new File(nombreArchivo);
    }
    public DataStore cargar() {
        if (!archivo.exists()) return new DataStore();
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(archivo))) {
            Object obj = ois.readObject();
            return (DataStore) obj;
        } catch (Exception e) {
            return new DataStore();
        }
    }
    public void guardar(DataStore data) {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(archivo))) {
            oos.writeObject(data);
        } catch (IOException e) {
            throw new RuntimeException("Error guardando datos: " + e.getMessage());
        }
    }
}
