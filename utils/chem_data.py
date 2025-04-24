import pandas as pd
import numpy as np

# Dictionary of chemistry topics and associated experiment types
CHEMISTRY_TOPICS = {
    "Stoichiometry": [
        "Gravimetric Analysis",
        "Titration Analysis",
        "Gas Evolution",
        "Limiting Reagent Determination"
    ],
    "Acid-Base Chemistry": [
        "Acid-Base Titration",
        "Buffer Solutions",
        "pH Measurement",
        "Indicators and pH Range"
    ],
    "Redox Chemistry": [
        "Redox Titration",
        "Electrochemical Cells",
        "Electrolysis",
        "Corrosion Studies"
    ],
    "Thermochemistry": [
        "Calorimetry",
        "Enthalpy of Reaction",
        "Enthalpy of Solution",
        "Hess's Law Verification"
    ],
    "Kinetics": [
        "Rate of Reaction",
        "Effect of Temperature on Rate",
        "Effect of Concentration on Rate",
        "Effect of Catalyst on Rate"
    ],
    "Equilibrium": [
        "Le Chatelier's Principle",
        "Equilibrium Constants",
        "Solubility Product",
        "Common Ion Effect"
    ],
    "Organic Chemistry": [
        "Esterification",
        "Saponification",
        "Organic Synthesis",
        "Functional Group Tests"
    ],
    "Analytical Chemistry": [
        "Spectrophotometry",
        "Chromatography",
        "Colorimetry",
        "Conductivity Measurements"
    ],
    "Electrochemistry": [
        "Galvanic Cells",
        "Electrolytic Cells",
        "Nernst Equation Verification",
        "Faraday's Laws"
    ],
    "Biochemistry": [
        "Enzyme Kinetics",
        "Protein Denaturation",
        "Vitamin Content Analysis",
        "Fermentation"
    ],
    "Environmental Chemistry": [
        "Water Quality Analysis",
        "Soil Analysis",
        "Air Pollution Measurement",
        "Biodegradation Studies"
    ]
}

