"""
Anime Carousel – Flask backend
Run:  pip install -r requirements.txt
      python index.py
Open: http://127.0.0.1:5000

Put each character image in images/ using the matching image_file
name in CHARACTERS. If an image is missing, a generated placeholder is shown.
"""
from html import escape
from pathlib import Path

from flask import Flask, Response, abort, jsonify, render_template, send_from_directory, url_for

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"
EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

app = Flask(__name__, template_folder=".", static_folder=None)

CHARACTERS = [
    {
        "id": "all-might",
        "image_file": "all-might.jpg",
        "name": "All Might (Toshinori Yagi)",
        "anime": "My Hero Academia",
        "tags": ["Hero", "Mentor", "Symbol of Peace"],
        "bio": "The world’s most celebrated hero and the former holder of One For All. "
               "After choosing Izuku Midoriya as his successor, All Might mentors him "
               "while fighting to inspire people even after losing most of his power.",
    },
    {
        "id": "asta",
        "image_file": "asta.jpg",
        "name": "Asta",
        "anime": "Black Clover",
        "tags": ["Magic Knight", "Anti-magic", "Black Bulls"],
        "bio": "Born without magic in a world where magic defines status, Asta joins "
               "the Black Bulls and wields anti-magic swords. His persistence fuels "
               "his dream of becoming the Clover Kingdom’s Wizard King.",
    },
    {
        "id": "bachira",
        "image_file": "bachira.jpg",
        "name": "Meguru Bachira",
        "anime": "Blue Lock",
        "tags": ["Striker", "Dribbler", "Blue Lock"],
        "bio": "A creative forward whose instinctive dribbling makes him unpredictable "
               "on the pitch. Through Blue Lock, Bachira learns to trust his own style "
               "and compete as an independent striker.",
    },
    {
        "id": "baki",
        "image_file": "baki.jpg",
        "name": "Baki Hanma",
        "anime": "Baki",
        "tags": ["Martial artist", "Fighter", "Hanma"],
        "bio": "A fiercely determined young martial artist who trains to surpass his "
               "father, Yujiro Hanma, known as the world’s strongest creature. Baki’s "
               "battles test both his technique and his limits.",
    },
    {
        "id": "chainsawman",
        "image_file": "chainsawman.jpg",
        "name": "Denji",
        "anime": "Chainsaw Man",
        "tags": ["Devil Hunter", "Chainsaw Devil", "Public Safety"],
        "bio": "After a betrayal leaves him near death, impoverished devil hunter Denji "
               "merges with Pochita and becomes Chainsaw Man. He joins Public Safety, "
               "chasing simple comforts while confronting dangerous devils.",
    },
    {
        "id": "escanor",
        "image_file": "escanor.jpg",
        "name": "Escanor",
        "anime": "The Seven Deadly Sins",
        "tags": ["Lion’s Sin of Pride", "Sunshine", "Seven Deadly Sins"],
        "bio": "The Lion’s Sin of Pride whose Sunshine power grows with the sun, making "
               "him timid at night and overwhelmingly strong at noon. Escanor fights "
               "beside the Seven Deadly Sins and accepts the cost of his power.",
    },
    {
        "id": "goblin-slayer",
        "image_file": "goblin-slayer.jpg",
        "name": "Goblin Slayer",
        "anime": "Goblin Slayer",
        "tags": ["Adventurer", "Tactician", "Goblin hunter"],
        "bio": "A silver-ranked adventurer who devotes himself to eliminating goblins. "
               "Rather than relying on brute strength, he uses preparation, knowledge "
               "of his enemy, and practical tactics to protect nearby communities.",
    },
    {
        "id": "ichigo",
        "image_file": "ichigo.jpg",
        "name": "Ichigo Kurosaki",
        "anime": "Bleach",
        "tags": ["Soul Reaper", "Protector", "Substitute"],
        "bio": "A teenager who gains Soul Reaper powers and takes on the duty of "
               "protecting people from Hollows. Ichigo’s journey brings him into "
               "conflict with threats spanning the worlds of the living and the dead.",
    },
    {
        "id": "kaiju-8",
        "image_file": "kaiju-8.jpg",
        "name": "Kafka Hibino",
        "anime": "Kaiju No. 8",
        "tags": ["Defense Force", "Kaiju", "Determined"],
        "bio": "A cleanup worker who has long dreamed of joining the Anti-Kaiju Defense "
               "Force. After gaining the ability to transform into a kaiju, Kafka must "
               "hide his secret while fighting to defend Japan alongside his comrades.",
    },
    {
        "id": "kira",
        "image_file": "kira.jpg",
        "name": "Light Yagami (Kira)",
        "anime": "Death Note",
        "tags": ["Thriller", "Death Note", "Mastermind"],
        "bio": "A brilliant student who discovers a notebook that can kill anyone "
               "whose name is written in it. Taking the name Kira, Light tries to "
               "reshape the world while a determined detective closes in.",
    },
    {
        "id": "levi",
        "image_file": "levi.jpg",
        "name": "Levi Ackerman",
        "anime": "Attack on Titan",
        "tags": ["Captain", "Survey Corps", "Soldier"],
        "bio": "Humanity’s strongest soldier and a captain in the Survey Corps. "
               "Calm and exacting in battle, Levi uses his exceptional skill to fight "
               "Titans while carrying the losses of the soldiers under his command.",
    },
    {
        "id": "luffy",
        "image_file": "luffy.jpg",
        "name": "Monkey D. Luffy",
        "anime": "One Piece",
        "tags": ["Pirate", "Captain", "Straw Hat"],
        "bio": "Captain of the Straw Hat Pirates, Luffy sets sail in search of the "
               "legendary One Piece and the title of Pirate King. His rubber-like "
               "powers, fearless optimism, and loyalty draw a diverse crew to his side.",
    },
    {
        "id": "macks",
        "image_file": "macks.jpg",
        "name": "Macxs the Creator",
        "anime": "XXX Code of Shadows",
        "tags": ["Creator", "Reality-shaping", "Purple · Red · Green"],
        "bio": "A creator figure from an upcoming anime, distinct from the other Macxs. "
               "Like Zeno-sama in the comic, he can make anything happen within his "
               "creations. He has three brothers whose power is red; Macxs is associated "
               "with purple, red, and green.",
    },
    {
        "id": "pain",
        "image_file": "pain.jpg",
        "name": "Pain (Nagato)",
        "anime": "Naruto Shippuden",
        "tags": ["Akatsuki", "Rinnegan", "Antagonist"],
        "bio": "The name used by Nagato and the Six Paths he controls. Shaped by war "
               "and loss, Pain leads the Akatsuki and seeks peace through overwhelming "
               "power, becoming one of Naruto’s most consequential opponents.",
    },
    {
        "id": "sung-jin-woo",
        "image_file": "sung-jin-woo.jpg",
        "name": "Sung Jinwoo",
        "anime": "Solo Leveling",
        "tags": ["Hunter", "Shadow Monarch", "Leveling"],
        "bio": "Once known as the weakest hunter, Jinwoo survives a deadly dungeon and "
               "gains a mysterious system that lets him grow stronger. His rise draws "
               "him into a conflict threatening the entire world.",
    },
    {
        "id": "tanjiro",
        "image_file": "tanjiro.jpg",
        "name": "Tanjiro Kamado",
        "anime": "Demon Slayer: Kimetsu no Yaiba",
        "tags": ["Demon Slayer", "Swordsman", "Compassionate"],
        "bio": "After demons attack his family and his sister Nezuko is transformed, "
               "Tanjiro joins the Demon Slayer Corps to find a cure. His sharp senses "
               "and resolve are matched by compassion for those he faces.",
    },
    {
        "id": "thorfinn",
        "image_file": "thorfinn.jpg",
        "name": "Thorfinn",
        "anime": "Vinland Saga",
        "tags": ["Warrior", "Viking", "Revenge"],
        "bio": "A young Icelandic warrior consumed by revenge after his father’s death. "
               "Through years of conflict and hardship, Thorfinn confronts the violence "
               "that shaped him and searches for a more peaceful purpose.",
    },
    {
        "id": "okarun",
        "image_file": "ukarun.jpg",
        "name": "Ken Takakura (Okarun)",
        "anime": "Dandadan",
        "tags": ["Occult", "Alien encounters", "Turbo Granny"],
        "bio": "A shy occult enthusiast nicknamed Okarun who gets caught up in bizarre "
               "encounters with aliens and spirits alongside Momo Ayase. A supernatural "
               "curse gives him unusual powers and pulls him into their adventures.",
    },
    {
        "id": "vegeta",
        "image_file": "vegeta.jpg",
        "name": "Vegeta",
        "anime": "Dragon Ball",
        "tags": ["Saiyan", "Prince", "Rival"],
        "bio": "The proud prince of the Saiyans begins as an enemy of Goku, then becomes "
               "one of Earth’s fiercest defenders. His rivalry with Goku drives him to "
               "push beyond his limits and redefine what strength means to him.",
    },
    {
        "id": "yuji",
        "image_file": "yuji.jpg",
        "name": "Yuji Itadori",
        "anime": "Jujutsu Kaisen",
        "tags": ["Jujutsu Sorcerer", "Sukuna", "Courage"],
        "bio": "A kind-hearted student who becomes the vessel of the powerful curse "
               "Sukuna after swallowing one of his fingers. Yuji enters the world of "
               "jujutsu sorcery and fights curses while trying to give people a proper end.",
    },
]

