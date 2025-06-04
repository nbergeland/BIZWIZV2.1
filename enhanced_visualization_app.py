# === ENHANCED MULTI-CITY VISUALIZATION APP ===
# Save this as: enhanced_visualization_app.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pickle
import os
import json
from datetime import datetime
from city_config import CityConfigManager

# === ENHANCED DATA LOADER ===
class EnhancedDataLoader:
    """Enhanced data loader that handles multiple cities"""
    
    def __init__(self):
        self.city_manager = CityConfigManager()
        self.current_data = None
        self.current_city_id = None
        
    def load_city_data(self, city_id: str):
        """Load data for a specific city"""
        if city_id == self.current_city_id and self.current_data:
            return self.current_data
            
        cache_dir = f"cache_{city_id}"
        processed_data_file = os.path.join(cache_dir, 'processed_location_data.pkl')
        
        if not os.path.exists(processed_data_file):
            print(f"No processed data found for {city_id}")
            return None
            
        try:
            with open(processed_data_file, 'rb') as f:
                data = pickle.load(f)
            
            self.current_data = data
            self.current_city_id = city_id
            print(f"Loaded data for {city_id}: {len(data['df_filtered'])} locations")
            return data
            
        except Exception as e:
            print(f"Error loading data for {city_id}: {e}")
            return None
    
    def get_available_cities(self):
        """Get list of cities with available data"""
        available = []
        for city_id in self.city_manager.list_cities():
            cache_dir = f"cache_{city_id}"
            processed_data_file = os.path.join(cache_dir, 'processed_location_data.pkl')
            if os.path.exists(processed_data_file):
                config = self.city_manager.get_config(city_id)
                available.append({
                    'city_id': city_id,
                    'display_name': config.display_name,
                    'file_path': processed_data_file
                })
        return available

# Initialize data loader
data_loader = EnhancedDataLoader()
available_cities = data_loader.get_available_cities()

if not available_cities:
    print("No processed data found for any cities!")
    print("Please run enhanced_data_collection.py first")
    exit(1)

# Load initial city data
initial_city = available_cities[0]['city_id']
current_data = data_loader.load_city_data(initial_city)

if not current_data:
    print("Failed to load initial city data")
    exit(1)

# === DASH APP ===
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# === APP LAYOUT ===
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🍗 Enhanced Raising Cane's Location Analysis", className="text-center mb-3"),
            html.P("Multi-City Commercial Location Intelligence System", 
                   className="text-center text-muted mb-4")
        ])
    ]),
    
    # City Selection and Metrics Row
    dbc.Row([
        dbc.Col([
            html.Label("Select City:", className="fw-bold"),
            dcc.Dropdown(
                id='city-dropdown',
                options=[
                    {'label': city['display_name'], 'value': city['city_id']} 
                    for city in available_cities
                ],
                value=initial_city,
                clearable=False
            )
        ], width=4),
        
        dbc.Col([
            html.Div(id='city-metrics', className="text-center")
        ], width=8)
    ], className="mb-4"),
    
    # Main content
    dbc.Row([
        # Filters Column
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🎯 Analysis Filters", className="mb-0")),
                dbc.CardBody([
                    html.Label("Minimum Predicted Revenue:", className="fw-bold"),
                    dcc.Slider(
                        id='revenue-slider', 
                        min=0, 
                        max=100000,  # Will be updated dynamically
                        step=1000, 
                        value=50000,
                        tooltip={"placement": "bottom", "always_visible": True},
                        marks={}
                    ),
                    html.Br(),
                    
                    html.Label("Maximum Distance to Primary Competitor (miles):", className="fw-bold"),
                    dcc.Slider(
                        id='competitor-distance-slider', 
                        min=0, 
                        max=15, 
                        step=1, 
                        value=8,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    html.Label("Minimum Commercial Traffic Score:", className="fw-bold"),
                    dcc.Slider(
                        id='commercial-traffic-slider', 
                        min=0, 
                        max=200,  # Will be updated dynamically
                        step=10, 
                        value=20,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    html.Label("Maximum Fast Food Competition:", className="fw-bold"),
                    dcc.Slider(
                        id='competition-slider', 
                        min=0, 
                        max=15, 
                        step=1, 
                        value=8,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    html.Label("Zoning Compliance:", className="fw-bold"),
                    dcc.RadioItems(
                        id='zoning-radio', 
                        options=[
                            {'label': 'All Locations', 'value': 'all'}, 
                            {'label': 'Only Compliant', 'value': 'compliant'}
                        ], 
                        value='compliant',
                        className="mb-3"
                    ),
                    
                    html.Label("Minimum Model Score (R²):", className="fw-bold"),
                    html.Div(id='model-score-display', className="text-muted mb-3"),
                    
                    html.Hr(),
                    html.Div(id='location-stats', className="mt-3")
                ])
            ])
        ], width=3),
        
        # Map and Analysis Column
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="📍 Location Map", tab_id="map-tab"),
                dbc.Tab(label="📊 Analytics Dashboard", tab_id="analytics-tab"),
                dbc.Tab(label="🏆 Top Locations", tab_id="top-locations-tab"),
                dbc.Tab(label="🔬 Model Performance", tab_id="model-tab")
            ], id="main-tabs", active_tab="map-tab"),
            
            html.Div(id='tab-content', style={'height': '85vh'})
        ], width=9)
    ])
], fluid=True)

