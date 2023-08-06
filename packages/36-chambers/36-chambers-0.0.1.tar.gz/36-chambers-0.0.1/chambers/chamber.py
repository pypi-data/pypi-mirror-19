#!/usr/bin/env python

class Chamber(object):
    """
    The main chamber.
    """

    bv = None

    def __init__(self, bv=None):
        """
        Do a crude check to see if `bv` is not some standard object. If it is,
        note that it should be a `BinaryView` object.

        If it's something we don't check for, or a true BinaryView object, set
        the class attribute for use in methods. If a developer decides to pass
        something that isn't checked by us and isn't a BinaryView object, they
        can deal with the exceptions being thrown to figure it out.
        """

        if bv is None or isinstance(bv, (basestring,
                                         dict,
                                         float,
                                         int,
                                         list,
                                         long,
                                         str,
                                         )):
            raise Exception(
                "Must provide a valid Binary Ninja BinaryView object")
        self.bv = bv

    def instructions(self, instruction=None):
        """
        Loop through all of the functions, then all of the blocks in the IL, and
        for each one check to see if it contains the provided instruction. If it
        does, print it and its instructions.

        TODO: Figure out why Binja doesn't show some instructions, like `xor`.

        :param instruction: The instruction to search for.
        :type instruction: str
        """
        for func in self.bv.functions:
            for block in func.low_level_il:
                f = False
                for i in block:
                    if instruction in str(i):
                        f = True
                        break
                if f:
                    print("\t{0}".format(block))
                    for insn in block:
                        print("\t\t{0}".format(insn))
