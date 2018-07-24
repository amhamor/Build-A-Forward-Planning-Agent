from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

classical_planning_results_dictionary = {"ProblemName": [], "SearchType": [], "Heuristic": [], "PlanLength": [], "SecondsToFindSolution": [], "ActionsCount": [], "ExpansionsCount": [], "GoalTestsCount": [], "NewNodesCount": []}
get_integer_boolean = False

def extract_data(line, start_index_string, end_index_string, header_string, is_integer=False, is_float=False):
	words_list = line.split(" ")
	start_index = line.index(start_index_string) + len(start_index_string)
	end_index = line.index(end_index_string)
	if is_integer:
		classical_planning_results_dictionary[header_string].append(int(line[start_index:end_index]))
	elif is_float:
		classical_planning_results_dictionary[header_string].append(float(line[start_index:end_index]))
	else:
		classical_planning_results_dictionary[header_string].append(line[start_index:end_index])

def truncate_spaces(line):
	integer_string = ""
	for character in line:
		if character != " ":
			integer_string += character
		elif (character == " ") and (integer_string != "") and (integer_string[-1] != " "):
			integer_string += character
	return integer_string

with open("ClassicalPlanningProjectResults", 'r') as input_file_object:
	for line in input_file_object:
		if get_integer_boolean:
			line_with_truncated_spaces = truncate_spaces(line)
			integer_strings_list = line_with_truncated_spaces.split(" ")[:-1]
			integers_list = [int(integer_string) for integer_string in integer_strings_list]

			classical_planning_results_dictionary["ActionsCount"].append(integers_list[0]), classical_planning_results_dictionary["ExpansionsCount"].append(integers_list[1]), classical_planning_results_dictionary["GoalTestsCount"].append(integers_list[2]), classical_planning_results_dictionary["NewNodesCount"].append(integers_list[3])
			get_integer_boolean = False
					
		if "Solving" in line:
			extract_data(line=line, start_index_string="Solving ", end_index_string=" using ", header_string="ProblemName")
			if " with " not in line:
				extract_data(line=line, start_index_string=" using ", end_index_string="...", header_string="SearchType")
				classical_planning_results_dictionary["Heuristic"].append(None)
			if " with " in line:
				extract_data(line=line, start_index_string=" using ", end_index_string=" with ", header_string="SearchType")
				extract_data(line=line, start_index_string=" with ", end_index_string="...", header_string="Heuristic")
		if "# Actions" in line:
			get_integer_boolean = True

		if "Plan length: " in line:
			extract_data(line=line, start_index_string="Plan length: ", end_index_string="  Time elapsed in seconds: ", header_string="PlanLength", is_integer=True)
			extract_data(line=line, start_index_string="  Time elapsed in seconds: ", end_index_string="\n", header_string="SecondsToFindSolution", is_float=True)

classical_planning_results_dataframe = DataFrame(classical_planning_results_dictionary)

problem_names_list = []
search_type_list = []

for problem_name in classical_planning_results_dataframe.loc[:, "ProblemName"].drop_duplicates():
	problem_names_list.append(problem_name)

for search_type in classical_planning_results_dataframe.loc[:, "SearchType"].drop_duplicates():
	search_type_list.append(search_type)

