package sistematalleresmvc;

import controlador.ControladorMenuPrincipal;
import controlador.ListaTalleresController;
import controlador.ReporteController;
import controlador.TallerController;
import modelo.Persistencia;
import modelo.TallerDAO;
import vista.ListaTalleresView;
import vista.MenuPrincipal;
import vista.ReporteView;
import vista.TallerView;
import javax.swing.*;

public class SistemaTalleresMVC {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            // DAO
            Persistencia p = new Persistencia("datos_talleres.dat");
            TallerDAO dao = new TallerDAO(p);
            // Login simple (roles)
            boolean esAdmin = mostrarLogin();
            // Vistas
            MenuPrincipal menu = new MenuPrincipal();
            TallerView vistaTaller = new TallerView();
            ListaTalleresView vistaLista = new ListaTalleresView();
            ReporteView vistaReporte = new ReporteView();
            // Controladores
            TallerController tallerController = new TallerController(vistaTaller, dao);
            ListaTalleresController listaController = new ListaTalleresController(vistaLista, dao);
            ReporteController reporteController = new ReporteController(vistaReporte, dao);
            //Permisos
            tallerController.setEsAdmin(esAdmin);
            listaController.setEsAdmin(esAdmin);
            reporteController.setEsAdmin(esAdmin);
            menu.setRolTexto(esAdmin ? "Administrador" : "Usuario");
            //Menu
            ControladorMenuPrincipal menuController = new ControladorMenuPrincipal(
                    menu, vistaTaller, vistaLista, listaController, vistaReporte, reporteController
            );
            menuController.setEsAdmin(esAdmin);

            menu.setVisible(true);
        });
    }

    private static boolean mostrarLogin() {
        String[] opciones = {"Administrador", "Usuario"};
        int sel = JOptionPane.showOptionDialog(
                null,
                "Seleccione el tipo de usuario para ingresar:",
                "Login",
                JOptionPane.DEFAULT_OPTION,
                JOptionPane.QUESTION_MESSAGE,
                null,
                opciones,
                opciones[1]
        );

        // entra como usuario
        if (sel != 0) return false;

        JPasswordField pass = new JPasswordField();
        int ok = JOptionPane.showConfirmDialog(
                null,
                pass,
                "Clave de administrador",
                JOptionPane.OK_CANCEL_OPTION,
                JOptionPane.PLAIN_MESSAGE
        );

        if (ok != JOptionPane.OK_OPTION) return false;
        String clave = new String(pass.getPassword());
        if ("admin".equals(clave)) return true;
        JOptionPane.showMessageDialog(null, "Clave incorrecta. Se ingresará como Usuario.", "Aviso", JOptionPane.WARNING_MESSAGE);
        return false;
    }
}
