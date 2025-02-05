#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append(".") # noqa
# sys.path.insert(0,'/Users/nikhilvaidyamath/Desktop/
# devops1/Emu86/assembler/Intel/fp_arithmetic.py')

import operator as opfunc
import functools


from unittest import TestCase, main

from assembler.tokens import MAX_INT, MIN_INT, BITS
from assembler.virtual_machine import intel_machine, STACK_TOP, STACK_BOTTOM
from assembler.assemble import assemble
from assembler.Intel.fp_arithmetic import convert_hex_to_decimal
from assembler.Intel.fp_arithmetic import convert_dec_to_hex
# from assembler.Intel.math_operations import Mathops

NUM_TESTS = 100
MAX_SHIFT = BITS // 2
MIN_TEST = MIN_INT // 10   # right now we don't want to overflow!
MAX_TEST = MAX_INT // 10   # right now we don't want to overflow!
MAX_MUL = 10000  # right now we don't want to overflow!
MIN_MUL = -10000  # right now we don't want to overflow!
REGISTER_SIZE = BITS

INT = 0
FLOAT = 1

intel_machine.base = "dec"
intel_machine.flavor = "intel"


class AssembleTestCase(TestCase):

    #####################
    # Two Operand Tests #
    #####################

    def two_op_test(self, operator, instr, low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST, op_type=INT,
                    first_val=INT, second_val=INT):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            if op_type == FLOAT:
                if first_val == FLOAT:
                    a = float(random.uniform(MIN_MUL, MAX_MUL))
                if second_val == FLOAT:
                    b = float(random.uniform(MIN_MUL, MAX_MUL))
                correct = operator(a, b)
                intel_machine.registers["ST0"] = a
                intel_machine.registers["ST1"] = b
                assemble(instr + " st0, st1", intel_machine)
                self.assertAlmostEqual(intel_machine.registers["ST0"], correct)
            else:
                correct = operator(a, b)
                intel_machine.registers["EAX"] = a
                intel_machine.registers["EBX"] = b
                assemble(instr + " eax, ebx", intel_machine)

                self.assertEqual(intel_machine.registers["EAX"], correct)

    def test_convert_hex_to_decimal(self):
        self.assertEqual(convert_hex_to_decimal('a2.4c'), 162.296875)

    def test_convert_dec_to_hex(self):
        self.assertEqual(convert_dec_to_hex(162.296875), 'a2.4c')

    def test_fadd(self):
        self.two_op_test(opfunc.add, "FADD", op_type=FLOAT,
                         first_val=FLOAT, second_val=FLOAT)

    def test_fsub(self):
        self.two_op_test(opfunc.sub, "FSUB", op_type=FLOAT,
                         first_val=FLOAT, second_val=FLOAT)

    def test_fmul(self):
        self.two_op_test(opfunc.mul, "FMUL", op_type=FLOAT,
                         first_val=FLOAT, second_val=FLOAT)

    def test_fdiv(self):
        self.two_op_test(opfunc.truediv, "FDIV", op_type=FLOAT,
                         first_val=FLOAT, second_val=FLOAT)

    def test_add(self):
        self.two_op_test(opfunc.add, "add")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "sub")

    def test_imul(self):
        self.two_op_test(opfunc.mul, "imul",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=MIN_MUL, high2=MAX_MUL)

    def test_and(self):
        self.two_op_test(opfunc.and_, "and")

    def test_or(self):
        self.two_op_test(opfunc.or_, "or")

    def test_xor(self):
        self.two_op_test(opfunc.xor, "xor")

    def test_shl(self):
        self.two_op_test(opfunc.lshift, "shl",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_shr(self):
        self.two_op_test(opfunc.rshift, "shr",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    ###################
    # Single Op Tests #
    ###################

    def one_op_test(self, operator, instr, op_type=None, replaces=True):
        """replace boolean needed because some fp instructions
        do not replace the contents of the register,
        but rather place it another register"""
        for i in range(NUM_TESTS):  # changeback to num_tests
            if op_type == FLOAT:
                a = float(random.uniform(MIN_MUL, MAX_MUL))
                intel_machine.registers["FRB"] = a  # source float register
                correct = operator(a)
                """
                if replaces == False:
                     intel_machine.registers["FRT"] = None
                     #since no replacement, destination float register
                     assemble(instr + ' frb', 'intel', intel_machine)
                     self.assertEqual(intel_machine.registers["FRT"], correct)
                     #since the new value is in the destination register,
                     #compare correct to FRT
                else:"""
                # needs to be corrected to not use frb
                # assemble(instr + ' frb', intel_machine)
                # self.assertEqual(intel_machine.registers["FRB"], correct)
                # since the new value has not been replaced
                # (in source register), compare FRB to correct

            else:
                a = random.randint(MIN_TEST, MAX_TEST)
                intel_machine.registers["EAX"] = a
                correct = operator(a)
                assemble(instr + " eax", intel_machine)
                self.assertEqual(intel_machine.registers["EAX"], correct)

    def test_not(self):
        self.one_op_test(opfunc.inv, "not")

    def test_neg(self):
        self.one_op_test(opfunc.neg, "neg")

    def test_inc(self):
        inc = functools.partial(opfunc.add, 1)
        self.one_op_test(inc, "inc")

    def test_dec(self):
        dec = functools.partial(opfunc.add, -1)
        self.one_op_test(dec, "dec")
    """
    # def test_fabs(self):
    #     self.one_op_test(opfunc.abs, "FABS",FLOAT,False)
    # def test_chs(self):
    #     self.one_op_test(Mathops.change_sign, "FCHS",FLOAT)
    """
    ##################
    # Push / Pop     #
    ##################

    def test_push_and_pop(self):
        # Note: size(correct_stack) = size(stack + memory)

        correct_stack = [None] * (STACK_TOP+1)

        # Traverse the stack registers.
        for i in range(STACK_TOP, STACK_BOTTOM-1, -1):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct_stack[i] = a
            intel_machine.registers["EAX"] = a
            assemble("push eax", intel_machine)

        for i in range(STACK_BOTTOM, STACK_TOP+1):
            assemble("pop ebx", intel_machine)
            self.assertEqual(intel_machine.registers["EBX"], correct_stack[i])

    ##################
    # Other          #
    ##################

    def test_mov(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct = a
            intel_machine.registers["EAX"] = a
            assemble("mov eax, " + str(a), intel_machine)
            self.assertEqual(intel_machine.registers["EAX"], correct)

    def test_idiv(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            d = random.randint(MIN_TEST, MAX_TEST)
            b = 0
            while(b == 0):    # Divisor can't be zero.
                b = random.randint(MIN_TEST, MAX_TEST)
            correct_quotient = (opfunc.lshift(d, REGISTER_SIZE) + a) // b
            correct_remainder = (opfunc.lshift(d, REGISTER_SIZE) + a) % b
            intel_machine.registers["EAX"] = a
            intel_machine.registers["EDX"] = d
            intel_machine.registers["EBX"] = b
            assemble("idiv ebx", intel_machine)
            self.assertEqual(intel_machine.registers["EAX"],
                             correct_quotient)
            self.assertEqual(intel_machine.registers["EDX"],
                             correct_remainder)

    def test_cmp_eq(self):
        intel_machine.registers["EAX"] = 1
        intel_machine.registers["EBX"] = 1
        intel_machine.flags["ZF"] = 0
        intel_machine.flags["SF"] = 0
        assemble("cmp eax, ebx", intel_machine)
        self.assertEqual(intel_machine.flags["ZF"], 1)
        self.assertEqual(intel_machine.flags["SF"], 0)

    def test_cmp_l(self):
        intel_machine.registers["EAX"] = 0
        intel_machine.registers["EBX"] = 1
        intel_machine.flags["ZF"] = 0
        intel_machine.flags["SF"] = 0
        assemble("cmp eax, ebx", intel_machine)
        self.assertEqual(intel_machine.flags["ZF"], 0)
        self.assertEqual(intel_machine.flags["SF"], 1)


if __name__ == '__main__':
    main()
