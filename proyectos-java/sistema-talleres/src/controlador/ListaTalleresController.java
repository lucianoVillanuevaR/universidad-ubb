package controlador;

import modelo.Inscripcion;
import modelo.Taller;
import modelo.TallerDAO;
import vista.ListaTalleresView;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.io.File;
import java.io.FileWriter;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class ListaTalleresController {

    private final ListaTalleresView vista;
    private final TallerDAO dao;
    private boolean esAdmin = true;

    public ListaTalleresController(ListaTalleresView vista, TallerDAO dao) {
        this.vista = vista;
        this.dao = dao;
        init();
    }

    public void setEsAdmin(boolean esAdmin) {
        this.esAdmin = esAdmin;
        aplicarPermisos();
    }

    private void init() {
        refrescar();

        vista.getBtnBuscar().addActionListener(e -> buscar());
        vista.getTxtBuscar().addActionListener(e -> buscar());

        vista.getBtnEliminar().addActionListener(e -> eliminarSeleccionado());
        vista.getBtnEditar().addActionListener(e -> editarSeleccionado());
        vista.getBtnExportarCSV().addActionListener(e -> exportarCSV());

        vista.getBtnUnirme().addActionListener(e -> unirmeATaller());
        vista.getBtnVolver().addActionListener(e -> vista.dispose());

        aplicarPermisos();
    }

    private void aplicarPermisos() {
        vista.getBtnEliminar().setEnabled(esAdmin);
        vista.getBtnEditar().setEnabled(esAdmin);
        vista.getBtnUnirme().setEnabled(true);
    }

    public void refrescar() {
        cargarTabla(dao.obtenerTodos());
    }

    private void buscar() {
        String q = vista.getTxtBuscar().getText().trim();
        List<Taller> filtrados = dao.buscar(q);
        cargarTabla(filtrados);
    }

    private void unirmeATaller() {
        int fila = vista.getTabla().getSelectedRow();
        if (fila == -1) {
            JOptionPane.showMessageDialog(vista, "Seleccione un taller para unirse.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int tallerId = (int) vista.getTabla().getValueAt(fila, 0);

        String nombre = JOptionPane.showInputDialog(vista, "Ingrese su nombre para inscribirse:", "Unirse a Taller", JOptionPane.QUESTION_MESSAGE);
        if (nombre == null) return;
        nombre = nombre.trim();

        if (nombre.isEmpty()) {
            JOptionPane.showMessageDialog(vista, "El nombre no puede estar vacío.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        try {
            Inscripcion ins = dao.inscribir(tallerId, nombre);

            if (ins.getEstado() == Inscripcion.Estado.INSCRITO) {
                JOptionPane.showMessageDialog(vista, "Inscripción exitosa: quedaste INSCRITO.", "OK", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(vista, "No hay cupos: quedaste EN LISTA DE ESPERA.", "OK", JOptionPane.INFORMATION_MESSAGE);
            }

            buscar();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista, "No se pudo inscribir: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void eliminarSeleccionado() {
        if (!esAdmin) {
            JOptionPane.showMessageDialog(vista, "Acción no permitida para usuario estándar.", "Permisos", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int fila = vista.getTabla().getSelectedRow();
        if (fila == -1) {
            JOptionPane.showMessageDialog(vista, "Seleccione un taller.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int id = (int) vista.getTabla().getValueAt(fila, 0);
        int op = JOptionPane.showConfirmDialog(vista, "¿Eliminar el taller ID " + id + "?", "Confirmar", JOptionPane.YES_NO_OPTION);
        if (op == JOptionPane.YES_OPTION) {
            dao.eliminarPorId(id);
            JOptionPane.showMessageDialog(vista, "Taller eliminado.", "OK", JOptionPane.INFORMATION_MESSAGE);
            buscar();
        }
    }

    private void editarSeleccionado() {
        if (!esAdmin) {
            JOptionPane.showMessageDialog(vista, "Acción no permitida para usuario estándar.", "Permisos", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int fila = vista.getTabla().getSelectedRow();
        if (fila == -1) {
            JOptionPane.showMessageDialog(vista, "Seleccione un taller.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int id = (int) vista.getTabla().getValueAt(fila, 0);
        String nombre = String.valueOf(vista.getTabla().getValueAt(fila, 1));
        String desc = String.valueOf(vista.getTabla().getValueAt(fila, 2));
        String cuposStr = String.valueOf(vista.getTabla().getValueAt(fila, 3));
        String horario = String.valueOf(vista.getTabla().getValueAt(fila, 4));
        String instructor = String.valueOf(vista.getTabla().getValueAt(fila, 5));

        JTextField fNombre = new JTextField(nombre);
        JTextField fDesc = new JTextField(desc);
        JTextField fCupos = new JTextField(cuposStr);
        JTextField fHorario = new JTextField(horario);
        JTextField fInstructor = new JTextField(instructor);

        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.add(new JLabel("Nombre:")); panel.add(fNombre);
        panel.add(new JLabel("Descripción:")); panel.add(fDesc);
        panel.add(new JLabel("Cupos:")); panel.add(fCupos);
        panel.add(new JLabel("Horario:")); panel.add(fHorario);
        panel.add(new JLabel("Instructor:")); panel.add(fInstructor);

        int op = JOptionPane.showConfirmDialog(vista, panel, "Editar Taller (ID " + id + ")", JOptionPane.OK_CANCEL_OPTION);
        if (op != JOptionPane.OK_OPTION) return;

        String n = fNombre.getText().trim();
        String d = fDesc.getText().trim();
        String cText = fCupos.getText().trim();
        String h = fHorario.getText().trim();
        String inst = fInstructor.getText().trim();

        if (n.isEmpty() || d.isEmpty() || cText.isEmpty() || h.isEmpty() || inst.isEmpty()) {
            JOptionPane.showMessageDialog(vista, "Complete todos los campos.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        int cupos;
        try { cupos = Integer.parseInt(cText); }
        catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(vista, "Cupos debe ser un número entero.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }
        if (cupos <= 0) {
            JOptionPane.showMessageDialog(vista, "Los cupos deben ser mayores a 0.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        boolean ok = dao.actualizarTaller(id, n, d, cupos, h, inst);
        if (ok) {
            JOptionPane.showMessageDialog(vista, "Taller actualizado.", "OK", JOptionPane.INFORMATION_MESSAGE);
            buscar();
        } else {
            JOptionPane.showMessageDialog(vista, "No se pudo actualizar (ID no encontrado).", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void exportarCSV() {
        JFileChooser fc = new JFileChooser();
        fc.setDialogTitle("Guardar CSV");
        fc.setSelectedFile(new File("talleres.csv"));

        int result = fc.showSaveDialog(vista);
        if (result != JFileChooser.APPROVE_OPTION) return;

        File file = fc.getSelectedFile();
        try (FileWriter fw = new FileWriter(file, StandardCharsets.UTF_8)) {
            fw.write("ID,Nombre,Descripción,Cupos,Horario,Instructor\n");

            DefaultTableModel m = (DefaultTableModel) vista.getTabla().getModel();
            for (int r = 0; r < m.getRowCount(); r++) {
                fw.write(escape(m.getValueAt(r, 0)) + "," +
                        escape(m.getValueAt(r, 1)) + "," +
                        escape(m.getValueAt(r, 2)) + "," +
                        escape(m.getValueAt(r, 3)) + "," +
                        escape(m.getValueAt(r, 4)) + "," +
                        escape(m.getValueAt(r, 5)) + "\n");
            }
            JOptionPane.showMessageDialog(vista, "CSV exportado correctamente.", "OK", JOptionPane.INFORMATION_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista, "Error exportando CSV: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private String escape(Object o) {
        String s = String.valueOf(o);
        s = s.replace("\"", "\"\"");
        if (s.contains(",") || s.contains("\n") || s.contains("\r")) s = "\"" + s + "\"";
        return s;
    }

    private void cargarTabla(List<Taller> lista) {
        DefaultTableModel m = (DefaultTableModel) vista.getTabla().getModel();
        m.setRowCount(0);
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
