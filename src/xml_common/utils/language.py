from __future__ import annotations

from enum import Enum


TWO_LETTERS = {
    "en": "ENG",
    "ja": "JPN",
    "es": "SPA",
    "it": "ITA",
    "ru": "RUS",
    "pl": "POL",
    "fi": "FIN",
    "pt": "POR",
    "ca": "CAT",
    "tr": "TUR",
    "no": "NOR",
    "sv": "SWE",
    "nb": "NOB",
    "nn": "NNO",
    "co": "COS",
    "hu": "HUN",
    "af": "AFR",
    "hr": "HRV",
    "sl": "SLV",
    "gl": "GLG",
    "gd": "GLA",
    "da": "DAN",
    "et": "EST",
    "ar": "ARA",
    "he": "HEB",
    "sr": "SRP",
    "mt": "MLT",
    "mg": "MLG",
    "vi": "VIE",
    "wo": "WOL",
    "tl": "TGL",
    "ko": "KOR",
    "fo": "FAO",
    "sm": "SMO",
    "so": "SOM",
    "km": "KHM",
    "te": "TEL",
    "ta": "TAM",
    "id": "IND",
    "ty": "TAH",
    "sw": "SWA",
    "dv": "DIV",
    "ml": "MAL",
    "th": "THA",
    "jv": "JAV",
    "mr": "MAR",
    "gu": "GUJ",
    "to": "TON",
    "fj": "FIJ",
    "sd": "SND",
    "kn": "KAN",
    "si": "SIN",
    "mh": "MAH",
    "bg": "BUL",
    "kl": "KAL",
    "gv": "GLV",
    "iu": "IKU",
    "bn": "BEN",
    "ch": "CHA",
    "lt": "LIT",
    "lv": "LAV",
    "ky": "KIR",
    "am": "AMH",
    "uk": "UKR",
    "ve": "VEN",
    "ks": "KAS",
    "ne": "NEP",
    "cr": "CRE",
    "ee": "EWE",
    "or": "ORI",
    "eo": "EPO",
    "de": "DEU",
    "nl": "NLD",
    "fr": "FRA",
    "el": "ELL",
    "cs": "CES",
    "sq": "SQI",
    "ka": "KAT",
    "zh": "ZHO",
    "eu": "EUS",
    "ro": "RON",
    "sk": "SLK",
    "is": "ISL",
    "mi": "MRI",
    "cy": "CYM",
    "ms": "MSA",
    "fa": "FAS",
    "my": "MYA",
    "mk": "MKD",
}


