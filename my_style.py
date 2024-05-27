from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Whitespace

class MyStyle(Style):
    default_style = ""
    styles = {
        Whitespace:         "#bbbbbb",
        Comment:            "italic #888888",
        Keyword:            "bold #0055ff",
        Name:               "#000080",
        Name.Function:      "#00a000",
        Name.Class:         "bold #00a000",
        String:             "#dd2200",
        Number:             "#ff0000",
        Operator:           "#0000ff",
        Generic.Heading:    "bold #000080",
        Generic.Subheading: "bold #800080",
        Generic.Deleted:    "border:#CC0000",
        Generic.Inserted:   "border:#00CC00",
        Generic.Error:      "#FF0000",
        Generic.Emph:       "italic",
        Generic.Strong:     "bold",
        Generic.Prompt:     "bold #000080",
        Generic.Output:     "#888888",
        Generic.Traceback:  "#04D"
    }


