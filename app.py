import json
import gradio as gr
from tokenizers import Tokenizer


# Wörterbuch laden
with open("dictionary.json", "r", encoding="utf-8") as f:
    dictionary = json.load(f)


# K-Laut-Tokenizer laden
tokenizer = Tokenizer.from_file(
    "tokenizer_70_klaut.json"
)


def k_laut_ai(choice, text):

    text = text.strip().replace(" ", "")

    # Wörterbuch-Eintrag suchen
    entry = None
    word = None

    for key, data in dictionary.items():

        if choice == "K-Laut" and text in data.get("k_laut", []):
            entry = data
            word = key
            break

        elif choice == "Hangul" and text in data.get("korean", []):
            entry = data
            word = key
            break

        elif choice == "Deutsch" and data.get("bedeutung") == text:
            entry = data
            word = key
            break

        elif choice == "Sildam" and data.get("sildam") == text:
            entry = data
            word = key
            break

    if not entry:
        return "Eintrag nicht im Wörterbuch gefunden."

    k_laut = entry["k_laut"]

    result = []

    result.append(f"Eingabe: {text}")
    result.append(f"K-Laut: {k_laut}")
    result.append("")

    for kl in k_laut:

        encoding = tokenizer.encode(kl)

        result.append(f"K-Laut-Variante: {kl}")
        result.append(f"Tokens: {encoding.tokens}")
        result.append(f"IDs: {encoding.ids}")
        result.append("")

    result.append(f"Wort: {word}")
    result.append(f"Sildam: {entry.get('sildam', '')}")
    result.append(f"Hangul: {entry.get('korean', '')}")
    result.append(f"Deutsch: {entry.get('bedeutung', '')}")

    return "\n".join(result)


# Gradio-Oberfläche


with gr.Blocks(title="K-Laut AI") as demo:

    gr.Markdown(
        """
        # K-Laut AI

        ### K-Laut – Sprache, Klang und Tokenisierung

        Eine experimentelle K-Laut-Sprachoberfläche.
        """
    )

    start_button = gr.Button(
        "K-Laut AI starten",
        variant="primary",
        size="lg"
    )

    input_area = gr.Group(visible=False)

    with input_area:

        choice = gr.Dropdown(
            ["K-Laut", "Hangul", "Deutsch", "Sildam"],
            label="Eingabeart",
            value="K-Laut"
        )

        text = gr.Textbox(
            label="Eingabe",
            placeholder="z. B. ㅁㅡㄹ"
        )

        submit_button = gr.Button(
            "Suchen",
            variant="primary"
        )

        output = gr.Textbox(
            label="K-Laut AI Ausgabe",
            lines=15
        )

        submit_button.click(
            fn=k_laut_ai,
            inputs=[choice, text],
            outputs=output
        )

    start_button.click(
        fn=lambda: gr.update(visible=True),
        inputs=None,
        outputs=input_area
    )


demo.launch()






