from jinja2 import Markup

class momentjs(object):
    def __init__(self, datetime):
        self.datetime = datetime

    def render(self, output_format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.datetime, output_format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)