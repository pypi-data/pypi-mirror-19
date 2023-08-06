#-*- encoding: utf-8 -*-
import json
import requests

__author__ = 'João Mario'
__mail__ = 'joaok63@outlook.com'
__copyright__ = 'Copyright © 2017 %s'% __author__


_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20170115T074830Z.8a5bd677ee8ea4a5.68827abae5e86da93e6de1131576122d8a5fe3f2&text={text}&lang={frm}-{to}'



def Translate(TEXT,FR0M,T0):
    """

    >>> from translator import Translate
    >>> Translate('Ola Mundo!','pt','en')
    Hello World!

    Languages:

    Macedonian : mk                                                     Albanian   : sq         Maori       : mi
    Amharic    : am         Marathi     : mr
    English    : en         Mari        : mhr
    Arabic     : ar         Mongolian   : mn
    Armenian   : hy         German      : de
    Afrikaans  : af         Nepali      : ne
    Basque     : eu         Norwegian   : no
    Bashkir    : ba         Punjabi     : pa                            Belarusian : be         Papiamento  : pap
    Bengali    : bn         Persian     : fa
    Bulgarian  : bg         Polish      : pl
    Bosnian    : bs         Portuguese  : pt
    Welsh      : cy         Romanian    : ro                            Hungarian  : hu         Russian     : ru
    Vietnamese : vi         Cebuano     : ceb
    Haitian(Creole) : ht    Serbian     : sr
    Galician   : gl         Sinhala     : si
    Dutch      : nl         Slovakian   : sk
    Hill Mari  : mrj        Slovenian   : sl
    Greek      : el         Swahili     : sw
    Georgian   : ka         Sundanese   : su
    Gujarati   : gu         Tajik       : tg
    Danish     : da         Thai        : th
    Hebrew     : he         Tagalog     : tl
    Yiddish    : yi         Tamil       : ta
    Indonesian : id         Tatar       : tt
    Irish      : ga         Telugu      : te
    Italian    : it         Turkish     : tr
    Icelandic  : is         Udmurt      : udm
    Spanish    : es         Uzbek       : uz
    Kazakh     : kk         Ukrainian   : uk
    Kannada    : kn         Urdu        : ur
    Catalan    : ca         Finnish     : fi
    Kyrgyz     : ky         French      : fr
    Chinese    : zh         Hindi       : hi
    Korean     : ko         Croatian    : hr
    Xhosa      : xh         Czech       : cs
    Latin      : la         Swedish     : sv
    Latvian    : lv         Scottish    : gd
    Lithuanian : lt         Estonian    : et
    Malagasy   : mg         Esperanto   : eo
    Malay      : ms         Javanese    : jv
    Malayalam  : ml         Japanese    : ja
    Maltese    : mt
    
    """


    try:
        url = _URL.format(text=TEXT,frm=FR0M,to=T0)
        res = requests.get(url)
        trd = json.loads(res.text)
        if trd['code'] == 200:
            print(trd['text'][0])

        elif trd['code'] == 501:
            print(('%d: %s')% (trd['code'],trd['message']))

        elif trd['code'] == 401:
            print(('%d: %s')% (trd['code'],trd['message']))

    except :
        print('Error')
