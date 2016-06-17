# copyright 2016 Siavoosh Payandeh Azad and Behrad Niazmand

import copy
from build_list_of_candidates import build_list_of_candidates
from check_feasibility import check_feasibility
from area_coverage_calc import calculate_area
from area_coverage_calc import calculate_coverage
from cost_function import calculate_coverage_cost, calculate_value_density
import package_file
from file_generator import make_folders
from essential_checker_extraction import find_essential_checker
import sys
import logger


if '--help' in sys.argv[1:]:
    print "there is no help in the world!\n"
    sys.exit()

for i in range(1, package_file.number_of_checkers+1):
    package_file.list_of_checkers.append(str(i))

make_folders()
# we need to prepare a dictionary of all the single checker's info
# The dictionary format is the following     checker number:  [coverage,  area]
build_list_of_candidates()

# Just for getting a copy of the current console
sys.stdout = logger.Logger()

# the area of the best solution
best_cost = 0

print "\033[32m* NOTE::\033[0m starting greedy optimization!"

for item in package_file.list_of_checkers:
    area = calculate_area([item])
    package_file.list_of_candidates[item] = [None, area]
    if package_file.cost_function_type == "cov":
        package_file.list_of_candidates[item] = [calculate_coverage_cost([item]), area]
    elif package_file.cost_function_type == "val_density":
        package_file.list_of_candidates[item] = [calculate_value_density([item]), area]


# sorting the dictionary based on the coverage
sorted_coverage = sorted(package_file.list_of_candidates.items(),  key=lambda e: e[1][0], reverse=True)
print "sorted list of checkers:", sorted_coverage

