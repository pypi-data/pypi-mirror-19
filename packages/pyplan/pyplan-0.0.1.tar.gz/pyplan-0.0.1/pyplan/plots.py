import plotly.graph_objs as go
import numpy as np



def create_scatter_trace(data, name, mode = 'lines+markers',
                         lineshape = 'hv', marker_shp='circle',
                         width=2, show=True, benefit_col='Eliminated',
                         text=None):
    """
    create a Plotly scatter trace object with benefit data.

    data = Pandas dataframe holding the following columns:
        Option_ID = id of the SFR scenario
        Cost = cost of implementation
        Improved = count of parcels with flood risk reduced
        incr_benefit_cost = incremental ratio of benefit/cost

    """
    # #calculate dot size
    # marker_size = np.sqrt(data.incr_benefit_cost)
    b = data.Option_ID.tolist()
    if 'incr_benefit_cost' in data.columns:
        a = data.incr_benefit_cost.tolist()
        text = data.label.tolist()
    else:
        df = data[:]
        df['incr_benefit_cost'] = (df[benefit_col] / df.Cost).round()
        a = df.incr_benefit_cost.tolist()

        text = ["{}<br>({} parcels/$M)".format(b_, int(a_)) for a_, b_ in zip(a, b)]

    #create a Plotly scatter graph object
    scatter = go.Scatter(
                x = data.Cost.tolist(),
                y = data[benefit_col].tolist(),
                name = name,
                mode = mode,
                text= text,#data.Option_ID.tolist(),
                line = {'shape':lineshape, 'width':width},
                marker=dict(
                    # size=marker_size,
                    symbol=marker_shp,
                ),
                visible = show,
            )
    return scatter

def implementation_sequences(all_options, sequences, title, benefit_col='Eliminated'):
    """
    generate Plotly figure object representing all options as a scatter with
    each sequence plotted as line.
    """

    #create the Plotly chart layout object
    layout = go.Layout(
        hovermode='closest',
        plot_bgcolor='E5E5E5',
        title=title,
        legend = {'x':0.05, 'y':0.9},
        xaxis = dict(title='Capital Cost (Millions)',tickprefix='$'),
        yaxis = dict(title='Parcels with Flood Risk {}'.format(benefit_col)),
        # height = 700,
    )

    #generate the all options scatter Graph Object (go)
    all_ops_go = create_scatter_trace(all_options,'All Projects', mode='markers',
                                      marker_shp='circle-open',
                                      benefit_col=benefit_col)

    #generate the other scatter graph objects with the dataframes passed in
    sequences_gos = [create_scatter_trace(s.data, s.name, benefit_col = s.benefit_col)
                     for s in sequences]

    #construct the Plotly figure object
    fig_data = [all_ops_go] + sequences_gos
    figure = go.Figure(data=fig_data, layout=layout)

    return figure
