'''
Python version of the Doctor Who episode timeline plot
originally developed in R.

Originally written by Philip Bett, summer 2022.

'''
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image
import datetime as dt
#============================================================
# Option:
# mydevs = ["x11"]
mydevs = ["png"]



# Other constants:
DATEMIN = dt.date(1963,1,1)
DATEMAX = dt.date(2023,1,1)

# These are the exact same colours used in my old R version.
# Not all of them are have names in matplotlib, 
# so their hex codes are used instead.
DCOLS = ["black",        "mediumblue",
         "#b23aee",      "firebrick",
         "#00cd66",      "tomato",
         "violet",       "darkgoldenrod",
         "saddlebrown",  "mediumturquoise",
         "seagreen",     "#8b2252",
         "goldenrod" ]


NDOCS =  len(DCOLS) # = 13

#============================================================




#============================================================
print("Reading data...",flush=True)
df = pd.read_csv("DWAllEpisodes_to2022-04.csv", parse_dates=['Date'])
# Season	Episode	Part	Length	Date
# 	Doc1	Doc2	Doc3	Doc4	Doc5	Doc6	Doc7
# 	Doc8	Doc9	Doc10	Doc11	Doc12 	Doc13   Title
#============================================================


#============================================================
# Plot!
print("Plotting!",flush=True)
dpi = 96
xpx = 475  ;  xin = xpx/dpi
ypx = 1700 ;  yin = ypx/dpi


nrow = 2
ncol = 1

outfnames = ["DWepisodes_pythonplot." + adev for adev in mydevs]

fig = plt.figure(figsize=[xin,yin], dpi=dpi)
gs = matplotlib.gridspec.GridSpec(nrow,ncol, figure=fig,
                                  height_ratios=[1,7])

# 2 subplots. Doctor 1-13 on x-axis.

#-------------------------------------------
# Top panel: Bar chart:
# Total number of minutes in episodes with that Doctor
ax1 = fig.add_subplot(gs[0])
ax1.set_title("Doctor Who")

for doc in range(1,NDOCS+1):
    height = np.sum( df.Length[ df["Doc"+str(doc)]=="y" ] )
    ax1.bar(doc, height,width=1.0, align="center",
            color=DCOLS[doc-1], linewidth=0
    )


# Add pictures of the Doctors
for doc in range(1,NDOCS+1):
    img = matplotlib.image.imread("DWThumbs/ThumbD{:02d}a.png".format(doc))
    imgaxpos = [doc-0.5, 4700, 1,800]  # [x0,y0,w,h]
    axin = ax1.inset_axes(imgaxpos, transform=ax1.transData)
    axin.imshow(img)
    axin.axis('off')


ax1.text(5, 3500, "Total number of minutes\nin episodes with that Doctor")

ax1.set_xlabel('Doctor')
ax1.set_ylabel('Minutes')
ax1.set_xlim(0.5, NDOCS+0.5 )
ax1.set_ylim(0, 5500)
ax1.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
ax1.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1000))
ax1.tick_params(axis="y",which="both", direction="in",
                left=True,right=True, labelleft=True,labelright=True)
ax1.tick_params(axis="x",which="both", direction="in",
                top=True,bottom=True, labeltop=True, labelbottom=True)
#-------------------------------------------




#-------------------------------------------
# Bottom panel:
# Tickmarks: Each episode, where DocX=="y"
ax2 = fig.add_subplot(gs[1])

# This might be done with ax.eventplot(),
# but as we have to filter the dataframe anyway,
# we may as well do it "manually" with hlines.
for doc in range(1,NDOCS+1):
    xmin = doc-0.5
    xmax = doc+0.5
    ypoints = df.Date[ df["Doc"+str(doc)]=="y" ] 
    ax2.hlines(ypoints,xmin,xmax,
               colors=[DCOLS[doc-1]],
               linestyles="solid",
               linewidth=1.0
    )


ax2.set_xlabel('Doctor')
# ax2.set_ylabel('Date')
ax2.set_xlim(0.5, NDOCS+0.5 )
ax2.set_ylim(DATEMIN, DATEMAX)

ax2.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
ax2.yaxis.set_major_locator(matplotlib.dates.YearLocator(base=5, month=1, day=1))
ax2.yaxis.set_minor_locator(matplotlib.dates.YearLocator(base=1, month=1, day=1))
ax2.yaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
ax2.tick_params(axis="y",which="both", direction="in",
                left=True,right=True, labelleft=True,labelright=True)
ax2.tick_params(axis="x",which="both", direction="in",
                top=True,bottom=True, labeltop=False, labelbottom=True)
ax2.grid(which='both',axis='y',   linestyle='-', color='lightgrey') # silver
ax2.set_axisbelow(True)
#-------------------------------------------


#-------------------------------------------
# Finish off:
# fig.suptitle("Doctor Who")
fig.tight_layout()
fig.subplots_adjust(top=0.97, hspace=0.0)

for outfname in outfnames:
    if outfname[-3:].lower() != "x11":
        plt.savefig(outfname, dpi=dpi)
    else:
        plt.show()

plt.close()
#============================================================
print("All done.")