"""
sorted_coverage = [('9', [0.88065714285714292, 70.0]), ('8', [0.68822807017543863, 57.0]),
                   ('5', [0.57208888888888887, 45.0]), ('3', [0.48573584905660377, 53.0]),
                   ('4', [0.44386206896551722, 58.0]), ('2', [0.40863492063492063, 63.0]),
                   ('1', [0.38423880597014926, 67.0]), ('7', [0.37858823529411767, 68.0]),
                   ('6', [0.22650000000000001, 52.0]), ('12', [0.21811111111111112, 54.0]),
                   ('10', [0.062266666666666665, 45.0]), ('11', [0.042962264150943397, 53.0])]

package_file.list_of_detection_info_sa0 = {
    '11': ['0', '4', '0', '0', '0', '0', '5', '0', '0', '0', '2', '5', '0', '0', '2', '2', '0', '0', '0', '0', '0', '0',
           '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    '10': ['0', '0', '0', '0', '0', '8', '0', '0', '0', '0', '0', '8', '0', '0', '0', '0', '16', '0', '0', '0', '8',
           '0', '0', '0', '0', '16', '0', '0', '0', '0', '0', '8', '0', '0'],
    '12': ['0', '15', '0', '0', '5', '0', '0', '0', '0', '0', '0', '0', '5', '39', '0', '0', '0', '0', '0', '0', '0',
           '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    '1': ['0', '0', '0', '0', '20', '0', '20', '0', '0', '0', '0', '0', '20', '20', '0', '0', '30', '10', '0', '0',
          '15', '5', '5', '0', '0', '0', '40', '0', '0', '5', '5', '15', '0', '0'],
    '3': ['0', '60', '0', '0', '0', '0', '15', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '10', '0', '0', '0',
          '0', '0', '0', '0', '0', '40', '0', '0', '0', '0', '0', '0', '0'],
    '2': ['0', '0', '0', '0', '0', '32', '0', '0', '0', '0', '160', '32', '0', '0', '32', '32', '64', '0', '32', '32',
          '32', '0', '0', '32', '32', '64', '0', '32', '32', '0', '0', '32', '32', '32'],
    '5': ['0', '0', '0', '0', '0', '0', '20', '0', '0', '0', '160', '0', '0', '0', '32', '32', '0', '10', '32', '32',
          '0', '0', '0', '32', '32', '0', '40', '32', '32', '5', '0', '0', '32', '32'],
    '4': ['0', '0', '0', '0', '0', '8', '0', '0', '0', '0', '0', '8', '0', '0', '0', '0', '16', '0', '0', '0', '8', '0',
          '0', '0', '0', '16', '0', '0', '0', '0', '0', '8', '0', '0'],
    '7': ['0', '0', '0', '0', '20', '0', '20', '0', '0', '0', '0', '0', '20', '20', '0', '0', '30', '10', '0', '0',
          '15', '5', '5', '0', '0', '0', '40', '0', '0', '5', '5', '15', '0', '0'],
    '6': ['0', '0', '0', '0', '0', '16', '0', '0', '0', '0', '0', '16', '0', '0', '0', '0', '32', '0', '0', '0', '16',
          '0', '0', '0', '0', '32', '0', '0', '0', '0', '0', '16', '0', '0'],
    '9': ['0', '0', '0', '0', '0', '36', '0', '0', '0', '0', '160', '36', '0', '0', '32', '32', '72', '0', '32', '32',
          '36', '0', '0', '32', '32', '72', '0', '32', '32', '0', '0', '36', '32', '32'],
    '8': ['0', '0', '0', '0', '0', '32', '0', '0', '0', '0', '0', '32', '0', '0', '0', '0', '64', '0', '0', '0', '32',
          '0', '0', '0', '0', '64', '0', '0', '0', '0', '0', '32', '0', '0']}

package_file.list_of_detection_info_sa1 = {
    '11': ['4', '0', '4', '4', '5', '5', '0', '0', '0', '0', '0', '0', '5', '5', '0', '0', '0', '0', '0', '0', '0', '0',
           '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    '10': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
           '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    '12': ['15', '0', '15', '15', '0', '0', '5', '0', '0', '0', '15', '5', '0', '0', '120', '15', '0', '0', '0', '0',
           '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    '1': ['0', '0', '0', '0', '20', '20', '20', '0', '0', '0', '64', '20', '20', '20', '0', '12', '10', '10', '0', '14',
          '5', '5', '5', '0', '15', '40', '40', '0', '8', '5', '5', '5', '0', '15'],
    '3': ['60', '0', '60', '60', '15', '15', '0', '0', '0', '0', '0', '20', '20', '20', '0', '0', '10', '0', '0', '0',
          '5', '5', '5', '0', '0', '40', '0', '0', '0', '0', '0', '0', '0', '0'],
    '2': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '128', '0', '0', '0', '128', '0', '0',
          '0', '0', '128', '0', '0', '0', '128', '0', '0', '0', '0', '128', '0'],
    '5': ['0', '0', '0', '0', '20', '20', '0', '0', '0', '0', '0', '20', '20', '20', '0', '0', '10', '0', '0', '0', '5',
          '5', '5', '0', '0', '40', '0', '0', '0', '0', '5', '5', '0', '0'],
    '4': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    '7': ['0', '0', '0', '0', '20', '20', '20', '0', '0', '0', '64', '20', '20', '20', '0', '12', '10', '10', '0', '14',
          '5', '5', '5', '0', '15', '40', '40', '0', '8', '5', '5', '5', '0', '15'],
    '6': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '64', '0', '0', '0', '64', '0', '0',
          '0', '0', '64', '0', '0', '0', '64', '0', '0', '0', '0', '64', '0'],
    '9': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '128', '0', '0', '0', '128', '0', '0',
          '0', '0', '128', '0', '0', '0', '128', '0', '0', '0', '0', '128', '0'],
    '8': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '128', '0', '0', '0', '128', '0', '0',
          '0', '0', '128', '0', '0', '0', '128', '0', '0', '0', '0', '128', '0']}

package_file.list_of_true_misses_sa0 = {
    11: ['0', '60', '0', '0', '20', '40', '15', '0', '0', '0', '158', '0', '5', '55', '30', '30', '40', '20', '20',
         '32', '32', '110', '10', '32', '32', '55', '5', '5', '32', '32', '80', '40', '32', '32'],
    10: ['0', '64', '0', '0', '20', '32', '20', '0', '0', '0', '160', '32', '20', '20', '32', '32', '94', '10', '32',
         '32', '47', '5', '5', '32', '32', '64', '40', '32', '32', '5', '5', '47', '32', '32'],
    12: ['0', '49', '0', '0', '15', '40', '20', '0', '0', '0', '160', '5', '0', '16', '32', '32', '40', '20', '20',
         '32', '32', '110', '10', '32', '32', '55', '5', '5', '32', '32', '80', '40', '32', '32'],
    1: ['0', '64', '0', '0', '0', '40', '0', '0', '0', '0', '160', '40', '0', '0', '32', '32', '80', '0', '32', '32',
        '40', '0', '0', '32', '32', '80', '0', '32', '32', '0', '0', '40', '32', '32'],
    3: ['0', '4', '0', '0', '20', '40', '5', '0', '0', '0', '160', '40', '20', '20', '32', '32', '110', '0', '32', '32',
        '55', '5', '5', '32', '32', '80', '0', '32', '32', '5', '5', '55', '32', '32'],
    2: ['0', '64', '0', '0', '20', '8', '20', '0', '0', '0', '0', '8', '20', '20', '0', '0', '46', '10', '0', '0', '23',
        '5', '5', '0', '0', '16', '40', '0', '0', '5', '5', '23', '0', '0'],
    5: ['0', '64', '0', '0', '20', '40', '0', '0', '0', '0', '0', '40', '20', '20', '0', '0', '110', '0', '0', '0',
        '55', '5', '5', '0', '0', '80', '0', '0', '0', '0', '5', '55', '0', '0'],
    4: ['0', '64', '0', '0', '20', '32', '20', '0', '0', '0', '160', '32', '20', '20', '32', '32', '94', '10', '32',
        '32', '47', '5', '5', '32', '32', '64', '40', '32', '32', '5', '5', '47', '32', '32'],
    7: ['0', '64', '0', '0', '0', '40', '0', '0', '0', '0', '160', '40', '0', '0', '32', '32', '80', '0', '32', '32',
        '40', '0', '0', '32', '32', '80', '0', '32', '32', '0', '0', '40', '32', '32'],
    6: ['0', '64', '0', '0', '20', '24', '20', '0', '0', '0', '160', '24', '20', '20', '32', '32', '78', '10', '32',
        '32', '39', '5', '5', '32', '32', '48', '40', '32', '32', '5', '5', '39', '32', '32'],
    9: ['0', '64', '0', '0', '20', '4', '20', '0', '0', '0', '0', '4', '20', '20', '0', '0', '38', '10', '0', '0', '19',
        '5', '5', '0', '0', '8', '40', '0', '0', '5', '5', '19', '0', '0'],
    8: ['0', '64', '0', '0', '20', '8', '20', '0', '0', '0', '160', '8', '20', '20', '32', '32', '46', '10', '32', '32',
        '23', '5', '5', '32', '32', '16', '40', '32', '32', '5', '5', '23', '32', '32']}

package_file.list_of_true_misses_sa1 = {
    11: ['60', '0', '60', '60', '15', '15', '20', '0', '0', '0', '64', '5', '0', '0', '128', '15', '20', '20', '20',
         '128', '12', '10', '10', '128', '14', '5', '5', '5', '128', '15', '40', '40', '128', '8'],
    10: ['64', '0', '64', '64', '20', '20', '20', '0', '0', '0', '64', '20', '20', '20', '128', '12', '10', '10', '128',
         '14', '5', '5', '5', '128', '15', '40', '40', '128', '8', '5', '5', '5', '128', '15'],
    12: ['49', '0', '49', '49', '20', '20', '15', '0', '0', '0', '49', '0', '5', '5', '8', '0', '20', '20', '20', '128',
         '12', '10', '10', '128', '14', '5', '5', '5', '128', '15', '40', '40', '128', '8'],
    1: ['64', '0', '64', '64', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '128', '0', '0', '0', '128', '0', '0',
        '0', '0', '128', '0', '0', '0', '128', '0', '0', '0', '0', '128', '0'],
    3: ['4', '0', '4', '4', '5', '5', '20', '0', '0', '0', '64', '0', '0', '0', '128', '12', '0', '10', '128', '14',
        '0', '0', '0', '128', '15', '0', '40', '128', '8', '5', '5', '5', '128', '15'],
    2: ['64', '0', '64', '64', '20', '20', '20', '0', '0', '0', '64', '20', '20', '20', '0', '12', '10', '10', '0',
        '14', '5', '5', '5', '0', '15', '40', '40', '0', '8', '5', '5', '5', '0', '15'],
    5: ['64', '0', '64', '64', '0', '0', '20', '0', '0', '0', '64', '0', '0', '0', '128', '12', '0', '10', '128', '14',
        '0', '0', '0', '128', '15', '0', '40', '128', '8', '5', '0', '0', '128', '15'],
    4: ['64', '0', '64', '64', '20', '20', '20', '0', '0', '0', '64', '20', '20', '20', '128', '12', '10', '10', '128',
        '14', '5', '5', '5', '128', '15', '40', '40', '128', '8', '5', '5', '5', '128', '15'],
    7: ['64', '0', '64', '64', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '128', '0', '0', '0', '128', '0', '0',
        '0', '0', '128', '0', '0', '0', '128', '0', '0', '0', '0', '128', '0'],
    6: ['64', '0', '64', '64', '20', '20', '20', '0', '0', '0', '64', '20', '20', '20', '64', '12', '10', '10', '64',
        '14', '5', '5', '5', '64', '15', '40', '40', '64', '8', '5', '5', '5', '64', '15'],
    9: ['64', '0', '64', '64', '20', '20', '20', '0', '0', '0', '64', '20', '20', '20', '0', '12', '10', '10', '0',
        '14', '5', '5', '5', '0', '15', '40', '40', '0', '8', '5', '5', '5', '0', '15'],
    8: ['64', '0', '64', '64', '20', '20', '20', '0', '0', '0', '64', '20', '20', '20', '0', '12', '10', '10', '0',
        '14', '5', '5', '5', '0', '15', '40', '40', '0', '8', '5', '5', '5', '0', '15']
}
"""

