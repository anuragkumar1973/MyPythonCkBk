"""
Architecture Diagram Generator for Agent007 Azure Foundry Integration
Creates a visual representation of the platform architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set up the figure and style
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(1, 1, figsize=(16, 12), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Color scheme
color_cloud = '#0078D4'      # Azure Blue
color_foundry = '#8661C5'    # Foundry Purple
color_agent = '#107C10'      # Agent Green
color_data = '#FF8C00'       # Data Orange
color_pipeline = '#E74C3C'   # Pipeline Red
color_util = '#95A5A6'       # Utility Gray

# Helper function to create boxes
def create_box(ax, x, y, width, height, label, color, fontsize=10, fontweight='normal'):
    """Create a styled box with label"""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.05", 
        edgecolor='black', 
        facecolor=color, 
        alpha=0.8,
        linewidth=2
    )
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center', 
            fontsize=fontsize, fontweight=fontweight, 
            wrap=True, color='white')

# Helper function to create arrows
def create_arrow(ax, x1, y1, x2, y2, label='', style='->'):
    """Create an arrow between two points"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=20, 
        linewidth=2, color='black', alpha=0.7
    )
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + 0.15, mid_y + 0.15, label, 
                fontsize=8, bbox=dict(boxstyle='round', 
                facecolor='white', alpha=0.8))

# Title
ax.text(5, 9.6, 'Agent007: Azure Foundry Platform Architecture', 
        ha='center', va='center', fontsize=18, fontweight='bold')

# ============ LAYER 1: Cloud Infrastructure (Top) ============
ax.text(0.3, 9, 'Cloud Infrastructure Layer', fontsize=11, fontweight='bold', 
        bbox=dict(boxstyle='round', facecolor=color_cloud, alpha=0.3))

create_box(ax, 2, 8.3, 1.2, 0.5, 'Azure\nSubscription', color_cloud)
create_box(ax, 4, 8.3, 1.2, 0.5, 'Resource\nGroup', color_cloud)
create_box(ax, 6, 8.3, 1.2, 0.5, 'Storage\nAccount', color_cloud)
create_box(ax, 8, 8.3, 1.2, 0.5, 'Key Vault', color_cloud)

create_arrow(ax, 2, 8.05, 2, 7.6)
create_arrow(ax, 4, 8.05, 4, 7.6)
create_arrow(ax, 6, 8.05, 6, 7.6)
create_arrow(ax, 8, 8.05, 8, 7.6)

# ============ LAYER 2: Azure Foundry Core ============
ax.text(0.3, 7.4, 'Azure Foundry Core', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor=color_foundry, alpha=0.3))

create_box(ax, 2, 7, 1.4, 0.6, 'Foundry\nWorkspace', color_foundry, fontsize=9)
create_box(ax, 4, 7, 1.4, 0.6, 'Spark\nCluster', color_foundry, fontsize=9)
create_box(ax, 6, 7, 1.4, 0.6, 'Delta Lake\nCatalog', color_foundry, fontsize=9)
create_box(ax, 8, 7, 1.4, 0.6, 'Foundry\nClient', color_foundry, fontsize=9)

create_arrow(ax, 2.7, 7, 3.3, 7, '← Integration →')
create_arrow(ax, 4.7, 7, 5.3, 7, '← Via Spark →')
create_arrow(ax, 6.7, 7, 7.3, 7, '← API →')

# ============ LAYER 3: Agent System (Middle-Upper) ============
ax.text(0.3, 6.2, 'Agent System (src/agents/)', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor=color_agent, alpha=0.3))

create_box(ax, 1.2, 5.5, 1.2, 0.6, 'BaseAgent\n(Abstract)', color_agent, fontsize=9)
create_box(ax, 2.8, 5.5, 1.2, 0.6, 'HostedAgent\n(Concrete)', color_agent, fontsize=9)
create_box(ax, 4.4, 5.5, 1.2, 0.6, 'Agent\nOrchestrator', color_agent, fontsize=9)
create_box(ax, 6, 5.5, 1.2, 0.6, 'Agent\nExamples', color_agent, fontsize=9)

# Agent hierarchy arrows
create_arrow(ax, 1.8, 5.2, 2.2, 5.2, '')
create_arrow(ax, 2.8, 5.2, 3.8, 5.2, '')
create_arrow(ax, 5, 5.2, 5.5, 5.2, '')

# Connection to Foundry
create_arrow(ax, 2.8, 5.2, 4, 5.9, 'uses')
create_arrow(ax, 4.4, 5.2, 6.5, 5.9, 'manages')

# ============ LAYER 4: Data Processing (Middle) ============
ax.text(0.3, 4.7, 'Data Processing Layer', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor=color_pipeline, alpha=0.3))

create_box(ax, 1.5, 4, 1.3, 0.6, 'Sample\nPipeline', color_pipeline, fontsize=9)
create_box(ax, 3.2, 4, 1.3, 0.6, 'Data\nTransforms', color_pipeline, fontsize=9)
create_box(ax, 4.9, 4, 1.3, 0.6, 'Data\nCleaning', color_pipeline, fontsize=9)
create_box(ax, 6.6, 4, 1.3, 0.6, 'Data\nFiltering', color_pipeline, fontsize=9)
create_box(ax, 8.3, 4, 1.3, 0.6, 'Results\nAggregation', color_pipeline, fontsize=9)