# Experiment templates with default variables and methodologies
EXPERIMENT_TEMPLATES = {
    "Stoichiometry": {
        "Titration Analysis": {
            "independent_var": "Concentration of the titrant (mol/L)",
            "dependent_var": "Volume of titrant required to reach endpoint (mL)",
            "controlled_vars": [
                "Temperature of solutions",
                "Size of conical flask",
                "Amount of indicator used",
                "Initial volume of analyte",
                "Stirring rate"
            ],
            "methodology": """1. Prepare standard solutions of sodium hydroxide at concentrations of 0.05, 0.10, 0.15, 0.20, and 0.25 mol/L.
2. Pipette exactly 25.0 mL of 0.1 mol/L hydrochloric acid into a clean conical flask.
3. Add 2-3 drops of phenolphthalein indicator.
4. Fill the burette with the sodium hydroxide solution.
5. Record the initial burette reading.
6. Slowly add the sodium hydroxide solution to the acid while swirling the flask.
7. Stop when the solution turns a persistent pale pink color.
8. Record the final burette reading and calculate the volume used.
9. Repeat steps 2-8 for each concentration of sodium hydroxide.
10. Repeat the entire experiment twice more for a total of three trials.
11. Calculate the average volume required for each concentration.""",
            "materials": [
                "Burette (50 mL)",
                "Pipette (25 mL)",
                "Conical flasks (250 mL)",
                "Sodium hydroxide",
                "Hydrochloric acid",
                "Phenolphthalein indicator",
                "Distilled water",
                "Analytical balance",
                "Volumetric flasks (100 mL)",
                "Wash bottle",
                "White tile"
            ]
        },
        "Gravimetric Analysis": {
            "independent_var": "Mass of reactant (g)",
            "dependent_var": "Mass of product formed (g)",
            "controlled_vars": [
                "Temperature",
                "Reaction time",
                "Purity of reactants",
                "Crucible size",
                "Heating method"
            ],
            "methodology": """1. Clean and dry a crucible, then heat it in a Bunsen burner flame for approximately 5 minutes.
2. Allow the crucible to cool in a desiccator for 15 minutes.
3. Weigh the crucible to the nearest 0.001 g.
4. Add approximately 1.000 g of the sample to the crucible and weigh again.
5. Heat the crucible gently at first, then strongly for 20 minutes.
6. Allow the crucible to cool in a desiccator for 15 minutes.
7. Weigh the crucible and product.
8. Repeat steps 5-7 until a constant mass is achieved (difference between consecutive weighings < 0.002 g).
9. Repeat the entire procedure for different masses of the reactant (1.500 g, 2.000 g, 2.500 g, 3.000 g).
10. Repeat each measurement three times.""",
            "materials": [
                "Crucible with lid",
                "Crucible tongs",
                "Analytical balance",
                "Bunsen burner",
                "Tripod stand",
                "Pipe-clay triangle",
                "Desiccator",
                "Sample material",
                "Heat-resistant mat"
            ]
        }
    },
    "Kinetics": {
        "Rate of Reaction": {
            "independent_var": "Concentration of reactant (mol/L)",
            "dependent_var": "Rate of reaction (mol/L/s)",
            "controlled_vars": [
                "Temperature",
                "Pressure",
                "Stirring rate",
                "Surface area (if solid reactant)",
                "Volume of reaction mixture"
            ],
            "methodology": """1. Prepare solutions of sodium thiosulfate at concentrations of 0.05, 0.10, 0.15, 0.20, and 0.25 mol/L.
2. Mark an X on a piece of paper and place it under a 250 mL beaker.
3. Measure 50 mL of sodium thiosulfate solution and pour it into the beaker.
4. Add 5 mL of 1.0 mol/L hydrochloric acid quickly to the beaker and immediately start the stopwatch.
5. Look down through the solution at the X and stop the stopwatch when the X disappears from view due to sulfur precipitation.
6. Record the time taken for the X to disappear.
7. Rinse the beaker thoroughly with distilled water and dry it.
8. Repeat steps 3-7 for each concentration of sodium thiosulfate.
9. Repeat the entire experiment twice more for a total of three trials.
10. Calculate the rate of reaction (1/time) for each concentration.""",
            "materials": [
                "Sodium thiosulfate",
                "Hydrochloric acid (1.0 mol/L)",
                "Beakers (250 mL)",
                "Measuring cylinders (50 mL and 10 mL)",
                "Stopwatch",
                "Paper with X marked",
                "Distilled water",
                "Analytical balance",
                "Volumetric flasks (100 mL)"
            ]
        },
        "Effect of Temperature on Rate": {
            "independent_var": "Temperature (°C)",
            "dependent_var": "Rate of reaction (mol/L/s)",
            "controlled_vars": [
                "Concentration of reactants",
                "Pressure",
                "Stirring rate",
                "Surface area (if solid reactant)",
                "Volume of reaction mixture"
            ],
            "methodology": """1. Prepare 100 mL of 0.2 mol/L sodium thiosulfate solution.
2. Prepare a water bath at 10°C using ice and water.
3. Place 20 mL of the sodium thiosulfate solution in a test tube and place it in the water bath for 5 minutes to equilibrate.
4. Mark an X on a piece of paper and place it under a clean, dry beaker.
5. Pour the temperature-equilibrated sodium thiosulfate solution into the beaker.
6. Measure the temperature of the solution in the beaker.
7. Add 2 mL of 1.0 mol/L hydrochloric acid quickly to the beaker and immediately start the stopwatch.
8. Look down through the solution at the X and stop the stopwatch when the X disappears from view due to sulfur precipitation.
9. Record the time taken for the X to disappear.
10. Repeat steps 2-9 for temperatures of 20°C, 30°C, 40°C, and 50°C.
11. Repeat the entire experiment twice more for a total of three trials.
12. Calculate the rate of reaction (1/time) for each temperature.""",
            "materials": [
                "Sodium thiosulfate",
                "Hydrochloric acid (1.0 mol/L)",
                "Beakers (100 mL)",
                "Test tubes",
                "Water bath or hot plates",
                "Ice bath",
                "Thermometer (0-100°C)",
                "Stopwatch",
                "Paper with X marked",
                "Measuring cylinders (25 mL and 5 mL)",
                "Distilled water"
            ]
        }
    },
    "Acid-Base Chemistry": {
        "Acid-Base Titration": {
            "independent_var": "Volume of acid/base added (mL)",
            "dependent_var": "pH of solution",
            "controlled_vars": [
                "Temperature",
                "Concentration of solutions",
                "Stirring rate",
                "Type of indicator used",
                "Initial volume of analyte"
            ],
            "methodology": """1. Prepare a standard solution of 0.1 mol/L sodium hydroxide by dissolving 0.4 g of NaOH in 100 mL of distilled water.
2. Prepare a standard solution of 0.1 mol/L hydrochloric acid by diluting concentrated HCl.
3. Calibrate the pH meter using standard buffer solutions (pH 4, 7, and 10).
4. Add 25 mL of the acid solution to a clean beaker.
5. Place the pH electrode in the solution and record the initial pH.
6. Fill the burette with the base solution and record the initial volume.
7. Add the base solution in 1 mL increments, stirring after each addition.
8. Record the pH after each addition.
9. Near the equivalence point, add the base in 0.1 mL increments.
10. Continue until the pH stabilizes at a high value.
11. Repeat the titration twice more for a total of three trials.
12. Plot a titration curve (pH vs. volume of base added) for each trial.""",
            "materials": [
                "Sodium hydroxide",
                "Hydrochloric acid",
                "pH meter with electrode",
                "Buffer solutions (pH 4, 7, and 10)",
                "Burette (50 mL)",
                "Beakers (100 mL)",
                "Pipette (25 mL)",
                "Magnetic stirrer and stir bar",
                "Distilled water",
                "Analytical balance",
                "Volumetric flasks (100 mL)"
            ]
        }
    }
}

