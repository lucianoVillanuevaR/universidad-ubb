package controlador;

import vista.MenuPrincipal;
import vista.TallerView;
import vista.ListaTalleresView;
import vista.ReporteView;

public class ControladorMenuPrincipal {

    private final MenuPrincipal menu;
    private final TallerView vistaRegistro;
    private final ListaTalleresView vistaLista;
    private final ListaTalleresController controladorLista;
    private final ReporteView vistaReporte;
    private final ReporteController controladorReporte;
    private boolean esAdmin = true;

    public ControladorMenuPrincipal(MenuPrincipal menu,
    TallerView vistaRegistro,
    ListaTalleresView vistaLista,
    ListaTalleresController controladorLista,
    ReporteView vistaReporte,
    ReporteController controladorReporte) {
        this.menu = menu;
        this.vistaRegistro = vistaRegistro;
        this.vistaLista = vistaLista;
        this.controladorLista = controladorLista;
        this.vistaReporte = vistaReporte;
        this.controladorReporte = controladorReporte;
        initController();
    }
    public void setEsAdmin(boolean esAdmin) {
        this.esAdmin = esAdmin;
        menu.getBtnGestionar().setEnabled(esAdmin);
    }
    private void initController() {
        menu.getBtnGestionar().addActionListener(e -> abrirRegistro());
        menu.getBtnVisualizar().addActionListener(e -> abrirVisualizacion());
        menu.getBtnReportes().addActionListener(e -> abrirReportes());
    }
    private void abrirRegistro() {
        if (!esAdmin) return;
        vistaRegistro.setVisible(true);
    }
    private void abrirVisualizacion() {
        controladorLista.refrescar();
        vistaLista.setVisible(true);
    }
    private void abrirReportes() {
        controladorReporte.refrescar();
        vistaReporte.setVisible(true);
    }
}
