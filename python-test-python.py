from time import time_ns

def testPerformance(function: function, arguments : list = None, iterations_per_cycle : int = 100000, seconds_per_cycle : int = None, number_of_cycles : int = 7):
    """Test the performance of function using a single set of arguments and print the results.

    function - reference of the function you want to test
    arguments - arguments to be put inside of that function
    iterations_per_cycle - how many times you want to run a function during a single cycle
    time_per_cycle - how many seconds do you give the code to run per cycle, overrides iterations_per_cycle functionality
    number_of_cycles - how many times do you want to repeat a cycle"""

    if (seconds_per_cycle):
        for i in range(number_of_cycles):
            cycle_end_time = time_ns()+ 1000000000*seconds_per_cycle
            cycle_results = []
            while time_ns() < cycle_end_time:
                start_time = time_ns()
                function(arguments)
                end_time = time_ns()




    
