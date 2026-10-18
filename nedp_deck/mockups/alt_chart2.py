import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
B=[('Sany Palfinger',30),('XCMG',14),('Palfinger',5),('Others',11)]; T=60
C=['#0B4D2A','#1E9E57','#6FCF97','#D9D9D9']
fig=plt.figure(figsize=(18,6.2),dpi=100)
# A ranked bar
ax=fig.add_axes([.03,.12,.28,.66]); ax.axis('off')
fig.text(.03,.9,'A  Ranked bar',fontsize=15,weight='bold'); fig.text(.03,.84,'Medium 2025, n of units (60)',fontsize=11,color='#6B6B6B')
for i,(n,u) in enumerate(B):
    y=3-i; ax.barh(y,u,color='#1E9E57' if i==0 else ('#BFBFBF' if n=='Others' else '#6FCF97'),height=.6)
    ax.text(-1,y,n,ha='right',va='center',fontsize=11,weight='bold' if i==0 else None)
    ax.text(u+.6,y,f'{u}  ({u/T:.0%})',va='center',fontsize=11,weight='bold')
ax.set_xlim(-14,40)
# B single 100% bar
ax=fig.add_axes([.37,.12,.27,.66]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1)
fig.text(.37,.9,'B  One 100% bar + callouts',fontsize=15,weight='bold'); fig.text(.37,.84,'Medium 2025, share of units',fontsize=11,color='#6B6B6B')
x=0
for (n,u),c in zip(B,C):
    w=u/T; ax.add_patch(Rectangle((x,.45),w,.25,color=c,ec='white',lw=2))
    ax.text(x+w/2,.575,f'{w:.0%}',ha='center',va='center',fontsize=12,weight='bold',color='white' if c in C[:2] else 'k')
    ax.plot([x+w/2,x+w/2],[.45,.3],color='grey',lw=.8); ax.text(x+w/2,.25,f'{n}\n{u} units',ha='center',va='top',fontsize=10)
    x+=w
ax.text(0,.8,'60 units  ·  Rp 28,2 Bio',fontsize=12,weight='bold')
# C units vs value per brand (bar pairs)
ax=fig.add_axes([.70,.12,.28,.66]); ax.axis('off')
fig.text(.70,.9,'C  Units vs value share per brand',fontsize=15,weight='bold'); fig.text(.70,.84,'Medium 2025, % of class',fontsize=11,color='#6B6B6B')
VS={'Sany Palfinger':47,'XCMG':26,'Palfinger':17,'Others':10}
for i,(n,u) in enumerate(B):
    y=3-i; us=round(u/T*100); vs=VS[n]
    ax.barh(y+.17,us,color='#BFBFBF',height=.32); ax.barh(y-.17,vs,color='#1E9E57',height=.32)
    ax.text(-1,y,n,ha='right',va='center',fontsize=11)
    ax.text(us+.8,y+.17,f'{us}% units',va='center',fontsize=9.5); ax.text(vs+.8,y-.17,f'{vs}% value',va='center',fontsize=9.5,weight='bold',color='#1E9E57')
ax.set_xlim(-22,70)
fig.savefig('alt_chart2.png',bbox_inches='tight')
