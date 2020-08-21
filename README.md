# GenesPy

A pure python genetic algorithms library. The intention is to create a library
without any external dependence. Standard Python only.

# Usage guide for a simple case

1. Create a *Task* object.

    ```
    task = Task()
    ```

2. **Write your own evaluation function**. This function must accept two
   parameters:
   * A list (the genome). Each item in the list is a gene.
   * An arbitrary object (which is defined by you, as complementary data to
     evaluate the individuals). By default, this object is *None*.

   The function must return a floating value as *fitness* of the individual.
   
   ```
   def my_eval_function(genome, data):
       # x - genome[0]
       # y - genome[1]
   
       return (genome[0] * data[0]) + (genome[1] * data[1])
   ```

3. Define the structure of your variables. These can be floating values, binary
   strings, or permutations:
   ```
   # Declaration of binary string structure as tuple of tuples (2 variables)
   struct = ((True, 5, 5),  # x (sign bit, integer bits, mantissa bits)
            (True, 5, 5))   # y (sign bit, integer bits, mantissa bits)
   ```

4. Create a population and assign to the *Task* object.

   ```
   the_pop = init_binary_pop(1000, struct)  # Binary population
   data = [5, 20]  # Arbitrary data
   task.set_population(the_pop)
   task.set_data(data)
   ```

5. Choose the *selection*, *crossover* and *mutation* functions that will be
   used, and assign them to the *Task* object as well.
   
   ```
   task.set_evals([my_eval_function], [-1.0])  # (-1 minimizes, +1 maximizes)
   task.set_mutator(mutate_flip, {'mp': .3})
   task.set_crossover(crossover_one_point)
   task.set_selector(select_vasconcelos, {'cp': .5})
   ```

6. Define the desired execution parameters (generations, execution times, etc.).
   Choose a genetic algorithm and ...

7. Run it!

   ```
   elitism = 1.0  # % of puplation in elitism
   duration = 10  # Max duration (in seconds)
   gens = 1000  # Maximum number of generations
   verbose = 2  # Report every n generations
   answer = general_ga(
       task,
       elitism,
       duration,
       gens,
       verbose
   )
   ```
   
# More examples

Check the *examples* directory to see the solution of simple problems, using
different ways to encode the genome.

# TODO

- Documentation
- More selection algorithms
- Add multiobjective selector(s)
- More mutation operators
- More crossover operators
- User documentation and examples
