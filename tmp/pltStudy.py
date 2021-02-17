import matplotlib.pyplot as plt
import numpy as np

"""x=np.linspace(-1,1,50)
y1=2*x+1
y2=x**2


#figure
plt.figure(num=3,figsize=(8,5))


#坐标轴
#x、y轴的取值范围
plt.xlim((-1,2))
plt.ylim((-2,3))

#坐标轴名称
plt.xlabel('I am x')
plt.ylabel('I am y')
 
#设置坐标显示
new_ticks=np.linspace(-1,2,5)
print(new_ticks)
plt.xticks(new_ticks)
plt.yticks([-2,-1.8,-1,1.22,3],
           ['really bad','bad','normal','good','really good'])

#图例
line_1,=plt.plot(x,y2,label='up')
line_2,=plt.plot(x,y1,color='red',linewidth=1.0,linestyle='--',label='down')
plt.legend(handles=[line_1,line_2],labels=['aaa','bbb'],loc='best') #loc:upper、right、center
#plt.legend(handles=[line_1,],labels=['aaa',],loc='best') #loc:upper、right、center

plt.show()"""


"""x=np.linspace(-3,3,50)
y=2*x+1

plt.figure(num=1,figsize=(8,5),)
plt.plot(x,y,linewidth=2)

ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data',0))
ax.spines['left'].set_position(('data',0))

x0=1
y0=2*x0+1
#plt.scatter(x,y) 散点图
plt.scatter(x0,y0,s=50,color='b')    #s:size b:blue
plt.plot([x0,x0],[y0,0],'k--',lw=2.5)   #k:black lw:linewith

#annotation 标注

for label in ax.get_xticklabels()+ax.get_yticklabels():
    label.set_fontsize(12)
    label.set_bbox(dict(facecolor='white',edgecolor='None',alpha=0.7))
plt.show()"""

"""n=1024

X=np.random.normal(0,1,n)
Y=np.random.normal(0,1,n)

T=np.arctan2(Y,X)   #for color value

plt.scatter(X,Y,s=75,c=T,alpha=0.5) #s:size, c:color
plt.scatter(np.arange(5),np.arange(5))

plt.xlim((-1.5,1.5))
plt.ylim((-1.5,1.5))

plt.xticks(())
plt.yticks(())
plt.show()
"""

"""n=12
X=np.arange(n)
Y1=(1-X/float(n))*np.random.uniform(0.5,1.0,n)
Y2=(1-X/float(n))*np.random.uniform(0.5,1.0,n)

print(Y1)
print(Y2)

plt.bar(X,+Y1,facecolor='#9999ff',edgecolor='white')
plt.bar(X,-Y1,facecolor='#ff9999',edgecolor='white')

for x,y in zip(X,Y1):
    plt.text(x+0.4,y+0.05,'%.2f' % y,ha='center',va='bottom') #ha:horizontal alignment

for x,y in zip(X,Y2):
    plt.text(x+0.4,-y-0.05,'%-.2f' % y,ha='center',va='bottom') #ha:horizontal alignment
    
plt.xlim(-0.5,n)
plt.xticks(())
plt.ylim(-1.25,1.25)
plt.yticks(())

plt.show()"""

"""plt.figure()

plt.subplot(2,1,1)
plt.plot([0,1],[0,1])

plt.subplot(2,3,4)
plt.plot([0,1],[0,2])

plt.subplot(2,3,5)
plt.plot([0,1],[0,3])

plt.subplot(2,3,6)
plt.plot([0,1],[0,4])


plt.show()"""

import matplotlib.gridspec as gridspec

#方法1：subplot2grid
"""plt.figure()
ax1=plt.subplot2grid((3,3),(0,0),colspan=3,rowspan=1)
ax1.plot([1,2],[1,2])
ax1.set_title('ax1_titile')

ax2=plt.subplot2grid((3,3),(1,0),colspan=2,rowspan=1)

ax3=plt.subplot2grid((3,3),(1,2),colspan=1,rowspan=2)

ax4=plt.subplot2grid((3,3),(2,0),colspan=1,rowspan=1)

ax5=plt.subplot2grid((3,3),(2,1),colspan=1,rowspan=1)"""

#方法2：gridspec
"""plt.figure()
gs=gridspec.GridSpec(3,3)

ax1=plt.subplot(gs[0,:])
ax2=plt.subplot(gs[1,:2])
ax3=plt.subplot(gs[1:,2])
ax4=plt.subplot(gs[-1,0])
ax5=plt.subplot(gs[-1,-2])

#方法3：easy to define stucture
f,((ax11,ax12),(ax21,ax22))=plt.subplots(2,2,sharex=True,sharey=True)
ax11.scatter([1,2],[1,2])

plt.tight_layout()
plt.show()"""

fig=plt.figure()
x=[1,2,3,4,5,6,7]
y=[1,3,4,2,5,8,6]

left,bottom,width,height=0.1,0.1,0.8,0.8
