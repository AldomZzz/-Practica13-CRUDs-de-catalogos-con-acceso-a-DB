import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
    QDialog, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="oxxo",
    port=3306
)
cursor = conn.cursor()

# Colores OXXO
COLOR_ROJO = "#D91E18"
COLOR_AMARILLO = "#FFC300"
COLOR_BLANCO = "#FFFFFF"
COLOR_FONDO = "#F2F2F2"

def center_window(window, parent=None):
    # Asegurarse de que la ventana tiene su tamaño final
    window.adjustSize()
    
    # Obtener geometría de la ventana
    qr = window.frameGeometry()
    
    if parent is None:
        # Centrado en pantalla
        screen_geometry = window.screen().availableGeometry()
        
        # Verificar si la ventana es más grande que la pantalla disponible
        if qr.width() > screen_geometry.width():
            qr.setWidth(screen_geometry.width())
        if qr.height() > screen_geometry.height():
            qr.setHeight(screen_geometry.height())
            
        cp = screen_geometry.center()
    else:
        # Centrado relativo al padre
        parent_geometry = parent.frameGeometry()
        cp = parent_geometry.center()
        
        # Verificar que la ventana no se salga de la pantalla del padre
        screen_geometry = parent.screen().availableGeometry()
        right_edge = cp.x() + qr.width()/2
        left_edge = cp.x() - qr.width()/2
        bottom_edge = cp.y() + qr.height()/2
        top_edge = cp.y() - qr.height()/2
        
        if right_edge > screen_geometry.right():
            cp.setX(screen_geometry.right() - qr.width()/2)
        if left_edge < screen_geometry.left():
            cp.setX(screen_geometry.left() + qr.width()/2)
        if bottom_edge > screen_geometry.bottom():
            cp.setY(screen_geometry.bottom() - qr.height()/2)
        if top_edge < screen_geometry.top():
            cp.setY(screen_geometry.top() + qr.height()/2)
    
    # Mover y ajustar la ventana
    qr.moveCenter(cp)
    window.move(qr.topLeft())
    
    # Asegurarse de que la ventana permanezca visible
    window_top_left = qr.topLeft()
    screen_top_left = screen_geometry.topLeft()
    
    if window_top_left.x() < screen_top_left.x():
        window.move(screen_top_left.x(), window_top_left.y())
    if window_top_left.y() < screen_top_left.y():
        window.move(window_top_left.x(), screen_top_left.y())

class ConsultaCategoriasWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Consulta de Categorías - OXXO")
        self.setGeometry(150, 150, 540, 440)
        self.setStyleSheet(f"background-color: {COLOR_FONDO}; border-radius: 16px;")

        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(18, 18, 18, 18)

        lbl_titulo = QLabel("LISTADO DE CATEGORÍAS")
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet(f"color: {COLOR_ROJO}; letter-spacing: 2px;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)

        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        linea.setStyleSheet(f"color: {COLOR_AMARILLO};")
        layout.addWidget(linea)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.lbl_resultados = QLabel()
        self.lbl_resultados.setWordWrap(True)
        self.lbl_resultados.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.lbl_resultados.setFont(QFont("Courier New", 10))
        self.lbl_resultados.setStyleSheet(
            f"""
            color: black;  /* Cambiado a negro */
            background-color: {COLOR_BLANCO};
            padding: 18px;
            border: 2px solid {COLOR_ROJO};
            border-radius: 10px;
            """
        )

        scroll.setWidget(self.lbl_resultados)
        layout.addWidget(scroll)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn_cerrar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AMARILLO};
                color: {COLOR_ROJO};
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background-color: #ffe066;
            }}
        """)
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.mostrar_categorias()
        center_window(self, parent)

    def mostrar_categorias(self):
        cursor.execute("SELECT * FROM categorias ORDER BY id_categoria")
        categorias = cursor.fetchall()

        texto = ""
        for cat in categorias:
            texto += (
                f"ID: {cat[0]}\n"
                f"Nombre: {cat[1]}\n"
                "------------------------\n"
            )

        self.lbl_resultados.setText(texto if texto else "No hay categorías registradas.")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Categorías - OXXO")
        self.setGeometry(500, 500, 480, 400)
        self.setStyleSheet(f"background-color: {COLOR_FONDO}; border-radius: 18px;")

        self.init_ui()
        center_window(self)

    def init_ui(self):
        font_label = QFont("Arial", 12, QFont.Weight.Bold)
        font_input = QFont("Arial", 11)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(28, 22, 28, 22)

        # Logo OXXO (opcional)
        try:
            logo = QLabel()
            logo.setPixmap(QPixmap("oxxo_logo.png").scaled(240, 80, Qt.AspectRatioMode.KeepAspectRatio))
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(logo)
        except Exception:
            pass

        # Título
        titulo = QLabel("Gestión de Categorías")
        titulo.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        titulo.setStyleSheet(f"color: {COLOR_ROJO}; letter-spacing: 1.5px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo)

        # Línea divisoria
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        linea.setStyleSheet(f"color: {COLOR_AMARILLO};")
        main_layout.addWidget(linea)

        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(14)
        form_layout.setHorizontalSpacing(12)

        # ID Categoría
        self.lbl_id = QLabel("ID Categoría:")
        self.lbl_id.setFont(font_label)
        self.lbl_id.setStyleSheet(f"color: {COLOR_ROJO};")
        form_layout.addWidget(self.lbl_id, 0, 0)
        self.txt_id = QLineEdit()
        self.txt_id.setFont(font_input)
        self.txt_id.setPlaceholderText("Solo para actualizar/eliminar")
        self.txt_id.setStyleSheet("""
            background: #fff;
            border: 2px solid #D91E18;
            border-radius: 9px;
            padding: 7px 12px;
            color: black;
        """)
        form_layout.addWidget(self.txt_id, 0, 1)

        # Nombre
        self.lbl_nombre = QLabel("Nombre:")
        self.lbl_nombre.setFont(font_label)
        self.lbl_nombre.setStyleSheet(f"color: {COLOR_ROJO};")
        form_layout.addWidget(self.lbl_nombre, 1, 0)
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setFont(font_input)
        self.txt_nombre.setPlaceholderText("Nombre de la categoría")
        self.txt_nombre.setStyleSheet("""
            background: #fff;
            border: 1.5px solid #D91E18;
            border-radius: 9px;
            padding: 7px 12px;
            color: black;
        """)
        form_layout.addWidget(self.txt_nombre, 1, 1)

        main_layout.addLayout(form_layout)

        # Botones CRUD
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(18)

        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.setFont(font_label)
        self.btn_agregar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ROJO};
                color: {COLOR_BLANCO};
                border-radius: 10px;
                padding: 10px 22px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #a31510;
            }}
        """)
        btn_layout.addWidget(self.btn_agregar)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setFont(font_label)
        self.btn_actualizar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AMARILLO};
                color: {COLOR_ROJO};
                border-radius: 10px;
                padding: 10px 22px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ffe066;
            }}
        """)
        btn_layout.addWidget(self.btn_actualizar)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setFont(font_label)
        self.btn_eliminar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ROJO};
                color: {COLOR_BLANCO};
                border-radius: 10px;
                padding: 10px 22px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #a31510;
            }}
        """)
        btn_layout.addWidget(self.btn_eliminar)

        main_layout.addLayout(btn_layout)

        # Botón consultar
        self.btn_consultar = QPushButton("Consultar Categorías")
        self.btn_consultar.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.btn_consultar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AMARILLO};
                color: {COLOR_ROJO};
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
                margin-top: 18px;
            }}
            QPushButton:hover {{
                background-color: #ffe066;
            }}
        """)
        main_layout.addWidget(self.btn_consultar)

        self.setLayout(main_layout)

        # Conectar señales
        self.btn_agregar.clicked.connect(self.agregar_categoria)
        self.btn_actualizar.clicked.connect(self.actualizar_categoria)
        self.btn_eliminar.clicked.connect(self.eliminar_categoria)
        self.btn_consultar.clicked.connect(self.mostrar_consulta)

    def agregar_categoria(self):
        nombre = self.txt_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Advertencia", "El nombre es obligatorio")
            return

        try:
            cursor.execute(
                "INSERT INTO categorias (nombre) VALUES (%s)",
                (nombre,)
            )
            conn.commit()
            QMessageBox.information(self, "Éxito", "Categoría agregada")
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar: {str(e)}")

    def actualizar_categoria(self):
        id_cat = self.txt_id.text().strip()
        nombre = self.txt_nombre.text().strip()
        
        if not id_cat or not nombre:
            QMessageBox.warning(self, "Advertencia", "ID y nombre son obligatorios")
            return

        try:
            cursor.execute(
                "UPDATE categorias SET nombre = %s WHERE id_categoria = %s",
                (nombre, id_cat)
            )
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Advertencia", "No se encontró categoría con ese ID")
            else:
                conn.commit()
                QMessageBox.information(self, "Éxito", "Categoría actualizada")
                self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar: {str(e)}")

    def eliminar_categoria(self):
        id_cat = self.txt_id.text().strip()
        if not id_cat:
            QMessageBox.warning(self, "Advertencia", "Ingrese el ID de la categoría a eliminar")
            return

        confirmar = QMessageBox.question(
            self, "Confirmar",
            "¿Eliminar esta categoría?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                cursor.execute(
                    "DELETE FROM categorias WHERE id_categoria = %s",
                    (id_cat,)
                )
                if cursor.rowcount == 0:
                    QMessageBox.warning(self, "Advertencia", "No se encontró categoría con ese ID")
                else:
                    conn.commit()
                    QMessageBox.information(self, "Éxito", "Categoría eliminada")
                    self.limpiar_campos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")

    def limpiar_campos(self):
        self.txt_id.clear()
        self.txt_nombre.clear()

    def mostrar_consulta(self):
        consulta = ConsultaCategoriasWindow(self)
        consulta.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Estilo global mejorado
    app.setStyleSheet(f"""
        /* Estilo para QMessageBox */
        QMessageBox {{
            background-color: {COLOR_FONDO};
        }}
        QMessageBox QLabel {{
            color: black;
            font: 12px Arial;
        }}
        QMessageBox QPushButton {{
            background-color: {COLOR_AMARILLO};
            color: {COLOR_ROJO};
            border-radius: 5px;
            padding: 8px 15px;
            min-width: 80px;
            font-weight: bold;
        }}
        QMessageBox QPushButton:hover {{
            background-color: #ffe066;
        }}
    """)
    
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())