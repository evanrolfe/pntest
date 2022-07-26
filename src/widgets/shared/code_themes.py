from PyQt6 import QtCore, QtWidgets, Qsci, QtGui

# These values are just used for testing, you can delete them:
VALUE_JSON = """{
    "asdf": "123",
    "array": [
        {
            "hello": "world",
            "age": 123
        }
    ]
}"""

VALUE = """<!DOCTYPE html>
<html lang="en-US">
 <head>
  <!-- Global site tag (gtag.js) - Google Analytics -->
  <script async="" src="https://www.googletagmanager.com/gtag/js?id=UA-38714717-1">
  </script>
  <script>
   window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-38714717-1');
  </script>
  <!-- Google Optimize -->
  <script src="https://www.googleoptimize.com/optimize.js?id=OPT-56H9SXM">
  </script>
  <!-- Google Tag Manager -->
  <script>
   (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-W82WNBG');
  </script>
  <!-- End Google Tag Manager -->
  <!-- META DATA -->
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <!--[if IE]><meta http-equiv="cleartype" content="on" /><![endif]-->
  <!--[if IE]><meta http-equiv="X-UA-Compatible" content="IE=edge" /><![endif]-->
  <link href="http://gmpg.org/xfn/11" rel="profile"/>
  <link href="https://www.synack.com/xmlrpc.php" rel="pingback"/>"""

VALUE_JS = """(function() {
    var didInit = false;
    function initMunchkin() {
        if(didInit === false) {
            didInit = true;
            Munchkin.init('738-OEX-476');
        }
    }
    var s = document.createElement('script');
    s.type = 'text/javascript';
    s.async = true;
    s.src = '//munchkin.marketo.net/munchkin.js';
    s.onreadystatechange = function() {
        if (this.readyState == 'complete' || this.readyState == 'loaded') {
            initMunchkin();
        }
    };
    s.onload = initMunchkin;
    document.getElementsByTagName('head')[0].appendChild(s);
})();"""

