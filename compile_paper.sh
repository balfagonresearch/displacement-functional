#!/bin/bash
source venv/bin/activate
make paper
echo ""
echo "✓ Paper compiled: displacement_functional_improved.pdf"
open displacement_functional_improved.pdf 2>/dev/null || echo "Open the PDF manually"
