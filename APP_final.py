import tkinter as tk
from tkinter import ttk, messagebox
import oracledb


# ============================================================
# CONFIGURACIÓN DE ORACLE
# ============================================================

DB_USER = "TU_USUARIO"
DB_PASSWORD = "TU_PASSWORD"
DB_DSN = "localhost:1521/XEPDB1"


# ============================================================
# PALETA DE COLORES
# ============================================================

PURPLE = "#6C4AB6"
PURPLE_DARK = "#49327A"
PURPLE_LIGHT = "#EEE9FA"

BLUE = "#2878D7"
BLUE_DARK = "#1859A5"
BLUE_LIGHT = "#E8F2FF"

BG = "#F5F6FA"
CARD = "#FFFFFF"

TEXT = "#202536"
MUTED = "#73798A"
BORDER = "#E1E4EC"

SUCCESS = "#2E9B68"
DANGER = "#D95363"

WHITE = "#FFFFFF"


# ============================================================
# CONEXIÓN
# ============================================================

def get_conn():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def mostrar_error(error):
    messagebox.showerror(
        "Error",
        str(error)
    )


def limpiar_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)


def confirmar(mensaje):
    return messagebox.askyesno(
        "Confirmar",
        mensaje
    )


# ============================================================
# FUNCIONES DE USUARIOS
# ============================================================

def user_insert(name, email):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_id = cur.var(
            oracledb.DB_TYPE_NUMBER
        )

        cur.callproc(
            "user_insert",
            [name, email, out_id]
        )

        user_id = out_id.getvalue()

        conn.commit()

        return user_id

    finally:
        conn.close()


def user_get(user_id):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_name = cur.var(
            oracledb.DB_TYPE_VARCHAR
        )

        out_email = cur.var(
            oracledb.DB_TYPE_VARCHAR
        )

        cur.callproc(
            "user_get",
            [
                user_id,
                out_name,
                out_email
            ]
        )

        return (
            out_name.getvalue(),
            out_email.getvalue()
        )

    finally:
        conn.close()


def existe_email(email):
    conn = get_conn()

    try:
        cur = conn.cursor()

        resultado = cur.callfunc(
            "fn_existe_email",
            oracledb.DB_TYPE_NUMBER,
            [email]
        )

        return resultado

    finally:
        conn.close()


# ============================================================
# FUNCIONES DE ARTÍCULOS
# ============================================================

def article_insert(user_id, title, text):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_id = cur.var(
            oracledb.DB_TYPE_NUMBER
        )

        cur.callproc(
            "article_insert",
            [
                user_id,
                title,
                text,
                out_id
            ]
        )

        article_id = out_id.getvalue()

        conn.commit()

        return article_id

    finally:
        conn.close()


def article_update(article_id, title, text):
    conn = get_conn()

    try:
        cur = conn.cursor()

        cur.callproc(
            "article_update",
            [
                article_id,
                title,
                text
            ]
        )

        conn.commit()

    finally:
        conn.close()


def article_delete(article_id):
    conn = get_conn()

    try:
        cur = conn.cursor()

        cur.callproc(
            "article_delete",
            [article_id]
        )

        conn.commit()

    finally:
        conn.close()


def article_get(article_id):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_title = cur.var(
            oracledb.DB_TYPE_VARCHAR
        )

        out_date = cur.var(
            oracledb.DB_TYPE_DATE
        )

        out_text = cur.var(
            oracledb.DB_TYPE_VARCHAR
        )

        out_user_id = cur.var(
            oracledb.DB_TYPE_NUMBER
        )

        cur.callproc(
            "article_get",
            [
                article_id,
                out_title,
                out_date,
                out_text,
                out_user_id
            ]
        )

        return (
            out_title.getvalue(),
            out_date.getvalue(),
            out_text.getvalue(),
            out_user_id.getvalue()
        )

    finally:
        conn.close()


def article_all():
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_cursor = cur.var(
            oracledb.DB_TYPE_CURSOR
        )

        cur.callproc(
            "article_all",
            [out_cursor]
        )

        cursor = out_cursor.getvalue()

        return cursor.fetchall()

    finally:
        conn.close()


def article_all_ordenado(atributo, tipo):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_cursor = cur.var(
            oracledb.DB_TYPE_CURSOR
        )

        cur.callproc(
            "article_all_ordenado",
            [
                atributo,
                tipo,
                out_cursor
            ]
        )

        cursor = out_cursor.getvalue()

        return cursor.fetchall()

    finally:
        conn.close()


# ============================================================
# FUNCIONES DE COMENTARIOS
# ============================================================

def comment_insert(article_id, name, url):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_id = cur.var(
            oracledb.DB_TYPE_NUMBER
        )

        cur.callproc(
            "comment_insert",
            [
                article_id,
                name,
                url,
                out_id
            ]
        )

        comment_id = out_id.getvalue()

        conn.commit()

        return comment_id

    finally:
        conn.close()


def comment_all(article_id):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_cursor = cur.var(
            oracledb.DB_TYPE_CURSOR
        )

        cur.callproc(
            "comment_all",
            [
                article_id,
                out_cursor
            ]
        )

        cursor = out_cursor.getvalue()

        return cursor.fetchall()

    finally:
        conn.close()


