package controlador;

import modelo.Inscripcion;
import modelo.Notificacion;
import modelo.Taller;
import modelo.TallerDAO;
import vista.ReporteView;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.util.List;

public class ReporteController {

    private final ReporteView vista;
    private final TallerDAO dao;
    private boolean esAdmin = true;

    public ReporteController(ReporteView vista, TallerDAO dao) {
        this.vista = vista;
        this.dao = dao;
        init();
    }

    public void setEsAdmin(boolean esAdmin) {
        this.esAdmin = esAdmin;
        vista.getBtnMarcarAsistencia().setEnabled(esAdmin);
    }

    private void init() {
        vista.getBtnRefrescar().addActionListener(e -> refrescar());
        vista.getBtnMarcarAsistencia().addActionListener(e -> toggleAsistenciaSeleccionada());
        vista.getBtnCerrar().addActionListener(e -> vista.dispose());

        refrescar();
    }

    // compatibilidad con ControladorMenuPrincipal
    public void refrescar() {
        cargarResumen();
        cargarInscripciones();
        cargarNotificaciones();
    }

    private void cargarResumen() {
        DefaultTableModel m = (DefaultTableModel) vista.getTablaResumen().getModel();
        m.setRowCount(0);

        List<Taller> talleres = dao.obtenerTodos();
        for (Taller t : talleres) {
            int ocupados = dao.cuposOcupados(t.getId());
            int espera = dao.enEspera(t.getId());
            m.addRow(new Object[]{
                    t.getNombre(),
                    t.getInstructor(),
                    t.getCuposTotal(),
                    ocupados,
                    espera
            });
        }
    }

    private void cargarInscripciones() {
        DefaultTableModel m = (DefaultTableModel) vista.getTablaInscripciones().getModel();
        m.setRowCount(0);

        List<Inscripcion> ins = dao.obtenerInscripciones();
        for (Inscripcion i : ins) {
            Taller t = dao.buscarPorId(i.getTallerId());
            String nombreTaller = (t != null) ? t.getNombre() : ("ID " + i.getTallerId());

            m.addRow(new Object[]{
                    i.getId(),
                    nombreTaller,
                    i.getNombrePersona(),
                    i.getEstado().toString(),
                    i.isAsistio() ? "SI" : "NO"
            });
        }
    }

    private void cargarNotificaciones() {
        DefaultTableModel m = (DefaultTableModel) vista.getTablaNotificaciones().getModel();
        m.setRowCount(0);

        List<Notificacion> notis = dao.obtenerNotificaciones();
        for (Notificacion n : notis) {
            m.addRow(new Object[]{
                    n.getFechaEpochMs(),
                    n.getTallerId(),
                    n.getMensaje()
            });
        }
    }

    private void toggleAsistenciaSeleccionada() {
        if (!esAdmin) return;

        int fila = vista.getTablaInscripciones().getSelectedRow();
        if (fila == -1) {
            JOptionPane.showMessageDialog(vista, "Seleccione una inscripción en la pestaña Inscripciones.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int idIns = (int) vista.getTablaInscripciones().getValueAt(fila, 0);
        String asistioStr = String.valueOf(vista.getTablaInscripciones().getValueAt(fila, 4));
        boolean actual = "SI".equalsIgnoreCase(asistioStr);
        boolean nuevo = !actual;

        boolean ok = dao.marcarAsistencia(idIns, nuevo);
        if (ok) {
            JOptionPane.showMessageDialog(vista, "Asistencia actualizada.", "OK", JOptionPane.INFORMATION_MESSAGE);
            refrescar();
        } else {
            JOptionPane.showMessageDialog(vista, "No se encontró la inscripción.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
