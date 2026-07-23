import flet as ft
import datetime, random, requests, difflib, time

# ==========================================
# CONSTANTES Y COLORES EVA-01
# ==========================================
BG_COLOR = "#08040C"          
CARD_BG = "#13071E"           
SURFACE_COLOR = "#221036"     
NEON_GREEN = "#39FF14"
NEON_PURPLE = "#A855F7"       
WARNING_ORANGE = "#F97316"    
DANGER_RED = "#EF4444"
TEXT_WHITE = "#F8FAFC"
TEXT_MUTED = "#94A3B8"        

# ==========================================
# CEREBRO MAGI Y DICCIONARIO
# ==========================================
ALIMENTOS_OFFLINE = {
    "es": {
        "pollo": {"carbs": 0.0, "kcal": 165, "cat": "Natural"}, "carne de res": {"carbs": 0.0, "kcal": 250, "cat": "Natural"},
        "cerdo": {"carbs": 0.0, "kcal": 242, "cat": "Natural"}, "pescado": {"carbs": 0.0, "kcal": 205, "cat": "Natural"},
        "huevo": {"carbs": 1.1, "kcal": 155, "cat": "Natural"}, "salchicha": {"carbs": 4.0, "kcal": 300, "cat": "Embutido"},
        "queso": {"carbs": 1.3, "kcal": 402, "cat": "Natural"}, "arroz": {"carbs": 28.0, "kcal": 130, "cat": "Natural"},
        "pasta": {"carbs": 30.0, "kcal": 131, "cat": "Preparada"}, "pan": {"carbs": 49.0, "kcal": 265, "cat": "Preparada"},
        "papa": {"carbs": 17.0, "kcal": 77, "cat": "Natural"}, "manzana": {"carbs": 14.0, "kcal": 52, "cat": "Natural"},
        "arepa": {"carbs": 45.0, "kcal": 210, "cat": "Preparada"}, "empanada": {"carbs": 35.0, "kcal": 250, "cat": "Fritura"},
        "pizza": {"carbs": 33.0, "kcal": 266, "cat": "Preparada"}, "hamburguesa": {"carbs": 30.0, "kcal": 295, "cat": "Preparada"},
        "chocoramo": {"carbs": 45.0, "kcal": 350, "cat": "Mecato - Dulce"}, "papas margarita": {"carbs": 50.0, "kcal": 536, "cat": "Mecato"}
    },
    "en": {
        "chicken": {"carbs": 0.0, "kcal": 165, "cat": "Natural"}, "beef": {"carbs": 0.0, "kcal": 250, "cat": "Natural"},
        "egg": {"carbs": 1.1, "kcal": 155, "cat": "Natural"}, "sausage": {"carbs": 4.0, "kcal": 300, "cat": "Processed"},
        "rice": {"carbs": 28.0, "kcal": 130, "cat": "Natural"}, "pasta": {"carbs": 30.0, "kcal": 131, "cat": "Prepared"},
        "bread": {"carbs": 49.0, "kcal": 265, "cat": "Prepared"}, "potato": {"carbs": 17.0, "kcal": 77, "cat": "Natural"},
        "pizza": {"carbs": 33.0, "kcal": 266, "cat": "Prepared"}, "hamburger": {"carbs": 30.0, "kcal": 295, "cat": "Prepared"},
        "candy": {"carbs": 90.0, "kcal": 400, "cat": "Sweet"}, "potato chips": {"carbs": 50.0, "kcal": 536, "cat": "Snack"}
    }
}