# Safety information for different experiment types
SAFETY_INFO = {
    "Titration Analysis": """
Safety precautions for working with acids and bases:
- Wear safety goggles, lab coat, and appropriate gloves at all times
- Work in a well-ventilated area
- Handle concentrated acids and bases with extreme care
- Keep a solution of sodium bicarbonate (for acid spills) and dilute acetic acid (for base spills) available
- Know the location of the nearest eye wash station and safety shower
- Dispose of waste solutions according to school regulations
""",
    "Gravimetric Analysis": """
Safety precautions for heating and working with crucibles:
- Wear safety goggles, lab coat, and heat-resistant gloves when handling hot equipment
- Use crucible tongs to handle hot crucibles
- Never leave a flame unattended
- Allow equipment to cool completely before touching with bare hands
- Be aware of the fire hazards in the laboratory
- Ensure the work area is free from flammable materials
""",
    "Rate of Reaction": """
Safety precautions for working with sodium thiosulfate and hydrochloric acid:
- Wear safety goggles, lab coat, and gloves at all times
- Work in a well-ventilated area
- Handle acids with care, adding acid to water (never water to acid)
- Avoid inhaling hydrogen sulfide gas that may be produced
- Wash hands thoroughly after handling chemicals
- Dispose of waste solutions according to school regulations
""",
    "Effect of Temperature on Rate": """
Safety precautions for working with hot solutions:
- Wear safety goggles, lab coat, and appropriate gloves at all times
- Use tongs or heat-resistant gloves when handling hot containers
- Be careful when using water baths, particularly at high temperatures
- Never leave heating equipment unattended
- Allow heated solutions to cool before handling
- Use a thermometer to check temperatures, never test by touch
""",
    "Acid-Base Titration": """
Safety precautions for working with acids, bases, and pH meters:
- Wear safety goggles, lab coat, and appropriate gloves at all times
- Work in a well-ventilated area
- Handle concentrated acids and bases with extreme care
- Keep the pH electrode in suitable storage solution when not in use
- Calibrate the pH meter carefully to ensure accurate readings
- Dispose of waste solutions according to school regulations
"""
}

def get_chemistry_topics():
    """Return a list of chemistry topics"""
    return list(CHEMISTRY_TOPICS.keys())

def get_experiment_types(topic):
    """Return a list of experiment types for a given topic"""
    if topic in CHEMISTRY_TOPICS:
        return CHEMISTRY_TOPICS[topic]
    return []

def get_experiment_template(topic, experiment_type):
    """Return a template for a given topic and experiment type"""
    if topic in EXPERIMENT_TEMPLATES and experiment_type in EXPERIMENT_TEMPLATES[topic]:
        return EXPERIMENT_TEMPLATES[topic][experiment_type]
    return {
        "independent_var": "",
        "dependent_var": "",
        "controlled_vars": [],
        "methodology": "",
        "materials": []
    }

def get_safety_info(experiment_type):
    """Return safety information for a given experiment type"""
    if experiment_type in SAFETY_INFO:
        return SAFETY_INFO[experiment_type]
    return "Please research and follow all appropriate safety protocols for this experiment."
