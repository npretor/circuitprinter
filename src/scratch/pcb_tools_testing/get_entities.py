import gerber
# Does not work, use below: from gerber.render import GerberCairoContext 
from gerber.render.cairo_backend import GerberCairoContext

top_layer = './nRF52840_qiaa_var5/copper_top_l1.gtl'
bottom_layer = './nRF52840_qiaa_var5/copper_bottom_l4.gbl'

# Read gerber and Excellon files
top_copper = gerber.read(top_layer)
bottom_copper = gerber.read(bottom_layer)

# Rendering context
ctx = GerberCairoContext()

# Create SVG image
print('rendering top')
top_copper.render(ctx)
print('rendering bottom')
bottom_copper.render(ctx, 'composite.svg')