with PdfPages("report.pdf") as pdf:
	figure1 = plt.figure(figsize=(17, 13))
	axis1 = figure1.add_axes([0.06, 0.17, 0.93, 0.7])

	for search_type in search_type_list:
		axis1.scatter(classical_planning_results_dataframe.loc[classical_planning_results_dataframe.loc[:, "SearchType"] == search_type, "ActionsCount"].apply(str), classical_planning_results_dataframe.loc[classical_planning_results_dataframe.loc[:, "SearchType"] == search_type, "ExpansionsCount"])
	
	plt.title("Actions Count Versus Expansions Count")
	axis1.set_yscale("log")
	axis1.set_xlabel("Actions Count")
	axis1.set_ylabel("Expansions Count \n(log-converted)")
	axis1.legend(search_type_list)

	figure1_caption_text = "All search algorithms except depth-first and greedy-best-first search increase the number of nodes expanded exponentially as the number of actions taken to find a solution increases. Depth-first and greedy-best-first\nsearch algorithms seem to increase more linearly than the rest of the search algorithms in regards to the number of expansions increasing the number of actions taken to find a solution increases."
	figure1.text(0.03, .085, figure1_caption_text, ha="left", va="baseline")
	
	#figure1.tight_layout()

	pdf.savefig()

	figure2 = plt.figure(figsize=(17, 13))
	axis2 = figure2.add_axes([0.06, 0.17, 0.93, 0.7])

	for search_type in search_type_list:
		axis2.scatter(classical_planning_results_dataframe.loc[classical_planning_results_dataframe.loc[:, "SearchType"] == search_type, "ActionsCount"].apply(str), classical_planning_results_dataframe.loc[classical_planning_results_dataframe.loc[:, "SearchType"] == search_type, "SecondsToFindSolution"])

	plt.title("Actions Count Versus Seconds To Find Solution")
	axis2.set_yscale("log")
	axis2.set_xlabel("Actions Count")
	axis2.set_ylabel("Seconds To Find Solution \n(log-converted)")
	axis2.legend(search_type_list)

	figure2_caption_text = "Generally and for all search algorithms, as the number of actions taken before finding a solution increases, the time to find the optimal solution increases exponentially. A-star and breadth-first searches seem most\nreliable in finding the optimal solution the fastest for two reasons: 1) there exists at least one data point for each of A-star and breadth-first searches that is close to or below the average time taken to find a solution\nfor each set of data points plotted for each number of actions taken to find a solution. 2) A-star and breadth-first searches always find the optimal solution when a solution is found. Greedy-best-first, uniform-cost, and\ndepth-first searches are shown to find some solution the fastest but may not have found the optimal solution."
	figure2.text(0.03, .04, figure2_caption_text, ha="left", va="baseline")

	#figure2.tight_layout()

	pdf.savefig()

	figure3 = plt.figure(figsize=(17, 13))
	axis3 = figure3.add_axes([0.05, 0.1, 0.93, 0.8])

	for problem_name, index in zip(problem_names_list, range(len(problem_names_list))):
		axis3.scatter(classical_planning_results_dataframe.loc[classical_planning_results_dataframe.loc[:, "ProblemName"] == problem_name, "SearchType"], classical_planning_results_dataframe.loc[classical_planning_results_dataframe.loc[:, "ProblemName"] == problem_name, "PlanLength"])

	axis3.set_yscale("log")
	axis3.set_xlabel("Search Type")
	axis3.set_ylabel("Plan Length \n(log-converted)")
	axis3.legend(problem_names_list)

	plt.title("Search Type Versus Plan Length")
	#figure3.tight_layout()

	pdf.savefig()

	figure4 = plt.figure(figsize=(17, 13))
	plt.axis("off")
	plt.title("Algorithm Analysis")
	figure4_caption_text = """
Which algorithm or algorithms would be most appropriate for planning in a very restricted domain (i.e., one that has only a few actions) and needs to operate in real time?

    When very few actions are taken to find a solution (e.g. 20 actions), uniform-cost search finds the optimal solution the fastest when compared with the other search algorithms graphed in the previous pages 
and most reliably due to uniform-cost search finding the optimal solution when a solution is found.

Which algorithm or algorithms would be most appropriate for planning in very large domains (e.g., planning delivery routes for all UPS drivers in the U.S. on a given day)

    When planning in very large domains (e.g. domains that require more than 72 actions to find a solution), greedy-best-first search is the most appropriate to use due to it finding a solution the fastest when
compared with all of the other search algorithms graphed in the above pages.

Which algorithm or algorithms would be most appropriate for planning problems where it is important to find only optimal plans?

    A-star search is the most appropriate search algorithm when finding only optimal plans is important to use due to it finding the optimal solution in or below average time when compared with all of the other 
search algorithms graphed in the above pages.
"""
	figure4.text(0.05, .60, figure4_caption_text)

	pdf.savefig()

	plt.show()
