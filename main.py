import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QDialog, QScrollArea, QHBoxLayout, 
    QGridLayout, QFrame, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QSpinBox, QDoubleSpinBox, QInputDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPixmap

# Colores OXXO
COLOR_ROJO = "#D91E18"
COLOR_AMARILLO = "#FFC300"
COLOR_BLANCO = "#FFFFFF"
COLOR_FONDO = "#F2F2F2"

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="",
            database="oxxo",
        )
        return conexion
    except Exception as e:
        QMessageBox.critical(None, "Error de conexión", f"No se pudo conectar a la base de datos:\n{str(e)}")
        return None

def center_window(window, parent=None):
    window.adjustSize()
    qr = window.frameGeometry()
    
    if parent is None:
        screen_geometry = window.screen().availableGeometry()
        if qr.width() > screen_geometry.width():
            qr.setWidth(screen_geometry.width())
        if qr.height() > screen_geometry.height():
            qr.setHeight(screen_geometry.height())
        cp = screen_geometry.center()
    else:
        parent_geometry = parent.frameGeometry()
        cp = parent_geometry.center()
        
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
    
    qr.moveCenter(cp)
    window.move(qr.topLeft())
    
    window_top_left = qr.topLeft()
    screen_top_left = screen_geometry.topLeft()
    
    if window_top_left.x() < screen_top_left.x():
        window.move(screen_top_left.x(), window_top_left.y())
    if window_top_left.y() < screen_top_left.y():
        window.move(window_top_left.x(), screen_top_left.y())

