#!/bin/bash
# Quick setup and run script for Microsoft Foundry Project

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  Microsoft Foundry Project - Quick Start                                  ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if venv is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📍 Activating virtual environment..."
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "✓ Virtual environment already active"
fi

echo ""
echo "🚀 Available Commands:"
echo "   1. Demo (no Java required):      python demo.py"
echo "   2. Full Pipeline (needs Java):   python run_pipeline.py"
echo "   3. Run Tests:                    pytest tests/ -v"
echo "   4. Format Code:                  black src/ tests/"
echo ""
echo "📚 Documentation:"
echo "   • README.md         - Project overview"
echo "   • SETUP_GUIDE.md    - Detailed setup"
echo "   • SUMMARY.md        - Full summary"
echo ""
echo "🎯 Next Steps:"
echo "   1. Run demo:        python demo.py"
echo "   2. Install Java:    brew install openjdk@11"
echo "   3. Run pipeline:    python run_pipeline.py"
echo "   4. Create transforms in src/transforms/"
echo ""
