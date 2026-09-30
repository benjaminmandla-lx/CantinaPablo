import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from banco.database import criar_banco
from banco.seed import popular_banco
from telas.login import TelaLogin
from telas.principal import iniciar_app


def main():
    criar_banco()
    popular_banco()

    app = QApplication(sys.argv)

    caminho_estilo = Path(__file__).parent / "recursos" / "estilos" / "estilo.qss"
    with open(caminho_estilo, encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    login = TelaLogin(ao_logar=iniciar_app)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()