# === CALLBACK FUNCTIONS ===

@app.callback(
    [Output('revenue-slider', 'max'),
     Output('revenue-slider', 'value'),
     Output('revenue-slider', 'marks'),
     Output('commercial-traffic-slider', 'max'),
     Output('city-metrics', 'children'),
     Output('model-score-display', 'children')],
    [Input('city-dropdown', 'value')]
)
def update_city_data(city_id):
    """Update all components when city changes"""
    data = data_loader.load_city_data(city_id)
    
    if not data:
        return 100000, 50000, {}, 200, "No data available", "No model data"
    
    df = data['df_filtered']
    metrics = data.get('metrics', {})
    city_config = data.get('city_config')
    
    # Update slider ranges
    max_revenue = int(df['predicted_revenue'].max())
    revenue_marks = {
        0: '0',
        max_revenue//4: f'{max_revenue//4:,}',
        max_revenue//2: f'{max_revenue//2:,}',
        3*max_revenue//4: f'{3*max_revenue//4:,}',
        max_revenue: f'{max_revenue:,}'
    }
    
    max_commercial = int(df['commercial_traffic_score'].max())
    initial_revenue = int(df['predicted_revenue'].quantile(0.6))
    
    # City metrics
    city_name = city_config.display_name if city_config else city_id
    city_metrics = dbc.Row([
        dbc.Col([
            html.H6("📍 Locations Analyzed", className="text-muted mb-1"),
            html.H4(f"{len(df):,}", className="text-primary mb-0")
        ], width=2),
        dbc.Col([
            html.H6("💰 Avg Revenue Potential", className="text-muted mb-1"),
            html.H4(f"${df['predicted_revenue'].mean():,.0f}", className="text-success mb-0")
        ], width=3),
        dbc.Col([
            html.H6("🏆 Top Location Revenue", className="text-muted mb-1"),
            html.H4(f"${df['predicted_revenue'].max():,.0f}", className="text-warning mb-0")
        ], width=3),
        dbc.Col([
            html.H6("🎯 Competitors Mapped", className="text-muted mb-1"),
            html.H4(f"{len(data.get('chickfila_locations', []))}", className="text-info mb-0")
        ], width=2),
        dbc.Col([
            html.H6("🍗 Existing Cane's", className="text-muted mb-1"),
            html.H4(f"{len(data.get('raising_canes_locations', []))}", className="text-danger mb-0")
        ], width=2)
    ])
    
    # Model performance
    if metrics:
        model_score = f"R² Score: {metrics.get('train_r2', 0):.3f} | CV MAE: ${metrics.get('cv_mae_mean', 0):,.0f}"
    else:
        model_score = "Model metrics not available"
    
    return max_revenue, initial_revenue, revenue_marks, max_commercial, city_metrics, model_score

@app.callback(
    Output('tab-content', 'children'),
    [Input('main-tabs', 'active_tab'),
     Input('city-dropdown', 'value'),
     Input('revenue-slider', 'value'), 
     Input('competitor-distance-slider', 'value'), 
     Input('commercial-traffic-slider', 'value'),
     Input('competition-slider', 'value'),
     Input('zoning-radio', 'value')]
)
def update_tab_content(active_tab, city_id, min_revenue, max_competitor_distance, 
                      min_commercial_traffic, max_competition, zoning_filter):
    """Update tab content based on active tab and filters"""
    
    data = data_loader.load_city_data(city_id)
    if not data:
        return html.Div("No data available for selected city")
    
    df = data['df_filtered']
    
    # Apply filters
    filtered = df[
        (df['predicted_revenue'] >= min_revenue) &
        (df['distance_to_chickfila'] <= max_competitor_distance) &
        (df['commercial_traffic_score'] >= min_commercial_traffic) &
        (df['fast_food_competition'] <= max_competition)
    ]
    
    if zoning_filter == 'compliant':
        filtered = filtered[filtered['zoning_compliant'] == 1]
    
    if active_tab == "map-tab":
        return create_map_tab(data, filtered)
    elif active_tab == "analytics-tab":
        return create_analytics_tab(data, filtered)
    elif active_tab == "top-locations-tab":
        return create_top_locations_tab(data, filtered)
    elif active_tab == "model-tab":
        return create_model_tab(data)
    
    return html.Div("Select a tab")

