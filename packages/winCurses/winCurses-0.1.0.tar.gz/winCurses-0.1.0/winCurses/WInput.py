from threading import Thread, Event
from threading import Thread
from .Win import *

class WInput(Win, Thread):
    accents = {
            169 : 'é',
            168 : 'è',
            160 : 'à',
            185 : 'ù',
            170 : 'ê',
            180 : 'ô',
            187 : 'û',
            167 : 'ç',
            137 : 'É',
            136 : 'È',
            128 : 'À',
            153 : 'Ù',
            138 : 'Ê',
            148 : 'Ô',
            155 : 'Û',
            135 : 'Ç',
            }

    ctrl_chars = {
            14 : 'CTRL_P',
            16 : 'CTRL_N',
            }

    def __init__(self, *args, **kwargs):
        """ Creates an Input window, in which text can be entered and keypresses
        will be handled.
        In order to handle events, each Input will have its own process (so it
        have to be started with my_input.start() and can be stopped with 
        my_input.terminate().

        It takes the same arguments as winCurses.Win.__init__, but can also take
        functions to handle events, that will overload existing Input methods
        (all this methods start with "on_"). This functions can be passed as 
        kwarg values, with the method name for key. For instance :
            
            Input(..., on_return=lambda x:print(x))
        """
        Thread.__init__(self, daemon=True)
        
        clean_kwargs = {}

        # Overload on_* methods
        for (k, v) in kwargs.items():
            if k.startswith('on') and k in self.__dir__():
                self.__setattr__(k, v)
            else:
                clean_kwargs[k] = v

        # Fixed height
        if 'dim' in clean_kwargs:
            clean_kwargs['dim'].y = 3
            clean_kwargs['dim'].relative_y = False
        else:
            args[2].y = 3
            args[2].relative_y = False

        Win.__init__(self, *args, **clean_kwargs)
        
        self.window.keypad(True)
        
        self.input_buff = ""

    def run(self):
        """ The main loop executed in this process
        It will be ran when my_input.start() is called
        """
        accent      = False
        escape_mode = False
        typing      = False

        while True:
            ch = self.window.getkey()

            if type(ch) != str:
                raise KeyTypeError(ch, type(ch))

            # Special keys
            if len(ch) > 1:
                if ch == 'KEY_RESIZE':
                    self.root.resize_window()
                self.on_spec_key(ch)
                continue
            # Accents & region-specific chars
            elif ord(ch) == 195:
                accent = True
                continue
            elif accent:
                if ord(ch) in self.accents:
                    self.input_buff += self.accents[ord(ch)]
                accent = False
            # Carriage return
            elif ch == '\n':
                self.on_return(self.input_buff)
                self.input_buff = ""
            # Escape mode
            # Here for historical reasons
            # Maybe one day, it will be usefull (cf VI)
            elif ord(ch) == 27:
                escape_mode = not escape_mode
                continue
            # Erase whole line
            elif ord(ch) == 21:
                self.input_buff = ""
            # Normal aplhabetical char
            elif 32 <= ord(ch) <= 126:
                self.input_buff += ch
            # Backspace
            elif ord(ch) == 127:
                if self.input_buff:
                    self.input_buff = self.input_buff[:-1]
            elif ord(ch) in self.ctrl_chars:
                self.on_spec_key(self.ctrl_chars[ord(ch)])
                continue

            if bool(self.input_buff) != typing:
                typing = bool(self.input_buff)
                self.on_typing(typing)

            self.refresh_input()

    def refresh_input(self):
        """ Refreshes the visual content of the input """
        self.clear()
        self.window.addstr(1, 1, (self.input_buff if len(self.input_buff) <= self.line_length else self.input_buff[-self.line_length:]))
        self.refresh(True)

    def resize_window(self):
        Win.resize_window(self)
        self.refresh_input()

    def set_focus(self):
        """ Gives the focus to this windows
        All the event will be handled in the focused window
        There can be only one
        """
        self.root.focus = self

    def on_spec_key(self, key):
        """ Called when a special key is hit
        Can be overloaded

        key -- special key code
        """
        pass

    def on_return(self, buff):
        """ Called when <RETURN> is hit
        Can be overloaded

        buff -- content of the input buffer when return is pressed
        """
        pass

    def on_typing(self, boolean):
        """ Called when the input buff is written in or emptied

        boolean -- True if someone has started typing, False if the buffer has
                   just been emptied
        """
        pass

class KeyTypeError(Exception):
    def __init__(self, key_name, key_type):
        """ Creates a KeyTypeError exceptions, which describes an unknown or
        unhandled keys

        key_name -- the string/object describing the key
        key_type -- the type (should be str, but who knows...)
        """
        self.key_name = key_name
        self.key_type = key_type

    def __str__(self):
        return("Key %s %s cannot be handled" % (str(self.key_name), str(self.key_type)))
