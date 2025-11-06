from time import time_ns

def printResults(results_in_nanoseconds: list) -> None:
    """Convert the nanoseconds to appropriate units and then print to console the appropriate results."""

    magnitudes_table = [
        [1, "ns"],
        [1000, "μs"],
        [1000000, "ms"],
        [1000000000, "s"]
    ]

    if len(results_in_nanoseconds) == 0:
        return
    # Get average number of digits from both lowest and higest values
    average_digits = (len(str(int(max(results_in_nanoseconds))))+len(str(int(min(results_in_nanoseconds)))))//2
    # Get index based on dividing the number of digits, capping at end of the table
    magnitude_index = min(average_digits//3-1, len(magnitudes_table)-1)
    # Get corresponding data from table
    magnitude_factor = magnitudes_table[magnitude_index][0]
    unit = magnitudes_table[magnitude_index][1]

    average = round((sum(results_in_nanoseconds)/len(results_in_nanoseconds))/magnitude_factor, 5)
    minimum = round(min(results_in_nanoseconds)/magnitude_factor, 5)
    maximum = round(max(results_in_nanoseconds)/magnitude_factor, 5)
    deviation = round(((average-minimum)+(maximum-average))/2, 5)

    print(f"Average: {average} {unit}\nDeviation: +/-{deviation} {unit}\nMinimum: {minimum} {unit}\nMaximum: {maximum} {unit}")


def testPerformance(test_function: callable, test_arguments : list = None, test_kword_arguments : dict = None, iterations_per_cycle : int = 100000, seconds_per_cycle : int = None, number_of_cycles : int = 7, print_performance : bool = True) -> list:
    """Test the performance of function using a single set of arguments and return the results in nanoseconds.

    function - reference of the function you want to test
    test_arguments - arguments to be put inside of that function
    test_kword_arguments - arguments with names
    iterations_per_cycle - how many times you want to run a function during a single cycle
    time_per_cycle - how many seconds do you give the code to run per cycle, overrides iterations_per_cycle functionality
    number_of_cycles - how many times do you want to repeat a cycle
    print_performance - if true will print out the results to console
    """

    # Initialise objects if not initialised
    if not test_arguments:
        test_arguments = []
    if not test_kword_arguments:
        test_kword_arguments = {}

    if (seconds_per_cycle):
        overall_results = []
        for cycle in range(number_of_cycles):
            cycle_end_time = time_ns() + 1000000000*seconds_per_cycle
            cycle_results = []
            while time_ns() < cycle_end_time:
                start_time = time_ns()
                try:
                    test_function(*test_arguments, **test_kword_arguments)
                except:
                    print(f"Failed on cycle {cycle}")
                    continue
                end_time = time_ns()
                cycle_results.append(end_time-start_time)
            if (len(cycle_results) > 0):
                overall_results.append(sum(cycle_results)/len(cycle_results))

        if (print_performance):
            printResults(overall_results)
        return(overall_results)
    
    overall_results = []
    for cycle in range(number_of_cycles):
        cycle_results = []
        for iteration in range(iterations_per_cycle):
            start_time = time_ns()
            try:
                test_function(*test_arguments, **test_kword_arguments)
            except Exception as e:
                print(f"Failed on cycle {cycle}, iteration {iteration}")
                break
            end_time = time_ns()
            cycle_results.append(end_time-start_time)
        if (len(cycle_results) > 0):
            overall_results.append(sum(cycle_results)/len(cycle_results))
    
    if (print_performance):
        printResults(overall_results)
    return(overall_results)

def testCorrectness(test_function: callable, test_table: list) -> list:
    """Test the correctness of a function against a table of arguments, keyword arguments and expected results.
    Print results and return list of names of functions that have failed.
    
    Test table is to be formated as:
    [
        ["test name 1", [argument1, argument2], {keyword_argument1: argument}, expected_result],
        ["test name 2", [], {}, expected_result]
    ]
    """
    failed = []
    passed = 0
    for test in test_table:
        try:
            test_result = test_function(*test[1], **test[2])
        except Exception as e:
            print(f"Test {test[0]} failed to execute! - {e}")
            failed.append({test[0]})
            continue

        if (test_result == test[3]):
            passed += 1
        else:
            print(f"Test {test[0]} failed, expected {test[3]} of type {str(type(test[3]))}, got {test_result} of type {str(type(test_result))}!")
            failed.append({test[0]})
        
    print(f"Passed {passed}/{len(test_table)} tests!")
    return failed

