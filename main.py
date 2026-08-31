import flet as ft
import datetime, random, difflib, time, json, os, threading

BG_COLOR = "#08040C"          
CARD_BG = "#13071E"           
SURFACE_COLOR = "#221036"     
NEON_GREEN = "#39FF14"
NEON_PURPLE = "#A855F7"       
WARNING_ORANGE = "#F97316"    
DANGER_RED = "#EF4444"
TEXT_WHITE = "#F8FAFC"
TEXT_MUTED = "#94A3B8"        

DATA_FILE = "magi_data_v17.json"

ALIMENTOS_OFFLINE = {
    "es": {
        "pollo": {"carbs": 0.0, "kcal": 165, "cat": "Natural"}, "carne de res": {"carbs": 0.0, "kcal": 250, "cat": "Natural"},
        "cerdo": {"carbs": 0.0, "kcal": 242, "cat": "Natural"}, "pescado": {"carbs": 0.0, "kcal": 205, "cat": "Natural"},
        "huevo": {"carbs": 1.1, "kcal": 155, "cat": "Natural"}, "salchicha": {"carbs": 4.0, "kcal": 300, "cat": "Embutido"},
        "queso": {"carbs": 1.3, "kcal": 402, "cat": "Natural"}, "arroz": {"carbs": 28.0, "kcal": 130, "cat": "Natural"},
        "pasta": {"carbs": 30.0, "kcal": 131, "cat": "Preparada"}, "pan": {"carbs": 49.0, "kcal": 265, "cat": "Preparada"},
        "papa": {"carbs": 17.0, "kcal": 77, "cat": "Natural"}, "manzana": {"carbs": 14.0, "kcal": 52, "cat": "Natural"},
        "chocoramo": {"carbs": 55.0, "kcal": 420, "cat": "Snack"}, "gansito": {"carbs": 62.0, "kcal": 410, "cat": "Snack"},
        "papas margarita limon": {"carbs": 52.0, "kcal": 536, "cat": "Snack"}, "galletas tosh miel": {"carbs": 71.0, "kcal": 430, "cat": "Snack"},
        "galletas saltin noel": {"carbs": 72.0, "kcal": 430, "cat": "Snack"}, "chocolatina jet": {"carbs": 62.0, "kcal": 530, "cat": "Snack"},
        "todo rico": {"carbs": 45.0, "kcal": 530, "cat": "Snack"}, "pony malta": {"carbs": 11.0, "kcal": 42, "cat": "Bebida"},
        "bocadillo veleño": {"carbs": 85.0, "kcal": 350, "cat": "Snack"}, "arequipe": {"carbs": 60.0, "kcal": 315, "cat": "Snack"}, 
        "ajiaco": {"carbs": 14.0, "kcal": 85, "cat": "Preparada"}, "bandeja paisa": {"carbs": 28.0, "kcal": 290, "cat": "Preparada"},
        "buñuelo": {"carbs": 35.0, "kcal": 380, "cat": "Preparada"}, "empanada": {"carbs": 30.0, "kcal": 260, "cat": "Fritura"}, 
        "arepa de queso": {"carbs": 35.0, "kcal": 300, "cat": "Preparada"}, "patacon": {"carbs": 35.0, "kcal": 250, "cat": "Fritura"},
        "morcilla": {"carbs": 12.0, "kcal": 320, "cat": "Embutido"}, "chunchurria": {"carbs": 0.0, "kcal": 280, "cat": "Natural"},
        "chorizo antioqueño": {"carbs": 3.0, "kcal": 350, "cat": "Embutido"}, "quesito antioqueño": {"carbs": 3.0, "kcal": 270, "cat": "Natural"}
    },
    "en": {
        "chicken": {"carbs": 0.0, "kcal": 165, "cat": "Natural"}, "beef": {"carbs": 0.0, "kcal": 250, "cat": "Natural"}
    }
}

