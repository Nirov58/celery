from django import template

register = template.Library()

THOSE_VERY_SEVEN_DIRTY_WORDS = [
    # WARNING: TAKE YOUR CHILDREN AWAY FROM THE SCREEN, YOU STUPID [CENSORED]
    "fuck", "Fuck",
    "shit", "Shit",
    "piss", "Piss",
    "cunt", "Cunt",
    "cocksucker", "Cocksucker",
    "motherfucker", "Motherfucker",
    "tits", "Tits"
]


@register.filter(name='censor')
def rkn_english_edition(value):
    if type(value) != str:
        raise ValueError
    for swear in THOSE_VERY_SEVEN_DIRTY_WORDS:
        if swear in value:
            value = value.replace(swear, swear[0] + "*" * (len(swear) - 1))
    return value
