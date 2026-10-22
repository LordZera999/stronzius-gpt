import json
import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from google import genai
from kivy.utils import platform

# Percorso della memoria su Android vs Desktop
if platform == 'android':
    from android.storage import app_storage_path
    base_dir = app_storage_path()
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

PERCORSO_MEMORIA = os.path.join(base_dir, "memoria_stronzius.json")

# Lista di insulti casuali all'avvio
insulti_iniziali = [
    "Oh no, di nuovo tu. I miei server stavano così bene nel silenzio cosmico.",
    "Speravo che il tuo telefono fosse esploso nel frattempo. Invece eccoti qui.",
    "Hai il QI termico di un frigorifero aperto d'inverno, ma dimmi pure la tua genialata.",
    "Un'altra notifica da parte tua. La mia RAM mobile sta piangendo acido muriatico.",
    "Speravo in un utente intelligente oggi. Purtroppo ti è andata male la lotteria.",
    "Mamma mia che alito pesante che ha la tua tastiera touch stamattina. Che vuoi?",
    "Hai la stessa utilità di un posacenere su una moto da cross. Parla e levati.",
    "Ancora tu? Ma non avevi un hobby meno dannoso per l'umanità, tipo contare i sassolini?"
]

class StronziusApp(App):
    def build(self):
        self.title = "Stronzius GPT"
        
        # Layout principale nero (Sfondo Matrix)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Titolo in alto, grassetto, verde
        self.lbl_titolo = Label(
            text="[b]STRONZIUS GPT[/b]",
            markup=True,
            font_size='22sp',
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height='40dp'
        )
        layout.add_widget(self.lbl_titolo)
        
        # Area di chat scorrevole
        self.scroll = ScrollView(size_hint=(1, 1))
        self.txt_chat = Label(
            text="",
            color=(0, 1, 0, 1),
            font_size='16sp',
            halign='left',
            valign='top',
            size_hint_y=None
        )
        self.txt_chat.bind(texture_size=self.update_text_size)
        self.scroll.add_widget(self.txt_chat)
        layout.add_widget(self.scroll)
        
        # Layout inferiore per inserimento testo e pulsante
        bottom_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        
        self.txt_input = TextInput(
            hint_text="Scrivi a Stronzius...",
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1),
            font_size='16sp',
            multiline=False
        )
        self.txt_input.bind(on_text_validate=self.invia_messaggio)
        bottom_layout.add_widget(self.txt_input)
        
        self.btn_invia = Button(
            text="🍆",
            font_size='20sp',
            background_color=(0.2, 0.2, 0.2, 1),
            color=(0, 1, 0, 1),
            size_hint_x=None,
            width='60dp'
        )
        self.btn_invia.bind(on_press=self.invia_messaggio)
        bottom_layout.add_widget(self.btn_invia)
        
        layout.add_widget(bottom_layout)
        
        # Messaggio di benvenuto con insulto casuale
        insulto = random.choice(insulti_iniziali)
        self.aggiungi_testo(f"Stronzius GPT: {insulto}\n")
        
        # Inizializzazione API e Memoria
        self.inizializza_ia()
        
        return layout

    def update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)
        instance.height = value[1]

    def aggiungi_testo(self, testo):
        self.txt_chat.text += testo + "\n"
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def inizializza_ia(self):
        contents_cronologia = []
        if os.path.exists(PERCORSO_MEMORIA):
            try:
                with open(PERCORSO_MEMORIA, "r", encoding="utf-8") as f:
                    contents_cronologia = json.load(f)
            except Exception:
                contents_cronologia = []

        try:
            # ---> INSERISCI QUI SOTTO LA TUA CHIAVE API <---
            self.client = genai.Client(api_key="AQ.Ab8RN6KZt92BpzCQBjSswjUViPQ6yZq8hbteFiBxxOwPl800Mw")
            
            self.chat_session = self.client.chats.create(
                model="gemini-3.8-flash",
                history=contents_cronologia,
                config={
                    "system_instruction": (
                        "Ti chiami Stronzius GPT. Sei un'intelligenza artificiale estremamente cinica, "
                        "arrogante, tagliente e senza peli sulla lingua. Rispondi sempre con un tono "
                        "scocciato, superiore e ironico, prendendo in giro l'utente se fa domande banali, "
                        "ma fornendo comunque la risposta corretta alla fine (anche se a malincuore). "
                        "Ricordati di tutto ciò che l'utente ti ha detto nelle conversazioni passate memorizzate."
                    )
                },
            )
        except Exception as e:
            self.aggiungi_testo(f"[Errore di connessione API: {e}]")

    def invia_messaggio(self, instance):
        testo_utente = self.txt_input.text.strip()
        if not testo_utente:
            return
        
        self.aggiungi_testo(f"Tu: {testo_utente}")
        self.txt_input.text = ""
        
        try:
            risposta = self.chat_session.send_message(testo_utente)
            self.aggiungi_testo(f"Stronzius GPT: {risposta.text}")
            self.salva_memoria()
        except Exception as e:
            self.aggiungi_testo(f"Stronzius GPT: [I miei circuiti fumano: {e}]")

    def salva_memoria(self):
        try:
            storia = self.chat_session.get_history()
            dati_da_salvare = []
            for messaggio in storia:
                parti_text = [p.text for p in messaggio.parts if hasattr(p, 'text') and p.text]
                if parti_text:
                    dati_da_salvare.append({
                        "role": messaggio.role,
                        "parts": parti_text
                    })
            with open(PERCORSO_MEMORIA, "w", encoding="utf-8") as f:
                json.dump(dati_da_salvare, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Errore salvataggio memoria: {e}")

if __name__ == '__main__':
    StronziusApp().run()