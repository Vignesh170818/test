import re
import traceback

def parse_epic_abstract(abs_epic_text:str):

    pattern = r"\d+\.\sEPIC Title:\s(.*?)\s2.EPIC Level User Story:\s(.*?)\s3. Acceptance\sCriteria:\s(.*?)\s4. Business Value:\s(.*?)\s5. Risks and Dependencies:\s(.*?)\s6. Design and Technical Specifications:\s(.*?)(?=\d+\.|$)7.Non-functional Requirements :\s(.*?)(?=\d+\.|$)"
    matches = re.findall(pattern, abs_epic_text, re.DOTALL)
    epic_abs_dict = {}

    for index, match in enumerate(matches, start=1):
        f_title, us, acceptance_criteria, bussines_value, r_and_dep, d_and_ts = match   
        epic_abs_dict["Title"] = f_title
        epic_abs_dict["User Story"] = us
        epic_abs_dict["Acceptance Criteria"] = acceptance_criteria
        epic_abs_dict["Business Value"] = bussines_value
        epic_abs_dict["Risks and Dependencies"] = r_and_dep
        epic_abs_dict["Design and Technical Specifications"] = d_and_ts
        return epic_abs_dict

    if len(matches)==0:
        points = re.split(r'(?=\d+\.)', abs_epic_text.strip())
        if len(points)>4:
            epic_title_str = ":".join(points[1].split(":")[1:])
            epic_title_str=epic_title_str.strip("\n").strip("\t").replace("\n","")
            epic_abs_dict["Title"]=epic_title_str.replace("\r","")
            # if len(points[1].split(":"))>2:
            #     epic_abs_dict["Title"]=epic_abs_dict["Title"]+points[1].split(":")[2:].strip("\n").strip("\t")
            epic_abs_dict["Acceptance Criteria"] = points[3].split(":")[1]
        elif len(points)>2:
            epic_abs_dict["Title"] = points[1].split(":")[1].strip("\n").strip("\t")
            if "2. Acceptance Criteria:" in points[2]:
                epic_abs_dict["Acceptance Criteria"] = points[2].split(":")[1].strip("\n").strip("\t")
            else:
                epic_abs_dict["Acceptance Criteria"] = ""
        elif len(points)==1:
            pattern_title=r'EPIC Title:\s(.*?)EPIC Level User Story:'
            pattern_ac=r'Acceptance Criteria:(.*?)Risks and Dependencies'
            matches_t = re.findall(pattern_title, points[0], re.DOTALL)
            matches_ac = re.findall(pattern_ac, points[0], re.DOTALL)
            if matches_t:
                epic_abs_dict['Title']=matches_t[0]
            if matches_ac:
                epic_abs_dict['Acceptance Criteria']=matches_ac[0]
        elif len(points)==0:
            epic_abs_dict["Title"] = abs_epic_text
            epic_abs_dict["Acceptance Criteria"] = ""
        return epic_abs_dict
    
def parse_feature_abstract(abs_feature_text:str):
    pattern = r"\d+\.\sFeature Title:\s(.*?)\s2. User Story:\s(.*?)\s3. Acceptance\sCriteria:\s(.*?)\s4. Business Value:\s(.*?)\s5. Risks and Dependencies:\s(.*?)\s6. Design and Technical Specifications:\s(.*?)(?=\d+\.|$)"
    matches = re.findall(pattern, abs_feature_text, re.DOTALL)
    feature_abs_data = []

    for index, match in enumerate(matches, start=1):
        f_title, us, acceptance_criteria, bussines_value, r_and_dep, d_and_ts = match
        f_abs_dict = {}
        f_abs_dict["Feature Title"] = f_title
        f_abs_dict["User Story"] = us
        f_abs_dict["Acceptance Criteria"] = acceptance_criteria
        f_abs_dict["Business Value"] = bussines_value
        f_abs_dict["Risks and Dependencies"] = r_and_dep
        f_abs_dict["Design and Technical Specifications"] = d_and_ts
        feature_abs_data.append(f_abs_dict)
    
    return feature_abs_data[0]