LANG = {
    "es": {
        "onb_titulo": "SINC. DE PILOTO REQUERIDA", "onb_peso": "Peso (kg)", "onb_altura": "Altura (cm)",
        "onb_meta": "Objetivo Táctico", "onb_eq": "Arsenal Disponible", "onb_cond": "Acondicionamiento",
        "onb_btn": "ESTABLECER ENLACE",
        "metas": ["Perder Peso", "Ganar Masa", "Mantenimiento"],
        "equipos": ["Calistenia", "Pesas Básicas", "Gimnasio"],
        "niveles": ["1 - Sedentario", "2 - Principiante", "3 - Intermedio", "4 - Avanzado", "5 - Élite"],
        "imc_res": "Análisis Biométrico Completado", 
        "btn_directiva": "NUEVA DIRECTIVA", "reg_gl": "Ingreso (mg/dL)", 
        "filtros_gl": ["Hoy", "Ayer", "7 Días", "30 Días", "Todo"],
        "gl_momentos": ["Ayunas", "Post-comida", "Otro"], 
        "combate_title": "MISIÓN:", "sync_rate": "TASA DE SINC.:",
        "momento": "Momento", "alimento": "Alimento", "gramos": "Gramos",
        "btn_anadir": "AÑADIR", "btn_ensenar": "ENSEÑAR MAGI", 
        "momentos_lista": ["Desayuno", "Almuerzo", "Cena", "Snack"],
        "alerta_val": "Ingrese datos válidos.", "quotes": ["No debes huir. Entrena.", "La insulina se controla."]
    },
    "en": {
        "onb_titulo": "PILOT SYNC REQUIRED", "onb_peso": "Weight (kg)", "onb_altura": "Height (cm)",
        "onb_meta": "Tactical Goal", "onb_eq": "Available Arsenal", "onb_cond": "Conditioning",
        "onb_btn": "ESTABLISH LINK",
        "metas": ["Lose Weight", "Gain Mass", "Maintenance"],
        "equipos": ["Calisthenics", "Basic Weights", "Full Gym"],
        "niveles": ["1 - Sedentary", "2 - Beginner", "3 - Intermediate", "4 - Advanced", "5 - Elite"],
        "imc_res": "Biometric Analysis", 
        "btn_directiva": "NEW DIRECTIVE", "reg_gl": "Input (mg/dL)", 
        "filtros_gl": ["Today", "Yesterday", "7 Days", "30 Days", "All"],
        "gl_momentos": ["Fasting", "Post-meal", "Other"], 
        "combate_title": "MISSION:", "sync_rate": "SYNC RATE:",
        "momento": "Meal", "alimento": "Food", "gramos": "Grams",
        "btn_anadir": "ADD", "btn_ensenar": "TEACH MAGI", 
        "momentos_lista": ["Breakfast", "Lunch", "Dinner", "Snack"],
        "alerta_val": "Enter valid data.", "quotes": ["You mustn't run away. Train.", "Insulin is controlled."]
    }
}

def generar_pool_rutinas(meta_idx, eq_idx, cond):
    s_txt = "3x12" if cond < 3 else "4x15"
    if cond <= 2: cardio = "CARDIO OPCIONAL: 10-15 min de caminata ligera o bici."
    elif cond == 3: cardio = "CARDIO OPCIONAL: 15-20 min de trote moderado."
    else: cardio = "CARDIO OPCIONAL: 20 min de HIIT o carrera intensa."
        
    if eq_idx == 0: 
        return [("CALISTENIA A", ["Push-ups", "Squats", "Plank", "Burpees"], s_txt, cardio), ("CALISTENIA B", ["Dips", "Lunges", "Crunches", "Jumping Jacks"], s_txt, cardio)]
    elif eq_idx == 2: 
        return [("GYM A", ["Bench Press", "Squats", "Lat Pulldown", "Cables"], s_txt, cardio), ("GYM B", ["Deadlift", "OHP", "Rows", "Leg Press"], s_txt, cardio)]
    else: 
        return [("HOME PESAS A", ["DB Press", "Goblet Squat", "DB Row", "Thrusters"], s_txt, cardio), ("HOME PESAS B", ["DB RDL", "Arnold Press", "Lunges", "Swings"], s_txt, cardio)]