BY_ID = {c["id"]: c for c in CHARACTERS}


def find_image(char_id):
    """Return the filename of a real image for this character, or None."""
    char = BY_ID.get(char_id)
    if char and "image_file" in char:
        image_file = char["image_file"]
        return image_file if (IMAGE_DIR / image_file).is_file() else None
    for ext in EXTENSIONS:
        if (IMAGE_DIR / f"{char_id}{ext}").exists():
            return f"{char_id}{ext}"
    return None


def placeholder_svg(char):
    """Generate a dark indigo placeholder so the UI works before you add images."""
    index = CHARACTERS.index(char)
    hue = (245 + index * 18) % 360
    initials = "".join(w[0] for w in char["name"].split()[:2]).upper()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="hsl({hue},70%,22%)"/>
<stop offset="1" stop-color="hsl({(hue + 40) % 360},60%,8%)"/>
</linearGradient>
</defs>
<rect width="1200" height="800" fill="url(#g)"/>
<circle cx="900" cy="220" r="260" fill="hsl({hue},80%,60%)" opacity=".12"/>
<text x="600" y="460" text-anchor="middle" font-family="Arial, sans-serif" font-size="260" font-weight="800" fill="#fff" opacity=".9">{escape(initials)}</text>
<text x="600" y="580" text-anchor="middle" font-family="Arial, sans-serif" font-size="44" fill="#fff" opacity=".6">{escape(char["name"])}</text>
</svg>"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/style.css")
def stylesheet():
    return send_from_directory(BASE_DIR, "style.css")


@app.route("/script.js")
def javascript():
    return send_from_directory(BASE_DIR, "script.js")


@app.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(IMAGE_DIR, filename)


@app.route("/api/characters")
def api_characters():
    data = []
    for c in CHARACTERS:
        real = find_image(c["id"])
        image = (
            url_for("image_file", filename=real)
            if real
            else url_for("placeholder", char_id=c["id"])
        )
        public_data = {key: value for key, value in c.items() if key != "image_file"}
        data.append({**public_data, "image": image, "download": url_for("download", char_id=c["id"])})
    return jsonify(data)


@app.route("/placeholder/<char_id>.svg")
def placeholder(char_id):
    char = BY_ID.get(char_id) or abort(404)
    return Response(placeholder_svg(char), mimetype="image/svg+xml")


@app.route("/download/<char_id>")
def download(char_id):
    """Forces the browser to save the image to the user's device."""
    char = BY_ID.get(char_id) or abort(404)
    real = find_image(char_id)
    if real:
        return send_from_directory(IMAGE_DIR, real, as_attachment=True)
    return Response(
        placeholder_svg(char),
        mimetype="image/svg+xml",
        headers={"Content-Disposition": f"attachment; filename={char_id}.svg"},
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)