class Language(Enum):
    """
    The language of the resource.

    Attributes
    ----------
    ENG : str
        English language.
    JPN : str
        Japanese language.
    SPA : str
        Spanish language.
    ITA : str
        Italian language.
    RUS : str
        Russian language.
    POL : str
        Polish language.
    FIN : str
        Finnish language.
    POR : str
        Portuguese language.
    CAT : str
        Catalan language.
    TUR : str
        Turkish language.
    NOR : str
        Norwegian language.
    SWE : str
        Swedish language.
    NOB : str
        Bokmål, Norwegian language.
    NNO : str
        Norwegian Nynorsk language.
    COS : str
        Corsican language.
    HUN : str
        Hungarian language.
    AFR : str
        Afrikaans language.
    HRV : str
        Croatian language.
    SLV : str
        Slovenian language.
    GLG : str
        Galician language.
    GLA : str
        Gaelic language.
    DAN : str
        Danish language.
    EST : str
        Estonian language.
    ARA : str
        Arabic language.
    SCO : str
        Scots language.
    HEB : str
        Hebrew language.
    SRP : str
        Serbian language.
    MLT : str
        Maltese language.
    MLG : str
        Malagasy language.
    VIE : str
        Vietnamese language.
    WOL : str
        Wolof language.
    HAW : str
        Hawaiian language.
    TGL : str
        Tagalog language.
    ROM : str
        Romany language.
    PAP : str
        Papiamento language.
    KOR : str
        Korean language.
    FAO : str
        Faroese language.
    SMO : str
        Samoan language.
    SOM : str
        Somali language.
    KHM : str
        Central Khmer language.
    TEL : str
        Telugu language.
    TAM : str
        Tamil language.
    IND : str
        Indonesian language.
    TAH : str
        Tahitian language.
    NIU : str
        Niuean language.
    SWA : str
        Swahili language.
    SRN : str
        Sranan Tongo language.
    DIV : str
        Divehi language.
    TKL : str
        Tokelau language.
    MAL : str
        Malayalam language.
    THA : str
        Thai language.
    JAV : str
        Javanese language.
    MAR : str
        Marathi language.
    GUJ : str
        Gujarati language.
    BIK : str
        Bikol language.
    TSI : str
        Tsimshian language.
    TON : str
        Tonga (Tonga Islands) language.
    FIJ : str
        Fijian language.
    PAU : str
        Palauan language.
    ACE : str
        Achinese language.
    PAG : str
        Pangasinan language.
    ILO : str
        Iloko language.
    WAR : str
        Waray language.
    SND : str
        Sindhi language.
    PAM : str
        Pampanga language.
    CEB : str
        Cebuano language.
    KAN : str
        Kannada language.
    HAI : str
        Haida language.
    SIN : str
        Sinhala language.
    FON : str
        Fon language.
    FAN : str
        Fang language.
    MAH : str
        Marshallese language.
    TVL : str
        Tuvalu language.
    BUL : str
        Bulgarian language.
    KAL : str
        Kalaallisut language.
    GLV : str
        Manx language.
    IKU : str
        Inuktitut language.
    BEN : str
        Bengali language.
    HIL : str
        Hiligaynon language.
    MEN : str
        Mende language.
    CHA : str
        Chamorro language.
    LIT : str
        Lithuanian language.
    LAV : str
        Latvian language.
    KIR : str
        Kirghiz language.
    AMH : str
        Amharic language.
    UKR : str
        Ukrainian language.
    VEN : str
        Venda language.
    KAS : str
        Kashmiri language.
    RAP : str
        Rapanui language.
    NEP : str
        Nepali language.
    KOK : str
        Konkani language.
    CRE : str
        Cree language.
    KOS : str
        Kosraean language.
    SUS : str
        Susu language.
    EWE : str
        Ewe language.
    ORI : str
        Oriya language.
    EPO : str
        Esperanto language.
    DEU : str
        German language.
    NLD : str
        Dutch language.
    FRA : str
        French language.
    ELL : str
        Greek, Modern (1453-) language.
    CES : str
        Czech language.
    SQI : str
        Albanian language.
    KAT : str
        Georgian language.
    ZHO : str
        Chinese language.
    EUS : str
        Basque language.
    RON : str
        Romanian language.
    SLK : str
        Slovak language.
    ISL : str
        Icelandic language.
    MRI : str
        Maori language.
    CYM : str
        Welsh language.
    MSA : str
        Malay language.
    FAS : str
        Persian language.
    MYA : str
        Burmese language.
    MKD : str
        Macedonian language.
    MEY : str
        Hassaniyya language.
    CMN : str
        Mandarin Chinese language.
    DNJ : str
        Dan language.
    BCN : str
        Bali (Nigeria) language.
    VIF : str
        Vili language.
    NLG : str
        Gela language.
    CAL : str
        Carolinian language.
    UND : str
        Undetermined code for unknown languages.
    """
    ENG = "English"
    JPN = "Japanese"
    SPA = "Spanish"
    ITA = "Italian"
    RUS = "Russian"
    POL = "Polish"
    FIN = "Finnish"
    POR = "Portuguese"
    CAT = "Catalan"
    TUR = "Turkish"
    NOR = "Norwegian"
    SWE = "Swedish"
    NOB = "Bokmål, Norwegian"
    NNO = "Norwegian Nynorsk"
    COS = "Corsican"
    HUN = "Hungarian"
    AFR = "Afrikaans"
    HRV = "Croatian"
    SLV = "Slovenian"
    GLG = "Galician"
    GLA = "Gaelic"
    DAN = "Danish"
    EST = "Estonian"
    ARA = "Arabic"
    SCO = "Scots"
    HEB = "Hebrew"
    SRP = "Serbian"
    MLT = "Maltese"
    MLG = "Malagasy"
    VIE = "Vietnamese"
    WOL = "Wolof"
    HAW = "Hawaiian"
    TGL = "Tagalog"
    ROM = "Romany"
    PAP = "Papiamento"
    KOR = "Korean"
    FAO = "Faroese"
    SMO = "Samoan"
    SOM = "Somali"
    KHM = "Central Khmer"
    TEL = "Telugu"
    TAM = "Tamil"
    IND = "Indonesian"
    TAH = "Tahitian"
    NIU = "Niuean"
    SWA = "Swahili"
    SRN = "Sranan Tongo"
    DIV = "Divehi"
    TKL = "Tokelau"
    MAL = "Malayalam"
    THA = "Thai"
    JAV = "Javanese"
    MAR = "Marathi"
    GUJ = "Gujarati"
    BIK = "Bikol"
    TSI = "Tsimshian"
    TON = "Tonga (Tonga Islands)"
    FIJ = "Fijian"
    PAU = "Palauan"
    ACE = "Achinese"
    PAG = "Pangasinan"
    ILO = "Iloko"
    WAR = "Waray"
    SND = "Sindhi"
    PAM = "Pampanga"
    CEB = "Cebuano"
    KAN = "Kannada"
    HAI = "Haida"
    SIN = "Sinhala"
    FON = "Fon"
    FAN = "Fang"
    MAH = "Marshallese"
    TVL = "Tuvalu"
    BUL = "Bulgarian"
    KAL = "Kalaallisut"
    GLV = "Manx"
    IKU = "Inuktitut"
    BEN = "Bengali"
    HIL = "Hiligaynon"
    MEN = "Mende"
    CHA = "Chamorro"
    LIT = "Lithuanian"
    LAV = "Latvian"
    KIR = "Kirghiz"
    AMH = "Amharic"
    UKR = "Ukrainian"
    VEN = "Venda"
    KAS = "Kashmiri"
    RAP = "Rapanui"
    NEP = "Nepali"
    KOK = "Konkani"
    CRE = "Cree"
    KOS = "Kosraean"
    SUS = "Susu"
    EWE = "Ewe"
    ORI = "Oriya"
    EPO = "Esperanto"
    DEU = "German"
    NLD = "Dutch"
    FRA = "French"
    ELL = "Greek, Modern (1453-)"
    CES = "Czech"
    SQI = "Albanian"
    KAT = "Georgian"
    ZHO = "Chinese"
    EUS = "Basque"
    RON = "Romanian"
    SLK = "Slovak"
    ISL = "Icelandic"
    MRI = "Maori"
    CYM = "Welsh"
    MSA = "Malay"
    FAS = "Persian"
    MYA = "Burmese"
    MKD = "Macedonian"
    MEY = "Hassaniyya"
    CMN = "Mandarin Chinese"
    DNJ = "Dan"
    BCN = "Bali (Nigeria)"
    VIF = "Vili"
    NLG = "Gela"
    CAL = "Carolinian"
    UND = "Undetermined"

    @staticmethod
    def get_language(abbreviation: str) -> Language:
        if abbreviation == "":
            return Language.UND
        for lang in Language:
            try:
                if lang.name.lower() == TWO_LETTERS[abbreviation.lower()].lower():
                    return lang
            except KeyError:
                if lang.name.lower() == abbreviation.lower():
                    return lang
                elif lang.value.lower() == abbreviation.lower():
                    return lang
        raise NotImplementedError(f"{abbreviation} language not implemented yet")

    @property
    def two_letters(self):
        for key, value in TWO_LETTERS.items():
            if value == self.name:
                return key
        raise ValueError(f"{repr(self)} does not have a two-letters abbreviation in ISO 639-1")
