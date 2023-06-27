import random

from dotenv import load_dotenv
from Utils.logger import log

import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPEN_AI_KEY")

personalities: list[str] = [
    "Aggressif",
    "Homme d'affaire",
    "Timide",
    "Extraverti",
    "Introverti",
    "Audacieux"
    "Rêveuse/ur",
    "Intrigué",
    "Gourmand",
    "Joyeux",
    "Distingué"
    "Déterminé",
    "Excentrique",
]

pnjs: list[str] = [
    "Pirate",
    "Francait avec l'accent anglais",
    "Francais avec un accent ch'ti",
    "Allemand qui parle un peu francais",
    "Francais avec un accent du sud",
    "Francais de Paris",
    "Poisson",
    "Homer Simpson",
    "Président de la république",
    "Jessie Pinkman",
    "Spiderman",
    "Quelqu'un qui bégaie",
    "Enfant de 5 ans"
]

meals: list[dict[str, list[str] | str]] = [
    {
        "type": "hamburger",
        "name": "Hamburger simple",
        "meals": [
            "steak"
        ]
    },
    {
        "type": "hamburger",
        "name": "Hamburger au fromage",
        "meals": [
            "steak",
            "fromage"
        ]
    },
    {
        "type": "hamburger",
        "name": "Double Hamburger",
        "meals": [
            "steak",
            "fromage",
            "steak"
            "onion"
            "bacon"
        ]
    },
    {
        "type": "hamburger",
        "name": "Le monstre",
        "meals": [
            "steak",
            "fromage",
            "steak",
            "onion",
            "fromage",
            "steak",
        ]
    },

]


def is_empty_or_null(s):
    return s is None or not s.strip()


