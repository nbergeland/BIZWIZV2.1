# BizWizV2 Enhanced - Multi-City Commercial Location Analysis

![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 What's New in Version 2.1.0

**🏙️ Multi-City Support**
- Configurable city boundaries and demographics
- Easy switching between different markets
- City-specific caching and optimization

**🏢 Real Zoning Data Integration**
- Replaces randomized zoning with actual data sources
- OpenStreetMap integration for commercial zones
- Government API support for zoning compliance

**🤖 Enhanced Machine Learning Pipeline**
- Cross-validation and hyperparameter tuning
- Model performance metrics (R², MAE, RMSE)
- Feature importance analysis
- Automated model validation

**📊 Advanced Analytics Dashboard**
- Multi-tab interface with specialized views
- Real-time filtering and analysis
- Top locations ranking table
- Model performance visualization

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/BizWizV2.git
cd BizWizV2

# Run the installation script
python install.py
```

### 2. Configure API Keys
Edit the `.env` file with your API keys:
```bash
GOOGLE_API_KEY=your_google_maps_api_key
CENSUS_API_KEY=your_census_api_key
RENTCAST_API_KEY=your_rentcast_api_key
```

### 3. Run Analysis
```bash
# Quick start with menu
python enhanced_run_analysis.py

# Or run individual components
python enhanced_data_collection.py --list-cities
python enhanced_data_collection.py --city grand_forks_nd
python enhanced_visualization_app.py
```

## 📁 Project Structure

```
BizWizV2/
├── 📄 Enhanced Core Files
│   ├── city_config.py                    # Multi-city configuration system
│   ├── enhanced_data_collection.py       # Advanced data collection with ML
│   ├── enhanced_visualization_app.py     # Multi-tab dashboard
│   └── enhanced_run_analysis.py          # Enhanced orchestration script
│
├── 🛠️ Setup and Installation
│   ├── install.py                        # Automated installation script
│   ├── requirements.txt                  # Python dependencies
│   ├── setup.py                         # Package configuration
│   └── quick_start.py                   # User-friendly launcher
│
├── 📊 Configuration and Data
│   ├── .env                             # API keys (create from template)
│   ├── city_configs.yaml               # Multi-city configurations
│   └── version.json                    # Version tracking
│
├── 💾 City-Specific Cache Directories
│   ├── cache_grand_forks_nd/           # Grand Forks data cache
│   ├── cache_fargo_nd/                 # Fargo data cache
│   └── cache_bismarck_nd/              # Bismarck data cache
│
└── 📋 Legacy Files (for reference)
    ├── data_collection.py              # Original data collection
    ├── visualization_app.py            # Original visualization
    └── run_analysis.py                 # Original runner
```

## 🏙️ Supported Cities

**Current Configurations:**
- **Grand Forks, ND** - University town with student demographics
- **Fargo, ND** - Larger market with higher competition
- **Bismarck, ND** - State capital with government employment

**Adding New Cities:**
The system is designed for easy expansion. Edit `city_config.py` to add new markets with specific demographic and competitive profiles.

## 📊 Enhanced Features

### 🎯 Multi-City Analysis
- **Configurable Boundaries**: Each city has specific geographic bounds and grid spacing
- **Demographic Normalization**: City-specific income and age adjustments
- **Market Factors**: Competition saturation and preference scoring
- **Cached Data**: City-specific caching prevents API waste

### 🤖 Advanced Machine Learning
- **Hyperparameter Tuning**: GridSearchCV optimization for best model performance
- **Cross-Validation**: 5-fold CV for robust performance estimation
- **Feature Engineering**: City-specific feature adjustments
- **Performance Metrics**: R², MAE, RMSE tracking with historical comparison

### 🏢 Real Zoning Integration
- **OpenStreetMap Data**: Commercial/retail zone identification
- **Government APIs**: Integration with city planning databases
- **Proximity Analysis**: Commercial establishment clustering
- **Fallback Systems**: Multiple data sources for reliability

### 📈 Enhanced Visualizations
- **Interactive Map**: Color-coded revenue potential with competitor overlay
- **Analytics Dashboard**: Multi-chart analysis with demographic insights
- **Top Locations Table**: Sortable ranking with detailed metrics
- **Model Performance**: Feature importance and validation metrics

## 🔧 API Requirements

### Required APIs
1. **Google Maps API** - Location and POI data
   - Places API
   - Geocoding API
   - Get it: [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

2. **US Census Bureau API** - Demographic data
   - American Community Survey (ACS)
   - Get it: [Census API Key](https://api.census.gov/data/key_signup.html)

3. **RentCast API** - Real estate data
   - Rental listings and market data
   - Get it: [RentCast API](https://app.rentcast.io/app/api-access)

### Optional Data Sources
- **OpenStreetMap Overpass API** - Free road and zoning data
- **City Government APIs** - Municipal zoning databases (city-specific)

## 💻 Usage Examples

### Basic Analysis
```python
# Analyze current city
python enhanced_data_collection.py

# Analyze specific city
python enhanced_data_collection.py --city fargo_nd

# List available cities
python enhanced_data_collection.py --list-cities
```

### Advanced Configuration
```python
from city_config import CityConfigManager, CityConfiguration

# Load city manager
manager = CityConfigManager()

# Switch cities
manager.set_current_city("fargo_nd")

# Get city configuration
config = manager.get_current_config()
print(f"Analyzing {config.display_name}")
```

### Custom Analysis
```python
from enhanced_data_collection import collect_and_process_all_data

# Run analysis with custom city
data = collect_and_process_all_data("grand_forks_nd")

# Access results
df = data['df_filtered']
model = data['model'] 
metrics = data['metrics']

print(f"Model R² Score: {metrics['train_r2']:.3f}")
print(f"Best location revenue: ${df['predicted_revenue'].max():,.0f}")
```

## 📊 Dashboard Features

### 🗺️ Interactive Map
- **Revenue Heatmap**: Color-coded location potential
- **Competitor Overlay**: Chick-fil-A locations with 🐔 markers
- **Existing Stores**: Current Raising Cane's with 🍗 markers
- **Dynamic Filtering**: Real-time filter application
- **Hover Details**: Comprehensive location metrics

### 📈 Analytics Dashboard
- **Revenue Distribution**: Histogram of potential earnings
- **Traffic Analysis**: Commercial score vs revenue correlation
- **Competition Impact**: Revenue by competition level
- **Demographics**: Income vs age with revenue coloring

### 🏆 Top Locations Table
- **Sortable Rankings**: Click columns to sort
- **Comprehensive Metrics**: All key factors in one view
- **Export Ready**: Easy copy/paste for reports
- **Visual Indicators**: Zoning compliance with ✅/❌

### 🔬 Model Performance
- **Key Metrics**: R², MAE, RMSE display cards
- **Feature Importance**: Top 15 factors visualization
- **Model Parameters**: Optimal hyperparameters display
- **Validation Results**: Cross-validation performance

## 🎛️ Filter Options

### Revenue Controls
- **Minimum Revenue**: Filter by predicted earnings threshold
- **Revenue Percentiles**: Quick selection of top performers

### Location Factors
- **Competitor Distance**: Maximum distance to primary competitor
- **Commercial Traffic**: Minimum foot traffic score
- **Competition Level**: Maximum nearby fast-food density
- **Zoning Compliance**: Include only compliant locations

### Demographics
- **Income Ranges**: Filter by median household income
- **Age Demographics**: Target specific age groups
- **Population Density**: Urban vs suburban preferences

## 🔍 Model Validation

### Performance Metrics
- **R² Score**: Variance explained by model (target: >0.7)
- **Cross-Validation MAE**: Average prediction error across folds
- **RMSE**: Root mean square error for large prediction penalties
- **Feature Count**: Number of variables used in prediction

### Key Features (Typical Importance)
1. **Zoning Compliance** (~15-20%) - Legal ability to operate
2. **Commercial Traffic Score** (~12-18%) - Foot traffic potential
3. **Road Accessibility** (~10-15%) - Visibility and access
4. **Competition Distance** (~8-12%) - Strategic positioning
5. **Income Demographics** (~8-12%) - Customer spending power

## 🚨 Troubleshooting

### Common Issues

**"No processed data found"**
```bash
# Run data collection first
python enhanced_data_collection.py --city grand_forks_nd
```

**"API quota exceeded"**
```bash
# Check daily usage
cat cache_*/api_usage.json
# Wait 24 hours or upgrade API plan
```

**"Module not found" errors**
```bash
# Reinstall dependencies
python install.py
# Or manually: pip install -r requirements.txt
```

**"No city configuration found"**
```bash
# Check available cities
python enhanced_data_collection.py --list-cities
# Verify city_configs.yaml exists
```

### Performance Optimization

**Slow data collection:**
- Use cached data when possible
- Reduce grid spacing in city_config.py
- Implement API rate limiting

**Memory issues:**
- Process cities individually
- Clear cache between runs
- Reduce feature set for large datasets

## 🔄 Migration from V1

### Automatic Migration
The enhanced system is backward compatible. Your existing `.env` file and cached data will work, but you'll get additional features by using the new scripts.

### Manual Migration Steps
1. **Backup existing data**: Copy your `processed_location_data.pkl`
2. **Install new dependencies**: Run `python install.py`
3. **Configure cities**: The system will auto-create `city_configs.yaml`
4. **Re-run analysis**: Use `enhanced_data_collection.py` for better results

### What's Preserved
- ✅ API keys and configuration
- ✅ Cached Google Maps data
- ✅ Core analysis methodology
- ✅ Visualization preferences

### What's Enhanced
- 🔄 Better caching system
- 🔄 Real zoning data
- 🔄 Model validation
- 🔄 Multi-city support

## 📈 Future Roadmap

### Version 2.2 (Planned)
- **Advanced Geospatial Analysis**: Drive-time polygons and visibility analysis
- **Financial Modeling**: ROI calculations and lease cost integration
- **Competitive Intelligence**: Market share analysis and pricing models
- **API Expansion**: Additional data sources and real-time updates

### Version 2.3 (Planned)
- **Cloud Deployment**: AWS/Azure hosting with web interface
- **Team Collaboration**: Multi-user support and shared analysis
- **Advanced Reporting**: PDF generation and executive dashboards
- **Machine Learning**: Deep learning models and time-series forecasting

## 🤝 Contributing

We welcome contributions! See our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black .
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenStreetMap** for free geographic data
- **US Census Bureau** for demographic data
- **Google Maps Platform** for location intelligence
- **RentCast** for real estate market data
- **Plotly and Dash** for visualization framework

---

**Built with ❤️ for data-driven location intelligence**

*For support, feature requests, or questions, please open an issue on GitHub.*