LANG = {
    "es": {
        "onb_titulo": "SINC. DE PILOTO", "onb_peso": "Peso (kg)", "onb_altura": "Altura (cm)",
        "onb_meta": "Objetivo", "onb_eq": "Arsenal", "onb_cond": "Acondicionamiento",
        "onb_btn": "ESTABLECER ENLACE", "metas": ["Perder Peso", "Ganar Masa", "Mantenimiento"],
        "equipos": ["Calistenia", "Pesas Básicas", "Gimnasio"], "niveles": ["1 - Sedentario", "2 - Principiante", "3 - Intermedio", "4 - Avanzado", "5 - Élite"],
        "imc_res": "Análisis Listo", "btn_directiva": "NUEVA DIRECTIVA", "reg_gl": "Ingreso (mg/dL)", 
        "filtros_gl": ["Hoy", "Ayer", "7 Días", "30 Días", "Todo"], "gl_momentos": ["Ayunas", "Post-comida", "Otro"], 
        "combate_title": "MISIÓN:", "sync_rate": "TASA DE SINC.:", "momento": "Momento", "alimento": "Alimento", "gramos": "Gramos",
        "btn_anadir": "AÑADIR", "btn_ensenar": "NUEVO ALIMENTO", "momentos_lista": ["Desayuno", "Almuerzo", "Cena", "Snack"],
        "alerta_val": "Dato inválido."
    },
    "en": {
        "onb_titulo": "PILOT SYNC", "onb_peso": "Weight (kg)", "onb_altura": "Height (cm)",
        "onb_btn": "ESTABLISH LINK", "metas": ["Lose Weight", "Gain Mass", "Maintenance"],
        "equipos": ["Calisthenics", "Basic Weights", "Full Gym"], "niveles": ["1 - Sedentary", "2 - Beginner", "3 - Intermediate", "4 - Advanced", "5 - Elite"],
        "imc_res": "Analysis Ready", "btn_directiva": "NEW DIRECTIVE", "reg_gl": "Input (mg/dL)", 
        "filtros_gl": ["Today", "Yesterday", "7 Days", "30 Days", "All"], "gl_momentos": ["Fasting", "Post-meal", "Other"], 
        "combate_title": "MISSION:", "sync_rate": "SYNC RATE:", "momento": "Meal", "alimento": "Food", "gramos": "Grams",
        "btn_anadir": "ADD", "btn_ensenar": "NEW FOOD", "momentos_lista": ["Breakfast", "Lunch", "Dinner", "Snack"],
        "alerta_val": "Invalid data."
    }
}

def generar_rutina_del_dia(eq_idx, cond, dia_idx):
    s_txt = "3x12" if cond <= 2 else ("4x12" if cond == 3 else "4x15")
    cardio = "CARDIO OPCIONAL: 15-20 min." if cond >= 3 else "CARDIO OPCIONAL: 10 min."
    
    if cond <= 2: 
        t1, t2 = 90, 120
        iso_t = "30s"
    elif cond == 3: 
        t1, t2 = 60, 90
        iso_t = "45s"
    else: 
        t1, t2 = 45, 60
        iso_t = "60s"
        
    descanso_txt = f"Descanso: {t1}s - {t2}s"
        
    if dia_idx == 6:
        return "DOMINGO - DESCANSO ACTIVO", ["Día Libre", "Masaje o Estiramiento"], s_txt, "CARDIO OPCIONAL: Caminata 20 min.", "Recuperación Libre", t1, t2
        
    variante = dia_idx % 3
    dias_nombres = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO"]
    dia_str = dias_nombres[dia_idx]

    if eq_idx == 0: 
        formato = f"FORMATO: Por Bloques (Circuito) | {descanso_txt}"
        rutinas = [
            ("RUTINA A: EMPUJE", ["Flexiones Clásicas", "Fondos en Silla", "Flexiones en Pica", f"Plancha Estricta ({iso_t})"]),
            ("RUTINA B: TIRÓN Y CORE", ["Dominadas", f"Hollow Body ({iso_t})", f"Superman ({iso_t})", "Escaladores"]),
            ("RUTINA C: PIERNAS", ["Sentadillas Libres", "Zancadas Alternas", "Puentes de Glúteo", "Elevación de Pantorrillas"])
        ]
    elif eq_idx == 2: 
        formato = f"FORMATO: Series Tradicionales | {descanso_txt}"
        rutinas = [
            ("RUTINA A: PECHO Y TRÍCEPS", ["Press de Banca", "Press Inclinado", "Extensión de Tríceps", "Aperturas"]),
            ("RUTINA B: ESPALDA Y BÍCEPS", ["Jalón al Pecho", "Remo Sentado", "Curl de Bíceps", "Face Pulls"]),
            ("RUTINA C: PIERNAS", ["Sentadillas con Barra", "Prensa de Piernas", "Extensiones de Cuádriceps", "Elevación de Pantorrillas"])
        ]
    else: 
        formato = f"FORMATO: Series Tradicionales | {descanso_txt}"
        rutinas = [
            ("RUTINA A: EMPUJE", ["Press Suelo Mancuernas", "Push Press", "Elevaciones Laterales", "Tríceps Tras Nuca"]),
            ("RUTINA B: TIRÓN", ["Remo a una Mano", "Pullover", "Curl Martillo", f"Plancha Toque Hombros ({iso_t})"]),
            ("RUTINA C: PIERNAS", ["Sentadilla Copa", "Peso Muerto Rumano", "Zancadas", "Elevación de Pantorrillas"])
        ]

    titulo, ejs = rutinas[variante]
    return f"{dia_str} | {titulo}", ejs, s_txt, cardio, formato, t1, t2

