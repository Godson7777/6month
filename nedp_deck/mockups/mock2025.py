import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams['font.family']='DejaVu Sans'
FX=16000
CLS=['Light','Small','Medium','Heavy']; COL=['#C7EFD5','#6FCF97','#1E9E57','#0B4D2A']
U=[53,75,60,39]; V=[551005*FX/1e9,1777124*FX/1e9,1759387*FX/1e9,2951742*FX/1e9]
TU=sum(U); TV=sum(V)
BR={'Medium':[('Sany Palfinger',47),('XCMG',26),('Palfinger',17),('Others',10)],
    'Heavy':[('Palfinger',62),('Amco Veba',23),('XCMG',10),('Others',5)]}
BC={'Sany Palfinger':'#0B4D2A','Palfinger':'#1E9E57','XCMG':'#6FCF97','Amco Veba':'#9ADBB5','Others':'#D9D9D9'}
fig=plt.figure(figsize=(16,9),dpi=110); fig.patch.set_facecolor('white')
fig.text(.03,.94,'Indonesian Import Folding Crane 2025',fontsize=26,weight='bold')
fig.text(.03,.895,'Market of 227 units and Rp 112,6 Bio; Heavy is 17% of units but 42% of value, and Palfinger takes 62% of it',fontsize=14,weight='bold',color='#1E9E57')
fig.add_artist(plt.Line2D([.03,.97],[.875,.875],color='k',lw=2))
# ---- left: units & value twin 100% bar
ax=fig.add_axes([.05,.12,.33,.68]); ax.set_xlim(-.6,1.6); ax.set_ylim(0,1.08); ax.axis('off')
fig.text(.05,.82,'1  Market size by class, 2025',fontsize=13,weight='bold')
for k,(vals,T,fmt) in enumerate([(U,TU,lambda v:f'{v} units'),(V,TV,lambda v:f'Rp {v:,.1f} Bio'.replace('.',','))]):
    b=0; prev=[]
    for c,v,col in zip(CLS,vals,COL):
        h=v/T; ax.add_patch(Rectangle((k-.3,b),.6,h,color=col,ec='white',lw=1.5))
        ax.text(k,b+h/2,f'{fmt(v)}\n{h:.0%}',ha='center',va='center',fontsize=10.5,weight='bold',color='k' if c in('Light','Small') else 'white')
        b+=h; prev.append(b)
    if k==0: tops0=prev
    else:
        for a,bb in zip([0]+tops0,[0]+prev): ax.plot([.3,.7],[a,bb],color='grey',lw=.8)
    ax.text(k,1.03,['Units\n(227)','Value\n(Rp 112,6 Bio)'][k],ha='center',fontsize=11,weight='bold')
for i,(c,col) in enumerate(zip(CLS,COL)):
    ax.add_patch(Rectangle((1.4,.08+i*.08),.06,.05,color=col)); ax.text(1.5,.105+i*.08,c,va='center',fontsize=10)
# ---- right: marimekko class width = value, segments = brand share
ax2=fig.add_axes([.45,.12,.52,.68]); ax2.set_xlim(0,1); ax2.set_ylim(0,1.1); ax2.axis('off')
fig.text(.45,.82,'2  Who takes the cake: brand share of value by class, 2025 (width = class value)',fontsize=13,weight='bold')
x=0
for c,v in zip(CLS,V):
    w=v/TV
    ax2.text(x+w/2,1.03,f'{c}\nRp {v:,.1f} Bio ({w:.0%})'.replace('.',',',1) if False else f'{c}\nRp {str(round(v,1)).replace(".",",")} Bio · {w:.0%}',ha='center',fontsize=9.5,weight='bold')
    if c in BR:
        b=0
        for n,sh in BR[c][::-1]:
            h=sh/100; col=BC[n]; ax2.add_patch(Rectangle((x,b),w,h,color=col,ec='white',lw=1.5))
            rp=v*sh/100
            ax2.text(x+w/2,b+h/2,f'{n}\n{sh}% · Rp {str(round(rp,1)).replace(".",",")} Bio',ha='center',va='center',fontsize=9,weight='bold',
                     color='white' if col in('#0B4D2A','#1E9E57') else 'k')
            b+=h
    else:
        ax2.add_patch(Rectangle((x,0),w,1,facecolor='#F2F2F2',ec='white',lw=1.5,hatch='//',edgecolor='#BFBFBF'))
        ax2.text(x+w/2,.5,'Brand split\nnot yet\nin data',ha='center',va='center',fontsize=9,color='#6B6B6B',style='italic')
    x+=w
fig.text(.03,.05,'Source: Indonesia import records 2025, knuckle boom (folding) cranes. Value converted from USD at assumed Rp 16.000/USD. '
         'Brand shares for Medium and Heavy from earlier data cut; Light and Small brand split pending.',fontsize=9,color='#6B6B6B')
fig.savefig('mock_2025_market.png',bbox_inches='tight'); print(TU,round(TV,1),[round(v,1) for v in V])
