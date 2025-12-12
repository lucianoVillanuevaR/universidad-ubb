package vista;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class ListaTalleresView extends JFrame {

    private JTable tabla;
    private JTextField txtBuscar;
    private JButton btnBuscar;
    private JButton btnVolver;
    private JButton btnEliminar;
    private JButton btnEditar;
    private JButton btnExportarCSV;
    private JButton btnUnirme;

    public ListaTalleresView() {
        initComponents();
    }

    private void initComponents() {
        setTitle("Visualización de Talleres");
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setSize(950, 360);
        setLocationRelativeTo(null);

        tabla = new JTable(new DefaultTableModel(
                new Object[][]{},
                new String[]{"ID", "Nombre", "Descripción", "Cupos", "Horario", "Instructor"}
        ) {
            @Override public boolean isCellEditable(int r, int c) { return false; }
        });

        txtBuscar = new JTextField(25);
        btnBuscar = new JButton("Buscar");

        btnVolver = new JButton("Cerrar");
        btnEliminar = new JButton("Eliminar");
        btnEditar = new JButton("Editar");
        btnExportarCSV = new JButton("Exportar CSV");
        btnUnirme = new JButton("Unirme");

        JPanel panelTop = new JPanel(new FlowLayout(FlowLayout.LEFT));
        panelTop.add(new JLabel("Buscar:"));
        panelTop.add(txtBuscar);
        panelTop.add(btnBuscar);

        JPanel panelBotones = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        panelBotones.add(btnUnirme);
        panelBotones.add(btnExportarCSV);
        panelBotones.add(btnEditar);
        panelBotones.add(btnEliminar);
        panelBotones.add(btnVolver);

        setLayout(new BorderLayout());
        add(panelTop, BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        add(panelBotones, BorderLayout.SOUTH);
    }

    public JTable getTabla() { return tabla; }
    public JButton getBtnVolver() { return btnVolver; }
    public JTextField getTxtBuscar() { return txtBuscar; }
    public JButton getBtnBuscar() { return btnBuscar; }
    public JButton getBtnEliminar() { return btnEliminar; }
    public JButton getBtnEditar() { return btnEditar; }
    public JButton getBtnExportarCSV() { return btnExportarCSV; }
    public JButton getBtnUnirme() { return btnUnirme; }
}
