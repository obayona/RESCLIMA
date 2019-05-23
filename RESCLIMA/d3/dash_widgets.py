from django.template.loader import render_to_string
from django.conf import settings

from dash.base import BaseDashboardPluginWidget

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

# *************************************************************
# ***************** Base chart widget *************************
# *************************************************************


class BaseChartWidget(BaseDashboardPluginWidget):
    """Base chart widget."""

    _template = None

    def render(self, request=None):
        """Render."""
        context = {
            'plugin': self.plugin,
            'width': self.get_width(),
            'height': self.get_height(),
            'STATIC_URL': settings.STATIC_URL,
        }
        return render_to_string(
            self._template,
            context
        )


class BaseBarChartWidget(BaseChartWidget):
    """Base bar chart widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/plotly-latest.min.js', #plotly new Script
        'js/util.js',
        'js/plotly_bar_chart.js',
    )

    media_css = (
        'css/d3_bar_chart.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_bar_chart.html'

class BaseGroupedBarChartWidget(BaseChartWidget):
    """Base bar chart widget."""

    media_js = (
        'js/plotly-latest.min.js', #plotly new Script
        'js/util.js',
        'js/plotly_grouped_bar_chart.js',
        'js/interactiveRedirecting.js',
    )

    media_css = (
        'css/d3_grouped_bar_chart.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_grouped_bar_chart.html'

class BaseTimeSeriesWidget(BaseChartWidget):
    """Base time series widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3.queue.min.js', # D3 Queue
        'js/plotly-latest.min.js', #plotly new Script
        'js/util.js',
        'js/plotly_time_series.js',    
    )

    media_css = (
        'css/d3_time_series.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_time_series.html'

class BaseMultiTimeSeriesWidget(BaseChartWidget):
    """Base multi time series widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3.queue.min.js', # D3 Queue
        'js/plotly-latest.min.js', #plotly new Script
        'js/util.js',
        'js/plotly_multi_time_series.js',
    )

    media_css = (
        'css/d3_multi_time_series.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_multi_time_series.html'

class BasePieChartWidget(BaseChartWidget):
    """Pie chart widget."""

    media_js = (
        'js/plotly-latest.min.js', #plotly new Script
        'js/util.js',
        'js/plotly_pie_chart.js',
        'js/treemap-squared-0.5.min.js',
    )

    media_css = (
        #'css/d3_pie_chart.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_pie_chart.html'

class BaseLineChartWidget(BaseChartWidget):
    """Line chart widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3.queue.min.js', # D3 Queue
        'js/plotly-latest.min.js', #plotly new Script
        'js/util.js',
        'js/plotly_line_chart.js',
        'js/interactiveRedirecting.js',
    )

    media_css = (
        #'css/d3_line_chart.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_line_chart.html'

class BaseTreeMapWidget(BaseChartWidget):
    """Tree Map Widget"""

    media_js = (
        'js/plotly-latest.min.js', #plotly new Script
        'js/util.js',
        'js/plotly_tree_map.js',  # Helper script
        'js/treemap-squared-0.5.min.js',
    )

    media_css = (
        'css/d3_tree_map.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_tree_map.html'

class BaseBubbleChart(BaseChartWidget):
    """Bubble Chart Widget"""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/plotly-latest.min.js', #plotly new Script
        'js/plotly_bubble_chart.js' #Helper script

    )