def create_map_tab(data, filtered):
    """Create the interactive map tab"""
    city_config = data.get('city_config')
    chickfila_locations = data.get('chickfila_locations', [])
    raising_canes_locations = data.get('raising_canes_locations', [])
    
    # Create base scatter plot for potential locations
    if len(filtered) > 0:
        fig = px.scatter_mapbox(
            filtered, 
            lat='latitude', 
            lon='longitude', 
            size='predicted_revenue', 
            color='predicted_revenue',
            color_continuous_scale='RdYlGn', 
            size_max=25, 
            zoom=12, 
            mapbox_style='carto-positron',
            hover_data={
                'commercial_traffic_score': True,
                'road_accessibility_score': True,
                'distance_to_chickfila': ':.1f',
                'predicted_revenue': ':$,.0f',
                'median_income': ':$,.0f',
                'population': ':,.0f'
            },
            title=f"Commercial Locations in {city_config.display_name if city_config else 'Selected City'}"
        )
        
        # Set map center
        if city_config:
            fig.update_layout(
                mapbox=dict(
                    center=dict(lat=city_config.bounds.center_lat, lon=city_config.bounds.center_lon)
                )
            )
    else:
        # Empty map if no locations match filters
        center_lat = city_config.bounds.center_lat if city_config else 47.9
        center_lon = city_config.bounds.center_lon if city_config else -97.075
        
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style='carto-positron',
                center=dict(lat=center_lat, lon=center_lon),
                zoom=12
            ),
            title="No locations match current filters"
        )
    
    # Add competitor locations
    if chickfila_locations and len(chickfila_locations) > 0:
        chickfila_df = pd.DataFrame(chickfila_locations, columns=['latitude', 'longitude'])
        competitor_name = city_config.competitor_data.primary_competitor.replace('-', ' ').title() if city_config else "Primary Competitor"
        
        fig.add_trace(
            go.Scattermapbox(
                lat=chickfila_df['latitude'],
                lon=chickfila_df['longitude'],
                mode='markers+text',
                marker=dict(size=20, color='red', symbol='circle'),
                text='🐔',
                textfont=dict(size=16),
                textposition='middle center',
                name=f"{competitor_name} Locations",
                hovertemplate=f"<b>{competitor_name}</b><br>" +
                             "Lat: %{lat:.4f}<br>" +
                             "Lon: %{lon:.4f}<br>" +
                             "<extra></extra>"
            )
        )
    
    # Add existing Raising Cane's locations
    if raising_canes_locations and len(raising_canes_locations) > 0:
        canes_df = pd.DataFrame(raising_canes_locations, columns=['latitude', 'longitude', 'name'])
        
        fig.add_trace(
            go.Scattermapbox(
                lat=canes_df['latitude'],
                lon=canes_df['longitude'],
                mode='markers+text',
                marker=dict(size=20, color='purple', symbol='circle'),
                text='🍗',
                textfont=dict(size=16),
                textposition='middle center',
                name="Existing Raising Cane's",
                hovertemplate="<b>Existing Raising Cane's</b><br>" +
                             "Location: %{customdata}<br>" +
                             "<extra></extra>",
                customdata=canes_df['name']
            )
        )
    
    fig.update_layout(
        height=700,
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)")
    )
    
    return dcc.Graph(figure=fig, style={'height': '80vh'})

