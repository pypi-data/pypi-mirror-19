from IPython.core.magic import Magics, magics_class, line_cell_magic
import yapf
import codecs

@magics_class
class Pep8Magics(Magics):

    @line_cell_magic
    def pep8(self, line, cell=None):
        """
        pep8 IPython magic extension, cf. https://pypi.python.org/pypi/pep8

        Magic methods:
            %%pep8 
            < python code ... >
    
            %pep8 filename
        """
        source = cell if cell else codecs.open(line, "r", "utf8").read()
        result = yapf.yapf_api.FormatCode(source, style_config='pep8')[0]
        get_ipython().set_next_input(result.rstrip(), replace = True)