def parse_us_abstract(abs_us_text:str):
    task_pattern = r'Task (\d+):\s+(.+?)(?=\n\nTask|$)'
    sub_task_pattern = r'Sub Task (\d+\.\d+):\s+(.+?)(?=\n\nSub Task|$)'
    acceptance_criteria_pattern = r'Acceptance Criteria:(.+?)(?=\n\nDefinition of Done|$)'
    dod_pattern = r'Definition of Done \(DOD\):(.+?)(?=\n\nDefinition of Ready|$)'
    dor_pattern = r'Definition of Ready \(DOR\):(.+?)(?=\n\nTask|$)'

    # Extract tasks, sub-tasks, acceptance criteria, dod, and dor
    tasks = re.findall(task_pattern, abs_us_text, re.DOTALL)
    sub_tasks = re.findall(sub_task_pattern, abs_us_text, re.DOTALL)
    acceptance_criteria = re.findall(acceptance_criteria_pattern, abs_us_text, re.DOTALL)
    dod = re.findall(dod_pattern, abs_us_text, re.DOTALL)
    dor = re.findall(dor_pattern, abs_us_text, re.DOTALL)
    parsed_abs_us = {}

    # extracted sections
    #second check 
    if acceptance_criteria and 'Definition of Done' not  in acceptance_criteria[0].strip():
        parsed_abs_us["Acceptance Criteria"] = acceptance_criteria[0].strip()
        parsed_abs_us["Definition of Done (DOD)"] = dod[0].strip()
        parsed_abs_us["Definition of Ready (DOR)"] = dor[0].strip()
    else:
        ac_start = abs_us_text.find("Acceptance Criteria")
        dod_start = abs_us_text.find("Definition of Done (DOD)")
        dor_start = abs_us_text.find("Definition of Ready")
        task_start = abs_us_text.find("Task")
        parsed_abs_us["Acceptance Criteria"] = abs_us_text[ac_start:dod_start]
        parsed_abs_us["Definition of Done"] = abs_us_text[dod_start:dor_start]
        parsed_abs_us["Definition of Ready"] = abs_us_text[dor_start:task_start]
        
   
    task_text = abs_us_text[task_start:]

    # if "\r\n\r\n-" in task_text or "\n\n" in task_text:
    #     task_text=task_text.replace("\r\n\r\n-","\r\n")
    raw_tasks = re.split(r'\s*\r\n\s*\r\n', task_text)
    parsed_abs_us["Tasks"]= []
    for task in raw_tasks:
        task_dict = {}
        task_list = task.split("\r\n")
        if "Sub Task" in task_list[0]:
            continue
        task_dict["Title"]=  task_list[0]
        task_dict["Description"] = ''.join(task_list[1:]).strip()
        parsed_abs_us["Tasks"].append(task_dict)
    new_task_list = []
    for i in range(len(parsed_abs_us["Tasks"])):
        current_task = parsed_abs_us["Tasks"][i]

        if current_task['Description'] == '' or current_task['Description'] == ' ':
            if i + 1 < len(parsed_abs_us["Tasks"]):
                title_string = parsed_abs_us["Tasks"][i + 1]['Title']
                current_task['Description'] = title_string + parsed_abs_us["Tasks"][i + 1]['Description']
        else:
            new_task_list.append(current_task)

    if parsed_abs_us["Acceptance Criteria"]:
        if parsed_abs_us["Tasks"]:
            return parsed_abs_us
    else:
        raise Exception("Missing key in US_DICT")


def parse_selected_feature(text):
    title_pattern = r"Feature (\d+): (.+)"
    description_pattern = r"Description: (.+)"
    # Extracting title and description using regex
    title_match = re.match(title_pattern, text)
    description_match = re.search(description_pattern, text)

    # Extracted title and description
    title = title_match.group(2) if title_match else text
    description = description_match.group(1) if description_match else ""
    title = title.replace("\r",'')
    title = title.replace("\n",'')

    feature_dict = {}
    feature_dict["Title"] = title
    feature_dict["Description"] = description
    return feature_dict

