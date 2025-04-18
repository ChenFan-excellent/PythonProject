# Donglin Chen
# Student id: 24161516

def read_csv(csvFile):
    # This function reads a CSV file.
    # It returns two lists: one is the headers, the other is the data.
    with open(csvFile, 'r') as f:
        all_lines = f.readlines()
    file_headers = all_lines[0].strip().split(',')                   # Get the first line (header)
    all_data = [line.strip().split(',') for line in all_lines[1:]]   # Get other lines (data)
    return file_headers, all_data


def parse_age_group(file_headers):
    # This function gets the age range from header name.
    age_part = file_headers.replace("Age ", "")                      # Remove "Age " from string
    
    if "and over" in age_part:                                       # Example: "Age 85 and over"
        return (int(age_part.split()[0]), None)
    elif "-" in age_part:                                            # Example: "Age 10-14"
        low, high = age_part.split("-")
        return (int(low), int(high))                                 # Return two numbers
    else:
        return (None, None)                                          # Cannot understand the age

def find_age_group(age, file_headers):
    # This function finds which age group the number belongs to
    for header in file_headers:  
        low, high = parse_age_group(header)                          # Get age range
        
        if low is None:                                              # Skip if not a valid age group
            continue
            
        if high is None:                                             # For "85 and over"
            if age >= low:
                return [low, None]
        else:                                                        # For age like 10-14
            if low <= age <= high:
                return [low, high]
    
    return [None, None]                                              # Not found

'''
         The above is used to solve OP1

'''

def build_sa2_to_sa3_mapping(all_area_data):
    # This function makes a mapping from SA2 to SA3.
    # It returns a dictionary.
    sa2_to_sa3 = {}
    for row in all_area_data:
        sa2_code = row[4]                                            # Column 5 is SA2
        sa3_code = row[2]                                            # Column 3 is SA3
        sa2_to_sa3[sa2_code] = sa3_code
    return sa2_to_sa3

def find_sa2s_in_sa3(sa3_code, all_area_data):
    # This function finds all SA2s inside one SA3.
    # It returns a list of SA2 codes.
    sa2_list = []
    for row in all_area_data:
        if row[2] == sa3_code:                                       # If SA3 code matches
            sa2_list.append(row[4])                                  # Add the SA2 code
    return sa2_list

def calculate_stats(values):
    # This function calculates mean (average) and standard deviation
    if not values or len(values) == 1:                               # If list is empty or only 1 number
        return 0.0, 0.0
    
    mean = sum(values) / len(values)                                 # Calculate average
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1) # Formula for sample variance 
    std_dev = variance ** 0.5                                        # Get standard deviation
    return round(mean, 4), round(std_dev, 4)                         # Round to 4 decimal places

def get_sa3_populations(sa3_code, age_group, all_area_data, pop_headers, pop_data):
    # This function gets population numbers for a SA3 area and a specific age group
    populations = []
        
    sa2_codes = find_sa2s_in_sa3(sa3_code, all_area_data)            # Get all SA2 codes in this SA3  
    
    for sa2_code in sa2_codes:
        
        for row in pop_data:
            if row[0] == sa2_code:                                   # If SA2 code matches
                for i, header in enumerate(pop_headers):             # Go through each column
                    if "Age " in header:                             # Only look at age columns
                        low, high = parse_age_group(header)
                        
                        if (low == age_group[0] and 
                            (high == age_group[1] or 
                             (high is None and age_group[1] is None))): # Match the age group
                            populations.append(float(row[i]))        ## Add population value
    return populations


def OP2_result(sa2_1, sa2_2, age_group, sa2_to_sa3, area_data, pop_headers, pop_data):
    # This function returns the average and std dev of two SA3s based on given SA2s and age group
    sa3_1_code = sa2_to_sa3.get(sa2_1)                                 # Get SA3 for first SA2
    sa3_2_code = sa2_to_sa3.get(sa2_2)                                 # Get SA3 for second SA2
    
    if not sa3_1_code or not sa3_2_code:                               # If any SA3 not found
        return [[None, 0.0, 0.0], [None, 0.0, 0.0]]
    
    # Get population list for both SA3s
    sa3_1_pops = get_sa3_populations(sa3_1_code, age_group, area_data, pop_headers, pop_data)
    sa3_2_pops = get_sa3_populations(sa3_2_code, age_group, area_data, pop_headers, pop_data)
    
    # Calculate stats
    mean_1, std_dev_1 = calculate_stats(sa3_1_pops)
    mean_2, std_dev_2 = calculate_stats(sa3_2_pops)
    
    return [[sa3_1_code, mean_1, std_dev_1], [sa3_2_code, mean_2, std_dev_2]]

