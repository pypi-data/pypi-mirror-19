"""
helper functions
"""

def identify_project_codes(project_ids):
    """
    given a list of project ids, determine the unique project codes.
    Unique project codes should exist for each independent (combinable) project
    track.

    Project IDs should follow this covention:
        [code][implementation level]_[other project code][implementation level]_...


    For example, consider a scneario where projects are being considered along
    Street A and Street B that may or may not be implemented in combination.
    Projects on Street A can be implemented at 2 sequential levels of investment
    and projects on Street B can be implemented at 1 level of investment.
    The following project IDs will be identified:
        Project IDs = ['A01', 'A02', 'B01', 'A01_B01', 'A02_B01']

    here, the unique project "codes" are "A" and "B".

    """

    unique_pcodes = []
    for pid in project_ids:

        for code_lvl in pid.split('_'):
            #remove implementation level number from project id
            code = filter(str.isalpha, code_lvl)
            unique_pcodes.append(code)

    return list(set(unique_pcodes))

def identify_possible_next_ops(project_id=None, project_codes=None):

    """
    given a project_id, return a list of possible next project implementations.
        alt = alternative, the major category of an SFR solution. AKA a
        "segment category"

        degree = the level of implementation of the alternative. E.g.
        3rd implementation scenario of Mifflin alternative

    requires that the alternative ID "buckets" are sorted alphabetically in each
    alternative ID.
    """

    #e.g. {'M':0, 'R':0, 'W':0}
    alt_buckets = {x:0 for x in project_codes}

    if project_id is None:
        #first implementation level of each independent capital project
        firsties = ['{}{}'.format(k, str(v+1).zfill(2))
                    for k, v in alt_buckets.iteritems()]
        return sorted(firsties)

    #first, find the projects that are currently not implemented at all
    possibles = []
    possibles += [{x:1} for x in alt_buckets.keys() if x not in filter(str.isalpha, project_id)]

    #iterate through option id's components
    for op in project_id.split('_'):

        #parse the passed in option into its buckets
        alt_name = filter(str.isalpha, op)
        alt_degree = int(filter(str.isdigit, op))
        alt_buckets.update({alt_name:alt_degree})

        #increment the project_id
        nxt_degree = alt_degree + 1
        next_op = {alt_name:nxt_degree}
        possibles.append(next_op)


    results = [] # output list of potential next implementation scenarios
    for p in possibles:
        # "deep copy" the buckets dict
        d = {k:v for k,v in alt_buckets.items()} #{'M':1, 'R':1, 'W':0}
        d.update(p)

        #remove any genres with zero implementation
        d2 = { k:v for k, v in d.items() if v != 0 }

        #convert to id format, sort alphebetically
        string_alts = ['{}{}'.format(key, str(val).zfill(2)) for key, val in d2.iteritems()]
        reformatted_op = '_'.join(sorted(string_alts))
        results.append(reformatted_op)

    return results
