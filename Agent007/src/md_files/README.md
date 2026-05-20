# Microsoft Foundry Data Engineering Project

A production-ready data engineering and ML pipeline project built on Microsoft Foundry, featuring Apache Spark, Delta Lake, and Azure cloud integration.

## 🎯 Project Goals

- Build scalable data transformation pipelines
- Implement best practices for data engineering
- Integrate with Azure cloud services
- Provide reusable components and utilities
- Enable ML model training and deployment

## 📋 Requirements

- Python 3.9+
- Apache Spark 3.5.0+
- Azure subscription (for cloud features)
- Git

## 🚀 Quick Start

### 1. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp config/example.env .env
# Edit .env with your Azure credentials
```

### 4. Run Sample Pipeline

```bash
python src/pipelines/sample_pipeline.py
```

### 5. Run Tests

```bash
pytest tests/ -v --cov=src
```

## 📁 Project Structure

```
├── src/
│   ├── foundry/          # Foundry integrations and clients
│   ├── pipelines/        # Pipeline orchestration
│   ├── transforms/       # Data transformation logic
│   └── utils/            # Utility functions
├── tests/                # Unit and integration tests
├── config/               # Configuration files
├── data/
│   ├── raw/             # Input data
│   └── processed/       # Output data
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🔧 Configuration

Create a `.env` file in the project root:

```env
# Azure Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_STORAGE_ACCOUNT=your-storage-account
AZURE_STORAGE_KEY=your-storage-key

# Foundry Configuration
FOUNDRY_API_KEY=your-api-key
FOUNDRY_WORKSPACE=your-workspace

# Spark Configuration
SPARK_DRIVER_MEMORY=4g
SPARK_EXECUTOR_MEMORY=2g
```

## 💻 Development

### Code Style

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
pylint src/ tests/

# Type checking
mypy src/
```

### Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_transforms.py -v
```

## 📚 Key Components

### Foundry Integration (`src/foundry/`)
- Foundry client configuration
- Data source connections
- Schema management

### Pipelines (`src/pipelines/`)
- Pipeline definitions
- Data orchestration
- Error handling and retry logic

### Transforms (`src/transforms/`)
- Business logic for data transformation
- Aggregations and calculations
- Data quality checks

### Utilities (`src/utils/`)
- Common helper functions
- Logging configuration
- Configuration management

## 🔐 Security Best Practices

1. **Never commit secrets**: Use `.env` files and environment variables
2. **Use managed identities**: For Azure service authentication
3. **Implement least privilege**: Grant minimal required permissions
4. **Audit logging**: Enable detailed logging for compliance
5. **Data encryption**: Encrypt data at rest and in transit

## 📊 Monitoring & Logging

Structured logging is configured with JSON output for easy parsing:

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Pipeline started", extra={"pipeline_id": "123"})
```

## 🚀 Deployment

### Development Environment
```bash
python src/pipelines/sample_pipeline.py --env dev
```

### Production Environment
```bash
python src/pipelines/sample_pipeline.py --env prod
```

## 📖 Additional Resources

- [Microsoft Foundry Documentation](https://docs.microsoft.com/en-us/azure/foundry)
- [Apache Spark Documentation](https://spark.apache.org/docs/)
- [Delta Lake Guide](https://docs.delta.io/)
- [Azure Data Factory](https://docs.microsoft.com/en-us/azure/data-factory/)

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and test: `pytest tests/`
3. Format code: `black src/ tests/`
4. Commit with message: `git commit -m "Add my feature"`
5. Push to branch: `git push origin feature/my-feature`
6. Create Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🆘 Troubleshooting

### Spark not found
```bash
export SPARK_HOME=/path/to/spark
export PATH=$PATH:$SPARK_HOME/bin
```

### Azure authentication fails
```bash
az login
az account set --subscription <subscription-id>
```

### Memory errors with Spark
Adjust in `.env`:
```env
SPARK_DRIVER_MEMORY=8g
SPARK_EXECUTOR_MEMORY=4g
```

## 📞 Support

For issues and questions, please open an issue on GitHub or contact the team.
