package vista;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class TallerView extends JFrame {

    private JTextField txtNombre;
    private JTextField txtDescripcion;
    private JTextField txtCupos;
    private JTextField txtHorario;
    private JTextField txtInstructor;
    private JButton btnAgregar; 
    private JButton btnActualizar;
    private JButton btnEliminar;
    private JButton btnLimpiar;

    private JTable tablaTalleres;

    public TallerView() {
        initComponents();
    }

    private void initComponents() {
        setTitle("Sistema de Talleres - Gestión (Admin)");
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setSize(900, 520);
        setLocationRelativeTo(null);

        JPanel panelFormulario = new JPanel(new GridLayout(5, 2, 6, 6));
        panelFormulario.setBorder(BorderFactory.createTitledBorder("Datos del Taller"));

        panelFormulario.add(new JLabel("Nombre:"));
        txtNombre = new JTextField();
        panelFormulario.add(txtNombre);

        panelFormulario.add(new JLabel("Descripción:"));
        txtDescripcion = new JTextField();
        panelFormulario.add(txtDescripcion);

        panelFormulario.add(new JLabel("Cupos:"));
        txtCupos = new JTextField();
        panelFormulario.add(txtCupos);

        panelFormulario.add(new JLabel("Horario:"));
        txtHorario = new JTextField();
        panelFormulario.add(txtHorario);

        panelFormulario.add(new JLabel("Instructor:"));
        txtInstructor = new JTextField();
        panelFormulario.add(txtInstructor);

        JPanel panelBotones = new JPanel(new FlowLayout(FlowLayout.LEFT));
        btnAgregar = new JButton("Guardar");
        btnActualizar = new JButton("Actualizar seleccionado");
        btnEliminar = new JButton("Eliminar seleccionado");
        btnLimpiar = new JButton("Limpiar");

        panelBotones.add(btnAgregar);
        panelBotones.add(btnActualizar);
        panelBotones.add(btnEliminar);
        panelBotones.add(btnLimpiar);

        JPanel panelSuperior = new JPanel(new BorderLayout(8, 8));
        panelSuperior.add(panelFormulario, BorderLayout.CENTER);
        panelSuperior.add(panelBotones, BorderLayout.SOUTH);

        tablaTalleres = new JTable(new DefaultTableModel(
                new Object[][]{},
                new String[]{"ID", "Nombre", "Descripción", "Cupos", "Horario", "Instructor"}
        ) {
            @Override public boolean isCellEditable(int r, int c) { return false; }
        });

        JScrollPane scrollTabla = new JScrollPane(tablaTalleres);
        scrollTabla.setBorder(BorderFactory.createTitledBorder("Talleres registrados"));

        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, panelSuperior, scrollTabla);
        split.setResizeWeight(0.40);
        split.setDividerSize(8);

        setLayout(new BorderLayout());
        add(split, BorderLayout.CENTER);
    }
    public JTextField getTxtNombre() { return txtNombre; }
    public JTextField getTxtDescripcion() { return txtDescripcion; }
    public JTextField getTxtCupos() { return txtCupos; }
    public JTextField getTxtHorario() { return txtHorario; }
    public JTextField getTxtInstructor() { return txtInstructor; } // NUEVO

    public JButton getBtnAgregar() { return btnAgregar; }
    public JButton getBtnActualizar() { return btnActualizar; }
    public JButton getBtnEliminar() { return btnEliminar; }
    public JButton getBtnLimpiar() { return btnLimpiar; }

    public JTable getTablaTalleres() { return tablaTalleres; }
}
