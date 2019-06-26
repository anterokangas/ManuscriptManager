from tqdm import tqdm
# import copy
#
from manuscript.elements.definition import Definition
from manuscript.elements.settings import Settings
from manuscript.elements.role import Role
from manuscript.elements.wait import Wait

from manuscript.mmlanguage.lexer import ManuscriptLexer
from manuscript.mmlanguage.parser import ManuscriptParser
#
# from manuscript.messages.messages import message_text
#
import manuscript.tools.audio_tools as audio_tools
import manuscript.tools.constants as mc
import manuscript.tools.format as fmt
# import manuscript.tools.play as play

from manuscript.tools.subclasses import get_all_subclasses


class Work:
    """
    Work - class as a namespace.


    Class attributes
    ----------------
    defining_actions :  dictionary of form {NAME: NameClass, ...}
        Collection of classes that define Actions

    defined_action :    dictionary of form {NAME: object.do(), ...}
        Collection of defined action objects

    manuscript :        list of

    Class methods
    -------------
    """

    def __init__(self, manuscript_as_mm):
        """ Initialize and make a new work

        (1) Define defining actions
        (2) Initialize default defined actions
        (3) Create lexer and parser
        (4) Make lexical analysis and parse manuscript
        (5) create audio
        """
        # print(f"Create Work()={self}")
        # The defining actions are subclassess of Definition having class attribute COMMAND
        self.defining_actions = {}
        for subclass in get_all_subclasses(Definition):
            if 'COMMAND' in subclass.__dict__.keys():
                self.defining_actions[subclass.COMMAND] = subclass

        # Set of names whose re-definition is allowed
        self.re_definition_allowed = {mc.SETTINGS}

        # Initialize default defined actions
        self.defined_actions = {}

        self.manuscript_as_mm = manuscript_as_mm
        self.settings = Settings(self, name=mc.SETTINGS)
        self.narrator = Role(self, name=mc.NARRATOR)
        print(f"work=self .narrator.name={self.narrator.name}")
        self.break_ = Wait(self, name=mc.BREAK)  # (saving break makes testing easier)
        book = fmt.Book()
        self.defaults = {
            "lang": self.narrator.lang,
            "pitch": self.narrator.pitch,
            "speed": self.narrator.speed,
            "gain": self.narrator.gain
        }
        self.paragraphs = [
            Role(self, name="title", **fmt.merge(book.par_title, self.defaults)),
            Role(self, name="title_line", **fmt.merge(book.par_title_line, self.defaults)),
            Role(self, name="synopsis", **fmt.merge(book.par_synopsis, self.defaults)),
            Role(self, name="header", **fmt.merge(book.par_header, self.defaults)),
            Role(self, name="parenthesis", **fmt.merge(book.par_parenthesis, self.defaults)),
            Role(self, name="name", **fmt.merge(book.par_name, self.defaults)),
            Role(self, name="reply", **fmt.merge(book.par_reply, self.defaults)),
        ]


        # TODO: update pargaraph-Roles' lang-like when Settings is updated
        # Make lexer and parser
        lexer = ManuscriptLexer()
        parser = ManuscriptParser(work=self)
        # Make lexical analysisis and parse manuscript

        self.parsed_manuscript = parser.parse(lexer.tokenize(manuscript_as_mm))
        # print(f"\n++++work.settings:")
        # for key, val in self.settings.__dict__.items():
        #     print(f"++{key}: {val}")
        # print("\n")
        print(f"{'Parse manuscript'}: self.settings.print_defining_actions={self.settings.print_defining_actions}")
        if self.settings.print_defining_actions:
            print("\nwork: defining actions")
            for key, value in self.defining_actions.items():
                print(f"   {key:15}: {value}")

        if self.settings.print_manuscript_parsed:
            print("\nwork: parsed_manuscript")
            for act in self.parsed_manuscript:
                print(f"   {act}")

        if self.settings.print_defined_actions:
            print("\nwork: defined actions")
            for key, value in self.defined_actions.items():
                if isinstance(value, Sound):
                    audio_length = len(value.audio) if value.audio is not None else 0
                    input_ = value.input
                else:
                    audio_length = ""
                    input_ = ""

                print(f"   {key:15}: {value} {audio_length} {input_}")

        # Make audio
        print(f"{'Process manuscript'}")
        self.audio = self._process_structured_manuscript()
        if self.audio is None:
            length = "None"
        else:
            length = len(self.audio)
        print(f"==>audio: length={length}")

    # @staticmethod
    # def set_Work_attributes(cls, **kwargs):
    #     for key, value in kwargs.items():
    #         Work.set_attributes(key, value)
    #

    def define_action(self, action_name, object_):
        """ Add new defined action """
        # print(f"***define_action {action_name}")
        self.defined_actions[action_name] = object_
        if action_name == mc.SETTINGS:
            self.settings = object_
            # try:
            #     print(f"object_:")
            #     for key, val in object_.__dict__.items():
            #         print(f"{key}: {val}")
            #     print(f"settings updated -->{self.settings.print_defining_actions}")
            # except AttributeError:
            #     pass

    @property
    def settings(self):
        try:
            return self._settings
        except AttributeError:
            return None

    @settings.setter
    def settings(self, the_settings):
        self._settings = the_settings

        # if narrator has been defined, fix its language
        try:
            self.narrator.lang = self.settings.default_lang
        except AttributeError:
            pass

    #
    # def export_audio(self):
    #     if self.audio is None:
    #         print(f"Empty audio")
    #         return
    #     self.audio_tools.export(self.settings.export)
    #
    def _process_structured_manuscript(self):
        """ Process structured manuscript and create audio """
        the_audio = None

        # Execute defined actions
        i = 0
        for command, action, params in tqdm(self.parsed_manuscript):
            print(f"_p_c_s: command={command} action={action.name} params={params}")
            # If asked print current action
            if self.settings.print_executions:
                print(f"\n{i}: {command}, {action}, {params}")
            i += 1
            if command in self.defining_actions:
                continue

            if command not in self.defined_actions:
                continue

            if action is None:
                action = self.defined_actions[command]
            sound = action.do(**params)
            if params.get(mc.SOUND, "") == "":
                the_audio = audio_tools.append(the_audio, sound)
        return the_audio

    def definition_allowed(self, name):
        """  Decides can 'name' be defined or re-defined  """
        return (name != ""
                    and name not in self.defining_actions.keys()
                    and name not in self.defined_actions.keys()
                or name in self.re_definition_allowed)

    # def play(self):
    #     print(f"work play {self.audio} {len(self.audio)}")
    #     play.play_sound(self.audio)
    #
    # def to_formatted_text(self):
    #     # TODO: Create readable formatted manuscript
    #     pass
