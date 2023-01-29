from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
import pandas as pd
import plotly.graph_objects as go


# Domain
from ..models       import Item
from ..forms        import ItemForm, InteractionForm
from ..domain       import DomainContext
from ..recommender  import RecommenderContext, RecommenderCapability


from plotly.offline import plot
import plotly.express as px

ctx = DomainContext()


@login_required
def show_metrics(request):

    user_ndcg        = ctx.evaluation_service.find_metric_by_active_and_user(request.user)
    user_ndcg_values = ctx.evaluation_service.find_metric_values_by_active_and_user(request.user)

    all_users_ndgc        = ctx.evaluation_service.find_metric_by_active()
    all_users_ndgc_values = ctx.evaluation_service.find_metric_values_by_active()
    user_votes_df = ctx.evaluation_service.user_votes_by_active()

    user_ndcg_timeline_plot, user_ndcg_hist_plot = user_plots(user_ndcg_values)
    all_users_ndgc_timeline_plot, all_user_ndcg_hist_plot, user_votes_plot = all_users_plots(all_users_ndgc_values, user_votes_df)

    response = {
        'user_ndcg'                 : round(user_ndcg, 3) if user_ndcg else None,
        'user_ndcg_timeline'        : user_ndcg_timeline_plot,
        'user_ndcg_hist'            : user_ndcg_hist_plot,

        'all_users_ndgc'            : round(all_users_ndgc, 3) if all_users_ndgc else None,
        'all_users_ndgc_timeline'   : all_users_ndgc_timeline_plot,
        'all_users_ndcg_hist'       : all_user_ndcg_hist_plot,
        'user_n_interactions'       : ctx.interaction_service.count_by_user(request.user),

        'user_votes_table'          : user_votes_plot
    }

    return render(request, 'single/metrics.html', response)



def user_plots(df):
    if df.empty:
        return None, None
    else:
        df.rename(columns={'value': 'NDCG'}, inplace=True)
        df['Step'] = df.index
        df = df.round({'NDCG': 3})


        timeline_fig = px.line(
            df,
            x='Step',
            y='NDCG',
            markers=True,
            title='Timeline: NDCG by vote step.'
        )
        timeline_fig = plot(timeline_fig, output_type='div')

        hist_fig = px.histogram(
            df,
            x='NDCG',
            nbins=2,
            title='Histogram: Vote steps by NDCG.'
        )
        hist_fig = plot(hist_fig, output_type='div')

        return timeline_fig, hist_fig



def all_users_plots(df, user_votes_df):
    if df.empty:
        return None, None, None
    else:
        df = df \
            .groupby([df['datetime'].dt.minute], as_index=False) \
            .value \
            .mean() \
            .reset_index(names='datetime')

        df = df.rename(columns={'datetime': 'Minutes'})


        timeline_fig = px.line(
            df,
            x='Minutes',
            y='value',
            markers=True,
            title='Timeline: Mean NDCG by minute.',
            labels={
                'value': 'NDCG',
            }
        )
        timeline_fig = plot(timeline_fig, output_type='div')

        hist_fig = px.histogram(
            df,
            x='value',
            nbins=3,
            title='Histogram: Vote steps by NDCG.',
            labels={
                'value': 'NDCG'
            }
        )
        hist_fig = plot(hist_fig, output_type='div')

        user_votes_df = user_votes_df \
            .rename(columns={'user__username': 'User', 'total': 'Vote Steps'})\
            .sort_values(['Vote Steps'], ascending=False)

        user_votes_fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(user_votes_df.columns),
                        fill_color='paleturquoise',
                        align='left',
                        font_size=18,
                        height=35
                    ),
                    cells=dict(
                        values=user_votes_df.transpose().values.tolist(),
                        fill_color='lavender',
                        align='left',
                        font_size=18,
                        height=35
                    )
                )
            ]
        )
        user_votes_fig = plot(user_votes_fig, output_type='div')

        return timeline_fig, hist_fig, user_votes_fig