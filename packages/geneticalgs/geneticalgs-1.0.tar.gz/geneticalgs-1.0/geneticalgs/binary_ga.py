# Copyright 2017 Dmitriy Bobir <bobirdima@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import random

from .standard_ga import StandardGA, IndividualGA


class BinaryGA(StandardGA):
    """
    This class realizes GA over a binary encoded input data. In other words,
    the algorithm tries to find a combination of the input data with the best fitness value.

    You may initialize instance of this class the following way

    .. testcode::

       from geneticalgs import BinaryGA

       # define data whose best combination we are searching for
       input_data = [1,2,3,7,-1,-20]

       # define a simple fitness function
       def fitness_function(chromosome, data):
           # this function searches for the greatest sum of numbers in data
           # chromosome contains positions (from left 0 to right *len(data)-1) of bits 1
           sum = 0
           for bit in chromosome:
               sum += data[bit]

           return sum

       # initialize standard binary GA
       gen_alg = BinaryGA(input_data, fitness_function)
       # initialize random population of size 6
       gen_alg.init_random_population(6)

    Then you may start computation by *gen_alg.run(number_of_generations)* and obtain
    the currently best found solution by *gen_alg.best_solution*.
    """
    def __init__(self, data=None, fitness_func=None, optim='max', selection="rank", mut_prob=0.05, mut_type=1,
                 cross_prob=0.95, cross_type=1, elitism=True, tournament_size=None):
        """
        Args:
            data (list): A list with elements whose combination will be binary encoded and
                evaluated by a fitness function. Minimum amount of elements is 4.
            fitness_func (function): This function must compute fitness value of a single binary encoded chromosome.
                Function template is the following: *compute_fitness(chromosome, data) -> float*. Parameter *chromosome*
                is binary encoded the following way: it contains only positions of bit 1 according to *self.data*.
                Positions are indexed from left to right so the leftmost position is 0. Parameter *data* is
                the input *data* parameter from this constructor. The returned value of the fitness function
                must be a single number.
            optim (str): What this genetic algorithm must do with fitness value: maximize or minimize.
                May be 'min' or 'max'. Default is "max".
            selection (str): Parent selection type. May be "rank" (Rank Wheel Selection),
                "roulette" (Roulette Wheel Selection) or "tournament". Default is "rank".
            tournament_size (int): Defines the size of tournament in case of 'selection' == 'tournament'.
                Default is None.
            mut_prob (float): Probability of mutation. Recommended values are 0.5-1%. Default is 0.5% (0.05).
            mut_type (int): This parameter defines how many chromosome bits will be mutated.
                May be 1 (single-point), 2 (two-point), 3 or more (multiple point). Default is 1.
            cross_prob (float): Probability of crossover. Recommended values are 80-95%. Default is 95% (0.95).
            cross_type (int): This parameter defines crossover type. The following types are allowed:
                single point (1), two point (2) and multiple point (2 < cross_type).
                The extreme case of multiple point crossover is uniform one (cross_type == all_bits).
                The specified number of bits (cross_type) are crossed in case of multiple point crossover.
                Default is 1.
            elitism (True, False): Elitism on/off. Default is True.
        """
        super().__init__(fitness_func, optim, selection,
                         mut_prob, mut_type, cross_prob, cross_type,
                         elitism, tournament_size)
        if data is not None:
            self._data = list(data)
            self._bin_length = len(self._data)
        else:
            self._data = None

        self._check_parameters()

    def _check_parameters(self):
        if self._data is None or self._bin_length < 4 or \
                self.mut_type > self._bin_length or \
                self.cross_type > self._bin_length:
            raise ValueError('Wrong value of input parameter.')

    def _invert_bit(self, chromosome, bit_num):
        """
        This method mutates the appropriate bits of the given chromosome from *bit_num*
        with the specified mutation probability.

        Args:
            chromosome (list): Binary encoded chromosome (it contains positions of bit 1 according to *self.data*).
            bit_num (list): List of bits' numbers to invert.

        Returns:
            mutant (list): mutated chromosome as binary representation of *self.data* (it contains positions
            of bit 1)
        """
        for bit in bit_num:
            if random.uniform(0, 1) <= self.mutation_prob:
                # mutate
                if bit in chromosome:
                    # 1 -> 0
                    chromosome.remove(bit)
                else:
                    # 0 -> 1
                    chromosome.append(bit)

        return chromosome

    def _replace_bits(self, source, target, start, stop):
        """
        Replaces target bits with source bits in interval (start, stop) (both included)
        with the specified crossover probability and returns target. This interval represents
        positions of bits to replace (minimum start point is 0 and maximum end point is *self._bin_length - 1*).

        Args:
            source (list): Values in source are used as replacement for target.
            target (list): Values in target are replaced with values in source.
            start (int): Start point of interval (included).
            stop (int): End point of interval (included).

        Returns:
             target with replaced bits in the interval (start, stop) (both included)
        """
        if start < 0 or start >= self._bin_length or \
                stop < 0 or stop < start or stop >= self._bin_length:
            print('Interval error:', '(' + str(start) + ', ' + str(stop) + ')')
            raise ValueError('Replacement interval error')

        if start == stop:
            if random.uniform(0, 1) <= self.crossover_prob:
                # crossover
                if start in source:
                    # bit 'start' is 1 in source
                    if start not in target:
                        # bit 'start' is 0 in target
                        target.append(start)
                else:
                    # bit 'start' is 0 in source
                    if start in target:
                        # bit 'start' is 1 in target
                        target.remove(start)
        else:
            tmp_target = [0] * self._bin_length
            tmp_source = [0] * self._bin_length
            for index in target:
                tmp_target[index] = 1
            for index in source:
                tmp_source[index] = 1

            if random.uniform(0, 1) <= self.crossover_prob:
                # crossover
                tmp_target[start: stop+1] = tmp_source[start: stop+1]

            target = []
            for i in range(self._bin_length):
                if tmp_target[i] == 1:
                    target.append(i)

        return target

    def _compute_fitness(self, chromosome):
        """
        This method computes fitness value of the given chromosome.

        Args:
            chromosome (list): A binary encoded chromosome of genetic algorithm.
                Defined fitness function (*self.fitness_func*) must deal with this chromosome representation.

        Returns:
            fitness value of the given chromosome
        """
        return self.fitness_func(chromosome, self._data)

    def _get_bit_positions(self, number):
        """
        This method receives a positive decimal integer number and returns positions of bit 1 in
        its binary representation. However, these positions are transformed the following way: they
        are mapped on the data list (*self.data*) "as is". It means that LSB (least significant bit) is
        mapped on the last position of the data list (e.g. *self._bin_length* - 1), MSB is mapped on
        the first position of the data list (e.g. 0) and so on.

        Args:
            number (int): This decimal number represents binary encoded combination of the input data (*self.data*).

        Returns:
             list of positions with bit 1 (these positions are mapped on the input data list "as is" and thus,
             LSB is equal to index (*self._bin_length* - 1) of the input data list).
        """
        if number < 0:
            raise ValueError('The input number must be positive (0+)!')

        binary_list = []

        for i in range(self._bin_length):
            if number & (1 << i):
                binary_list.append(self._bin_length - 1 - i)

        return binary_list

    def _check_init_random_population(self, size):
        """
        This method verifies the input parameter of a random initialization.

        Args:
            size (int): Size of a new population to check.

        Returns:
            max_num (int): Maximum amount of the input data combinations.
        """
        max_num = 2 ** self._bin_length

        if size is None or size < 4 or size >= max_num:
            print('Wrong size of population:', size)
            raise ValueError('Wrong size of population')

        return max_num

    def _generate_random_population(self, max_num, size):
        """
        This method generates a new random population by the given input parameters.

        Args:
            max_num (int): Maximum amount of the input data combinations.
            size (int): Size of a new population.

        Returns:
            population (list): list if integers in interval [1, maxnum) that represents a binary encoded
            combination.
        """
        return self._random_diff(max_num, size, start=1)

    def init_random_population(self, size):
        """
        Initializes a new random population of the given size.

        Args:
            size (int): Size of a new random population. Must be greater than 3 and less than the amount
                of all possible combinations of the input data.
        """
        max_num = self._check_init_random_population(size)

        # generate population
        number_list = self._generate_random_population(max_num, size)

        self.population = []
        for num in number_list:
            chromosome = self._get_bit_positions(num)
            fit_val = self._compute_fitness(chromosome)

            self.population.append(IndividualGA(chromosome, fit_val))

        self._sort_population()
        self._update_solution(self.population[-1].chromosome, self.population[-1].fitness_val)