class CRUDTemplate(QWidget):
    def __init__(self, conexion, table_name, columns, headers, title):
        super().__init__()
        self.conexion = conexion
        self.table_name = table_name
        self.columns = columns
        self.headers = headers
        self.setWindowTitle(f"CRUD {title} - OXXO")
        self.setStyleSheet(f"background-color: {COLOR_FONDO};")
        
        self.init_ui()
        self.cargar_datos()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        titulo = QLabel(f"GESTIÓN DE {self.table_name.upper()}")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setStyleSheet(f"color: {COLOR_ROJO};")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Línea divisoria
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        linea.setStyleSheet(f"color: {COLOR_AMARILLO};")
        layout.addWidget(linea)

        # Formulario
        self.form_inputs = []
        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(15)
        
        for i, (col, header) in enumerate(zip(self.columns, self.headers)):
            label = QLabel(header)
            label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            label.setStyleSheet(f"color: {COLOR_ROJO};")
            
            if "enum" in col.lower():
                combo = QComboBox()
                combo.setStyleSheet("""
                    background: #fff;
                    border: 2px solid #D91E18;
                    border-radius: 9px;
                    padding: 7px 12px;
                    color: #000000;
                """)
                enum_values = col.split("'")[1::2]
                combo.addItems(enum_values)
                self.form_inputs.append(combo)
                form_layout.addWidget(label, i, 0)
                form_layout.addWidget(combo, i, 1)
            elif "date" in col.lower():
                date_edit = QDateEdit()
                date_edit.setCalendarPopup(True)
                date_edit.setDate(QDate.currentDate())
                self.form_inputs.append(date_edit)
                form_layout.addWidget(label, i, 0)
                form_layout.addWidget(date_edit, i, 1)
            elif "decimal" in col.lower() or "float" in col.lower() or "double" in col.lower():
                spin = QDoubleSpinBox()
                spin.setMaximum(999999.99)
                self.form_inputs.append(spin)
                form_layout.addWidget(label, i, 0)
                form_layout.addWidget(spin, i, 1)
            elif "int" in col.lower():
                spin = QSpinBox()
                spin.setMaximum(999999)
                self.form_inputs.append(spin)
                form_layout.addWidget(label, i, 0)
                form_layout.addWidget(spin, i, 1)
            else:
                input_field = QLineEdit()
                input_field.setStyleSheet("""
                    background: #fff;
                    border: 2px solid #D91E18;
                    border-radius: 9px;
                    padding: 7px 12px;
                    color: #000000;  /* Texto negro */
                """)
                self.form_inputs.append(input_field)
                form_layout.addWidget(label, i, 0)
                form_layout.addWidget(input_field, i, 1)
        
        layout.addLayout(form_layout)

        # Botones CRUD
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ROJO};
                color: {COLOR_BLANCO};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #a31510;
            }}
        """)
        self.btn_agregar.clicked.connect(self.agregar)
        btn_layout.addWidget(self.btn_agregar)
        
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AMARILLO};
                color: {COLOR_ROJO};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ffe066;
            }}
        """)
        self.btn_actualizar.clicked.connect(self.actualizar)
        btn_layout.addWidget(self.btn_actualizar)
        
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ROJO};
                color: {COLOR_BLANCO};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #a31510;
            }}
        """)
        self.btn_eliminar.clicked.connect(self.eliminar)
        btn_layout.addWidget(self.btn_eliminar)
        
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AMARILLO};
                color: {COLOR_ROJO};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ffe066;
            }}
        """)
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        btn_layout.addWidget(self.btn_limpiar)
        
        layout.addLayout(btn_layout)

        # Tabla de datos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(len(self.headers))
        self.tabla.setHorizontalHeaderLabels(self.headers)
        self.tabla.setStyleSheet(f"""
    QTableWidget {{
        background-color: {COLOR_BLANCO};
        border: 2px solid {COLOR_ROJO};
        border-radius: 8px;
    }}
    QHeaderView::section {{
        background-color: {COLOR_ROJO};
        color: {COLOR_BLANCO};
        font-weight: bold;
        padding: 5px;
    }}
    QTableWidget::item {{
        color: #000000;  /* Texto negro */
    }}
    QTableWidget::item:selected {{
        background-color: {COLOR_AMARILLO};
        color: {COLOR_ROJO};
    }}
""")
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
    
    def cargar_datos(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            datos = cursor.fetchall()
            
            self.tabla.setRowCount(0)
            for fila_idx, fila in enumerate(datos):
                self.tabla.insertRow(fila_idx)
                for col_idx, valor in enumerate(fila):
                    self.tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))
            
            cursor.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos:\n{e}")
    
    def seleccionar_fila(self, fila):
        for col_idx in range(self.tabla.columnCount()):
            item = self.tabla.item(fila, col_idx)
            if item:
                if isinstance(self.form_inputs[col_idx], QComboBox):
                    index = self.form_inputs[col_idx].findText(item.text())
                    if index >= 0:
                        self.form_inputs[col_idx].setCurrentIndex(index)
                elif isinstance(self.form_inputs[col_idx], QDateEdit):
                    date = QDate.fromString(item.text(), "yyyy-MM-dd")
                    self.form_inputs[col_idx].setDate(date)
                elif isinstance(self.form_inputs[col_idx], (QSpinBox, QDoubleSpinBox)):
                    self.form_inputs[col_idx].setValue(float(item.text()))
                else:
                    self.form_inputs[col_idx].setText(item.text())
    
    def obtener_valores(self):
        valores = []
        for input_field in self.form_inputs:
            if isinstance(input_field, QComboBox):
                valores.append(input_field.currentText())
            elif isinstance(input_field, QDateEdit):
                valores.append(input_field.date().toString("yyyy-MM-dd"))
            elif isinstance(input_field, (QSpinBox, QDoubleSpinBox)):
                valores.append(input_field.value())
            else:
                valores.append(input_field.text())
        return valores
    
    def agregar(self):
        valores = self.obtener_valores()
        try:
            cursor = self.conexion.cursor()
            placeholders = ", ".join(["%s"] * len(valores))
            query = f"INSERT INTO {self.table_name} VALUES ({placeholders})"
            cursor.execute(query, valores)
            self.conexion.commit()
            cursor.close()
            QMessageBox.information(self, "Éxito", "Registro agregado correctamente")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el registro:\n{e}")
    
    def actualizar(self):
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un registro para actualizar")
            return
            
        id_col = 0  # Asumimos que la primera columna es el ID
        id_val = self.tabla.item(fila_seleccionada, id_col).text()
        
        valores = self.obtener_valores()
        set_clause = ", ".join([f"{self.columns[i]} = %s" for i in range(len(valores))])
        
        try:
            cursor = self.conexion.cursor()
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.columns[0]} = %s"
            cursor.execute(query, valores + [id_val])
            self.conexion.commit()
            cursor.close()
            QMessageBox.information(self, "Éxito", "Registro actualizado correctamente")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el registro:\n{e}")
    
    def eliminar(self):
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un registro para eliminar")
            return
            
        id_col = 0  # Asumimos que la primera columna es el ID
        id_val = self.tabla.item(fila_seleccionada, id_col).text()
        
        confirmar = QMessageBox.question(
            self, "Confirmar", 
            "¿Estás seguro de eliminar este registro?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.conexion.cursor()
                query = f"DELETE FROM {self.table_name} WHERE {self.columns[0]} = %s"
                cursor.execute(query, (id_val,))
                self.conexion.commit()
                cursor.close()
                QMessageBox.information(self, "Éxito", "Registro eliminado correctamente")
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el registro:\n{e}")
    
    def limpiar_campos(self):
        for input_field in self.form_inputs:
            if isinstance(input_field, QComboBox):
                input_field.setCurrentIndex(0)
            elif isinstance(input_field, QDateEdit):
                input_field.setDate(QDate.currentDate())
            elif isinstance(input_field, (QSpinBox, QDoubleSpinBox)):
                input_field.setValue(0)
            else:
                input_field.clear()

class VentanaPuntoVenta(QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.carrito = []
        self.setWindowTitle("Punto de Venta - OXXO")
        self.setStyleSheet(f"background-color: {COLOR_FONDO};")
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        titulo = QLabel("PUNTO DE VENTA OXXO")
        titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        titulo.setStyleSheet(f"color: {COLOR_ROJO};")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Línea divisoria
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        linea.setStyleSheet(f"color: {COLOR_AMARILLO};")
        layout.addWidget(linea)

        # Formulario de búsqueda
        form_layout = QHBoxLayout()
        
        self.busqueda_input = QLineEdit()
        self.busqueda_input.setPlaceholderText("Buscar producto...")
        self.busqueda_input.setStyleSheet(f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 2px solid {COLOR_ROJO};
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: #000000; 
            }}
        """)
        form_layout.addWidget(self.busqueda_input)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AMARILLO};
                color: {COLOR_ROJO};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ffe066;
            }}
        """)
        form_layout.addWidget(self.btn_buscar)
        layout.addLayout(form_layout)

        # Tabla de productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(4)
        self.tabla_productos.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Stock"])
        self.tabla_productos.setStyleSheet(f"""
    QTableWidget {{
        background-color: {COLOR_BLANCO};
        border: 2px solid {COLOR_ROJO};
        border-radius: 8px;
    }}
    QHeaderView::section {{
        background-color: {COLOR_ROJO};
        color: {COLOR_BLANCO};
        font-weight: bold;
        padding: 5px;
    }}
    QTableWidget::item {{
        color: #000000;  /* Texto negro */
    }}
    QTableWidget::item:selected {{
        background-color: {COLOR_AMARILLO};
        color: {COLOR_ROJO};
    }}
""")

        layout.addWidget(self.tabla_productos)

        # Formulario de venta
        venta_layout = QHBoxLayout()
        
        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("Cantidad")
        self.cantidad_input.setStyleSheet(f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 2px solid {COLOR_ROJO};
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: #000000; 
            }}
        """)
        venta_layout.addWidget(self.cantidad_input)

        self.btn_agregar_carrito = QPushButton("Agregar al carrito")
        self.btn_agregar_carrito.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ROJO};
                color: {COLOR_BLANCO};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #a31510;
            }}
        """)
        venta_layout.addWidget(self.btn_agregar_carrito)
        layout.addLayout(venta_layout)

        # Tabla de carrito
        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(4)
        self.tabla_carrito.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Subtotal"])
        self.tabla_carrito.setStyleSheet(f"""
    QTableWidget {{
        background-color: {COLOR_BLANCO};
        border: 2px solid {COLOR_ROJO};
        border-radius: 8px;
    }}
    QHeaderView::section {{
        background-color: {COLOR_ROJO};
        color: {COLOR_BLANCO};
        font-weight: bold;
        padding: 5px;
    }}
    QTableWidget::item {{
        color: #000000;  /* Texto negro */
    }}
    QTableWidget::item:selected {{
        background-color: {COLOR_AMARILLO};
        color: {COLOR_ROJO};
    }}
""")
        layout.addWidget(self.tabla_carrito)

        # Total y botones
        total_layout = QHBoxLayout()
        
        self.lbl_total = QLabel("Total: $0.00")
        self.lbl_total.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.lbl_total.setStyleSheet(f"color: {COLOR_ROJO};")
        total_layout.addWidget(self.lbl_total)

        self.btn_finalizar = QPushButton("Finalizar Venta")
        self.btn_finalizar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AMARILLO};
                color: {COLOR_ROJO};
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ffe066;
            }}
        """)
        total_layout.addWidget(self.btn_finalizar)

        self.btn_limpiar = QPushButton("Limpiar Carrito")
        self.btn_limpiar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ROJO};
                color: {COLOR_BLANCO};
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #a31510;
            }}
        """)
        total_layout.addWidget(self.btn_limpiar)
        layout.addLayout(total_layout)

        # Conexión de eventos
        self.btn_buscar.clicked.connect(self.buscar_productos)
        self.btn_agregar_carrito.clicked.connect(self.agregar_al_carrito)
        self.btn_finalizar.clicked.connect(self.finalizar_venta)
        self.btn_limpiar.clicked.connect(self.limpiar_carrito)

        self.setLayout(layout)
        self.buscar_productos()

    def buscar_productos(self):
        try:
            cursor = self.conexion.cursor()
            busqueda = self.busqueda_input.text()
            self.tabla_productos.setRowCount(0)

            if busqueda.isdigit():
                query = "SELECT id_articulo, nombre, precio, stock FROM articulos WHERE id_articulo = %s"
                cursor.execute(query, (busqueda,))
            elif busqueda:
                query = "SELECT id_articulo, nombre, precio, stock FROM articulos WHERE nombre LIKE %s"
                cursor.execute(query, (f"%{busqueda}%",))
            else:
                cursor.execute("SELECT id_articulo, nombre, precio, stock FROM articulos LIMIT 20")

            productos = cursor.fetchall()

            for fila_idx, (id_art, nombre, precio, stock) in enumerate(productos):
                self.tabla_productos.insertRow(fila_idx)
                self.tabla_productos.setItem(fila_idx, 0, QTableWidgetItem(id_art))
                self.tabla_productos.setItem(fila_idx, 1, QTableWidgetItem(nombre))
                self.tabla_productos.setItem(fila_idx, 2, QTableWidgetItem(f"${precio:.2f}"))
                self.tabla_productos.setItem(fila_idx, 3, QTableWidgetItem(str(stock)))

            cursor.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos:\n{e}")

    def agregar_al_carrito(self):
        try:
            fila_seleccionada = self.tabla_productos.currentRow()
            if fila_seleccionada == -1:
                QMessageBox.warning(self, "Advertencia", "Selecciona un producto primero")
                return
                
            cantidad_texto = self.cantidad_input.text()
            if not cantidad_texto.isdigit() or int(cantidad_texto) <= 0:
                QMessageBox.warning(self, "Advertencia", "Ingresa una cantidad válida")
                return
                
            cantidad = int(cantidad_texto)
            id_art = self.tabla_productos.item(fila_seleccionada, 0).text()
            nombre = self.tabla_productos.item(fila_seleccionada, 1).text()
            precio = float(self.tabla_productos.item(fila_seleccionada, 2).text().replace("$", ""))
            stock = int(self.tabla_productos.item(fila_seleccionada, 3).text())
            
            if cantidad > stock:
                QMessageBox.warning(self, "Advertencia", "No hay suficiente stock")
                return
                
            # Verificar si ya está en el carrito
            for item in self.carrito:
                if item["id"] == id_art:
                    item["cantidad"] += cantidad
                    break
            else:
                self.carrito.append({
                    "id": id_art,
                    "nombre": nombre,
                    "precio": precio,
                    "cantidad": cantidad
                })
                
            self.actualizar_carrito()
            self.cantidad_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar al carrito:\n{e}")

    def actualizar_carrito(self):
        self.tabla_carrito.setRowCount(0)
        total = 0.0
        
        for fila_idx, item in enumerate(self.carrito):
            subtotal = item["precio"] * item["cantidad"]
            total += subtotal
            
            self.tabla_carrito.insertRow(fila_idx)
            self.tabla_carrito.setItem(fila_idx, 0, QTableWidgetItem(item["id"]))
            self.tabla_carrito.setItem(fila_idx, 1, QTableWidgetItem(item["nombre"]))
            self.tabla_carrito.setItem(fila_idx, 2, QTableWidgetItem(str(item["cantidad"])))
            self.tabla_carrito.setItem(fila_idx, 3, QTableWidgetItem(f"${subtotal:.2f}"))
            
        self.lbl_total.setText(f"Total: ${total:.2f}")

    def finalizar_venta(self):
        
        if not self.carrito:
            QMessageBox.warning(self, "Advertencia", "El carrito está vacío")
            return
            
            
        # Obtener información del cliente (simplificado)
        telefono, ok = QInputDialog.getText(self, "Cliente", "Ingrese teléfono del cliente:")
        if not ok:
            return
            
        # Verificar si el cliente existe o crear uno nuevo
        try:
            cursor = self.conexion.cursor()
            
            # Registrar venta
            total = sum(item["precio"] * item["cantidad"] for item in self.carrito)
            cursor.execute("INSERT INTO ventas (total, cajas_id_caja, clientes_telefono) VALUES (%s, %s, %s)",
                          (total, 1, telefono))
            id_venta = cursor.lastrowid
            
            # Registrar detalles de venta
            for item in self.carrito:
                cursor.execute("""
                    INSERT INTO detalles_venta 
                    (cantidad, subtotal, ventas_id_venta, articulos_id_articulo) 
                    VALUES (%s, %s, %s, %s)
                """, (item["cantidad"], item["precio"] * item["cantidad"], id_venta, item["id"]))
                
                # Actualizar stock
                cursor.execute("UPDATE articulos SET stock = stock - %s WHERE id_articulo = %s",
                              (item["cantidad"], item["id"]))
            
            self.conexion.commit()
            puntos = int(total // 5)
            cursor.execute("""
                UPDATE clientes
                SET puntos = puntos + %s
                WHERE telefono = %s
            """, (puntos, telefono))
            
            cursor.close()
            
            QMessageBox.information(self, "Éxito", f"Venta registrada correctamente\nNúmero de venta: {id_venta}")
            self.limpiar_carrito()
            
        except Exception as e:
            self.conexion.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo registrar la venta:\n{e}")

    def limpiar_carrito(self):
        self.carrito = []
        self.actualizar_carrito()

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema OXXO")
        self.setStyleSheet(f"background-color: {COLOR_FONDO};")
        
        try:
            self.conexion = obtener_conexion()
            if not self.conexion:
                sys.exit(1)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo conectar a la base de datos:\n{str(e)}")
            sys.exit(1)

        # Crear pestañas
        self.tabs = QTabWidget()
        
        # Punto de Venta
        self.tabs.addTab(VentanaPuntoVenta(self.conexion), "Punto de Venta")
        
        # CRUD para todas las tablas
        self.tabs.addTab(
            CRUDTemplate(
                self.conexion, 
                "proveedores", 
                ["nombre", "contacto", "telefono", "email"], 
                ["Nombre", "Contacto", "Teléfono", "Email"], 
                "Proveedores"
            ), 
            "Proveedores"
        )
        
        self.tabs.addTab(
            CRUDTemplate(
                self.conexion, 
                "categorias", 
                ["id_categoria", "nombre"], 
                ["ID", "Nombre"], 
                "Categorías"
            ), 
            "Categorías"
        )
        
        self.tabs.addTab(
            CRUDTemplate(
                self.conexion, 
                "articulos", 
                ["id_articulo", "nombre", "precio", "stock", "proveedores_nombre", "categorias_id_categoria"], 
                ["ID", "Nombre", "Precio", "Stock", "Proveedor", "Categoría"], 
                "Artículos"
            ), 
            "Artículos"
        )
        
        self.tabs.addTab(
            CRUDTemplate(
                self.conexion, 
                "empleados", 
                ["id_empleado", "nombre", "puesto enum('gerente','cajero','almacen')", "fecha_contratacion", "sueldo"], 
                ["ID", "Nombre", "Puesto", "Fecha Contratación", "Sueldo"], 
                "Empleados"
            ), 
            "Empleados"
        )
        
        self.tabs.addTab(
            CRUDTemplate(
                self.conexion, 
                "cajas", 
                ["id_caja", "numero_caja", "estado enum('activa','inactiva','mantenimiento')", "empleados_id_empleado"], 
                ["ID", "Número", "Estado", "ID Empleado"], 
                "Cajas"
            ), 
            "Cajas"
        )
        
        self.tabs.addTab(
            CRUDTemplate(
                self.conexion, 
                "clientes", 
                ["telefono", "nombre", "email", "puntos"], 
                ["Teléfono", "Nombre", "Email", "Puntos"], 
                "Clientes"
            ), 
            "Clientes"
        )
        
        self.tabs.addTab(
            CRUDTemplate(
                self.conexion, 
                "pedidos", 
                ["id_pedido", "fecha_pedido", "estado enum('Pendiente','Enviado','Recibido','Cancelado')", "proveedores_nombre"], 
                ["ID", "Fecha", "Estado", "Proveedor"], 
                "Pedidos"
            ), 
            "Pedidos"
        )
        
        # Nota: Las tablas de detalles y ventas se manejan automáticamente desde el punto de venta

        # Layout principal
        layout = QVBoxLayout()
        
        # Encabezado
        header = QHBoxLayout()
        
        logo = QLabel()
        try:
            logo.setPixmap(QPixmap("oxxo_logo.png").scaled(150, 50, Qt.AspectRatioMode.KeepAspectRatio))
        except:
            pass
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header.addWidget(logo)
        
        titulo = QLabel("SISTEMA DE GESTIÓN OXXO")
        titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        titulo.setStyleSheet(f"color: {COLOR_ROJO};")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(titulo)
        
        layout.addLayout(header)
        
        # Línea divisoria
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        linea.setStyleSheet(f"color: {COLOR_AMARILLO};")
        layout.addWidget(linea)
        
        # Añadir pestañas
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
        self.resize(1000, 700)
        center_window(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Estilo global
    app.setStyleSheet(f"""
        /* Estilo para QMessageBox */
        QMessageBox {{
            background-color: {COLOR_FONDO};
        }}
        QMessageBox QLabel {{
            color: #000000;  /* Texto negro */
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
        
        /* Estilo para QInputDialog */
        QInputDialog {{
            background-color: {COLOR_FONDO};
        }}
        QInputDialog QLabel {{
            color: #000000;
            font: 12px Arial;
        }}
        QInputDialog QLineEdit {{
            color: #000000;
            background-color: {COLOR_BLANCO};
            border: 1px solid {COLOR_ROJO};
            border-radius: 4px;
            padding: 5px;
        }}
        QInputDialog QPushButton {{
            background-color: {COLOR_AMARILLO};
            color: {COLOR_ROJO};
            border-radius: 4px;
            padding: 5px 10px;
            min-width: 80px;
            font-weight: bold;
        }}
        QInputDialog QPushButton:hover {{
            background-color: #ffe066;
        }}
        
        /* Estilo para QTabWidget */
        QTabWidget::pane {{
            border: 1px solid {COLOR_ROJO};
            border-radius: 4px;
        }}
        QTabBar::tab {{
            background: {COLOR_BLANCO};
            color: {COLOR_ROJO};
            padding: 8px;
            border: 1px solid {COLOR_ROJO};
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background: {COLOR_ROJO};
            color: {COLOR_BLANCO};
            font-weight: bold;
        }}
        
        /* Estilo para campos de entrada */
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{
            color: #000000;
        }}
        
        /* Estilo para tablas */
        QTableWidget {{
            background-color: {COLOR_BLANCO};
            border: 2px solid {COLOR_ROJO};
            border-radius: 8px;
        }}
        QHeaderView::section {{
            background-color: {COLOR_ROJO};
            color: {COLOR_BLANCO};
            font-weight: bold;
            padding: 5px;
        }}
        QTableWidget::item {{
            color: #000000;
        }}
        QTableWidget::item:selected {{
            background-color: {COLOR_AMARILLO};
            color: {COLOR_ROJO};
        }}
    """)
    
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())