create_arrow(ax, 2.15, 4, 2.65, 4, '')
create_arrow(ax, 3.85, 4, 4.25, 4, '')
create_arrow(ax, 5.55, 4, 5.95, 4, '')
create_arrow(ax, 7.25, 4, 7.65, 4, '')

# Connection from agents to data layer
create_arrow(ax, 2.8, 5.2, 1.5, 4.3, 'executes')
create_arrow(ax, 4.4, 5.2, 3.2, 4.3, 'orchestrates')

# ============ LAYER 5: Data Storage (Middle-Lower) ============
ax.text(0.3, 3.2, 'Data Storage & Management', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor=color_data, alpha=0.3))

create_box(ax, 1.8, 2.5, 1.3, 0.6, 'Raw\nData', color_data, fontsize=9)
create_box(ax, 3.6, 2.5, 1.3, 0.6, 'Processed\nData', color_data, fontsize=9)
create_box(ax, 5.4, 2.5, 1.3, 0.6, 'Delta\nTables', color_data, fontsize=9)
create_box(ax, 7.2, 2.5, 1.3, 0.6, 'Metadata\nCatalog', color_data, fontsize=9)

create_arrow(ax, 1.5, 4, 1.8, 2.8, '')
create_arrow(ax, 3.2, 4, 3.6, 2.8, '')
create_arrow(ax, 4.9, 4, 5.4, 2.8, '')
create_arrow(ax, 6.6, 4, 7.2, 2.8, '')

# Delta Lake connection
create_arrow(ax, 5.4, 5.5, 5.4, 2.8, 'manages', style='<->')

# ============ LAYER 6: Integration & Utilities (Lower) ============
ax.text(0.3, 1.8, 'Integration & Utilities', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor=color_util, alpha=0.3))

create_box(ax, 1.5, 1.2, 1.2, 0.5, 'Config\nManager', color_util, fontsize=9)
create_box(ax, 3, 1.2, 1.2, 0.5, 'Logger\nService', color_util, fontsize=9)
create_box(ax, 4.5, 1.2, 1.2, 0.5, 'Azure SDK\nIntegration', color_util, fontsize=9)
create_box(ax, 6, 1.2, 1.2, 0.5, 'Spark\nSession', color_util, fontsize=9)
create_box(ax, 7.5, 1.2, 1.2, 0.5, 'PySpark\n4.1.1', color_util, fontsize=9)

# Cross-layer connections
create_arrow(ax, 1.5, 1.475, 1.5, 1.95, '')
create_arrow(ax, 3, 1.475, 3, 1.95, '')
create_arrow(ax, 4.5, 1.475, 4.5, 1.95, '')
create_arrow(ax, 6, 1.475, 6, 1.95, '')
create_arrow(ax, 7.5, 1.475, 7.5, 1.95, '')

# ============ Data Flow Diagram (Right side) ============
ax.text(8.7, 6.5, 'Data Flow', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

flow_items = [
    ('1. Input Data', 8.7, 6.1),
    ('2. Clean & Transform', 8.7, 5.7),
    ('3. Filter Records', 8.7, 5.3),
    ('4. Aggregate Results', 8.7, 4.9),
    ('5. Store in Delta', 8.7, 4.5),
]

for label, x, y in flow_items:
    ax.text(x, y, label, fontsize=8, 
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

for i in range(len(flow_items) - 1):
    create_arrow(ax, flow_items[i][1], flow_items[i][2] - 0.15, 
                flow_items[i+1][1], flow_items[i+1][2] + 0.15, style='->')

# ============ Legend/Key Technologies (Bottom) ============
ax.text(5, 0.5, 'Key Technologies: Apache Spark 4.1.1 • Delta Lake • PySpark • Azure SDK • OpenJDK 17 • Python 3.13.7', 
        ha='center', fontsize=9, style='italic',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Add version info
ax.text(5, 0.05, 'Agent007 Multi-Agent Architecture | Azure Foundry Integration | Generated May 2026', 
        ha='center', fontsize=8, style='italic', color='gray')

plt.tight_layout()
plt.savefig('/Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007/multiagent.png', 
            bbox_inches='tight', dpi=300, facecolor='white', edgecolor='none')
print("✓ Architecture diagram created successfully: multiagent.png")
print("✓ Location: /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007/multiagent.png")
print("✓ Dimensions: High-resolution (300 DPI)")
print("✓ Layers visualized:")
print("  - Cloud Infrastructure (Azure resources)")
print("  - Azure Foundry Core (Workspace, Spark, Delta, Client)")
print("  - Agent System (BaseAgent, HostedAgent, Orchestrator, Examples)")
print("  - Data Processing (Pipelines and transforms)")
print("  - Data Storage (Raw, Processed, Delta Tables, Metadata)")
print("  - Integration & Utilities (Config, Logger, Azure SDK, Spark)")
plt.close()
