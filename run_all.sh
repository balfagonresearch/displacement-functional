#!/bin/bash
source venv/bin/activate
echo "Generating figures..."
make figures
echo "Compiling paper..."
make paper
echo ""
echo "✓ All done!"
echo "  - Figures: fig1_entropy.pdf, fig2_lambda.pdf, fig3_ion_trap.pdf"
echo "  - Paper: displacement_functional_improved.pdf"