def TacticalBtn(simbolo_texto, color, accion):
    return ft.Container(content=ft.Text(simbolo_texto, size=14, weight="bold", color=color), on_click=accion, padding=10, ink=True, border_radius=5)

def main(page: ft.Page):
    page.title = "MAGI OS"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG_COLOR
    page.padding = 0
    page.spacing = 0
    
    master_container = ft.Container(expand=True, padding=10)
    current_view_idx = 1 # 1 corresponde a Combate (0 es Estado, 2 es Energía)
    current_lang = "es"
    
    app_data = {"perfil": {"configurado": False}, "glicemias": [], "diccionario_magi": {}}
    
    def cargar_datos():
        nonlocal app_data
        try:
            if page.client_storage.contains_key("magi_data"):
                app_data = page.client_storage.get("magi_data")
        except: pass
        for lang in ["es", "en"]:
            for alim, vals in ALIMENTOS_OFFLINE[lang].items():
                if alim not in app_data["diccionario_magi"]:
                    app_data["diccionario_magi"][alim] = vals

    def guardar_datos():
        try: page.client_storage.set("magi_data", app_data)
        except: pass

    cargar_datos()

    def mostrar_alerta(texto, color=WARNING_ORANGE):
        sb = ft.SnackBar(content=ft.Text(texto, color=TEXT_WHITE, weight="bold"), bgcolor=color, duration=2000)
        page.overlay.append(sb)
        sb.open = True
        page.update()

    def open_dialog_safe(dlg):
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def close_dialog_safe(dlg):
        dlg.open = False
        page.update()

    def build_onboarding():
        l = LANG[current_lang]
        tf_peso = ft.TextField(label=l["onb_peso"], keyboard_type=ft.KeyboardType.NUMBER, bgcolor=SURFACE_COLOR, color=NEON_GREEN)
        tf_altura = ft.TextField(label=l["onb_altura"], keyboard_type=ft.KeyboardType.NUMBER, bgcolor=SURFACE_COLOR, color=NEON_GREEN)
        dd_meta = ft.Dropdown(label=l["onb_meta"], options=[ft.dropdown.Option(m) for m in l["metas"]], value=l["metas"][0], bgcolor=SURFACE_COLOR)
        dd_eq = ft.Dropdown(label=l["onb_eq"], options=[ft.dropdown.Option(m) for m in l["equipos"]], value=l["equipos"][1], bgcolor=SURFACE_COLOR)
        dd_cond = ft.Dropdown(label=l["onb_cond"], options=[ft.dropdown.Option(m) for m in l["niveles"]], value=l["niveles"][2], bgcolor=SURFACE_COLOR)

        def procesar_perfil(e):
            try:
                peso = float(tf_peso.value.replace(',', '.'))
                altura = float(tf_altura.value.replace(',', '.'))
                imc = peso / ((altura/100)**2)
                nivel_cond = int(dd_cond.value.split(" ")[0])
                app_data["perfil"] = {"peso": peso, "altura": altura, "imc": imc, "meta_idx": l["metas"].index(dd_meta.value), "equipo_idx": l["equipos"].index(dd_eq.value), "acondicionamiento": nivel_cond, "configurado": True}
                guardar_datos()
                mostrar_alerta(f"{l['imc_res']} | IMC: {imc:.1f}", NEON_PURPLE)
                show_main_interface()
            except: mostrar_alerta(l["alerta_val"], DANGER_RED)

        return ft.Container(
            content=ft.Column([
                ft.Text(l["onb_titulo"], size=22, weight="bold", color=WARNING_ORANGE),
                tf_peso, tf_altura, dd_meta, dd_eq, dd_cond,
                ft.ElevatedButton(l["onb_btn"], bgcolor=NEON_PURPLE, color=TEXT_WHITE, on_click=procesar_perfil, width=300)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=30, expand=True
        )

    def view_estado():
        l = LANG[current_lang]
        tf_gl = ft.TextField(label=l["reg_gl"], width=120, keyboard_type=ft.KeyboardType.NUMBER, bgcolor=SURFACE_COLOR)
        dd_mom = ft.Dropdown(options=[ft.dropdown.Option(m) for m in l["gl_momentos"]], value=l["gl_momentos"][0], width=140, bgcolor=SURFACE_COLOR)
        historial_lista = ft.ListView(expand=True, spacing=5)

        def actualizar_datos_estado():
            historial_lista.controls.clear()
            for r in reversed(app_data.get("glicemias", [])[-15:]):
                col = NEON_GREEN if r["estado_raw"] == "Óptimo" else (DANGER_RED if r["estado_raw"] == "Hipo" else WARNING_ORANGE)
                historial_lista.controls.append(ft.ListTile(title=ft.Text(f"{r['valor']} mg/dL", color=col, weight="bold"), subtitle=ft.Text(f"{r['fecha']} | {r['momento']}", color=TEXT_MUTED)))
            page.update()

        def guardar_gl(e):
            try:
                val = float(tf_gl.value.replace(',', '.'))
                estado = "Hipo" if val < 80 else ("Óptimo" if val <= 140 else "Hiper")
                ahora = datetime.datetime.now()
                app_data["glicemias"].append({"fecha": ahora.strftime("%Y-%m-%d"), "valor": val, "momento": dd_mom.value, "estado_raw": estado})
                guardar_datos(); tf_gl.value = ""; actualizar_datos_estado(); mostrar_alerta("Dato Guardado", NEON_GREEN)
            except: mostrar_alerta(l["alerta_val"], DANGER_RED)

        actualizar_datos_estado()
        return ft.Column([
            ft.Row([tf_gl, dd_mom, TacticalBtn("GUARDAR", NEON_PURPLE, guardar_gl)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(content=historial_lista, expand=True, bgcolor=CARD_BG, border_radius=10, padding=10)
        ], expand=True)

    def view_combate():
        l = LANG[current_lang]
        eq = app_data["perfil"].get("equipo_idx", 1)
        cond = app_data["perfil"].get("acondicionamiento", 2)
        dia_semana_actual = datetime.datetime.today().weekday()
        
        titulo, ejercicios, series_txt, recomendacion_cardio, formato_txt, t1, t2 = generar_rutina_del_dia(eq, cond, dia_semana_actual)
        num_series = int(series_txt.split('x')[0])
        total_checks = len(ejercicios) * num_series
        
        lbl_sync = ft.Text(f"{l['sync_rate']} 0%", color=NEON_GREEN, weight="bold")
        prog_bar = ft.ProgressBar(value=0, color=NEON_GREEN, bgcolor=SURFACE_COLOR)
        
        checks = []
        def update_progreso(e):
            completados = sum(1 for c in checks if c.value)
            prog_bar.value = completados / total_checks if total_checks else 0
            lbl_sync.value = f"{l['sync_rate']} {int(prog_bar.value * 100)}%"
            page.update()

        lista_ej = ft.ListView(expand=True, spacing=10)
        for ej in ejercicios:
            row_checks = ft.Row([ft.Checkbox(on_change=update_progreso, fill_color=NEON_PURPLE) for _ in range(num_series)])
            checks.extend(row_checks.controls)
            
            # Botón de Video Tutorial
            url_busqueda = f"https://www.youtube.com/results?search_query=como+hacer+{ej.replace(' ', '+')}+ejercicio"
            btn_tutorial = ft.TextButton(text="VER TUTORIAL", url=url_busqueda, style=ft.ButtonStyle(color=NEON_PURPLE))
            
            lista_ej.controls.append(ft.Container(content=ft.Column([
                ft.Row([ft.Text(ej, color=TEXT_WHITE, weight="bold", expand=True), btn_tutorial]),
                row_checks
            ]), bgcolor=CARD_BG, padding=10, border_radius=8))

        txt_timer = ft.Text("00:00", size=35, weight="bold", color=TEXT_WHITE)
        timer_running = False

        def run_timer(segundos):
            nonlocal timer_running; timer_running = True
            for i in range(segundos, -1, -1):
                if not timer_running: break
                mins, secs = divmod(i, 60)
                txt_timer.value = f"{mins:02d}:{secs:02d}"; page.update(); time.sleep(1)

        def start_timer(s): threading.Thread(target=run_timer, args=(s,), daemon=True).start()
        def stop_timer(e): nonlocal timer_running; timer_running = False; txt_timer.value="00:00"; page.update()
        
        return ft.Column([
            ft.Row([ft.Text(f"{titulo} ({series_txt})", color=WARNING_ORANGE, size=16, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text(formato_txt, color=TEXT_WHITE, size=12, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text(recomendacion_cardio, color=NEON_PURPLE, size=11, italic=True)], alignment=ft.MainAxisAlignment.CENTER),
            lbl_sync, prog_bar,
            ft.Container(content=lista_ej, expand=True),
            ft.Container(content=ft.Column([
                txt_timer,
                ft.Row([
                    ft.ElevatedButton(f"{t1}s", on_click=lambda e, s=t1: start_timer(s), bgcolor=NEON_GREEN, color=BG_COLOR),
                    ft.ElevatedButton(f"{t2}s", on_click=lambda e, s=t2: start_timer(s), bgcolor=WARNING_ORANGE, color=BG_COLOR),
                    TacticalBtn("DETENER", DANGER_RED, stop_timer)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor=CARD_BG, padding=10, border_radius=10)
        ], expand=True)

    def view_energia():
        l = LANG[current_lang]
        dd_mom = ft.Dropdown(options=[ft.dropdown.Option(m) for m in l["momentos_lista"]], value=l["momentos_lista"][0], width=140, bgcolor=SURFACE_COLOR)
        
        # Opciones dinámicas ordenadas desde nuestro Diccionario (API Local)
        opciones_alimentos = [ft.dropdown.Option(a.capitalize()) for a in sorted(app_data["diccionario_magi"].keys())]
        dd_alim = ft.Dropdown(label=l["alimento"], options=opciones_alimentos, expand=True, bgcolor=SURFACE_COLOR)
        
        tf_gr = ft.TextField(label=l["gramos"], width=100, keyboard_type=ft.KeyboardType.NUMBER, bgcolor=SURFACE_COLOR)
        
        lista_comidas = ft.ListView(expand=True, spacing=5)
        registro_actual = [] 
        lbl_tot = ft.Text("C: 0g | K: 0kcal", color=NEON_GREEN, weight="bold", size=16)

        def actualizar_pantalla_energia():
            lista_comidas.controls.clear()
            tc = tk = 0.0
            for item in registro_actual:
                tc += item["c"]; tk += item["k"]
                lista_comidas.controls.append(ft.Container(content=ft.Row([ft.Text(item["alim"].capitalize(), expand=True, color=TEXT_WHITE), ft.Text(f"C: {item['c']:.1f}g | K: {item['k']:.1f}", color=NEON_PURPLE, weight="bold")]), bgcolor=SURFACE_COLOR, padding=10, border_radius=8))
            lbl_tot.value = f"C: {tc:.1f}g | K: {tk:.1f}kcal"; page.update()

        tf_new_nombre = ft.TextField(label="Nombre Alimento", width=250, bgcolor=SURFACE_COLOR)
        tf_new_carbs = ft.TextField(label="Carbs/100g", keyboard_type=ft.KeyboardType.NUMBER, width=120, bgcolor=SURFACE_COLOR)
        tf_new_kcal = ft.TextField(label="Kcal/100g", keyboard_type=ft.KeyboardType.NUMBER, width=120, bgcolor=SURFACE_COLOR)

        def save_new_food(e):
            try:
                c = float(tf_new_carbs.value.replace(',', '.'))
                k = float(tf_new_kcal.value.replace(',', '.'))
                alim_raw = tf_new_nombre.value.lower().strip()
                if not alim_raw: return
                app_data["diccionario_magi"][alim_raw] = {"carbs": c, "kcal": k, "cat": "Personal"}
                guardar_datos()
                
                # Actualizar las opciones del Dropdown
                nuevas_opciones = [ft.dropdown.Option(a.capitalize()) for a in sorted(app_data["diccionario_magi"].keys())]
                dd_alim.options = nuevas_opciones
                dd_alim.value = alim_raw.capitalize()
                
                close_dialog_safe(dlg_new_food)
                mostrar_alerta("Alimento Registrado", NEON_GREEN)
            except: mostrar_alerta("Valores numéricos inválidos", DANGER_RED)

        dlg_new_food = ft.AlertDialog(
            title=ft.Text(l["btn_ensenar"], color=NEON_PURPLE, weight="bold"),
            content=ft.Column([ft.Text("Macros por cada 100g/ml:"), tf_new_nombre, ft.Row([tf_new_carbs, tf_new_kcal])], height=150),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog_safe(dlg_new_food)),
                ft.TextButton("Guardar", on_click=save_new_food)
            ]
        )

        def add_food(e):
            if not dd_alim.value: return
            alim_final = dd_alim.value.lower()
            try: gr = float(tf_gr.value.replace(',', '.'))
            except: mostrar_alerta(l["alerta_val"], DANGER_RED); return
            
            dic = app_data["diccionario_magi"]
            if alim_final in dic:
                c_calc = (gr*dic[alim_final]["carbs"])/100; k_calc = (gr*dic[alim_final]["kcal"])/100
                registro_actual.append({"alim": alim_final, "c": c_calc, "k": k_calc})
                tf_gr.value = ""; actualizar_pantalla_energia()

        def limpiar(e): registro_actual.clear(); actualizar_pantalla_energia()

        return ft.Column([
            ft.Row([dd_mom, dd_alim]),
            ft.Row([tf_gr, ft.ElevatedButton(l["btn_anadir"], on_click=add_food, bgcolor=WARNING_ORANGE, color=TEXT_WHITE), TacticalBtn("NUEVO ALIMENTO", NEON_PURPLE, lambda e: open_dialog_safe(dlg_new_food)), TacticalBtn("BORRAR TODO", DANGER_RED, limpiar)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(content=lista_comidas, expand=True, bgcolor=CARD_BG, border_radius=10, padding=10),
            ft.Container(content=ft.Row([lbl_tot], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=10)
        ], expand=True)

    def navigate_custom(idx):
        nonlocal current_view_idx; current_view_idx = idx
        vistas = [view_estado, view_combate, view_energia]
        master_container.content = vistas[idx]()
        page.update()

    def CustomNavBtn(text, idx):
        return ft.Container(content=ft.Text(text, size=13, color=TEXT_WHITE, weight="bold"), on_click=lambda e: navigate_custom(idx), expand=True, ink=True, padding=15, alignment=ft.alignment.center)

    bottom_nav = ft.Container(bgcolor=CARD_BG, margin=0, padding=0)

    def reset_app(e): app_data["perfil"]["configurado"] = False; guardar_datos(); show_onboarding_interface()

    def show_onboarding_interface():
        page.appbar = None; bottom_nav.visible = False; master_container.content = build_onboarding(); page.update()

    def show_main_interface():
        page.appbar = ft.AppBar(title=ft.Text("MAGI OS", color=NEON_GREEN, weight="bold", size=18), bgcolor=CARD_BG, actions=[TacticalBtn("AJUSTES", WARNING_ORANGE, reset_app)])
        # Pestañas limpias y sin emojis
        bottom_nav.content = ft.Row([CustomNavBtn("ESTADO", 0), CustomNavBtn("COMBATE", 1), CustomNavBtn("ENERGÍA", 2)], alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=0)
        bottom_nav.visible = True; navigate_custom(current_view_idx)

    page.add(master_container, bottom_nav)
    
    if app_data.get("perfil", {}).get("configurado", False): show_main_interface()
    else: show_onboarding_interface()

ft.app(target=main)
