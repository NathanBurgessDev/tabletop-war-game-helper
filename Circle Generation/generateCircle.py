import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math


# Data to plot
# labels = ['Python', 'C++', 'Ruby', 'Java']
sizes = []

for i in range (0,20):
    sizes.append(1)
    
labels_gender = ['Man','Woman','Man','Woman','Man','Woman','Man','Woman']
sizes_gender = [1]
weight_gender = [189,315,270,212,125,145,200,80]
colors = ['#ff0000', '#ffffff', '#000000', '#ffffff','#000000']
colors_gender = ['#FFFF00']
 
# Plot
plt.pie(sizes, colors=colors, startangle=90,frame=True)
plt.pie(sizes_gender,colors=colors_gender,radius=0.75,startangle=90)

centre_circle = plt.Circle((0,0),0.6,color='black', fc='white',linewidth=0)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
 
fig.set_facecolor("white")
plt.axis('equal')
plt.tight_layout()
plt.show()