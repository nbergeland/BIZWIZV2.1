# === MULTI-CITY CONFIGURATION SYSTEM ===
# Save this as: city_config.py

import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import yaml

@dataclass
class CityBounds:
    """Geographic boundaries for a city"""
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
    center_lat: float
    center_lon: float
    grid_spacing: float = 0.005
    
    def get_grid_points(self) -> List[Tuple[float, float]]:
        """Generate grid points for the city"""
        import numpy as np
        lats = np.arange(self.min_lat, self.max_lat, self.grid_spacing)
        lons = np.arange(self.min_lon, self.max_lon, self.grid_spacing)
        return [(lat, lon) for lat in lats for lon in lons]

@dataclass
class CityDemographics:
    """Expected demographic ranges for normalization"""
    typical_population_range: Tuple[int, int]
    typical_income_range: Tuple[int, int] 
    typical_age_range: Tuple[float, float]
    population_density_factor: float = 1.0

@dataclass
class CityMarketData:
    """Market-specific data and API configurations"""
    state_code: str
    county_name: str
    city_name_variations: List[str]  # Different ways the city might be referenced
    rental_api_city_name: str  # Specific name format for rental APIs
    major_universities: List[str]
    major_employers: List[str]
    
@dataclass 
class CityCompetitorData:
    """Competitor-specific search terms and market factors"""
    primary_competitor: str  # Main competitor (e.g., "chick-fil-a")
    competitor_search_terms: List[str]
    market_saturation_factor: float  # Adjustment for market maturity
    fast_casual_preference_score: float  # Market preference for fast-casual (0-1)

@dataclass
class CityConfiguration:
    """Complete city configuration"""
    city_id: str
    display_name: str
    bounds: CityBounds
    demographics: CityDemographics
    market_data: CityMarketData
    competitor_data: CityCompetitorData
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CityConfiguration':
        """Create from dictionary"""
        return cls(
            city_id=data['city_id'],
            display_name=data['display_name'],
            bounds=CityBounds(**data['bounds']),
            demographics=CityDemographics(**data['demographics']),
            market_data=CityMarketData(**data['market_data']),
            competitor_data=CityCompetitorData(**data['competitor_data'])
        )