def create_analytics_tab(data, filtered):
    """Create analytics dashboard with multiple charts"""
    if len(filtered) == 0:
        return html.Div("No data matches current filters", className="text-center mt-5")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue Distribution', 'Commercial Traffic vs Revenue', 
                       'Competition Analysis', 'Demographics Analysis'),
        specs=[[{"type": "histogram"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Revenue distribution histogram
    fig.add_trace(
        go.Histogram(x=filtered['predicted_revenue'], nbinsx=20, name="Revenue Distribution"),
        row=1, col=1
    )
    
    # Commercial traffic vs revenue scatter
    fig.add_trace(
        go.Scatter(
            x=filtered['commercial_traffic_score'],
            y=filtered['predicted_revenue'],
            mode='markers',
            name="Traffic vs Revenue",
            hovertemplate="Traffic: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>"
        ),
        row=1, col=2
    )
    
    # Competition analysis - group by competition level
    comp_analysis = filtered.groupby('fast_food_competition')['predicted_revenue'].agg(['mean', 'count']).reset_index()
    comp_analysis = comp_analysis[comp_analysis['count'] >= 5]  # Only show groups with 5+ locations
    
    fig.add_trace(
        go.Bar(
            x=comp_analysis['fast_food_competition'],
            y=comp_analysis['mean'],
            name="Avg Revenue by Competition",
            hovertemplate="Competition Level: %{x}<br>Avg Revenue: $%{y:,.0f}<extra></extra>"
        ),
        row=2, col=1
    )
    
    # Demographics - income vs age colored by revenue
    fig.add_trace(
        go.Scatter(
            x=filtered['median_age'],
            y=filtered['median_income'],
            mode='markers',
            marker=dict(
                size=8,
                color=filtered['predicted_revenue'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Revenue")
            ),
            name="Demographics",
            hovertemplate="Age: %{x}<br>Income: $%{y:,.0f}<br>Revenue: %{marker.color:$,.0f}<extra></extra>"
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Location Analytics Dashboard")
    
    return dcc.Graph(figure=fig)

def create_top_locations_tab(data, filtered):
    """Create top locations analysis table"""
    if len(filtered) == 0:
        return html.Div("No data matches current filters", className="text-center mt-5")
    
    # Get top 20 locations
    top_locations = filtered.nlargest(20, 'predicted_revenue')[
        ['latitude', 'longitude', 'predicted_revenue', 'commercial_traffic_score',
         'road_accessibility_score', 'distance_to_chickfila', 'fast_food_competition',
         'median_income', 'population', 'zoning_compliant']
    ].round(4)
    
    # Format for display
    display_df = top_locations.copy()
    display_df['predicted_revenue'] = display_df['predicted_revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['median_income'] = display_df['median_income'].apply(lambda x: f"${x:,.0f}")
    display_df['population'] = display_df['population'].apply(lambda x: f"{x:,.0f}")
    display_df['distance_to_chickfila'] = display_df['distance_to_chickfila'].apply(lambda x: f"{x:.1f} mi")
    display_df['zoning_compliant'] = display_df['zoning_compliant'].apply(lambda x: "✅" if x else "❌")
    
    # Rename columns for display
    display_df.columns = [
        'Latitude', 'Longitude', 'Predicted Revenue', 'Commercial Score',
        'Road Access', 'Distance to Competitor', 'Competition Level',
        'Median Income', 'Population', 'Zoning OK'
    ]
    
    table = dash_table.DataTable(
        data=display_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in display_df.columns],
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontFamily': 'Arial'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 0},
                'backgroundColor': '#d4edda',
                'color': 'black',
            }
        ],
        page_size=20,
        sort_action="native"
    )
    
    return html.Div([
        html.H4("🏆 Top Revenue Potential Locations", className="mb-3"),
        html.P(f"Showing top {min(20, len(filtered))} locations sorted by predicted revenue potential"),
        table
    ])

def create_model_tab(data):
    """Create model performance analysis tab"""
    metrics = data.get('metrics', {})
    feature_importance = data.get('feature_importance')
    
    if not metrics:
        return html.Div("No model metrics available", className="text-center mt-5")
    
    # Model performance metrics
    metrics_cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{metrics.get('train_r2', 0):.3f}", className="text-primary"),
                    html.P("R² Score", className="text-muted mb-0")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"${metrics.get('cv_mae_mean', 0):,.0f}", className="text-success"),
                    html.P("CV Mean Absolute Error", className="text-muted mb-0")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"${metrics.get('train_rmse', 0):,.0f}", className="text-warning"),
                    html.P("Root Mean Square Error", className="text-muted mb-0")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{metrics.get('feature_count', 0)}", className="text-info"),
                    html.P("Features Used", className="text-muted mb-0")
                ])
            ])
        ], width=3)
    ])
    
    # Feature importance chart
    if feature_importance is not None and len(feature_importance) > 0:
        top_features = feature_importance.head(15)
        fig = px.bar(
            top_features,
            x='importance',
            y='feature',
            orientation='h',
            title="Top 15 Most Important Features",
            labels={'importance': 'Feature Importance', 'feature': 'Feature'},
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        feature_chart = dcc.Graph(figure=fig)
    else:
        feature_chart = html.Div("Feature importance data not available")
    
    # Model parameters
    best_params = metrics.get('best_parameters', {})
    params_table = html.Div([
        html.H5("🎯 Optimal Model Parameters"),
        html.Ul([
            html.Li(f"{param}: {value}") for param, value in best_params.items()
        ]) if best_params else html.P("No parameter data available")
    ])
    
    return html.Div([
        html.H4("🔬 Model Performance Analysis", className="mb-4"),
        metrics_cards,
        html.Hr(className="my-4"),
        dbc.Row([
            dbc.Col([feature_chart], width=8),
            dbc.Col([params_table], width=4)
        ])
    ])

@app.callback(
    Output('location-stats', 'children'),
    [Input('city-dropdown', 'value'),
     Input('revenue-slider', 'value'), 
     Input('competitor-distance-slider', 'value'), 
     Input('commercial-traffic-slider', 'value'),
     Input('competition-slider', 'value'),
     Input('zoning-radio', 'value')]
)
def update_location_stats(city_id, min_revenue, max_competitor_distance, 
                         min_commercial_traffic, max_competition, zoning_filter):
    """Update location statistics sidebar"""
    data = data_loader.load_city_data(city_id)
    if not data:
        return html.Div("No data available")
    
    df = data['df_filtered']
    chickfila_locations = data.get('chickfila_locations', [])
    raising_canes_locations = data.get('raising_canes_locations', [])
    
    # Apply filters
    filtered = df[
        (df['predicted_revenue'] >= min_revenue) &
        (df['distance_to_chickfila'] <= max_competitor_distance) &
        (df['commercial_traffic_score'] >= min_commercial_traffic) &
        (df['fast_food_competition'] <= max_competition)
    ]
    
    if zoning_filter == 'compliant':
        filtered = filtered[filtered['zoning_compliant'] == 1]
    
    if len(filtered) > 0:
        best = filtered.loc[filtered['predicted_revenue'].idxmax()]
        avg_revenue = filtered['predicted_revenue'].mean()
        
        stats = html.Div([
            html.H5("📊 Analysis Summary", className="text-primary"),
            html.P(f"Filtered Locations: {len(filtered):,}"),
            html.P(f"Average Revenue: ${avg_revenue:,.0f}"),
            html.P(f"Competitors: {len(chickfila_locations)}"),
            html.P(f"Existing Cane's: {len(raising_canes_locations)}"),
            html.Hr(),
            html.H5("🎯 Top Location", className="text-success"),
            html.P(f"📍 {best['latitude']:.4f}, {best['longitude']:.4f}"),
            html.P(f"💰 Revenue: ${best['predicted_revenue']:,.0f}"),
            html.P(f"🏪 Commercial Score: {best['commercial_traffic_score']:.0f}"),
            html.P(f"🛣️ Road Access: {best['road_accessibility_score']:.0f}"),
            html.P(f"⛽ Gas Proximity: {best['gas_station_proximity']:.0f}"),
            html.P(f"🎯 Competitor Distance: {best['distance_to_chickfila']:.1f} mi"),
            html.P(f"🏢 Competition: {best['fast_food_competition']:.0f}"),
            html.P(f"👥 Median Age: {best['median_age']:.0f}"),
            html.P(f"💵 Median Income: ${best['median_income']:,.0f}"),
            html.P(f"🏠 Zoning: {'✅' if best['zoning_compliant'] else '❌'}")
        ])
    else:
        stats = html.Div([
            html.H5("⚠️ No Locations Found", className="text-warning"),
            html.P("Try adjusting your filters to see more locations."),
            html.P(f"Total Dataset: {len(df):,} locations"),
            html.P(f"Competitors: {len(chickfila_locations)}"),
            html.P(f"Existing Cane's: {len(raising_canes_locations)}")
        ])
    
    return stats

if __name__ == '__main__':
    print(f"🚀 Starting Enhanced Visualization App")
    print(f"📍 Available cities: {[city['display_name'] for city in available_cities]}")
    print(f"🌐 Open your browser to: http://127.0.0.1:8050")
    app.run(debug=True, host='127.0.0.1', port=8050)