class Order:
    id: int
    meal: str
    personality: str
    pnj: str
    sentence: str = None

    def __init__(self, id: int = -1, meal: str = None, personality: str = None, pnj: str = None):

        self.id = id

        if is_empty_or_null(meal):
            self.meal = random.choice(meals)["name"]
        else:
            self.meal = meal

        if is_empty_or_null(personality):
            self.personality = random.choice(personalities)
        else:
            self.personality = personality

        if is_empty_or_null(pnj):
            self.pnj = random.choice(pnjs)
        else:
            self.pnj = pnj

    def __str__(self):
        return self.format_order()

    def __repr__(self):
        return self.format_order()

    def format_order(self) -> str:
        """Format a meal with personality and pnj

        :param order: order to format
        :return: formatted meal
        """

        value: str = f"id: {self.id}\n"
        value: str = f"Plat: {self.meal}\n"

        for recipe in meals:
            if recipe["name"] == self.meal:
                for aliment in recipe["meals"]:
                    value += f"- {aliment}\n"

        value += f"Personne: {self.pnj}\n"
        value += f"Personnalité: {self.personality}\n"
        value += "\n"
        value += "Texte du client :\n"

        return value

    def get_sentence(self) -> str:
        """Get a sentence from the order

        :return: sentence.
        """

        if is_empty_or_null(self.sentence):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Je vais te donner un plat avec une liste d'aliments, un accent, un trait de personnalité. Tu dois me générer un texte d'un client faisant maximum 4 phrases appelant au téléphone un restaurent pour lui commander ce plat avec ses aliments précis.\nLe texte ne doit pas contenir un seule alimiment non listé plus haut.\nL'accent doit être visible dans le texte.\nNe précise pas les traits de personnalité dans la commande, ils doivent être implicite\n\n\n\nPlat: Pizza 4 fromage\nAliments:\n- Fromage de chèvre\n- Mozarella\n- Raclette\n- Ementale\nPersonne: Francais de Pirate\nPersonnalité: Aggressif\n\nTexte du client :\nYarrrr ! J'veux une pizza 4 fromage tout d'suite ! Avec du fromage de chèvre, de la mozarella, de la raclette et de l'ementale ! J'veux ça maintenant !\n\n\nPlat: Hamburger barbecue\nAliments:\n- steak\n- cheddar\n- beacon\n- salade\n- tomate\n- oignon\n- sauce barbecue\nPersonne: Francait avec l'accent anglais\nPersonnalité: Homme d'affaire\n\nTexte du client :\nHello, je vais vous prendre un Hamburge, avec un steak, du cheddar, du beacon, de la salade, de la tomate, de l'oignon et de la sauce barbecue. Thank you very much.\n\n\nPlat: Pizza pepperoni\nAliments:\n- pepperoni\nPersonne: Francait normal\nPersonnalité: Enfant de 5 ans\n\nTexte du client :\nB-b-b-bonjour monsieur ! J'aimerais bien une p-p-pizza pepperoni s'il vous plaît ! Avec du pepperoni et rien d'autre ! Au revoir monsieur !\n\n\nPlat: Pizza paysanne\nAliments:\n- Bacon\n- Pomme de terre\n- Jambon\nPersonne: Francais avec un accent espagnol\nPersonnalité: Timide\n\nTexte du client :\nHola, je voudrais une pizza paysanne s'il vous plait. Avec du bacon, des pommes de terre et du jambon. Est-ce possible ? Muchas gracias.\n\n\nPlat: Sandwich au jambon\nAliments:\n- Jambon\n- Mayonnaise\n- Fromage\n- Laitue\nPersonne: Francais normal\nPersonnalité: Enfant de 5 ans\n\nTexte du client :\nBonjour monsieur, ma maman voudrai un sandwich au jambon. Avec du jambon, de la mayonnaise, du fromage et de la laitue. Merci beaucoup !\n\n\nPlat: Salade de fruits\nAliments: \n- Ananas\n- Fraise\n- Framboise\n- Kiwi\nPersonne: Francais avec un accent ch'ti\nPersonnalité: Extraverti\n\nTexte du client :\nAh bin alors, j'ai envie d'une salade de fruits ! Avec de l'ananas, des fraises, des framboises et du kiwi ! Faites vite ça me d'mande !\n\n\nPlat: Lasagne\nAliments: \n- Viande hachée\n- Tomates\n- Oignons\nPersonne: Allemand qui parle un peu francais\nPersonnalité: Introverti\n\nTexte du client :\nGuten Tag, ich möchte eine Lasagne bitte. Mit Viande hachée, Tomates und Oignons. Danke sehr.\n\n\nPlat: Quiche Lorraine\nAliments: \n- Lardons\n- Fromage\n- Oeufs\nPersonne: Francais  avec un accent du sud\nPersonnalité: Audacieux\n\nTexte du client :\nHo fada ! J'ai besoing d'une Quiche Lorraine tout de suite ! Avec des lardons, du fromage et des oeufs ! Allez, magnez-vous !\n\n\nPlat: Gratin de courgettes\nAliments: \n- Courgettes\n- Oignons\n- Gruyère\nPersonne: Francais de Paris\nPersonnalité: Rêveuse\n\nTexte du client :\nBonjourrrr, je voudrais un gratin de courgettes s'il vous plait. Avec des courgettes, des oignons et du gruyère. Merciiii beaucoup.\n\n\nPlat:  Quiche aux légumes\nAliments:\n- Tomates\n- Courgettes\n- Carottes\nPersonne: Francais avec un accent arabe\nPersonnalité: Intrigué\n\nTexte du client :\nSalaam alaykoum ! Je voudrais une quiche aux légumes s'il vous plait. Avec des tomates, des courgettes et des carottes. Inchallah !\n\n\nPlat:  Croque-Monsieur\nAliments:\n- Fromage\n- Jambon\nPersonne: Poisson\nPersonnalité: Gourmand\n\nTexte du client :\nBlub blub ! J'aimerai un Croque-Monsieur. Avec du fromage et du jambon ! Y a pas le feu au lac !\n\n\nPlat:  Salade César\nAliments:\n- Laitue\n- Olives\n- Oeuf\n- Parmesan\nPersonne: Homer Simpson\nPersonnalité: Joyeux\n\nTexte du client :\nMmhmmm ! J'ai envie d'une salade César ! Avec de la laitue, des olives, des oeufs et du parmesan ! Oh pinaise\n\n\nPlat: Salade Nicoise\nAliments: \n- Thon\n- Tomates\n- Haricots verts\n- Olives\nPersonne: Président de la république\nPersonnalité: Distingué\n\nTexte du client :\nFrançais, Française. Je souhaiterais une salade Nicoise. Avec du thon, des tomates, des haricots verts et des olives. Vive la république\n\n\nPlat:  Pâtes sautées\nAliments:\n- Pâtes\n- Lardons\n- Crème fraiche\nPersonne: Jessie Pinkman\nPersonnalité: Déterminé\n\nTexte du client :\nYo bitch! Je voudrai des pâtes sautées. Avec des pâtes, des lardons et de la crème fraiche. Faites vite, j'ai pas toute la journée !\n\n\nPlat: Soupes aux légumes\nAliments:\n- Carottes\n- Oignons\n- Patates\nPersonne: Francais normal\nPersonnalité: Excentrique\n\nTexte du client :\nOh mon Dieu ! J'ai une folle envie de soupe aux légumes. Avec des carottes, des oignons et des patates ! Faites-moi rêver !\n\n\nPlat:  Salade de pâtes\nAliments: \n- Pâtes\n- Tomates\n- Oignons\n- Jambon\nPersonne: Spiderman\nPersonnalité: Débrouillard\n\nTexte du client :\nHey les amis ! Je voudrais une salade de pâtes. Avec des pâtes, des tomates, des oignons et du jambon. Vite, vite, ça presse !\n\nPlat:  Gratin de poisson\nAliments: \n- Poisson\n- Oignons\n- Tomates\n- Fromage\nPersonne: Quelqu'un qui bégaie\nPersonnalité: Timide\n\nTexte du client :\nB-b-b-bonjour, je v-v-voudrais un gratin de p-p-poisson s'il vous plaît. Avec du p-p-poisson, des oignons, des tomates et du fromage. M-m-merci beaucoup."
                       + str(self),
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            self.sentence = response["choices"][0]["text"]

        return self.sentence

    def get_ingredients(self) -> list[str]:
        for meal in meals:
            if meal["name"] == self.meal:
                return meal["meals"]
        return []

    def get_type(self) -> str:
        for meal in meals:
            if meal["name"] == self.meal:
                return meal["type"]
        return ""

    def to_dict(self) -> dict[str, str | list[str]]:
        value: dict[str, str | list[str]] = {
            "id": self.id,
            "type": self.get_type(),
            "meal": self.meal,
            "ingredients": self.get_ingredients(),
            "pnj": self.pnj,
            "personality": self.personality,

            "sentence": self.get_sentence(),
        }

        return value
