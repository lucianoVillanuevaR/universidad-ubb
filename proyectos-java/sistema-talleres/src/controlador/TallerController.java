package controlador;

import modelo.Taller;
import modelo.TallerDAO;
import vista.TallerView;

import javax.swing.*;
import javax.swing.event.ListSelectionEvent;
import javax.swing.table.DefaultTableModel;
import java.util.List;

public class TallerController {

    private final TallerView vista;
    private final TallerDAO dao;
    private boolean esAdmin = true;

    public TallerController(TallerView vista, TallerDAO dao) {
        this.vista = vista;
        this.dao = dao;
        initController();
    }

    private void initController() {
        vista.getBtnAgregar().addActionListener(e -> guardarTaller());
        vista.getBtnActualizar().addActionListener(e -> actualizarSeleccionado());
        vista.getBtnEliminar().addActionListener(e -> eliminarSeleccionado());
        vista.getBtnLimpiar().addActionListener(e -> limpiarCampos());

        vista.getTablaTalleres().getSelectionModel().addListSelectionListener(this::onSeleccion);

        cargarTabla();
    }

    public void setEsAdmin(boolean esAdmin) {
        this.esAdmin = esAdmin;

        vista.getBtnAgregar().setEnabled(esAdmin);
        vista.getBtnActualizar().setEnabled(esAdmin);
        vista.getBtnEliminar().setEnabled(esAdmin);
        vista.getBtnLimpiar().setEnabled(esAdmin);

        vista.getTxtNombre().setEditable(esAdmin);
        vista.getTxtDescripcion().setEditable(esAdmin);
        vista.getTxtCupos().setEditable(esAdmin);
        vista.getTxtHorario().setEditable(esAdmin);
        vista.getTxtInstructor().setEditable(esAdmin);
    }

    private void onSeleccion(ListSelectionEvent e) {
        if (e.getValueIsAdjusting()) return;
        int fila = vista.getTablaTalleres().getSelectedRow();
        if (fila == -1) return;

        vista.getTxtNombre().setText(String.valueOf(vista.getTablaTalleres().getValueAt(fila, 1)));
        vista.getTxtDescripcion().setText(String.valueOf(vista.getTablaTalleres().getValueAt(fila, 2)));
        vista.getTxtCupos().setText(String.valueOf(vista.getTablaTalleres().getValueAt(fila, 3)));
        vista.getTxtHorario().setText(String.valueOf(vista.getTablaTalleres().getValueAt(fila, 4)));
        vista.getTxtInstructor().setText(String.valueOf(vista.getTablaTalleres().getValueAt(fila, 5)));
    }

    private void guardarTaller() {
        if (!esAdmin) return;

        String nombre = vista.getTxtNombre().getText().trim();
        String descripcion = vista.getTxtDescripcion().getText().trim();
        String cuposTexto = vista.getTxtCupos().getText().trim();
        String horario = vista.getTxtHorario().getText().trim();
        String instructor = vista.getTxtInstructor().getText().trim();

        if (nombre.isEmpty() || descripcion.isEmpty() || cuposTexto.isEmpty() || horario.isEmpty() || instructor.isEmpty()) {
            JOptionPane.showMessageDialog(vista, "Complete todos los campos.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        int cupos;
        try { cupos = Integer.parseInt(cuposTexto); }
        catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(vista, "Cupos debe ser un número entero.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }
        if (cupos <= 0) {
            JOptionPane.showMessageDialog(vista, "Los cupos deben ser mayores a 0.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        try {
            dao.crearTaller(nombre, descripcion, cupos, horario, instructor);
            JOptionPane.showMessageDialog(vista, "Taller guardado.", "OK", JOptionPane.INFORMATION_MESSAGE);
            cargarTabla();
            limpiarCampos();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista, "No se pudo guardar: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void actualizarSeleccionado() {
        if (!esAdmin) return;

        int fila = vista.getTablaTalleres().getSelectedRow();
        if (fila == -1) {
            JOptionPane.showMessageDialog(vista, "Seleccione un taller para actualizar.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int id = (int) vista.getTablaTalleres().getValueAt(fila, 0);

        String nombre = vista.getTxtNombre().getText().trim();
        String descripcion = vista.getTxtDescripcion().getText().trim();
        String cuposTexto = vista.getTxtCupos().getText().trim();
        String horario = vista.getTxtHorario().getText().trim();
        String instructor = vista.getTxtInstructor().getText().trim();

        if (nombre.isEmpty() || descripcion.isEmpty() || cuposTexto.isEmpty() || horario.isEmpty() || instructor.isEmpty()) {
            JOptionPane.showMessageDialog(vista, "Complete todos los campos.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        int cupos;
        try { cupos = Integer.parseInt(cuposTexto); }
        catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(vista, "Cupos debe ser un número entero.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }
        if (cupos <= 0) {
            JOptionPane.showMessageDialog(vista, "Los cupos deben ser mayores a 0.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        int op = JOptionPane.showConfirmDialog(vista, "¿Actualizar taller ID " + id + "?", "Confirmar", JOptionPane.YES_NO_OPTION);
        if (op != JOptionPane.YES_OPTION) return;

        boolean ok = dao.actualizarTaller(id, nombre, descripcion, cupos, horario, instructor);
        if (ok) {
            JOptionPane.showMessageDialog(vista, "Taller actualizado.", "OK", JOptionPane.INFORMATION_MESSAGE);
            cargarTabla();
            limpiarCampos();
        } else {
            JOptionPane.showMessageDialog(vista, "No se pudo actualizar.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void eliminarSeleccionado() {
        if (!esAdmin) return;

        int fila = vista.getTablaTalleres().getSelectedRow();
        if (fila == -1) {
            JOptionPane.showMessageDialog(vista, "Seleccione un taller para eliminar.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int id = (int) vista.getTablaTalleres().getValueAt(fila, 0);
        int op = JOptionPane.showConfirmDialog(vista, "¿Eliminar taller ID " + id + "?", "Confirmar", JOptionPane.YES_NO_OPTION);
        if (op != JOptionPane.YES_OPTION) return;

        boolean ok = dao.eliminarPorId(id);
        if (ok) {
            JOptionPane.showMessageDialog(vista, "Taller eliminado.", "OK", JOptionPane.INFORMATION_MESSAGE);
            cargarTabla();
            limpiarCampos();
        } else {
            JOptionPane.showMessageDialog(vista, "No se pudo eliminar.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void limpiarCampos() {
        vista.getTxtNombre().setText("");
        vista.getTxtDescripcion().setText("");
        vista.getTxtCupos().setText("");
        vista.getTxtHorario().setText("");
        vista.getTxtInstructor().setText("");
        vista.getTablaTalleres().clearSelection();
        vista.getTxtNombre().requestFocus();
    }

    private void cargarTabla() {
        DefaultTableModel m = (DefaultTableModel) vista.getTablaTalleres().getModel();
        m.setRowCount(0);

        List<Taller> lista = dao.obtenerTodos();
        for (Taller t : lista) {
            m.addRow(new Object[]{
                    t.getId(),
                    t.getNombre(),
                    t.getDescripcion(),
                    t.getCuposTotal(),
                    t.getHorario(),
                    t.getInstructor()
            });
        }
    }
}
