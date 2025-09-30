"""
Demo application showing camels-attributes package information.
This is a simple Flask app to showcase the package documentation.
"""

from flask import Flask, render_template_string
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CAMELS Attributes Extractor Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background: #3498db;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #2980b9;
        }
        button:disabled {
            background: #95a5a6;
            cursor: not-allowed;
        }
        #result {
            margin-top: 30px;
            padding: 20px;
            background: #ecf0f1;
            border-radius: 5px;
            display: none;
        }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .error {
            color: #e74c3c;
            padding: 10px;
            background: #fadbd8;
            border-radius: 5px;
            margin-top: 10px;
        }
        .success {
            color: #27ae60;
            font-weight: bold;
        }
        pre {
            background: white;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            max-height: 500px;
            overflow-y: auto;
        }
        .info-box {
            background: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CAMELS Attributes Extractor</h1>
        <p class="subtitle">Extract comprehensive catchment attributes for any USGS gauge site</p>
        
        <div class="info-box">
            <strong>About:</strong> This package extracts 70+ watershed characteristics following the CAMELS methodology.
            <br><strong>Author:</strong> Mohammad Galib (mgalib@purdue.edu), Purdue University
            <br><br>
            <strong>Note:</strong> This is a demonstration page for the camels-attributes Python package.
            The package is designed to be installed via pip and used programmatically or via CLI.
        </div>
        
        <h3>Installation</h3>
        <pre style="background: #2c3e50; color: #ecf0f1;">pip install camels-attributes</pre>
        
        <h3>Quick Start - Python API</h3>
        <pre>from camels_attributes import CamelsExtractor

# Extract attributes for a gauge
extractor = CamelsExtractor('01031500')
attributes = extractor.extract_all()

# Save to CSV
extractor.save('attributes.csv')</pre>
        
        <h3>Quick Start - CLI</h3>
        <pre style="background: #2c3e50; color: #ecf0f1;"># Single gauge
camels-extract 01031500 -o attributes.csv

# Multiple gauges
camels-extract 01031500 02177000 06803530 -o combined.csv</pre>
        
        <h3>Features</h3>
        <ul>
            <li><strong>Watershed Delineation:</strong> Automated boundary extraction using NLDI</li>
            <li><strong>Topographic Attributes:</strong> Elevation, slope from 3DEP DEM</li>
            <li><strong>Climate Indices:</strong> Precipitation, temperature, aridity from GridMET</li>
            <li><strong>Soil Characteristics:</strong> Texture, porosity from gNATSGO and POLARIS</li>
            <li><strong>Vegetation Metrics:</strong> LAI, NDVI, land cover from MODIS and NLCD</li>
            <li><strong>Geological Properties:</strong> Lithology and permeability from GLiM and GLHYMPS</li>
            <li><strong>Hydrological Signatures:</strong> Flow statistics, baseflow index</li>
        </ul>
        
        <h3>Package Structure</h3>
        <pre>camels_attributes/
├── __init__.py         # Package initialization
├── extractor.py        # Main CamelsExtractor class
├── watershed.py        # Watershed delineation
├── topography.py       # Topographic attributes
├── climate.py          # Climate indices
├── soil.py             # Soil characteristics
├── vegetation.py       # Vegetation metrics
├── geology.py          # Geological properties
├── hydrology.py        # Hydrological signatures
└── cli.py              # Command-line interface</pre>
    </div>
    
    <script>
        // No JavaScript needed for static demo
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("="*60)
    print("CAMELS Attributes Package - Documentation Demo")
    print("="*60)
    print("\nThis is a demonstration page for the camels-attributes package.")
    print("The package is designed to be installed and used as a library:")
    print("\n  pip install camels-attributes")
    print("\nView the documentation at: http://localhost:5000")
    print("="*60)
    app.run(host='0.0.0.0', port=5000, debug=False)