class CityConfigManager:
    """Manages city configurations"""
    
    def __init__(self, config_file: str = "city_configs.yaml"):
        self.config_file = config_file
        self.configs: Dict[str, CityConfiguration] = {}
        self.current_city: Optional[str] = None
        self.load_configs()
    
    def load_configs(self):
        """Load city configurations from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = yaml.safe_load(f)
                    for city_id, city_data in data['cities'].items():
                        self.configs[city_id] = CityConfiguration.from_dict(city_data)
                    self.current_city = data.get('current_city')
            except Exception as e:
                print(f"Error loading city configs: {e}")
                self._create_default_configs()
        else:
            self._create_default_configs()
    
    def save_configs(self):
        """Save configurations to file"""
        data = {
            'current_city': self.current_city,
            'cities': {city_id: config.to_dict() for city_id, config in self.configs.items()}
        }
        with open(self.config_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, indent=2)
    
    def _create_default_configs(self):
        """Create default city configurations"""
        # Grand Forks, ND (your current city)
        grand_forks = CityConfiguration(
            city_id="grand_forks_nd",
            display_name="Grand Forks, ND",
            bounds=CityBounds(
                min_lat=47.85, max_lat=47.95,
                min_lon=-97.15, max_lon=-97.0,
                center_lat=47.9, center_lon=-97.075
            ),
            demographics=CityDemographics(
                typical_population_range=(3000, 12000),
                typical_income_range=(35000, 70000),
                typical_age_range=(22, 45),
                population_density_factor=1.0
            ),
            market_data=CityMarketData(
                state_code="ND",
                county_name="Grand Forks County",
                city_name_variations=["Grand Forks", "Grand Forks ND"],
                rental_api_city_name="Grand Forks",
                major_universities=["University of North Dakota"],
                major_employers=["University of North Dakota", "Altru Health System"]
            ),
            competitor_data=CityCompetitorData(
                primary_competitor="chick-fil-a",
                competitor_search_terms=['mcdonalds', 'kfc', 'taco bell', 'burger king', 'subway', 'wendys', 'popeyes'],
                market_saturation_factor=0.7,  # Lower saturation, more opportunity
                fast_casual_preference_score=0.8
            )
        )
        
        # Fargo, ND (nearby similar market)
        fargo = CityConfiguration(
            city_id="fargo_nd",
            display_name="Fargo, ND",
            bounds=CityBounds(
                min_lat=46.8, max_lat=46.95,
                min_lon=-96.9, max_lon=-96.7,
                center_lat=46.875, center_lon=-96.8
            ),
            demographics=CityDemographics(
                typical_population_range=(5000, 18000),
                typical_income_range=(40000, 80000),
                typical_age_range=(25, 40),
                population_density_factor=1.2
            ),
            market_data=CityMarketData(
                state_code="ND",
                county_name="Cass County",
                city_name_variations=["Fargo", "Fargo ND"],
                rental_api_city_name="Fargo",
                major_universities=["North Dakota State University"],
                major_employers=["Sanford Health", "Microsoft", "North Dakota State University"]
            ),
            competitor_data=CityCompetitorData(
                primary_competitor="chick-fil-a",
                competitor_search_terms=['mcdonalds', 'kfc', 'taco bell', 'burger king', 'subway', 'wendys', 'popeyes'],
                market_saturation_factor=0.9,  # Higher saturation
                fast_casual_preference_score=0.85
            )
        )
        
        # Bismarck, ND (state capital)
        bismarck = CityConfiguration(
            city_id="bismarck_nd",
            display_name="Bismarck, ND",
            bounds=CityBounds(
                min_lat=46.75, max_lat=46.85,
                min_lon=-100.85, max_lon=-100.7,
                center_lat=46.8, center_lon=-100.775
            ),
            demographics=CityDemographics(
                typical_population_range=(4000, 15000),
                typical_income_range=(45000, 85000),
                typical_age_range=(28, 45),
                population_density_factor=1.1
            ),
            market_data=CityMarketData(
                state_code="ND",
                county_name="Burleigh County",
                city_name_variations=["Bismarck", "Bismarck ND"],
                rental_api_city_name="Bismarck",
                major_universities=["University of Mary", "Bismarck State College"],
                major_employers=["State of North Dakota", "Sanford Health", "Basin Electric"]
            ),
            competitor_data=CityCompetitorData(
                primary_competitor="chick-fil-a",
                competitor_search_terms=['mcdonalds', 'kfc', 'taco bell', 'burger king', 'subway', 'wendys', 'popeyes'],
                market_saturation_factor=0.8,
                fast_casual_preference_score=0.75
            )
        )
        
        self.configs = {
            "grand_forks_nd": grand_forks,
            "fargo_nd": fargo,
            "bismarck_nd": bismarck
        }
        self.current_city = "grand_forks_nd"
        self.save_configs()
    
    def set_current_city(self, city_id: str):
        """Set the current active city"""
        if city_id in self.configs:
            self.current_city = city_id
            self.save_configs()
            return True
        return False
    
    def get_current_config(self) -> Optional[CityConfiguration]:
        """Get the current city configuration"""
        if self.current_city and self.current_city in self.configs:
            return self.configs[self.current_city]
        return None
    
    def get_config(self, city_id: str) -> Optional[CityConfiguration]:
        """Get configuration for a specific city"""
        return self.configs.get(city_id)
    
    def list_cities(self) -> List[str]:
        """List available cities"""
        return list(self.configs.keys())
    
    def add_city(self, config: CityConfiguration):
        """Add a new city configuration"""
        self.configs[config.city_id] = config
        self.save_configs()
    
    def remove_city(self, city_id: str) -> bool:
        """Remove a city configuration"""
        if city_id in self.configs:
            del self.configs[city_id]
            if self.current_city == city_id:
                self.current_city = next(iter(self.configs.keys()), None)
            self.save_configs()
            return True
        return False

# === UTILITY FUNCTIONS FOR BACKWARD COMPATIBILITY ===

def get_city_bounds() -> Tuple[float, float, float, float]:
    """Get current city bounds for backward compatibility"""
    manager = CityConfigManager()
    config = manager.get_current_config()
    if config:
        return (config.bounds.min_lat, config.bounds.max_lat, 
                config.bounds.min_lon, config.bounds.max_lon)
    # Fallback to Grand Forks
    return (47.85, 47.95, -97.15, -97.0)

def get_grid_points() -> List[Tuple[float, float]]:
    """Get current city grid points for backward compatibility"""
    manager = CityConfigManager()
    config = manager.get_current_config()
    if config:
        return config.bounds.get_grid_points()
    # Fallback
    import numpy as np
    min_lat, max_lat, min_lon, max_lon = get_city_bounds()
    lats = np.arange(min_lat, max_lat, 0.005)
    lons = np.arange(min_lon, max_lon, 0.005)
    return [(lat, lon) for lat in lats for lon in lons]

def get_current_city_name() -> str:
    """Get current city display name"""
    manager = CityConfigManager()
    config = manager.get_current_config()
    return config.display_name if config else "Grand Forks, ND"

# === EXAMPLE USAGE ===
if __name__ == "__main__":
    # Example of how to use the city configuration system
    manager = CityConfigManager()
    
    print("Available cities:")
    for city_id in manager.list_cities():
        config = manager.get_config(city_id)
        print(f"  {city_id}: {config.display_name}")
    
    print(f"\nCurrent city: {manager.current_city}")
    
    # Switch to a different city
    if manager.set_current_city("fargo_nd"):
        print("Switched to Fargo, ND")
        current = manager.get_current_config()
        print(f"Grid points: {len(current.bounds.get_grid_points())}")
        print(f"Center: {current.bounds.center_lat}, {current.bounds.center_lon}")