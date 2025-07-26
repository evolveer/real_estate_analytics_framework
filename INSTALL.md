# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- 2GB free disk space

## Installation Steps

### 1. Extract Package
```bash
tar -xzf real_estate_analytics_complete.tar.gz
cd real_estate_analytics_complete/
```

### 2. Install Dependencies
```bash
pip install -r config/requirements.txt
```

### 3. Verify Installation
```bash
cd tests/
python test_framework.py
```

### 4. Run Demo
```bash
cd ../examples/
python demo.py
```

### 5. Launch Web Interface
```bash
cd ../streamlit_ui/
streamlit run streamlit_app.py
```

## Troubleshooting

### Common Issues

**Import Errors:**
- Ensure all dependencies are installed
- Check Python version compatibility

**Database Errors:**
- Verify SQLite is available
- Check file permissions

**Streamlit Issues:**
- Update Streamlit: `pip install --upgrade streamlit`
- Clear cache: `streamlit cache clear`

### System Requirements

- **Memory:** 4GB RAM minimum
- **Storage:** 2GB free space
- **Network:** Internet connection for package installation

## Next Steps

1. Explore the framework with `examples/demo.py`
2. Customize the Streamlit interface
3. Add your own data sources
4. Configure KPIs for your business
5. Set up A/B tests for optimization

For detailed usage instructions, see `documentation/README.md`.

