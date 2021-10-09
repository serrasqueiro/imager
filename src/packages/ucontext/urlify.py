# urlify.py  (c)2021  Henrique Moreira
#
# class for URL with context

"""
URL with context
"""

# pylint: disable=unused-argument


from waxpage.redit import char_map


class Textual():
    """ Abstract class """
    _msg = ""

    def message(self) -> str:
        """ Returns the message string. """
        return self._msg


class URL(Textual):
    """ URL with context """
    url = ""

    def __init__(self, name:str, substr:str=""):
        self._msg = ""
        post = ""
        if ":" in name:
            self.url = '/'.join([name, substr])
        else:
            self.url = self._from_substr(name, substr, post)

    def is_ok(self) -> bool:
        """ Returns True if URL is ok """
        return self.url != ""

    def to_string(self) -> str:
        """ URL as string """
        return self.url

    def add_suffix(self, substr:str) -> str:
        """ Returns empty if all o.k. """
        suffix = substr if substr.startswith("&") or not substr else ("&" + substr)
        self.url += suffix
        return ""

    def __str__(self):
        """ String-ify """
        return self.to_string()

    def _from_substr(self, name:str, substr:str, post:str) -> str:
        """ Initialize from substring """
        self._msg = ""
        simpler = char_map.simpler_ascii(substr)
        if name in ("youtube",):
            if not substr:
                return ""
            if substr != simpler:
                self._msg = f"substr non-7bit ASCII: '{simpler}'"
                return ""
            pre = f"www.{name}.com/watch?v={substr}{post}"
        else:
            pre = f"{name}/{substr}{post}"
        return pre


# Main script
if __name__ == "__main__":
    print("import ucontext.urlify")