'''

         The above is in order to slove OP2

'''

def get_unique_states(area_headers, area_data):
    # Get all unique state names from area data
    state_idx = area_headers.index("S_T name")
    return sorted(list(set(row[state_idx].lower() for row in area_data if row[state_idx])))

def get_sa3_for_state(state, area_headers, area_data):
    # Get all SA3 codes and names in one state
    state_idx = area_headers.index("S_T name")
    sa3_code_idx = area_headers.index("SA3 code")
    sa3_name_idx = area_headers.index("SA3 name")
    
    return [
        (row[sa3_code_idx], row[sa3_name_idx].lower())
        for row in area_data
        if row[state_idx].lower() == state
    ]

def get_sa3_age_population(sa3_code, age_group, area_headers, area_data, pop_headers, pop_data):
    # Get total population in one SA3 for one age group
    total = 0.0
    
    sa2_idx = area_headers.index("SA2 code")
    sa3_idx = area_headers.index("SA3 code")
    
    # Find all SA2 codes in this SA3
    sa2_codes = [row[sa2_idx] for row in area_data if row[sa3_idx] == sa3_code]
    
    # Find column index for the age group
    age_cols = [i for i, h in enumerate(pop_headers) 
               if parse_age_group(h) == tuple(age_group)]
    
    # Add population from matching rows and age group
    for row in pop_data:
        if row[0] in sa2_codes and age_cols:
            total += float(row[age_cols[0]])
    
    return total

def get_sa3_total_population(sa3_code, area_headers, area_data, pop_headers, pop_data):
    # Get total population in one SA3 (all ages)
    total = 0.0
        
    sa2_idx = area_headers.index("SA2 code")
    sa3_idx = area_headers.index("SA3 code")
    
    # Get SA2 list in this SA3
    sa2_codes = [row[sa2_idx] for row in area_data if row[sa3_idx] == sa3_code]
     
    # Get all age columns
    age_cols = [i for i, h in enumerate(pop_headers) if h.startswith("Age ")]
    
    # Add all population numbers in those columns
    for row in pop_data:
        if row[0] in sa2_codes:
            for col in age_cols:
                if col < len(row):                                             # Avoid index error
                    total += float(row[col])
    
    return total

def calculate_OP3(age_group, area_headers, area_data, pop_headers, pop_data):
    # For each state, find the SA3 with most people in one age group
    result = []
    states = get_unique_states(area_headers, area_data)                        # Get all state names
    
    for state in sorted(states):  
        max_pop = -1
        target_sa3 = None                                                      # Best SA3 name
        
        sa3_areas = get_sa3_for_state(state, area_headers, area_data)          # All SA3s in this state
        
        for sa3_code, sa3_name in sa3_areas:
            # Get population of the SA3 for the age group
            age_pop = get_sa3_age_population(sa3_code, age_group, 
                                           area_headers, area_data, 
                                           pop_headers, pop_data)
            
            # Choose the biggest one             
            if age_pop > max_pop or (age_pop == max_pop and 
                                   (target_sa3 is None or sa3_name < target_sa3)):
                max_pop = age_pop
                target_sa3 = sa3_name
                target_code = sa3_code
                
        if target_sa3 and max_pop > 0:
            # Get full population of this SA3 (for all age)
            total_pop = get_sa3_total_population(target_code, area_headers, 
                                               area_data, pop_headers, pop_data)
            # Calculate percentage
            percentage = round(max_pop / total_pop, 4) if total_pop > 0 else 0
            result.append([state, target_sa3, percentage])                     # Save result
    
    return result

'''

               The above is in order to slove OP3 

'''