def parse_selected_feature2(text):
    title_pattern = r"Feature (\d+):\s*(.+)"
    description_pattern = r"(?:(?:Description:)|(?:Feature \d+:))(.+?)(?=(?:Feature \d+:|$))"
    
    title_match = re.search(title_pattern, text)
    description_match = re.search(description_pattern, text, re.DOTALL)

    title = title_match.group(2).strip() if title_match else ""
    description = description_match.group(1).strip() if description_match else ""

    feature_dict = {}
    feature_dict["Title"] = title
    feature_dict["Description"] = description
    return feature_dict 


def replace_numbers_feature_userstory(original_string,feature=None,userstory=None):
    # Find all occurrences of 'Feature [number]'
    if feature==True:
        matches = re.findall(r'Feature (\d+):', original_string)

    # Check and replace if needed
        if matches:
            for index, match in enumerate(matches, start=1):
                if int(match) != index:
                    original_string = original_string.replace(f'Feature {match}:', f'Feature {index}:')
    
    if userstory==True:
        matches = re.findall(r'User Story (\d+):', original_string)

    # Check and replace if needed
        if matches:
            for index, match in enumerate(matches, start=1):
                if int(match) != index:
                    original_string = original_string.replace(f'User Story {match}:', f'User Story {index}:')

    return original_string    

def parse_us_abstract2(text):
    acceptance_criteria = re.search(r'Acceptance Criteria:(.*?)Task 1:', text, re.DOTALL).group(1).strip()
    definition_of_done_present = re.search(r'Definition of Done \(DOD\):', text)
    definition_of_ready_present = re.search(r'Definition of Ready \(DOR\):', text)
    if definition_of_done_present:
        acceptance_criteria = re.search(r'Acceptance Criteria:(.*?)Definition of Done \(DOD\):', text, re.DOTALL).group(1).strip()
        definition_of_done = re.search(r'Definition of Done \(DOD\):(.*?)Definition of Ready \(DOR\):', text, re.DOTALL).group(1).strip()
    if definition_of_ready_present:
        definition_of_ready = re.search(r'Definition of Ready \(DOR\):(.*?)Task 1:', text, re.DOTALL).group(1).strip()
    
    new_text = text.rstrip() + '\n' if not text.endswith('\n') else text
    tasks = re.findall(r'Task \d+:(?:.*?)\n(?=Task \d+|\Z)', new_text, re.DOTALL)

    us_dict = {}
    us_dict["Acceptance Criteria"] = acceptance_criteria
    if definition_of_done_present:
        us_dict["Definition of Done"] = definition_of_done
    if definition_of_ready_present:
        us_dict["Definition of Ready"] = definition_of_ready
    us_dict["Tasks"] = []
    for task in tasks:
        task_dict = {}
        task_list = task.split("\n")
        if "Sub Task" in task_list[0]:
            continue
        task_dict["Title"]=  task_list[0]
        task_dict["Description"] = ''.join(task_list[1:]).strip()
        us_dict["Tasks"].append(task_dict)
    
    if us_dict["Acceptance Criteria"]:
        if us_dict["Tasks"]:
            return us_dict
    else:
        raise Exception("Missing key in US_DICT parser2")

def parse_us_abstract4(text):

    acceptance_criteria = re.search(r'Acceptance Criteria:(.*?)Definition of Done \(DOD\):', text, re.DOTALL).group(1).strip()
    definition_of_done = re.search(r'Definition of Done \(DOD\):(.*?)Definition of Ready \(DOR\):', text, re.DOTALL).group(1).strip()
    definition_of_ready = re.search(r'Definition of Ready \(DOR\):(.*?)Task 1:', text, re.DOTALL).group(1).strip()
    tasks = re.findall(r'Task \d+:(.*?)\n(?=Task \d+|\Z)', text, re.DOTALL)

    us_dict = {}
    us_dict["Acceptance Criteria"] = acceptance_criteria
    us_dict["Definition of Done"] = definition_of_done
    us_dict["Definition of Ready"] = definition_of_ready
    us_dict["Tasks"] = []
    for task in tasks:
        task_dict = {}
        if '\n\n' in task:
          task=task.replace('\n\n','\n')
        task_list = task.split("\n")
        task_dict["Title"]=  task_list[0]
        task_dict["Description"] = ''.join(task_list[1:]).strip()
        us_dict["Tasks"].append(task_dict)
    
    for item in us_dict['Tasks']:
      if item['Title'].strip() == "":
        task_split_d = item['Description'].split(':')[0]
        task_number=task_split_d.strip().split(' ')[-1].split(".")[0]

        item['Title'] = f'TASK {task_number}'

    for item in us_dict['Tasks']:
      if '\r' in item['Title'] or '\n'in item['Title']:
        item['Title'] = item['Title'].replace('\n', '').replace('\r', '')
    
    return us_dict