if package_file.debug:
    print "------------------------------"
    print "printing the checkers detection tables"
    print "stuck at 0:"
    for item in package_file.list_of_true_misses_sa0:
        print item,
        for node in range(0, len(package_file.list_of_true_misses_sa0[item])):
            print package_file.list_of_true_misses_sa0[item][node],
        print ""
    print "------------------------------"
    print "printing the checkers detection tables"
    print "stuck at 1:"
    for item in package_file.list_of_true_misses_sa1:
        print item,
        for node in range(0, len(package_file.list_of_true_misses_sa1[item])):
            print package_file.list_of_true_misses_sa1[item][node],
        print ""
    print "------------------------------"

if package_file.extract_essential_checkers:
    current_list, checkers_for_optimization = copy.deepcopy(find_essential_checker())
else:
    current_list = []
    checkers_for_optimization = copy.deepcopy(package_file.list_of_checkers)

print "------------------------------"
print "starting optimization with ", current_list, "checkers already chosen"
print "and running greedy algorithm on ", checkers_for_optimization
if check_feasibility(current_list[1:], current_list[0]):
    print "starting sequence is feasible...  going further..."
    for item in sorted_coverage:
        if item[0] in checkers_for_optimization:
            print "------------------------------"
            print "Picking item:", item[0]
            if item not in current_list:
                if check_feasibility(current_list, item[0]):
                    current_list.append(item[0])
                    coverage = calculate_coverage(current_list)
                    print "coverage:", coverage
                    if coverage == 100:
                        break

print "------------------------------"
print "\033[32m* NOTE::\033[0m best solution:", current_list
print "\033[32m* NOTE::\033[0m coverage:", calculate_coverage(current_list)