def TacticalBtn(simbolo_texto, color, accion):
    return ft.Container(
        content=ft.Text(simbolo_texto, size=24, color=color),
        on_click=accion,
        padding=15,          
        ink=True,            
        border_radius=50     
    )

def main(page: ft.Page):
    # ==========================================
    # CONFIGURACIÓN BASE
    # ==========================================
    page.title = "MAGI OS 6.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG_COLOR
    page.padding = 0
    page.fonts = {"Consolas": "Consolas"}
    
    master_container = ft.Container(expand=True, padding=10)
    
    # ==========================================
    # SISTEMA DE MEMORIA BLINDADO
    # ==========================================
    app_data = {"perfil": {"configurado": False}, "glicemias": [], "diccionario_magi": {}}
    
    try:
        if page.client_storage.contains_key("magi_data"):
            memoria_guardada = page.client_storage.get("magi_data")
            if memoria_guardada:
                app_data = memoria_guardada
    except:
        pass 
        
    def guardar_datos():
        try:
            page.client_storage.set("magi_data", app_data)
        except:
            pass
            
    for lang in ["es", "en"]:
        for alim, vals in ALIMENTOS_OFFLINE[lang].items():
            if alim not in app_data["diccionario_magi"]:
                app_data["diccionario_magi"][alim] = vals
    guardar_datos()

    current_lang = "es"
    variante_rutina = 0

    # ==========================================
    # SISTEMA DE NAVEGACIÓN BLINDADO V6.0
    # ==========================================
    # Se le inyectan los emojis al texto para evitar fallos visuales.
    drawer = ft.NavigationDrawer(
        bgcolor=SURFACE_COLOR,
        controls=[
            ft.Container(height=20),
            ft.Text("   MAGI OS TACTICAL", size=20, weight="bold", color=NEON_GREEN),
            ft.Divider(thickness=2, color=CARD_BG),
            ft.NavigationDrawerDestination(icon="lightbulb", label="💡 Mindset"),
            ft.NavigationDrawerDestination(icon="water_drop", label="🩸 Estado"),
            ft.NavigationDrawerDestination(icon="fitness_center", label="⚔️ Combate"),
            ft.NavigationDrawerDestination(icon="battery_full", label="🔋 Energía"),
            ft.Divider(thickness=2, color=CARD_BG),
        ],
    )

    def open_drawer_safe(e):
        try:
            page.open(drawer)  # Método para Flet moderno (0.22+)
        except Exception:
            try:
                page.drawer.open = True  # Método para versiones anteriores
                page.update()
            except Exception:
                pass 

    def close_drawer_safe():
        try:
            page.close(drawer)
        except Exception:
            try:
                page.drawer.open = False
                page.update()
            except Exception:
                pass

    def navigate(e):
        try:
            idx = e.control.selected_index
            if idx is not None:
                if idx == 0: master_container.content = view_mindset()
                elif idx == 1: master_container.content = view_estado()
                elif idx == 2: master_container.content = view_combate()
                elif idx == 3: master_container.content = view_energia()
            page.update()
        except Exception:
            pass 
        close_drawer_safe()

    def reset_app(e):
        app_data["perfil"]["configurado"] = False
        guardar_datos()
        close_drawer_safe()
        show_onboarding_interface()

    def toggle_lang(e):
        nonlocal current_lang
        current_lang = "en" if current_lang == "es" else "es"
        close_drawer_safe()
        show_main_interface()

    # Añadimos las funciones a los botones del menú aquí para evitar errores
    drawer.on_change = navigate
    drawer.controls.append(ft.ListTile(title=ft.Text("🌍 Language / Idioma"), on_click=toggle_lang))
    drawer.controls.append(ft.ListTile(title=ft.Text("⚙️ Reconfigurar"), on_click=reset_app))

    btn_menu_lateral = TacticalBtn("☰", TEXT_WHITE, open_drawer_safe)

    app_bar = ft.AppBar(
        leading=btn_menu_lateral,
        title=ft.Text("MAGI OS 6.0", color=TEXT_WHITE, font_family="Courier"),
        bgcolor=CARD_BG,
    )

    def mostrar_alerta(texto, color=WARNING_ORANGE):
        sb = ft.SnackBar(content=ft.Text(texto, color=TEXT_WHITE), bgcolor=color)
        try:
            page.open(sb)
        except AttributeError:
            page.snack_bar = sb
            page.snack_bar.open = True
            page.update()

    # ==========================================
    # VISTAS (PANTALLAS INTERNAS)
    # ==========================================
    def build_onboarding():
        l = LANG[current_lang]
        tf_peso = ft.TextField(label=l["onb_peso"], keyboard_type=ft.KeyboardType.NUMBER, bgcolor=SURFACE_COLOR, color=NEON_GREEN)
        tf_altura = ft.TextField(label=l["onb_altura"], keyboard_type=ft.KeyboardType.NUMBER, bgcolor=SURFACE_COLOR, color=NEON_GREEN)
        dd_meta = ft.Dropdown(label=l["onb_meta"], options=[ft.dropdown.Option(m) for m in l["metas"]], value=l["metas"][0], bgcolor=SURFACE_COLOR)
        dd_eq = ft.Dropdown(label=l["onb_eq"], options=[ft.dropdown.Option(m) for m in l["equipos"]], value=l["equipos"][1], bgcolor=SURFACE_COLOR)
        dd_cond = ft.Dropdown(label=l["onb_cond"], options=[ft.dropdown.Option(m) for m in l["niveles"]], value=l["niveles"][2], bgcolor=SURFACE_COLOR)

        def procesar_perfil(e):
            try:
                peso = float(tf_peso.value); altura = float(tf_altura.value)
                imc = peso / ((altura/100)**2)
                nivel_cond = int(dd_cond.value.split(" ")[0])
                
                app_data["perfil"] = {
                    "peso": peso, "altura": altura, "imc": imc,
                    "meta_idx": l["metas"].index(dd_meta.value), "equipo_idx": l["equipos"].index(dd_eq.value),
                    "acondicionamiento": nivel_cond, "configurado": True
                }
                guardar_datos()
                mostrar_alerta(f"{l['imc_res']} | IMC: {imc:.1f}", NEON_PURPLE)
                show_main_interface()
            except Exception:
                mostrar_alerta(l["alerta_val"], DANGER_RED)

        return ft.Container(
            content=ft.Column([
                ft.Text(l["onb_titulo"], size=22, weight="bold", color=WARNING_ORANGE),
                tf_peso, tf_altura, dd_meta, dd_eq, dd_cond,
                ft.ElevatedButton(l["onb_btn"], bgcolor=NEON_PURPLE, color=TEXT_WHITE, on_click=procesar_perfil, width=300)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=30, expand=True
        )

    def view_mindset():
        l = LANG[current_lang]
        texto_quote = ft.Text(random.choice(l["quotes"]), size=18, italic=True, color=TEXT_WHITE, text_align=ft.TextAlign.CENTER)
        
        def cambiar_frase(e):
            try:
                r = requests.get("https://zenquotes.io/api/random", timeout=2)
                texto_quote.value = f'"{r.json()[0]["q"]}"\n\n- {r.json()[0]["a"]}'
            except: texto_quote.value = random.choice(l["quotes"])
            page.update()

        return ft.Column([
            ft.Text("MINDSET", size=24, color=NEON_PURPLE, weight="bold"),
            ft.Container(content=texto_quote, padding=30, bgcolor=CARD_BG, border_radius=10, expand=True),
            ft.ElevatedButton(l["btn_directiva"], bgcolor=NEON_GREEN, color=BG_COLOR, on_click=cambiar_frase)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

    def view_estado():
        l = LANG[current_lang]
        tf_gl = ft.TextField(label=l["reg_gl"], width=120, keyboard_type=ft.KeyboardType.NUMBER, bgcolor=SURFACE_COLOR)
        dd_mom = ft.Dropdown(options=[ft.dropdown.Option(m) for m in l["gl_momentos"]], value=l["gl_momentos"][0], width=140, bgcolor=SURFACE_COLOR)
        dd_filtro = ft.Dropdown(options=[ft.dropdown.Option(m) for m in l["filtros_gl"]], value=l["filtros_gl"][0], width=140, bgcolor=SURFACE_COLOR)
        
        chart_container = ft.Container(height=180) 
        historial_lista = ft.ListView(expand=True, spacing=5)

        def actualizar_datos_estado(e=None):
            hoy = datetime.datetime.now().date()
            idx_filtro = l["filtros_gl"].index(dd_filtro.value)
            datos_filtrados = []
            
            for reg in app_data.get("glicemias", []):
                fecha_reg = datetime.datetime.strptime(reg["fecha"], "%Y-%m-%d").date()
                if idx_filtro == 0 and fecha_reg == hoy: datos_filtrados.append(reg)
                elif idx_filtro == 1 and fecha_reg == hoy - datetime.timedelta(days=1): datos_filtrados.append(reg)
                elif idx_filtro == 2 and (hoy - fecha_reg).days <= 7: datos_filtrados.append(reg)
                elif idx_filtro == 3 and (hoy - fecha_reg).days <= 30: datos_filtrados.append(reg)
                elif idx_filtro == 4: datos_filtrados.append(reg)

            historial_lista.controls.clear()
            for r in reversed(datos_filtrados[-15:]):
                col = NEON_GREEN if r["estado_raw"] == "Óptimo" else (DANGER_RED if r["estado_raw"] == "Hipo" else WARNING_ORANGE)
                historial_lista.controls.append(
                    ft.ListTile(title=ft.Text(f"{r['valor']} mg/dL - {r['estado_raw']}", color=col, weight="bold"),
                                subtitle=ft.Text(f"{r['fecha']} {r['hora']} | {r['momento']}", color=TEXT_MUTED))
                )

            hipo = sum(1 for d in datos_filtrados if d["valor"] < 80)
            optimo = sum(1 for d in datos_filtrados if 80 <= d["valor"] <= 140)
            hiper = sum(1 for d in datos_filtrados if d["valor"] > 140)
            
            sections = []
            if hipo > 0: sections.append(ft.PieChartSection(hipo, color=DANGER_RED, radius=45, title="Hipo"))
            if optimo > 0: sections.append(ft.PieChartSection(optimo, color=NEON_GREEN, radius=45, title="Óptimo"))
            if hiper > 0: sections.append(ft.PieChartSection(hiper, color=WARNING_ORANGE, radius=45, title="Hiper"))
            
            if sections: 
                chart_container.content = ft.Row([ft.PieChart(sections=sections, sections_space=2, center_space_radius=30)], alignment=ft.MainAxisAlignment.CENTER)
            else: 
                chart_container.content = ft.Row([ft.Text("Sin datos", color=TEXT_MUTED)], alignment=ft.MainAxisAlignment.CENTER)
                
            page.update()

        def guardar_gl(e):
            try:
                val = float(tf_gl.value)
                estado = "Hipo" if val < 80 else ("Óptimo" if val <= 140 else "Hiper")
                ahora = datetime.datetime.now()
                app_data["glicemias"].append({"fecha": ahora.strftime("%Y-%m-%d"), "hora": ahora.strftime("%H:%M"), "valor": val, "momento": dd_mom.value, "estado_raw": estado})
                guardar_datos()
                tf_gl.value = ""
                actualizar_datos_estado()
                mostrar_alerta("Dato Glucémico Guardado", NEON_GREEN)
            except: mostrar_alerta(l["alerta_val"], DANGER_RED)

        dd_filtro.on_change = actualizar_datos_estado
        actualizar_datos_estado()

        btn_guardar = TacticalBtn("💾", NEON_PURPLE, guardar_gl)

        return ft.Column([
            ft.Row([tf_gl, dd_mom, btn_guardar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            dd_filtro,
            ft.Container(content=chart_container, bgcolor=CARD_BG, border_radius=10, padding=10),
            ft.Container(content=historial_lista, expand=True, bgcolor=CARD_BG, border_radius=10, padding=10)
        ], expand=True)

    def view_combate():
        nonlocal variante_rutina
        l = LANG[current_lang]
        meta = app_data["perfil"].get("meta_idx", 0)
        eq = app_data["perfil"].get("equipo_idx", 1)
        cond = app_data["perfil"].get("acondicionamiento", 3)
        
        rutinas = generar_pool_rutinas(meta, eq, cond)
        titulo, ejercicios, series_txt, recomendacion_cardio = rutinas[variante_rutina % len(rutinas)]
        
        num_series = int(series_txt.split('x')[0])
        total_checks = len(ejercicios) * num_series
        
        lbl_sync = ft.Text(f"{l['sync_rate']} 0%", color=NEON_GREEN, weight="bold")
        prog_bar = ft.ProgressBar(value=0, color=NEON_GREEN, bgcolor=SURFACE_COLOR)
        
        checks = []
        def update_progreso(e):
            completados = sum(1 for c in checks if c.value)
            prog_bar.value = completados / total_checks if total_checks else 0
            lbl_sync.value = f"{l['sync_rate']} {int(prog_bar.value * 100)}%"
            if prog_bar.value >= 1: lbl_sync.color = WARNING_ORANGE
            page.update()

        lista_ej = ft.ListView(expand=True, spacing=10)
        for ej in ejercicios:
            row_checks = ft.Row([ft.Checkbox(on_change=update_progreso, fill_color=NEON_PURPLE) for _ in range(num_series)])
            checks.extend(row_checks.controls)
            lista_ej.controls.append(ft.Container(content=ft.Row([ft.Text(ej, color=TEXT_WHITE, expand=True), row_checks]), bgcolor=CARD_BG, padding=10, border_radius=8))

        txt_timer = ft.Text("00:00", size=35, weight="bold", color=TEXT_WHITE, font_family="Consolas")
        timer_running = False

        def run_timer(segundos):
            nonlocal timer_running
            timer_running = False
            time.sleep(0.1) 
            timer_running = True
            
            for i in range(segundos, -1, -1):
                if not timer_running: break
                mins, secs = divmod(i, 60)
                txt_timer.value = f"{mins:02d}:{secs:02d}"
                txt_timer.color = TEXT_WHITE
                page.update()
                time.sleep(1)
            
            if timer_running: 
                txt_timer.color = DANGER_RED; page.update()

        def start_timer(s): page.run_task(run_timer, s)
        def stop_timer(e): nonlocal timer_running; timer_running = False; txt_timer.value="00:00"; page.update()
        
        def cambiar_rutina(e):
            nonlocal variante_rutina; variante_rutina += 1;
            master_container.content = view_combate(); page.update()

        btn_refresh = TacticalBtn("🔄", WARNING_ORANGE, cambiar_rutina)
        btn_stop = TacticalBtn("🛑", DANGER_RED, stop_timer)

        return ft.Column([
            ft.Row([ft.Text(f"{titulo} ({series_txt})", color=WARNING_ORANGE, size=20, weight="bold"), btn_refresh], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text(recomendacion_cardio, color=NEON_PURPLE, size=12, italic=True, weight="bold"),
            lbl_sync, prog_bar,
            ft.Container(content=lista_ej, expand=True),
            ft.Container(content=ft.Column([
                txt_timer,
                ft.Row([
                    ft.ElevatedButton("90s", on_click=lambda e: start_timer(90), bgcolor=NEON_GREEN, color=BG_COLOR),
                    ft.ElevatedButton("120s", on_click=lambda e: start_timer(120), bgcolor=WARNING_ORANGE, color=BG_COLOR),
                    btn_stop
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor=CARD_BG, padding=10, border_radius=10)
        ], expand=True)

    def view_energia():
        l = LANG[current_lang]
        dd_mom = ft.Dropdown(options=[ft.dropdown.Option(m) for m in l["momentos_lista"]], value=l["momentos_lista"][0], width=120, bgcolor=SURFACE_COLOR)
        tf_alim = ft.TextField(label=l["alimento"], expand=True, bgcolor=SURFACE_COLOR)
        tf_gr = ft.TextField(label=l["gramos"], width=80, keyboard_type=ft.KeyboardType.NUMBER, bgcolor=SURFACE_COLOR)
        lbl_status = ft.Text("", size=10, color=TEXT_MUTED)
        
        tabla = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("Alimento")), ft.DataColumn(ft.Text("Cat.")), ft.DataColumn(ft.Text("C/K"))],
            rows=[]
        )
        
        lbl_tot = ft.Text("C: 0g | K: 0kcal", color=NEON_GREEN, weight="bold", size=16)

        def calc_totales():
            tc = tk = 0.0
            for r in tabla.rows:
                vals = r.cells[2].content.value.split("/")
                tc += float(vals[0]); tk += float(vals[1])
            lbl_tot.value = f"C: {tc:.1f}g | K: {tk:.1f}kcal"
            page.update()

        def add_food(e):
            alim_raw = tf_alim.value.lower().strip()
            try: gr = float(tf_gr.value)
            except: mostrar_alerta(l["alerta_val"], DANGER_RED); return
            if not alim_raw: return

            dic = app_data["diccionario_magi"]
            alim_final = alim_raw
            
            if alim_raw not in dic:
                matches = difflib.get_close_matches(alim_raw, dic.keys(), n=1, cutoff=0.65)
                if matches: alim_final = matches[0]; lbl_status.value = f"Fuzzy: '{alim_raw}' ➔ '{alim_final}'"
            
            if alim_final in dic:
                c100 = dic[alim_final]["carbs"]; k100 = dic[alim_final]["kcal"]; cat = dic[alim_final].get("cat", "Otro")
                tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(alim_final.capitalize())),
                    ft.DataCell(ft.Text(cat, size=10)),
                    ft.DataCell(ft.Text(f"{(gr*c100)/100:.1f}/{(gr*k100)/100:.1f}"))
                ]))
                tf_alim.value = ""; tf_gr.value = ""
                calc_totales()
            else:
                mostrar_alerta("No encontrado.", WARNING_ORANGE)

        def limpiar(e): tabla.rows.clear(); calc_totales()

        btn_eliminar = TacticalBtn("🗑️", DANGER_RED, limpiar)

        return ft.Column([
            ft.Row([dd_mom, tf_alim]),
            ft.Row([tf_gr, ft.ElevatedButton(l["btn_anadir"], on_click=add_food, bgcolor=WARNING_ORANGE, color=TEXT_WHITE), btn_eliminar]),
            lbl_status,
            ft.Container(content=ft.Column([tabla], scroll=ft.ScrollMode.ALWAYS), expand=True, bgcolor=CARD_BG, border_radius=10),
            ft.Container(content=ft.Row([lbl_tot], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=10)
        ], expand=True)


    def show_onboarding_interface():
        page.appbar = None
        try:
            page.drawer = None
        except:
            pass
        master_container.content = build_onboarding()
        page.update()

    def show_main_interface():
        page.appbar = app_bar
        # En caso de que se necesite anclar internamente para versiones viejas
        try:
            page.drawer = drawer
        except Exception:
            pass
        master_container.content = view_mindset()
        page.update()

    # ==========================================
    # ARRANQUE DE LA APLICACIÓN
    # ==========================================
    page.add(master_container)
    
    if app_data.get("perfil", {}).get("configurado", False):
        show_main_interface()
    else:
        show_onboarding_interface()

ft.app(target=main)
