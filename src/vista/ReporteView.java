package vista;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class ReporteView extends JFrame {

    private JTable tablaResumen;
    private JTable tablaInscripciones;
    private JTable tablaNotificaciones;

    private JButton btnRefrescar;
    private JButton btnMarcarAsistencia;
    private JButton btnCerrar;

    public ReporteView() {
        initComponents();
    }

    private void initComponents() {
        setTitle("Reportes");
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setSize(1000, 520);
        setLocationRelativeTo(null);

        tablaResumen = new JTable(new DefaultTableModel(
                new Object[][]{},
                new String[]{"Taller", "Instructor", "Cupos Totales", "Ocupados", "En Espera"}
        ) { @Override public boolean isCellEditable(int r, int c) { return false; } });

        tablaInscripciones = new JTable(new DefaultTableModel(
                new Object[][]{},
                new String[]{"ID Inscripción", "Taller", "Persona", "Estado", "Asistió"}
        ) { @Override public boolean isCellEditable(int r, int c) { return false; } });

        tablaNotificaciones = new JTable(new DefaultTableModel(
                new Object[][]{},
                new String[]{"Fecha (ms)", "TallerID", "Mensaje"}
        ) { @Override public boolean isCellEditable(int r, int c) { return false; } });

        JTabbedPane tabs = new JTabbedPane();
        tabs.addTab("Resumen Talleres", new JScrollPane(tablaResumen));
        tabs.addTab("Inscripciones", new JScrollPane(tablaInscripciones));
        tabs.addTab("Notificaciones", new JScrollPane(tablaNotificaciones));

        btnRefrescar = new JButton("Refrescar");
        btnMarcarAsistencia = new JButton("Marcar/Desmarcar asistencia");
        btnCerrar = new JButton("Cerrar");

        JPanel panelBotones = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        panelBotones.add(btnRefrescar);
        panelBotones.add(btnMarcarAsistencia);
        panelBotones.add(btnCerrar);

        setLayout(new BorderLayout(8, 8));
        add(tabs, BorderLayout.CENTER);
        add(panelBotones, BorderLayout.SOUTH);
    }

    public JTable getTablaResumen() { return tablaResumen; }
    public JTable getTablaInscripciones() { return tablaInscripciones; }
    public JTable getTablaNotificaciones() { return tablaNotificaciones; }

    public JButton getBtnRefrescar() { return btnRefrescar; }
    public JButton getBtnMarcarAsistencia() { return btnMarcarAsistencia; }
    public JButton getBtnCerrar() { return btnCerrar; }
}
