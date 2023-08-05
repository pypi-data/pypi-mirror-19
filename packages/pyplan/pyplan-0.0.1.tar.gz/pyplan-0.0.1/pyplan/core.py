import pandas as pd
import helpers as h


class BenefitCost(object):
    """
    object to process raw benefit cost data of a suite of progressive, combinable
    capital improvement alternatives.
    """
    def __init__(self, datafile, id_col=None, benefit_col=None, cost_col=None):

        #read datafile and store in dataframe with a benefit/cost column
        raw = pd.read_csv(datafile)

        self.raw_data = raw

        #if user does not pass in column headers, assume the raw file has
        #columns = project_ID, benefits, costs
        self.id_col = filter(None, [id_col, raw.columns[0]])[0]
        self.benefit_col = filter(None, [benefit_col, raw.columns[1]])[0]
        self.cost_col = filter(None, [cost_col, raw.columns[2]])[0]
        self.project_codes = h.identify_project_codes(raw[self.id_col].tolist())
        self.raw_data.loc[:,'benefit_cost'] = raw[self.benefit_col] / raw[self.cost_col]

    def most_efficient_sequence(self, start_sequence = None):
        """
        given the cost / benefit summary data of segment combination models,
        return a dataframe with each option in sequence of most efficient
        projects. This method prioritizes max efficiency at each implementation
        phase.

        optionally passing in a start_sequence forces the sequence to begin at
        that point. start_sequence is a list.
        """

        #grab the relevant dataframe column names and raw data
        benefits = self.benefit_col
        costs = self.cost_col
        ids = self.id_col
        pcodes = self.project_codes
        data = self.raw_data

        #empty df to hold the implemenation sequence
        data.loc[:,'incr_benefit_cost'] = data[benefits] / data[costs]
        sequence = pd.DataFrame(columns=data.columns)

        #set the initial incremental values
        data.loc[:,'incr_benefit'] = data[benefits]
        data.loc[:,'incr_cost'] = data[benefits]

        if start_sequence is None:
            #no starting point hard set, find the best overall starting point
            #first grab the index where incr_benefit_cost is max
            firsties = h.identify_possible_next_ops(project_codes=pcodes)
            firsties_df = data[data[ids].isin(firsties)]
            imax = firsties_df['incr_benefit_cost'].idxmax()
            best_nxt = firsties_df.ix[imax:imax] #look up single row df (so its not a series)
            sequence = sequence.append(best_nxt)

        else:
            #single row df of last (or only) item passed in
            best_nxt = data[data[ids] == start_sequence[-1]]

            #this copies the orginal data and changes the Option_ID column
            #to a Category type to allow sorting by Option_ID. This allows the
            #user's order of start_sequence to be honored in the resulting df
            df = data[:]
            sorter = start_sequence
            df[ids] = df[ids].astype("category")
            df[ids].cat.set_categories(sorter, inplace=True)
            df = df.loc[df[ids].isin(sorter)].sort_values([ids])
            df['incr_cost'] = df[costs].diff().fillna(df[costs])
            df['incr_benefit'] = df[benefits].diff().fillna(df[benefits])
            df['incr_benefit_cost'] = df.incr_benefit / df.incr_cost
            sequence = sequence.append(df)

        #get a df of all possible (logically) next options
        nxt_ids = h.identify_possible_next_ops(best_nxt[ids].values[0], pcodes)
        nxt_df = data[data[ids].isin(nxt_ids)]

        while len(nxt_df) > 0:

            #calculate the incremental cost/benefit data for each possible next
            #implementation level
            nxt_df.loc[:,'incr_cost'] = nxt_df.apply(lambda row:
                                                     row[costs] -
                                                     best_nxt.squeeze()[costs],
                                                     axis=1)
            nxt_df.loc[:,'incr_benefit'] = nxt_df.apply(lambda row:
                                                        row[benefits] -
                                                        best_nxt.squeeze()[benefits],
                                                        axis=1)
            nxt_df.loc[:,'incr_benefit_cost'] = nxt_df.incr_benefit / nxt_df.incr_cost

            #find the next implementation level with the highest benefit cost ratio
            #with respect to the current state of implementation. append to sequence
            best_nxt = nxt_df.ix[nxt_df['incr_benefit_cost'].idxmax()]
            sequence = sequence.append(best_nxt, ignore_index=True)

            #create a new dataframe with the possible next implementation levels
            nxt_ids = h.identify_possible_next_ops(best_nxt[ids], pcodes)
            nxt_df = data[data[ids].isin(nxt_ids)]

            #loop this process to build the sequence until no next options exist

        def make_label(row):

            projid = '{}'.format(row[ids])
            newbenes = '${}M for {} parcels'.format(round(row['incr_cost'],1),
                                                         int(row['incr_benefit']))

            eff = '({} parcels/$M)'.format(int(row.incr_benefit_cost))

            # eff = row.incr_benefit_cost
            # return "{}<br>({} parcels/$M)".format(row[ids], round(eff,1))
            return '<br>'.join([projid, newbenes, eff])

        sequence.loc[:,'label'] = sequence.apply(lambda row: make_label(row), axis=1)

        #rearrange columns back with id col first (not sure why we need to)
        scol = sequence.columns.tolist()
        scol.insert(0, scol.pop(scol.index(ids)))

        return sequence[scol]


class Sequence(BenefitCost):

    def __init__(self, datafile, name=None, id_col=None, benefit_col=None,
                 cost_col=None, start_sequence = None):

        BenefitCost.__init__(self, datafile, id_col, benefit_col, cost_col)

        self.name = name
        self.data = self.most_efficient_sequence(start_sequence)
