from manuscript.elements.definition import Definition

from manuscript.tools.castings import language, list_, bool_
import manuscript.tools.constants as mc


class Settings(Definition):

    COMMAND = mc.SETTINGS
    params = [
        {"name": (str, mc.SETTINGS)},
        {"default_lang": (language, mc.DEFAULT_LANG),
         "data_dirs":
             (lambda x: list_(". data "+x, tail=None),
              ""),  # Notice: add, not replace
         "temp_dir": (str, "."),
         # TODO: text export
         # text
         "page_width": (int, mc.PAGE_WIDTH),
         "page_length": (int, mc.PAGE_LENGTH),
         "text_export": (str, "output.txt"),
         # mp3 export
         "export": (str, "output.mp3"),
         "format": (str, "mp3"),
         "title": (str, ""),
         "artist": (str, "Various Artists"),
         "album": (str, ""),
         "comments": (str, ""),
         "date": (str, ""),
         "genre": (str, ""),
         "cover": (str, ""),
         # play results in the end
         "play_final": (bool_, True),
         # show results
         "print_final_text": (bool_, False),
         # debug settings
         "play_while": (bool_, False),
         "print_supported_languages": (bool_, False),
         "print_defining_actions": (bool_, False),
         "print_defined_actions": (bool_, False),
         "print_manuscript_text": (bool_, False),
         "print_manuscript_parsed": (bool_, False),
         "print_executions": (bool_, False)},
        {}
    ]

    def __init__(self, work, *args, **kwargs):
        # Name of settings is forced to mc.SETTINGS
        # TODO: it could be used to group settings
        kwargs["name"] = mc.SETTINGS
        super().__init__(work, *args, **kwargs)
