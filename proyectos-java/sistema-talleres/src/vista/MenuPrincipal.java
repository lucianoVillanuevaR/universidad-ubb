package vista;

import javax.swing.*;
import java.awt.*;

public class MenuPrincipal extends JFrame {

    private JButton btnGestionar;
    private JButton btnVisualizar;
    private JButton btnReportes;
    private JLabel lblRol;

    public MenuPrincipal() {
        initComponents();
    }

    private void initComponents() {
        setTitle("Menú Principal - Sistema de Talleres");
        setSize(400, 200);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        lblRol = new JLabel("Rol: -");

        btnGestionar = new JButton("Registrar / Gestionar talleres");
        btnVisualizar = new JButton("Visualizar lista de talleres");
        btnReportes = new JButton("Reportes");

        setLayout(new GridLayout(4, 1, 10, 10));
        add(lblRol);
        add(btnGestionar);
        add(btnVisualizar);
        add(btnReportes);
    }

    public JButton getBtnGestionar() {
        return btnGestionar;
    }

    public JButton getBtnVisualizar() {
        return btnVisualizar;
    }

    public JButton getBtnReportes() {
        return btnReportes;
    }

    public void setRolTexto(String rol) {
        lblRol.setText("Rol: " + rol);
    }
}