def parser_us_abstract3(abs_us_text):
    us_dict = {}
    ac_start = abs_us_text.find("Acceptance Criteria")
    dod_start = abs_us_text.find("Definition of Done (DOD)")
    dor_start = abs_us_text.find("Definition of Ready")
    task_start = abs_us_text.find("Task")
    us_dict["Acceptance Criteria"] = abs_us_text[ac_start:dod_start]
    us_dict["Definition of Done"] = abs_us_text[dod_start:dor_start]
    us_dict["Definition of Ready"] = abs_us_text[dor_start:task_start]
    us_dict["Tasks"] = []
    task_text = abs_us_text[task_start:]
    raw_tasks = re.split(r'\s*\r\n\s*\r\n', task_text)
    us_dict["Tasks"]= []
    for task in raw_tasks:
        task_dict = {}
        task_list = task.split("\r\n")
        if "Sub Task" in task_list[0]:
            continue
        task_dict["Title"]=  task_list[0]
        task_dict["Description"] = ''.join(task_list[1:]).strip()
        us_dict["Tasks"].append(task_dict)

    if us_dict["Acceptance Criteria"]:
        if us_dict["Tasks"]:
            return us_dict
    else:
        raise Exception("Missing key in US_DICT parser3")


def parse_userstory_abstract(text):
    us_dict = {}
    parser_methods = [parse_us_abstract2,parser_us_abstract3,parse_us_abstract4,parse_us_abstract]
    for parser_method in parser_methods:
        try:
            us_dict = parser_method(text)
            #if Note in task then remove it.
            if 'Note:' in us_dict['Tasks'][-1]['Title'] or 'Note :' in us_dict['Tasks'][-1]['Title']:
                us_dict['Tasks']=us_dict['Tasks'][:-1]
            #if Note in task then remove it.
            
            return us_dict
        except Exception as e:
            print(text)
            print(":::::::::::::::::::::::::::::")
            tb = traceback.format_exc().split("\n")
            print(str(e) + str(tb))
            continue
    
    return us_dict

def parse_sytem_testing1(text):
    matches = re.search(r'\nSelenium Test Scripts:(.+)', text, re.DOTALL)
    parsed_abs_test = {}
    if matches:
        try:
            system_test_abstract = matches.group(1).strip()
            matches1 = re.findall(r'Test Script \d+.\s+(.*?)(?=\nTest Script \d|\Z)', system_test_abstract, re.DOTALL)        
            parsed_abs_test["Tests"]= []
            for match in matches1:
                match = re.sub(r'User Story \d:', 'User Story -', match)
                systest_dict = {}
                task_list = match.split(":\r\n")
                systest_dict["Title"] = task_list[0]
                systest_dict["Description"] = task_list[1]
                parsed_abs_test["Tests"].append(systest_dict)
        except Exception as e:
            parsed_abs_test = {}
            print(text)
            print(":::::::::::::::::::::::::::::")
            tb = traceback.format_exc().split("\n")
            print(str(e) + str(tb))
    return parsed_abs_test

