import typing
import hashlib
from array import array
from itertools import repeat
import math
import bit_arithmetic




class HyperLogLog(object):

    def __init__(self, b: int):

        alphas = {16: 0.673, 32: 0.697, 64: 0.709}

        assert(b in range(4, 16))
        self.b = b
        self.num_registers = pow(2,self.b)
        self.alpha = None
        self.registers = array('i', repeat(0, self.num_registers))
        self._mask = (self.num_registers - 1)


        if self.num_registers in alphas:
            self.alpha = alphas[self.num_registers]
        else:
            self.alpha = 0.7213/(1 + 1.079/self.num_registers)

    def _register(self, i: int)-> int:
        return self._mask & i

    def _run_length(self, i : int) -> int:
        shifted = i >> self.b
        return bit_arithmetic.number_trailing_zeros(shifted)

    def _insert(self, i):
        register = self._register(i)
        run_length = self._run_length(i)
        self.registers[register] = max(self.registers[register], run_length)

    def _count_of_zero_registers(self)-> int:
        zero_count = 0
        for register in self.registers:
            if register == 0:
                zero_count += 1
        return zero_count

    def witness(self,i):
            self._insert(i)

    def estimate(self):

        registers_sum = sum([pow(2, -register) for register in self.registers])

        estimated = self.alpha * pow(self.num_registers, 2) * (1/registers_sum)

        conclusion = None
        if estimated < 5/2 * self.num_registers:
            num_zero_registers = self._count_of_zero_registers()
            if num_zero_registers == 0:  #
                return round(estimated)
            else:
                return round( self.num_registers * math.log(self.num_registers/num_zero_registers))

        if estimated <= ((1/30) * pow(2, 32)):
            return round(estimated)
        if estimated > ((1/30) * pow(2, 32)):
            return round(-pow(2, 32) * math.log( 1 - estimated/pow(2, 32)))