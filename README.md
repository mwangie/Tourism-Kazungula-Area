# 🏞️ Kazungula Tourism Investment Dashboard

Interactive analytics dashboard for tourism investors in the Kazungula area, providing strategic intelligence on visitor trends, accommodation infrastructure, and market opportunities.

## 📊 Features

- **Real-time Tourism Analytics**: Track visitor arrivals, source markets, and seasonal patterns
- **Accommodation Analysis**: Comprehensive infrastructure capacity and occupancy insights
- **Revenue Modeling**: Economic impact analysis and ROI calculators
- **Investment Opportunities**: Data-driven identification of market gaps and opportunities
- **Interactive Visualizations**: Powered by Plotly for engaging data exploration
- **Mobile Responsive**: Works perfectly on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/kazungula-tourism-dashboard.git
cd kazungula-tourism-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
streamlit run dashboard_tourism.py
```

4. Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
kazungula-tourism-dashboard/
├── dashboard_tourism.py          # Main dashboard application
├── requirements.txt              # Python dependencies
├── data/                        # Your actual data files (add your CSVs here)
├── data_templates/              # Templates for data collection
│   ├── arrivals_data_template.csv
│   └── accommodation_data_template.csv
├── DATA_COLLECTION_GUIDE.md    # Guide to gathering real data
├── DEPLOYMENT_GUIDE.md          # Step-by-step deployment instructions
└── README.md                    # This file
```

## 📊 Data Requirements

The dashboard requires three main datasets:

### 1. Tourist Arrivals Data
- Monthly time series from 2019 to present
- Breakdown by international vs regional visitors
- Source markets (countries/regions)
- Template provided in `data_templates/arrivals_data_template.csv`

### 2. Accommodation Data
- Current snapshot of facilities
- Room capacity and occupancy rates
- Average rates by facility type
- Template provided in `data_templates/accommodation_data_template.csv`

### 3. Revenue Data
- Can be calculated from arrivals × average spend
- Breakdown by accommodation, activities, F&B, transport
- Guidance provided in DATA_COLLECTION_GUIDE.md

## 🎯 Using Sample Data vs Real Data

### Sample Data (Default)
The dashboard comes with built-in sample data for demonstration. You can launch immediately with realistic, representative data.

### Adding Your Real Data
1. Follow the DATA_COLLECTION_GUIDE.md to gather actual tourism data
2. Format your data using the templates in `data_templates/`
3. Save your data files to the `data/` folder
4. Update the data loading functions in `dashboard_tourism.py`

Detailed instructions in DEPLOYMENT_GUIDE.md

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `dashboard_tourism.py` as main file
5. Click Deploy!

Your dashboard will be live at: `https://your-app-name.streamlit.app`

Full deployment guide: DEPLOYMENT_GUIDE.md

### Embed in Website

Add to your WordPress or HTML site:

```html
<iframe 
    src="https://your-app-name.streamlit.app?embed=true" 
    width="100%" 
    height="800px" 
    frameborder="0">
</iframe>
```

## 🎨 Customization

### Update Colors
Edit the CSS section in `dashboard_tourism.py` (around line 30) to match your brand colors.

### Add Your Logo
Replace the placeholder logo URL (around line 150) with your own logo image.

### Modify Metrics
All calculations and metrics can be customized to match your specific requirements.

## 📈 Data Sources

This dashboard is designed to work with data from:
- Zambia Ministry of Tourism (www.mota.gov.zm)
- Zambia Statistics Agency (www.zamstats.gov.zm)
- KAZA TFCA Secretariat (www.kavangozambezi.org)
- Kazungula Border Post statistics
- Livingstone Tourism Association
- Local accommodation surveys

See DATA_COLLECTION_GUIDE.md for contact information and data request templates.

## 🔄 Updating Data

### Monthly Updates
1. Update your CSV files in the `data/` folder
2. Commit and push changes to GitHub
3. Streamlit Cloud auto-redeploys within 1-2 minutes

### Clear Cache
If data doesn't update immediately:
- Press 'C' in the dashboard
- Or use the "Clear Cache" button in Streamlit Cloud dashboard

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Try using python -m
python -m streamlit run dashboard_tourism.py

# Or upgrade streamlit
pip install streamlit --upgrade
```

### Import errors
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Port already in use
```bash
# Use different port
streamlit run dashboard_tourism.py --server.port 8502
```

More troubleshooting in DEPLOYMENT_GUIDE.md

## 📊 Dashboard Sections

1. **Key Performance Indicators** - Headline metrics and growth trends
2. **Visitor Trends** - Time series analysis, source markets, seasonality
3. **Accommodation Analysis** - Infrastructure capacity, occupancy, pricing
4. **Revenue Analysis** - Economic impact and revenue breakdown
5. **Investment Opportunities** - Market gaps and ROI indicators
6. **Competitive Landscape** - Major players and positioning
7. **Infrastructure** - Transport and connectivity analysis

## 🎓 Technologies Used

- **Streamlit** - Dashboard framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computations

## 📞 Support

- **Data Collection**: See DATA_COLLECTION_GUIDE.md
- **Deployment**: See DEPLOYMENT_GUIDE.md
- **Streamlit Docs**: docs.streamlit.io
- **Plotly Docs**: plotly.com/python
- **Questions**: Open an issue on GitHub

## 📄 License

© 2024 Concise Data Analytics. All rights reserved.

## 🙏 Acknowledgments

Data sources:
- Zambia Ministry of Tourism
- Zambia Statistics Agency
- KAZA TFCA Secretariat
- Livingstone Tourism Association
- Local accommodation providers

## 🚀 Next Steps

1. **Review DEPLOYMENT_GUIDE.md** - Complete setup instructions
2. **Check DATA_COLLECTION_GUIDE.md** - Learn how to gather real data
3. **Test locally** - Run `streamlit run dashboard_tourism.py`
4. **Deploy to cloud** - Get it live on Streamlit Cloud
5. **Embed in website** - Add to your WordPress site
6. **Share with stakeholders** - Start attracting tourism investors!

---

**Built with ❤️ by Concise Data Analytics**

For custom dashboards and data intelligence services:
- 🌐 concise-analytics.com
- 📧 hello@concise-analytics.com
- 📍 Gaborone, Botswana

Specialized analytics for agriculture, tourism, and property markets across the SADC region.