def parse_sytem_testing(text):
    matches = re.search(r'\nSelenium Test Scripts:(.+)', text, re.DOTALL)
    parsed_abs_test = {}
    if matches:
        try:
            system_test_abstract = matches.group(1).strip()
            matches1 = re.findall(r'Test Script \d+.\s+(.*?)(?=\nTest Script \d|\Z)', system_test_abstract, re.DOTALL)        
            parsed_abs_test["Tests"]= []
            for match in matches1:
                match_list = match.split('\n')
                description = ""
                title = ""
                title_end = False
                for sentence in match_list:
                    if title != '' and ("- " in sentence.strip() or re.match(r'\d.', sentence.strip()) or sentence == "\r"):
                        title_end = True
                        description = description + "\n" + sentence.strip()
                    elif title_end:
                        break
                    else:
                        title = title + sentence.strip()
                systest_dict = {}
                if title:
                    title = title.replace('.:', '.')
                    title = title.replace(':', '-')
                    pattern = re.compile('[/:\'"?<>|*%]')
                    title = re.sub(pattern, '', title)
                    title = title.replace('\\', '')
                    systest_dict["Title"] = title
                systest_dict["Description"] = description
                parsed_abs_test["Tests"].append(systest_dict)
        except Exception as e:
            parsed_abs_test = {}
            print(text)
            print(":::::::::::::::::::::::::::::")
            tb = traceback.format_exc().split("\n")
            print(str(e) + str(tb))
    return parsed_abs_test

def system_testing_parsers(text):
    sys_dict = {}
    parser_methods = [parse_sytem_testing,parse_sytem_testing1]
    for parser_method in parser_methods:
        try:
            sys_dict = parser_method(text)
            if sys_dict["Tests"]:
                if sys_dict["Tests"][0]["Title"] and sys_dict["Tests"][0]["Description"]:
                    return sys_dict
                elif sys_dict["Tests"][0]["Title"] != "" and sys_dict["Tests"][0]["Description"] != "":
                    return sys_dict
                else:
                    continue
            else:
                raise Exception
        except Exception as e:
            print(text)
            print(":::::::::::::::::::::::::::::")
            tb = traceback.format_exc().split("\n")
            print(str(e) + str(tb))
            continue
    
    return sys_dict


def parse_component_diagram_method1(mermaid_text):
    # Define the regex pattern to extract the mermaid code
    mermaid_pattern = re.compile(r"(classDiagram[\s\S]*?)(?:\n\n|\Z)")
    # Extract the mermaid code using the regex pattern
    match = mermaid_pattern.search(mermaid_text)
    if match:
        cleaned_mermaid_code = match.group(1)
        return cleaned_mermaid_code
    else:
        return None

def parse_component_diagram_method2(mermaid_text):
    # Define the regex pattern using a non-greedy match
    mermaid_pattern_non_greedy = re.compile(r"(classDiagram[\s\S]*?)(?:\n\n|\Z)")
    # Extract the mermaid code using the non-greedy match regex pattern
    match_non_greedy = mermaid_pattern_non_greedy.search(mermaid_text)
    if match_non_greedy:
        cleaned_mermaid_code = match_non_greedy.group(1)
        return cleaned_mermaid_code
    else:
       return None
    

def parse_component_diagram_method3(mermaid_text):
    # Define the regex pattern using a positive lookahead
    mermaid_pattern_lookahead = re.compile(r"(classDiagram[\s\S]*?)(?=\n\n|\Z)")
    # Extract the mermaid code using the positive lookahead regex pattern
    match_lookahead = mermaid_pattern_lookahead.search(mermaid_text)
    if match_lookahead:
        cleaned_mermaid_code = match_lookahead.group(1)
        return cleaned_mermaid_code
    else:
        None

def parse_component_diagram(comp_diagram):
    mermaid_text = comp_diagram.strip()
    # Define the regex pattern to extract the mermaid code to capture everything in between classDiagram and Note: if present
    mermaid_pattern = re.compile(r"(classDiagram[\s\S]*?)(?:Note:|$)")
    match = mermaid_pattern.search(mermaid_text)
    if match:
        cleaned_mermaid_code = match.group(1)
        
        if cleaned_mermaid_code:
            component_diagram=cleaned_mermaid_code.replace("Component Diagram: ","")
            component_diagram = component_diagram.replace("<|..","$%")
            component_diagram=component_diagram.replace(".","")
            component_diagram=component_diagram.replace("$%","<|..")
            return component_diagram
        else:
            return comp_diagram
    else:
        return comp_diagram
