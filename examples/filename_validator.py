import re

class filename_validator:
    """ class to validate portable filenames """

    def __init__(self):
        """ 
            build compiled regexps, description message based on 
            ranges list and special characters accepted
        """
        self.special = '-._'
        self.ranges = [ 'a-z', 'A-Z', '0-9' ]
        joined= ''.join(self.ranges)
        self.check_re = re.compile(f"^[{self.special}{joined}]*$")
        self.fix_re = re.compile(f"[^{self.special}{joined}]")
        self.message = f"Filenames must consist of\n * characters in ranges {self.ranges}\n * special characters in {repr(self.special)}"

    def check(self, fname):
        """ check a filename for portability using check_re """
        m = self.check_re.match(fname)
        return m is not None

    def fix(self, fname):
        """ replace 'bad' characters with underscores using fix_re """
        return self.fix_re.sub("_", fname)

   
if __name__ == '__main__':
    """ demo code using above class """

    fv = filename_validator()

    print("message:\n" , fv.message)
    for fname in [ 'foo99.txt', 'Apple cider recipe', 'file_12:26:1998' ]:
        print( fname, fv.check(fname), fv.fix(fname))