class DarkTheme:
    default_bg = "#1E1E1E"
    default_color = "#EEFFFF"
    darker_color = "#545454"
    key_color = "#C792EA"
    value_color = "#C3E88D"
    number_color = "#FF5370"
    operator_color = "#569CD6"
    invalid_color = "#f14721"
    selected_secondary_color = "#4E5256"
    other_color = "#FFCB6B"

    bg_dark = "#252526"
    bg_input = "#404040"
    bg_input_hover = "#3A3A3A"

    @classmethod
    def new_html_lexer(cls):
        lexer = Qsci.QsciLexerHTML()

        lexer.setDefaultPaper(QtGui.QColor(cls.default_bg))
        lexer.setDefaultColor(QtGui.QColor(cls.default_color))

        tags = [
            Qsci.QsciLexerHTML.SGMLDefault,
            Qsci.QsciLexerHTML.SGMLCommand,
            Qsci.QsciLexerHTML.SGMLParameter,
            Qsci.QsciLexerHTML.SGMLDoubleQuotedString,
            Qsci.QsciLexerHTML.SGMLSingleQuotedString,
            Qsci.QsciLexerHTML.SGMLError,
            Qsci.QsciLexerHTML.SGMLSpecial,
            Qsci.QsciLexerHTML.SGMLEntity,
            Qsci.QsciLexerHTML.SGMLComment,
            Qsci.QsciLexerHTML.SGMLParameterComment,
            Qsci.QsciLexerHTML.SGMLBlockDefault,
        ]
        for tag in tags:
            lexer.setColor(QtGui.QColor(cls.other_color), tag)
            lexer.setPaper(QtGui.QColor(cls.default_bg), tag)

        lexer.setColor(QtGui.QColor(cls.number_color), Qsci.QsciLexerHTML.Tag)
        lexer.setColor(QtGui.QColor(cls.number_color), Qsci.QsciLexerHTML.UnknownTag)
        lexer.setColor(QtGui.QColor(cls.key_color), Qsci.QsciLexerHTML.Attribute)
        lexer.setColor(QtGui.QColor(cls.key_color), Qsci.QsciLexerHTML.UnknownAttribute)

        lexer.setColor(QtGui.QColor(cls.operator_color), Qsci.QsciLexerHTML.XMLStart)
        lexer.setColor(QtGui.QColor(cls.operator_color), Qsci.QsciLexerHTML.XMLEnd)

        lexer.setColor(QtGui.QColor(cls.value_color), Qsci.QsciLexerHTML.OtherInTag)
        lexer.setColor(QtGui.QColor(cls.value_color), Qsci.QsciLexerHTML.HTMLNumber)
        lexer.setColor(QtGui.QColor(cls.value_color), Qsci.QsciLexerHTML.HTMLDoubleQuotedString)
        lexer.setColor(QtGui.QColor(cls.value_color), Qsci.QsciLexerHTML.HTMLSingleQuotedString)

        lexer.setPaper(QtGui.QColor(cls.default_bg), Qsci.QsciLexerHTML.JavaScriptDefault)
        lexer.setColor(QtGui.QColor(cls.default_color), Qsci.QsciLexerHTML.JavaScriptDefault)
        lexer.setPaper(QtGui.QColor(cls.default_bg), Qsci.QsciLexerHTML.Script)
        lexer.setColor(QtGui.QColor(cls.default_color), Qsci.QsciLexerHTML.Script)

        lexer.setColor(QtGui.QColor(cls.darker_color), Qsci.QsciLexerHTML.HTMLComment)
        lexer.setColor(QtGui.QColor(cls.default_color), Qsci.QsciLexerHTML.Default)
        lexer.setPaper(QtGui.QColor(cls.default_bg), Qsci.QsciLexerHTML.Default)

        # Javascript colours
        colours = {
            Qsci.QsciLexerHTML.JavaScriptDefault: cls.default_color,
            Qsci.QsciLexerHTML.JavaScriptSymbol: cls.default_color,
            Qsci.QsciLexerHTML.JavaScriptKeyword: cls.operator_color,

            Qsci.QsciLexerHTML.JavaScriptWord: cls.key_color,
            Qsci.QsciLexerHTML.JavaScriptKeyword: cls.key_color,

            Qsci.QsciLexerHTML.JavaScriptDoubleQuotedString: cls.value_color,
            Qsci.QsciLexerHTML.JavaScriptSingleQuotedString: cls.value_color,
        }
        for key, colour in colours.items():
            lexer.setColor(QtGui.QColor(colour), key)
            lexer.setPaper(QtGui.QColor(cls.default_bg), key)

        lexer.setFont(cls.get_font())
        return lexer

    @classmethod
    def new_json_lexer(cls):
        lexer = Qsci.QsciLexerJSON()

        lexer.setHighlightEscapeSequences(False)

        lexer.setDefaultPaper(QtGui.QColor(cls.default_bg))
        lexer.setDefaultColor(QtGui.QColor(cls.default_color))

        lexer.setPaper(QtGui.QColor(cls.default_bg), Qsci.QsciLexerJSON.Error)
        lexer.setColor(QtGui.QColor(cls.invalid_color), Qsci.QsciLexerJSON.Error)
        lexer.setPaper(QtGui.QColor(cls.default_bg), Qsci.QsciLexerJSON.UnclosedString)
        lexer.setColor(QtGui.QColor(cls.invalid_color), Qsci.QsciLexerJSON.UnclosedString)

        lexer.setColor(QtGui.QColor(cls.key_color), Qsci.QsciLexerJSON.Property)
        lexer.setColor(QtGui.QColor(cls.value_color), Qsci.QsciLexerJSON.String)
        lexer.setColor(QtGui.QColor(cls.number_color), Qsci.QsciLexerJSON.Number)
        lexer.setColor(QtGui.QColor(cls.default_color), Qsci.QsciLexerJSON.Operator)

        lexer.setFont(cls.get_font())
        return lexer

    @classmethod
    def new_js_lexer(cls):
        lexer = Qsci.QsciLexerJavaScript()

        lexer.setHighlightEscapeSequences(False)

        lexer.setDefaultPaper(QtGui.QColor(cls.default_bg))
        lexer.setDefaultColor(QtGui.QColor(cls.default_color))

        colours = {
            Qsci.QsciLexerCPP.Default: cls.default_color,
            Qsci.QsciLexerCPP.Operator: cls.default_color,
            Qsci.QsciLexerCPP.InactiveOperator: cls.operator_color,
            Qsci.QsciLexerCPP.Identifier: cls.operator_color,

            Qsci.QsciLexerCPP.Keyword: cls.key_color,

            Qsci.QsciLexerCPP.DoubleQuotedString: cls.value_color,
            Qsci.QsciLexerCPP.SingleQuotedString: cls.value_color,
            Qsci.QsciLexerCPP.InactiveDoubleQuotedString: cls.value_color,
            Qsci.QsciLexerCPP.InactiveSingleQuotedString: cls.value_color,
        }
        for key, colour in colours.items():
            lexer.setColor(QtGui.QColor(colour), key)

        lexer.setFont(cls.get_font())
        return lexer

    @classmethod
    def get_font(cls) -> QtGui.QFont:
        # fonts = QtGui.QFontDatabase.families()
        # TODO: Search through the fonts and find one that matches
        font = QtGui.QFontDatabase.font('Menlo', 'Regular', 13)
        return font