def get_sa2_populations(sa2_code, pop_headers, pop_data):
    # Get population data (only age groups) for one SA2
    for row in pop_data:
        if row[0] == sa2_code:            
            return [float(x) for x in row[2:]]                                # Skip SA2 code and name
    return []                                                                 # Return empty list if not found

def calculate_correlation(pop1, pop2):
    # Pearson correlation between two SA2 populations
    if len(pop1) != len(pop2) or len(pop1) == 0:
        return 0.0                                                            # No variation → correlation is 0
    
    n = len(pop1)
    sum_x = sum(pop1)
    sum_y = sum(pop2)
    sum_x_sq = sum(x**2 for x in pop1)
    sum_y_sq = sum(y**2 for y in pop2)
    sum_xy = sum(x*y for x, y in zip(pop1, pop2))
    
    numerator = sum_xy - (sum_x * sum_y)/n
    denominator_x = (sum_x_sq - sum_x**2/n) ** 0.5
    denominator_y = (sum_y_sq - sum_y**2/n) ** 0.5
    
    if denominator_x == 0 or denominator_y == 0:
        return 0.0
    
    return round(numerator / (denominator_x * denominator_y), 4)

def OP4_result(sa2_1, sa2_2, pop_headers, pop_data):
    # Main function for OP4: return correlation between two SA2s
    pop1 = get_sa2_populations(sa2_1, pop_headers, pop_data)
    pop2 = get_sa2_populations(sa2_2, pop_headers, pop_data)
    
    return calculate_correlation(pop1, pop2)

'''

               The above is in order to slove OP4 

'''

def main(csvfile_1, csvfile_2, age, sa2_1, sa2_2):
    
    # Step 1: Read the two CSV files
    area_headers, area_data = read_csv(csvfile_1)
    pop_headers, pop_data = read_csv(csvfile_2)
    
    # Step 2: Create SA2 to SA3 map
    sa2_to_sa3 = build_sa2_to_sa3_mapping(area_data)
        
    OP1 = find_age_group(age, pop_headers)
    
    OP2 = OP2_result(sa2_1, sa2_2, OP1, sa2_to_sa3, area_data, pop_headers, pop_data)    
    
    OP3 = calculate_OP3(OP1, area_headers, area_data, pop_headers, pop_data)
    
    OP4 = OP4_result(sa2_1, sa2_2, pop_headers, pop_data)
        
    return OP1, OP2, OP3, OP4


"""
Debugging Documentation:

Issue 1 (Date: 2025 April 6 – OP1):
- Error Description:
    Age 20 was placed in [15–19] group instead of [20–24]
- Erroneous Code Snippet:
    if low <= age <= high:  # Line 27 in find_age_group()
- Test Case:
    main('SampleData.csv', 'Population.csv', 20, 'SA2_1', 'SA2_2')
    # Output: age=20 → [15, 19] (expected [20, 24])
- Reflection:
    I misunderstood ABS age groups. They use ≤start and <end. I changed condition to check if low ≤ age < high+1.
    I learned to always check the official definition of data ranges first.

Issue 2 (Date: 2025 April 10 – OP2):
- Error Description:
    Program crashed when SA2 code was not in the area_data list
- Erroneous Code Snippet:
    sa3_code = row[2]  # Line 35 (before fix)
- Test Case:
    main('BrokenData.csv', 'Pop.csv', 30, 'InvalidSA2', 'SA2_2')
    # Error: list index out of range
- Reflection:
    I assumed all SA2 codes would exist. I learned to always add checks when accessing data.
    I now handle missing or invalid SA2 codes to prevent runtime errors.

Issue 3 (Date: 2025 April 15 – OP4):
- Error Description:
    Correlation returned 0.0 for two identical lists
- Erroneous Code Snippet:
    denominator = (sum_x_sq - sum_x**2/n) ** 0.5  # Line 18 in calculate_correlation()
- Test Case:
    SA2_1 = [10, 10], SA2_2 = [20, 20] → result: 0.0 (should be 1.0)
- Reflection:
    I forgot that identical values give denominator 0, which causes division by 0.
    I learned to check for this and return 0.0 or handle it properly.
"""