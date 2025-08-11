import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mplsoccer import VerticalPitch
import matplotlib.image as mpimg

# Set up the figure and grid
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(2, 2, height_ratios=[4, 1], hspace=0.2)

# Pitches (side by side)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

# Draw vertical StatsBomb-style pitches
pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2)
pitch.draw(ax=ax1)
pitch.draw(ax=ax2)
ax1.set_title("England Women's, Starting Eleven", fontsize=12, loc='left')
ax2.set_title("Spain Women's, Starting Eleven", fontsize=12, loc='left')

# Legends row (spanning both columns)
legend_ax = fig.add_subplot(gs[1, :])
legend_ax.axis('off')  # Hide axes

# --- Custom circles legend ---
circle_sizes = [5, 10, 15, 20]
# circle_x = [0.35, 0.43, 0.51, 0.59]  # more compact horizontally
circle_x = [0.43, 0.47, 0.51, 0.55]
circle_y = 0.75  # higher up
for x, s in zip(circle_x, circle_sizes):
    legend_ax.plot(x, circle_y, 'o', color='k', markersize=s, clip_on=False)
# Arrow under circles
legend_ax.annotate(
    '', xy=(circle_x[0], circle_y-0.2), xytext=(circle_x[-1], circle_y-0.2),
    arrowprops=dict(arrowstyle='<-', lw=1, color='k'), annotation_clip=False
)
legend_ax.text(circle_x[0], circle_y-0.25, '1 pass', ha='center', va='top', fontsize=11)
legend_ax.text(circle_x[-1], circle_y-0.25, '100+ passes', ha='center', va='top', fontsize=11)

# --- Custom lines legend ---
line_widths = [1, 2, 4, 6]
# line_x = [0.37, 0.45, 0.53, 0.61]  
line_x = [0.43, 0.47, 0.51, 0.55]# more compact horizontally
line_y = 0.15  # lower down for separation
for x, lw in zip(line_x, line_widths):
    legend_ax.plot(
        # [x-0.025, x+0.025], [line_y-0.025, line_y+0.025], color='k', lw=lw, solid_capstyle='round', clip_on=False
        [x-0.0125, x+0.0125], [line_y-0.02165, line_y+0.02165], color='k', lw=lw, solid_capstyle='round', clip_on=False    
    )
# Arrow under lines
legend_ax.annotate(
    '', xy=(line_x[0], line_y-0.15), xytext=(line_x[-1], line_y-0.15),
    arrowprops=dict(arrowstyle='<-', lw=1, color='k'), annotation_clip=False
)
legend_ax.text(line_x[0], line_y-0.2, '4 passes', ha='center', va='top', fontsize=11)
legend_ax.text(line_x[-1], line_y-0.2, '40+ passes', ha='center', va='top', fontsize=11)

# Set limits for neatness
legend_ax.set_xlim(0, 1)
legend_ax.set_ylim(0, 1)

# Titles (using fig.text for flexible placement)
fig.text(0.01, 0.97, "Passing Network", fontsize=16, fontweight='bold', va='top', ha='left')
fig.text(0.99, 0.97, "England Women's 1 - 1 Spain Women's 2025-07-27\nUEFA Women's Euro 2025",
         fontsize=12, va='top', ha='right')

# Add branding icon between pitches
branding_img = mpimg.imread('./Euro_Women/logo.png')  
logo_ax = fig.add_axes([0.43, 0.5, 0.15, 0.15], anchor='C', zorder=10)  # [left, bottom, width, height] in 0-1
logo_ax.imshow(branding_img)
logo_ax.axis('off')

plt.show()