def contar_comentarios(article_id):
    conn = get_conn()

    try:
        cur = conn.cursor()

        resultado = cur.callfunc(
            "fn_contar_comentarios",
            oracledb.DB_TYPE_NUMBER,
            [article_id]
        )

        return resultado

    finally:
        conn.close()


# ============================================================
# FUNCIONES DE TAGS
# ============================================================

def tag_insert(name, url):
    conn = get_conn()
    try:
        cur = conn.cursor()
        out_id = cur.var(oracledb.DB_TYPE_NUMBER)
        url_val = url if url and url.strip() != '' else None
        cur.callproc("tag_insert", [name, url_val, out_id])
        conn.commit()
        return out_id.getvalue()
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if error.code in (20031, 20032, 20041, 20042, 20001):
            raise Exception(error.message)
        raise
    finally:
        conn.close()

def tag_associate(article_id, tag_id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.callproc("tag_associate", [article_id, tag_id])
        conn.commit()
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if error.code == 20032:
            raise Exception("Ese tag ya está asociado a ese artículo")
        raise
    finally:
        conn.close()

def tags_by_article(article_id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        out_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
        cur.callproc("tags_by_article", [article_id, out_cursor])
        rs = out_cursor.getvalue()
        data = rs.fetchall()
        rs.close()
        return data
    finally:
        conn.close()

def articles_by_tag(tag_name):
    conn = get_conn()
    try:
        cur = conn.cursor()
        out_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
        cur.callproc("articles_by_tag", [tag_name, out_cursor])
        rs = out_cursor.getvalue()
        data = rs.fetchall()
        rs.close()
        return data
    finally:
        conn.close()
        
# ============================================================
# FUNCIONES DE CATEGORÍAS
# ============================================================

def category_insert(name, url):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_id = cur.var(
            oracledb.DB_TYPE_NUMBER
        )

        cur.callproc(
            "category_insert",
            [
                name,
                url,
                out_id
            ]
        )

        category_id = out_id.getvalue()

        conn.commit()

        return category_id

    finally:
        conn.close()


def category_associate(article_id, category_id):
    conn = get_conn()

    try:
        cur = conn.cursor()

        cur.callproc(
            "category_associate",
            [
                article_id,
                category_id
            ]
        )

        conn.commit()

    finally:
        conn.close()


def categories_by_article(article_id):
    conn = get_conn()

    try:
        cur = conn.cursor()

        out_cursor = cur.var(
            oracledb.DB_TYPE_CURSOR
        )

        cur.callproc(
            "categories_by_article",
            [
                article_id,
                out_cursor
            ]
        )

        cursor = out_cursor.getvalue()

        return cursor.fetchall()

    finally:
        conn.close()


# ============================================================
# APLICACIÓN
# ============================================================

class BlogApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Blog | Bases de Datos Avanzadas"
        )

        self.root.geometry(
            "1280x780"
        )

        self.root.minsize(
            1050,
            680
        )

        self.crear_estilos()
        self.crear_interfaz()

    # ========================================================
    # ESTILOS
    # ========================================================

    def crear_estilos(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        # Fondo general
        style.configure(
            "TFrame",
            background=BG
        )

        # Etiquetas
        style.configure(
            "TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Titulo.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitulo.TLabel",
            background=BG,
            foreground=MUTED,
            font=("Segoe UI", 11)
        )

        style.configure(
            "Pequeno.TLabel",
            background=BG,
            foreground=MUTED,
            font=("Segoe UI", 9)
        )

        # LabelFrame
        style.configure(
            "TLabelframe",
            background=BG,
            bordercolor=BORDER,
            relief="solid"
        )

        style.configure(
            "TLabelframe.Label",
            background=BG,
            foreground=PURPLE_DARK,
            font=("Segoe UI", 11, "bold")
        )

        # Botones principales
        style.configure(
            "Accion.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
            background=PURPLE,
            foreground=WHITE,
            borderwidth=0
        )

        style.map(
            "Accion.TButton",
            background=[
                ("active", PURPLE_DARK),
                ("pressed", PURPLE_DARK)
            ]
        )

        style.configure(
            "Azul.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
            background=BLUE,
            foreground=WHITE,
            borderwidth=0
        )

        style.map(
            "Azul.TButton",
            background=[
                ("active", BLUE_DARK),
                ("pressed", BLUE_DARK)
            ]
        )

        style.configure(
            "Peligro.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
            background=DANGER,
            foreground=WHITE,
            borderwidth=0
        )

        style.map(
            "Peligro.TButton",
            background=[
                ("active", "#B73D4D"),
                ("pressed", "#B73D4D")
            ]
        )

        style.configure(
            "Claro.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 8),
            background="#E8EAF0",
            foreground=TEXT,
            borderwidth=0
        )

        style.map(
            "Claro.TButton",
            background=[
                ("active", "#D9DCE5"),
                ("pressed", "#D9DCE5")
            ]
        )

        # Entradas
        style.configure(
            "TEntry",
            padding=8,
            font=("Segoe UI", 10),
            fieldbackground=WHITE
        )

        style.configure(
            "TCombobox",
            padding=7,
            font=("Segoe UI", 10)
        )

        # Treeview
        style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=34,
            font=("Segoe UI", 10),
            bordercolor=BORDER,
            borderwidth=1
        )

        style.configure(
            "Treeview.Heading",
            background="#EDEEF3",
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[
                ("selected", PURPLE_LIGHT)
            ],
            foreground=[
                ("selected", PURPLE_DARK)
            ]
        )

    # ========================================================
    # INTERFAZ PRINCIPAL
    # ========================================================

    def crear_interfaz(self):

        contenedor = tk.Frame(
            self.root,
            bg=BG
        )

        contenedor.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # MENÚ LATERAL
        # ====================================================

        menu = tk.Frame(
            contenedor,
            bg=PURPLE_DARK,
            width=245
        )

        menu.pack(
            side="left",
            fill="y"
        )

        menu.pack_propagate(False)

        # Logo
        logo = tk.Label(
            menu,
            text="BLOG",
            bg=PURPLE_DARK,
            fg=WHITE,
            font=("Segoe UI", 26, "bold")
        )

        logo.pack(
            pady=(32, 2)
        )

        subtitulo = tk.Label(
            menu,
            text="BASES DE DATOS\nAVANZADAS",
            bg=PURPLE_DARK,
            fg="#D9D1EF",
            font=("Segoe UI", 9, "bold"),
            justify="center"
        )

        subtitulo.pack(
            pady=(0, 30)
        )

        linea = tk.Frame(
            menu,
            bg="#765CA7",
            height=1
        )

        linea.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        botones = [
            ("⌂   Inicio", self.mostrar_inicio),
            ("●   Usuarios", self.mostrar_usuarios),
            ("▣   Artículos", self.mostrar_articulos),
            ("◆   Comentarios", self.mostrar_comentarios),
            ("◇   Tags", self.mostrar_tags),
            ("▤   Categorías", self.mostrar_categorias)
        ]

        for texto, comando in botones:

            boton = tk.Button(
                menu,
                text=texto,
                command=comando,
                bg=PURPLE_DARK,
                fg=WHITE,
                activebackground=PURPLE,
                activeforeground=WHITE,
                relief="flat",
                borderwidth=0,
                anchor="w",
                font=("Segoe UI", 11, "bold"),
                padx=25,
                pady=13,
                cursor="hand2"
            )

            boton.pack(
                fill="x",
                padx=12,
                pady=2
            )

        # Pie del menú
        pie = tk.Frame(
            menu,
            bg=PURPLE_DARK
        )

        pie.pack(
            side="bottom",
            fill="x",
            pady=25
        )

        tk.Label(
            pie,
            text="Python  •  Oracle",
            bg=PURPLE_DARK,
            fg="#D9D1EF",
            font=("Segoe UI", 9)
        ).pack()

        tk.Label(
            pie,
            text="Proyecto académico",
            bg=PURPLE_DARK,
            fg="#AFA4CC",
            font=("Segoe UI", 8)
        ).pack(
            pady=(4, 0)
        )

        # ====================================================
        # CONTENIDO
        # ====================================================

        zona = tk.Frame(
            contenedor,
            bg=BG
        )

        zona.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.contenido = ttk.Frame(
            zona
        )

        self.contenido.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=30
        )

        self.mostrar_inicio()

    # ========================================================
    # LIMPIAR
    # ========================================================

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    # ========================================================
    # ENCABEZADO
    # ========================================================

    def encabezado(self, titulo, descripcion):

        frame = ttk.Frame(
            self.contenido
        )

        frame.pack(
            fill="x",
            pady=(0, 20)
        )

        ttk.Label(
            frame,
            text=titulo,
            style="Titulo.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            frame,
            text=descripcion,
            style="Subtitulo.TLabel"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    # ========================================================
    # TARJETA DEL DASHBOARD
    # ========================================================

    def tarjeta(self, parent, numero, titulo, descripcion):

        card = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        numero_label = tk.Label(
            card,
            text=numero,
            bg=CARD,
            fg=PURPLE,
            font=("Segoe UI", 25, "bold")
        )

        numero_label.pack(
            anchor="w",
            padx=18,
            pady=(16, 0)
        )

        tk.Label(
            card,
            text=titulo,
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 0)
        )

        tk.Label(
            card,
            text=descripcion,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 16)
        )

        return card

    # ========================================================
    # INICIO / DASHBOARD
    # ========================================================

    def mostrar_inicio(self):

        self.limpiar_contenido()

        # Hero
        hero = tk.Frame(
            self.contenido,
            bg=PURPLE,
            height=175
        )

        hero.pack(
            fill="x",
            pady=(0, 25)
        )

        hero.pack_propagate(False)

        tk.Label(
            hero,
            text="Bienvenido a tu Blog",
            bg=PURPLE,
            fg=WHITE,
            font=("Segoe UI", 25, "bold")
        ).pack(
            anchor="w",
            padx=28,
            pady=(25, 2)
        )

        tk.Label(
            hero,
            text="Sistema de gestión desarrollado con Python + Oracle Database",
            bg=PURPLE,
            fg="#EDE7FA",
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            padx=28
        )

        tk.Button(
            hero,
            text="Probar conexión con Oracle",
            command=self.probar_conexion,
            bg=WHITE,
            fg=PURPLE_DARK,
            activebackground="#F0ECF8",
            activeforeground=PURPLE_DARK,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=28,
            pady=18
        )

        # Título
        ttk.Label(
            self.contenido,
            text="Módulos del sistema",
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        # Tarjetas
        tarjetas = tk.Frame(
            self.contenido,
            bg=BG
        )

        tarjetas.pack(
            fill="x"
        )

        datos = [
            ("01", "Usuarios", "Crear y consultar usuarios"),
            ("02", "Artículos", "Crear, editar y eliminar"),
            ("03", "Comentarios", "Administrar comentarios"),
            ("04", "Tags", "Relacionar artículos y tags"),
            ("05", "Categorías", "Organizar contenido")
        ]

        for i, dato in enumerate(datos):

            card = self.tarjeta(
                tarjetas,
                dato[0],
                dato[1],
                dato[2]
            )

            card.grid(
                row=0,
                column=i,
                padx=5,
                sticky="nsew"
            )

            tarjetas.columnconfigure(
                i,
                weight=1
            )

        # Información
        info = tk.Frame(
            self.contenido,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        info.pack(
            fill="x",
            pady=25
        )

        tk.Label(
            info,
            text="Estado de la aplicación",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 4)
        )

        tk.Label(
            info,
            text="●  Oracle Database   •   XEPDB1   •   Python Tkinter",
            bg=CARD,
            fg=SUCCESS,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 18)
        )

    def probar_conexion(self):

        try:

            conn = get_conn()
            conn.close()

            messagebox.showinfo(
                "Conexión exitosa",
                "La conexión con Oracle se realizó correctamente."
            )

        except Exception as e:

            mostrar_error(e)

    # ========================================================
    # USUARIOS
    # ========================================================

    def mostrar_usuarios(self):

        self.limpiar_contenido()

        self.encabezado(
            "Usuarios",
            "Administra los usuarios registrados en el sistema."
        )

        formulario = ttk.LabelFrame(
            self.contenido,
            text="Crear usuario"
        )

        formulario.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        nombre = ttk.Entry(
            formulario,
            width=40
        )

        nombre.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

        ttk.Label(
            formulario,
            text="Email:"
        ).grid(
            row=0,
            column=2,
            padx=15,
            pady=15,
            sticky="w"
        )

        email = ttk.Entry(
            formulario,
            width=40
        )

        email.grid(
            row=0,
            column=3,
            padx=10,
            pady=15
        )

        def crear():

            if not nombre.get().strip() or not email.get().strip():

                messagebox.showwarning(
                    "Datos incompletos",
                    "Escriba el nombre y el email."
                )

                return

            try:

                correo = email.get().strip()

                if existe_email(correo) > 0:

                    messagebox.showwarning(
                        "Email existente",
                        "Ese email ya está registrado."
                    )

                    return

                user_id = user_insert(
                    nombre.get().strip(),
                    correo
                )

                messagebox.showinfo(
                    "Usuario creado",
                    f"Usuario creado correctamente.\nID: {user_id}"
                )

                nombre.delete(0, tk.END)
                email.delete(0, tk.END)

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            formulario,
            text="Crear usuario",
            command=crear,
            style="Accion.TButton"
        ).grid(
            row=1,
            column=3,
            padx=15,
            pady=12,
            sticky="e"
        )

        # Consulta
        consulta = ttk.LabelFrame(
            self.contenido,
            text="Consultar usuario"
        )

        consulta.pack(
            fill="x",
            pady=20
        )

        ttk.Label(
            consulta,
            text="ID usuario:"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=15
        )

        id_usuario = ttk.Entry(
            consulta,
            width=15
        )

        id_usuario.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

        resultado = ttk.Label(
            consulta,
            text="",
            font=("Segoe UI", 11)
        )

        resultado.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=15,
            pady=15
        )

        def consultar():

            try:

                uid = int(
                    id_usuario.get()
                )

                name, mail = user_get(uid)

                resultado.config(
                    text=f"Nombre: {name}     |     Email: {mail}"
                )

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            consulta,
            text="Consultar",
            command=consultar,
            style="Azul.TButton"
        ).grid(
            row=0,
            column=2,
            padx=15,
            pady=15
        )

    # ========================================================
    # ARTÍCULOS
    # ========================================================

    def mostrar_articulos(self):

        self.limpiar_contenido()

        self.encabezado(
            "Artículos",
            "Crea, consulta, actualiza, elimina y ordena los artículos."
        )

        formulario = ttk.LabelFrame(
            self.contenido,
            text="Datos del artículo"
        )

        formulario.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            formulario,
            text="ID artículo:"
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=8
        )

        id_articulo = ttk.Entry(
            formulario,
            width=10
        )

        id_articulo.grid(
            row=0,
            column=1,
            padx=8,
            pady=8
        )

        ttk.Label(
            formulario,
            text="ID usuario:"
        ).grid(
            row=0,
            column=2,
            padx=8,
            pady=8
        )

        id_usuario = ttk.Entry(
            formulario,
            width=10
        )

        id_usuario.grid(
            row=0,
            column=3,
            padx=8,
            pady=8
        )

        ttk.Label(
            formulario,
            text="Título:"
        ).grid(
            row=1,
            column=0,
            padx=8,
            pady=8
        )

        titulo = ttk.Entry(
            formulario,
            width=60
        )

        titulo.grid(
            row=1,
            column=1,
            columnspan=4,
            padx=8,
            pady=8,
            sticky="we"
        )

        ttk.Label(
            formulario,
            text="Texto:"
        ).grid(
            row=2,
            column=0,
            padx=8,
            pady=8,
            sticky="n"
        )

        texto = tk.Text(
            formulario,
            width=60,
            height=4,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1
        )

        texto.grid(
            row=2,
            column=1,
            columnspan=4,
            padx=8,
            pady=8,
            sticky="we"
        )

        def obtener_texto():

            return texto.get(
                "1.0",
                tk.END
            ).strip()

        def limpiar():

            id_articulo.delete(
                0,
                tk.END
            )

            id_usuario.delete(
                0,
                tk.END
            )

            titulo.delete(
                0,
                tk.END
            )

            texto.delete(
                "1.0",
                tk.END
            )

        def crear():

            try:

                uid = int(
                    id_usuario.get()
                )

                if not titulo.get().strip():

                    messagebox.showwarning(
                        "Datos",
                        "Escriba un título."
                    )

                    return

                aid = article_insert(
                    uid,
                    titulo.get().strip(),
                    obtener_texto()
                )

                messagebox.showinfo(
                    "Artículo creado",
                    f"Artículo creado correctamente.\nID: {aid}"
                )

                limpiar()
                cargar_articulos()

            except Exception as e:

                mostrar_error(e)

        def consultar():

            try:

                aid = int(
                    id_articulo.get()
                )

                t, fecha, txt, uid = article_get(
                    aid
                )

                titulo.delete(
                    0,
                    tk.END
                )

                titulo.insert(
                    0,
                    t
                )

                texto.delete(
                    "1.0",
                    tk.END
                )

                if txt:
                    texto.insert(
                        "1.0",
                        txt
                    )

                id_usuario.delete(
                    0,
                    tk.END
                )

                id_usuario.insert(
                    0,
                    str(uid)
                )

            except Exception as e:

                mostrar_error(e)

        def actualizar():

            try:

                aid = int(
                    id_articulo.get()
                )

                article_update(
                    aid,
                    titulo.get().strip(),
                    obtener_texto()
                )

                messagebox.showinfo(
                    "Actualizado",
                    "Artículo actualizado correctamente."
                )

                cargar_articulos()

            except Exception as e:

                mostrar_error(e)

        def eliminar():

            try:

                aid = int(
                    id_articulo.get()
                )

                if not confirmar(
                    f"¿Desea eliminar el artículo {aid}?"
                ):
                    return

                article_delete(
                    aid
                )

                messagebox.showinfo(
                    "Eliminado",
                    "Artículo eliminado correctamente."
                )

                limpiar()
                cargar_articulos()

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            formulario,
            text="Crear",
            command=crear,
            style="Accion.TButton"
        ).grid(
            row=3,
            column=0,
            padx=5,
            pady=10
        )

        ttk.Button(
            formulario,
            text="Consultar",
            command=consultar,
            style="Azul.TButton"
        ).grid(
            row=3,
            column=1,
            padx=5,
            pady=10
        )

        ttk.Button(
            formulario,
            text="Actualizar",
            command=actualizar,
            style="Accion.TButton"
        ).grid(
            row=3,
            column=2,
            padx=5,
            pady=10
        )

        ttk.Button(
            formulario,
            text="Eliminar",
            command=eliminar,
            style="Peligro.TButton"
        ).grid(
            row=3,
            column=3,
            padx=5,
            pady=10
        )

        ttk.Button(
            formulario,
            text="Limpiar",
            command=limpiar,
            style="Claro.TButton"
        ).grid(
            row=3,
            column=4,
            padx=5,
            pady=10
        )

        # Ordenamiento
        orden = ttk.Frame(
            self.contenido
        )

        orden.pack(
            fill="x",
            pady=12
        )

        ttk.Label(
            orden,
            text="Ordenar por:"
        ).pack(
            side="left",
            padx=5
        )

        atributo = ttk.Combobox(
            orden,
            values=[
                "Título",
                "Fecha"
            ],
            state="readonly",
            width=15
        )

        atributo.current(0)

        atributo.pack(
            side="left",
            padx=5
        )

        ttk.Label(
            orden,
            text="Tipo:"
        ).pack(
            side="left",
            padx=5
        )

        tipo = ttk.Combobox(
            orden,
            values=[
                "Ascendente",
                "Descendente"
            ],
            state="readonly",
            width=15
        )

        tipo.current(1)

        tipo.pack(
            side="left",
            padx=5
        )

        # Tabla
        tabla_frame = ttk.Frame(
            self.contenido
        )

        tabla_frame.pack(
            fill="both",
            expand=True
        )

        columnas = (
            "id",
            "titulo",
            "fecha",
            "usuario"
        )

        tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        tabla.heading(
            "id",
            text="ID"
        )

        tabla.heading(
            "titulo",
            text="Título"
        )

        tabla.heading(
            "fecha",
            text="Fecha"
        )

        tabla.heading(
            "usuario",
            text="Usuario"
        )

        tabla.column(
            "id",
            width=60
        )

        tabla.column(
            "titulo",
            width=430
        )

        tabla.column(
            "fecha",
            width=180
        )

        tabla.column(
            "usuario",
            width=100
        )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=tabla.yview
        )

        tabla.configure(
            yscrollcommand=scroll.set
        )

        tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        def cargar_datos(datos):

            limpiar_treeview(
                tabla
            )

            for fila in datos:

                aid, title, fecha, uid = fila

                fecha_texto = ""

                if fecha:
                    fecha_texto = fecha.strftime(
                        "%d/%m/%Y %H:%M"
                    )

                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        aid,
                        title,
                        fecha_texto,
                        uid
                    )
                )

        def cargar_articulos():

            try:

                datos = article_all()

                cargar_datos(
                    datos
                )

            except Exception as e:

                mostrar_error(e)

        def ordenar():

            try:

                atributo_db = (
                    "TITLE"
                    if atributo.get() == "Título"
                    else "ARTICLE_DATE"
                )

                tipo_db = (
                    "1"
                    if tipo.get() == "Ascendente"
                    else "2"
                )

                datos = article_all_ordenado(
                    atributo_db,
                    tipo_db
                )

                cargar_datos(
                    datos
                )

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            orden,
            text="Ordenar",
            command=ordenar,
            style="Accion.TButton"
        ).pack(
            side="left",
            padx=10
        )

        ttk.Button(
            orden,
            text="Mostrar todos",
            command=cargar_articulos,
            style="Claro.TButton"
        ).pack(
            side="left",
            padx=5
        )

        def seleccionar_articulo():

            seleccionado = tabla.selection()

            if not seleccionado:
                return

            valores = tabla.item(
                seleccionado[0],
                "values"
            )

            id_articulo.delete(
                0,
                tk.END
            )

            id_articulo.insert(
                0,
                valores[0]
            )

            id_usuario.delete(
                0,
                tk.END
            )

            id_usuario.insert(
                0,
                valores[3]
            )

            titulo.delete(
                0,
                tk.END
            )

            titulo.insert(
                0,
                valores[1]
            )

            try:

                t, fecha, txt, uid = article_get(
                    int(valores[0])
                )

                texto.delete(
                    "1.0",
                    tk.END
                )

                if txt:
                    texto.insert(
                        "1.0",
                        txt
                    )

            except:
                pass

        tabla.bind(
            "<Double-1>",
            lambda event: seleccionar_articulo()
        )

        cargar_articulos()

    # ========================================================
    # COMENTARIOS
    # ========================================================

    def mostrar_comentarios(self):

        self.limpiar_contenido()

        self.encabezado(
            "Comentarios",
            "Agrega y consulta los comentarios asociados a un artículo."
        )

        formulario = ttk.LabelFrame(
            self.contenido,
            text="Agregar comentario"
        )

        formulario.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            formulario,
            text="ID artículo:"
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=12
        )

        article_id = ttk.Entry(
            formulario,
            width=15
        )

        article_id.grid(
            row=0,
            column=1,
            padx=8,
            pady=12
        )

        ttk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=0,
            column=2,
            padx=12,
            pady=12
        )

        nombre = ttk.Entry(
            formulario,
            width=30
        )

        nombre.grid(
            row=0,
            column=3,
            padx=8,
            pady=12
        )

        ttk.Label(
            formulario,
            text="URL:"
        ).grid(
            row=0,
            column=4,
            padx=12,
            pady=12
        )

        url = ttk.Entry(
            formulario,
            width=35
        )

        url.grid(
            row=0,
            column=5,
            padx=8,
            pady=12
        )

        def agregar():

            try:

                aid = int(
                    article_id.get()
                )

                cid = comment_insert(
                    aid,
                    nombre.get().strip(),
                    url.get().strip()
                )

                messagebox.showinfo(
                    "Comentario",
                    f"Comentario agregado.\nID: {cid}"
                )

                cargar()

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            formulario,
            text="Agregar comentario",
            command=agregar,
            style="Accion.TButton"
        ).grid(
            row=1,
            column=5,
            padx=12,
            pady=12,
            sticky="e"
        )

        consulta = ttk.Frame(
            self.contenido
        )

        consulta.pack(
            fill="x",
            pady=15
        )

        ttk.Label(
            consulta,
            text="Consulta por ID de artículo",
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=5
        )

        # Tabla
        tabla_frame = ttk.Frame(
            self.contenido
        )

        tabla_frame.pack(
            fill="both",
            expand=True
        )

        columnas = (
            "id",
            "nombre",
            "url",
            "fecha"
        )

        tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        for columna, texto_columna in zip(
            columnas,
            [
                "ID",
                "Nombre",
                "URL",
                "Fecha"
            ]
        ):

            tabla.heading(
                columna,
                text=texto_columna
            )

        tabla.column(
            "id",
            width=60
        )

        tabla.column(
            "nombre",
            width=220
        )

        tabla.column(
            "url",
            width=380
        )

        tabla.column(
            "fecha",
            width=180
        )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=tabla.yview
        )

        tabla.configure(
            yscrollcommand=scroll.set
        )

        tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        def cargar():

            try:

                aid = int(
                    article_id.get()
                )

                datos = comment_all(
                    aid
                )

                limpiar_treeview(
                    tabla
                )

                for fila in datos:

                    cid, name, u, fecha = fila

                    fecha_texto = ""

                    if fecha:
                        fecha_texto = fecha.strftime(
                            "%d/%m/%Y %H:%M"
                        )

                    tabla.insert(
                        "",
                        tk.END,
                        values=(
                            cid,
                            name,
                            u,
                            fecha_texto
                        )
                    )

                cantidad = contar_comentarios(
                    aid
                )

                messagebox.showinfo(
                    "Comentarios",
                    f"El artículo tiene {cantidad} comentario(s)."
                )

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            consulta,
            text="Ver comentarios",
            command=cargar,
            style="Azul.TButton"
        ).pack(
            side="left",
            padx=10
        )

    # ========================================================
    # TAGS
    # ========================================================

    def mostrar_tags(self):

        self.limpiar_contenido()

        self.encabezado(
            "Tags",
            "Crea tags, relaciónalos con artículos y realiza búsquedas."
        )

        # Crear
        crear_frame = ttk.LabelFrame(
            self.contenido,
            text="Crear tag"
        )

        crear_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            crear_frame,
            text="Nombre:"
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=12
        )

        nombre = ttk.Entry(
            crear_frame,
            width=30
        )

        nombre.grid(
            row=0,
            column=1,
            padx=8,
            pady=12
        )

        ttk.Label(
            crear_frame,
            text="URL:"
        ).grid(
            row=0,
            column=2,
            padx=12,
            pady=12
        )

        url = ttk.Entry(
            crear_frame,
            width=40
        )

        url.grid(
            row=0,
            column=3,
            padx=8,
            pady=12
        )

        def crear():

            try:

                tid = tag_insert(
                    nombre.get().strip(),
                    url.get().strip()
                )

                messagebox.showinfo(
                    "Tag creado",
                    f"Tag creado correctamente.\nID: {tid}"
                )

                nombre.delete(
                    0,
                    tk.END
                )

                url.delete(
                    0,
                    tk.END
                )

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            crear_frame,
            text="Crear tag",
            command=crear,
            style="Accion.TButton"
        ).grid(
            row=0,
            column=4,
            padx=15,
            pady=12
        )

        # Asociar
        asociar = ttk.LabelFrame(
            self.contenido,
            text="Asociar tag a artículo"
        )

        asociar.pack(
            fill="x",
            pady=12
        )

        ttk.Label(
            asociar,
            text="ID artículo:"
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=12
        )

        article_id = ttk.Entry(
            asociar,
            width=15
        )

        article_id.grid(
            row=0,
            column=1,
            padx=8,
            pady=12
        )

        ttk.Label(
            asociar,
            text="ID tag:"
        ).grid(
            row=0,
            column=2,
            padx=12,
            pady=12
        )

        tag_id = ttk.Entry(
            asociar,
            width=15
        )

        tag_id.grid(
            row=0,
            column=3,
            padx=8,
            pady=12
        )

        def asociar_tag():

            try:

                tag_associate(
                    int(article_id.get()),
                    int(tag_id.get())
                )

                messagebox.showinfo(
                    "Asociación",
                    "Tag asociado correctamente."
                )

                cargar_tags()

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            asociar,
            text="Asociar",
            command=asociar_tag,
            style="Azul.TButton"
        ).grid(
            row=0,
            column=4,
            padx=15,
            pady=12
        )

        # Consulta
        consultar = ttk.LabelFrame(
            self.contenido,
            text="Consultar tags de un artículo"
        )

        consultar.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            consultar,
            text="ID artículo:"
        ).pack(
            side="left",
            padx=12,
            pady=12
        )

        consultar_id = ttk.Entry(
            consultar,
            width=15
        )

        consultar_id.pack(
            side="left",
            padx=8,
            pady=12
        )

        # Tabla
        tabla_frame = ttk.Frame(
            self.contenido
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            pady=(12, 0)
        )

        columnas = (
            "id",
            "nombre",
            "url"
        )

        tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        tabla.heading(
            "id",
            text="ID"
        )

        tabla.heading(
            "nombre",
            text="Nombre"
        )

        tabla.heading(
            "url",
            text="URL"
        )

        tabla.column(
            "id",
            width=80
        )

        tabla.column(
            "nombre",
            width=250
        )

        tabla.column(
            "url",
            width=450
        )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=tabla.yview
        )

        tabla.configure(
            yscrollcommand=scroll.set
        )

        tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        def cargar_tags():

            try:

                aid = int(
                    consultar_id.get()
                )

                datos = tags_by_article(
                    aid
                )

                limpiar_treeview(
                    tabla
                )

                for fila in datos:

                    tabla.insert(
                        "",
                        tk.END,
                        values=fila
                    )

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            consultar,
            text="Ver tags",
            command=cargar_tags,
            style="Azul.TButton"
        ).pack(
            side="left",
            padx=10
        )

        # Buscar por tag
        por_tag = ttk.LabelFrame(
            self.contenido,
            text="Buscar artículos por tag"
        )

        por_tag.pack(
            fill="x",
            pady=12
        )

        ttk.Label(
            por_tag,
            text="Nombre del tag:"
        ).pack(
            side="left",
            padx=12,
            pady=10
        )

        tag_nombre = ttk.Entry(
            por_tag,
            width=25
        )

        tag_nombre.pack(
            side="left",
            padx=8,
            pady=10
        )

        def buscar_articulos():

            try:

                datos = articles_by_tag(
                    tag_nombre.get().strip()
                )

                limpiar_treeview(
                    tabla
                )

                for fila in datos:

                    aid, title, fecha = fila

                    fecha_texto = ""

                    if fecha:
                        fecha_texto = fecha.strftime(
                            "%d/%m/%Y %H:%M"
                        )

                    tabla.insert(
                        "",
                        tk.END,
                        values=(
                            aid,
                            title,
                            fecha_texto
                        )
                    )

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            por_tag,
            text="Buscar",
            command=buscar_articulos,
            style="Accion.TButton"
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

    # ========================================================
    # CATEGORÍAS
    # ========================================================

    def mostrar_categorias(self):

        self.limpiar_contenido()

        self.encabezado(
            "Categorías",
            "Organiza los artículos mediante categorías."
        )

        # Crear categoría
        crear_frame = ttk.LabelFrame(
            self.contenido,
            text="Crear categoría"
        )

        crear_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            crear_frame,
            text="Nombre:"
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=12
        )

        nombre = ttk.Entry(
            crear_frame,
            width=30
        )

        nombre.grid(
            row=0,
            column=1,
            padx=8,
            pady=12
        )

        ttk.Label(
            crear_frame,
            text="URL:"
        ).grid(
            row=0,
            column=2,
            padx=12,
            pady=12
        )

        url = ttk.Entry(
            crear_frame,
            width=40
        )

        url.grid(
            row=0,
            column=3,
            padx=8,
            pady=12
        )

        def crear():

            try:

                cid = category_insert(
                    nombre.get().strip(),
                    url.get().strip()
                )

                messagebox.showinfo(
                    "Categoría creada",
                    f"Categoría creada correctamente.\nID: {cid}"
                )

                nombre.delete(
                    0,
                    tk.END
                )

                url.delete(
                    0,
                    tk.END
                )

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            crear_frame,
            text="Crear categoría",
            command=crear,
            style="Accion.TButton"
        ).grid(
            row=0,
            column=4,
            padx=15,
            pady=12
        )

        # Asociar
        asociar = ttk.LabelFrame(
            self.contenido,
            text="Asociar categoría a artículo"
        )

        asociar.pack(
            fill="x",
            pady=12
        )

        ttk.Label(
            asociar,
            text="ID artículo:"
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=12
        )

        article_id = ttk.Entry(
            asociar,
            width=15
        )

        article_id.grid(
            row=0,
            column=1,
            padx=8,
            pady=12
        )

        ttk.Label(
            asociar,
            text="ID categoría:"
        ).grid(
            row=0,
            column=2,
            padx=12,
            pady=12
        )

        category_id = ttk.Entry(
            asociar,
            width=15
        )

        category_id.grid(
            row=0,
            column=3,
            padx=8,
            pady=12
        )

        def asociar_categoria():

            try:

                category_associate(
                    int(article_id.get()),
                    int(category_id.get())
                )

                messagebox.showinfo(
                    "Asociación",
                    "Categoría asociada correctamente."
                )

                cargar_categorias()

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            asociar,
            text="Asociar",
            command=asociar_categoria,
            style="Azul.TButton"
        ).grid(
            row=0,
            column=4,
            padx=15,
            pady=12
        )

        # Consultar
        consultar = ttk.LabelFrame(
            self.contenido,
            text="Consultar categorías de un artículo"
        )

        consultar.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            consultar,
            text="ID artículo:"
        ).pack(
            side="left",
            padx=12,
            pady=12
        )

        consultar_id = ttk.Entry(
            consultar,
            width=15
        )

        consultar_id.pack(
            side="left",
            padx=8,
            pady=12
        )

        # Tabla
        tabla_frame = ttk.Frame(
            self.contenido
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            pady=(12, 0)
        )

        columnas = (
            "id",
            "nombre",
            "url"
        )

        tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        tabla.heading(
            "id",
            text="ID"
        )

        tabla.heading(
            "nombre",
            text="Nombre"
        )

        tabla.heading(
            "url",
            text="URL"
        )

        tabla.column(
            "id",
            width=80
        )

        tabla.column(
            "nombre",
            width=250
        )

        tabla.column(
            "url",
            width=450
        )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=tabla.yview
        )

        tabla.configure(
            yscrollcommand=scroll.set
        )

        tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        def cargar_categorias():

            try:

                aid = int(
                    consultar_id.get()
                )

                datos = categories_by_article(
                    aid
                )

                limpiar_treeview(
                    tabla
                )

                for fila in datos:

                    tabla.insert(
                        "",
                        tk.END,
                        values=fila
                    )

            except Exception as e:

                mostrar_error(e)

        ttk.Button(
            consultar,
            text="Ver categorías",
            command=cargar_categorias,
            style="Azul.TButton"
        ).pack(
            side="left",
            padx=10
        )


# ============================================================
# INICIAR APLICACIÓN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BlogApp(
        root
    )

    root.mainloop()