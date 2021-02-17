import mplfinance as mpf
import matplotlib.pyplot as plt
from cycler import cycler
import pandas as pd
import numpy as np

from matplotlib.pyplot import tight_layout
'''
Created on 2021年1月11日

@author: Administrator
'''

pd.set_option('precision', 15)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr',False)
pd.set_option('display.float_format',lambda x : '%.4f' % x)

# 解决mplfinance绘制输出中文乱码
plt.rcParams['font.sans-serif']=['SimHei'] #用来显示正常中文的标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号

def demo():
    df=pd.read_csv('../updateData/data/dailyPrice/index/000001.XSHG.csv')
    df.rename(columns={'date':'Date',
                        'open':'Open',
                       'close':'Close',
                       'low':'Low',
                       'high':'High',
                       'volume':'Volume'
                       },inplace=True)
    
    df['Date']=pd.to_datetime(df['Date'])
    df.set_index(['Date'],inplace=True)
    
    df=df[-250:]
    print(df)
    
    addPlot=[mpf.make_addplot(df['ema_20'],color='lightgray'),
             mpf.make_addplot(df['ma_20'],color='lightgray',linestyle='dotted'),
             mpf.make_addplot(df['ema_60'],color='darkorange'),
             mpf.make_addplot(df['ma_60'],color='darkorange',linestyle='dotted'),
             mpf.make_addplot(df['ema_120'],color='dodgerblue'),
             mpf.make_addplot(df['ma_120'],color='dodgerblue',linestyle='dotted'),
             mpf.make_addplot(df['mav_20'],color='y',panel='lower')]
    
    # 设置基本参数
    # type:绘制图形的类型，有candle, renko, ohlc, line等
    # 此处选择candle,即K线图
    # mav(moving average):均线类型,此处设置7,30,60日线
    # volume:布尔类型，设置是否显示成交量，默认False
    # title:设置标题
    # y_label_lower:设置成交量图一栏的标题
    # figratio:设置图形纵横比
    # figscale:设置图形尺寸(数值越大图像质量越高)
    kwargs=dict(
        type='candle',
        #mav=(20,60,120),
        volume=True,
        title=u'上证指数',
        ylabel_lower='volume',
        addplot=addPlot,
        figratio=(15,10),
        figscale=2.3
        )
    
    # 设置marketcolors
    # up:设置K线线柱颜色，up意为收盘价大于等于开盘价
    # down:与up相反，这样设置与国内K线颜色标准相符
    # edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
    # wick:灯芯(上下影线)颜色
    # volume:成交量直方图的颜色
    # inherit:是否继承，选填
    myColor=mpf.make_marketcolors(
        #up='red',
        down='green',
        #down='darkturquoise',
        edge={'up':'green','down':'green'},
        wick='i',
        #volume='in',
        volume='lightgray',
        #inherit=True,
        #ohlc='black',
        )
    
    # 设置图形风格
    # gridaxis:设置网格线位置
    # gridstyle:设置网格线线型
    # y_on_right:设置y轴位置是否在右
    myStyle=mpf.make_mpf_style(
        gridaxis='both',
        gridstyle='-.',
        y_on_right=False,
        marketcolors=myColor,
        rc={'font.family': 'SimHei'})
    
    # 设置均线颜色，配色表可见下图
    # 建议设置较深的颜色且与红色、绿色形成对比
    # 此处设置七条均线的颜色，也可应用默认设置
    """mpl.rcParams['axes.prop_cycle']=cycler(
        color=['dodgerblue', 'deeppink', 
        'navy', 'teal', 'maroon', 'darkorange', 
        'indigo'])
    
    mpl.rcParams['lines.linewidth']=.5"""
    
    # 图形绘制
    # show_nontrading:是否显示非交易日，默认False
    # savefig:导出图片，填写文件名及后缀
    mpf.plot(df,
             **kwargs,
             style=myStyle,
             show_nontrading=False)
    
class Paint():
    """
    绘制各类图形
    """
    def __init__(self,csvFile,years=1):
        #df=pd.read_csv('../updateData/data/dailyPrice/index/000001.XSHG.csv')
        df=pd.read_csv(csvFile)
        df.rename(columns={'date':'Date',
                            'open':'Open',
                           'close':'Close',
                           'low':'Low',
                           'high':'High',
                           'volume':'Volume'
                           },inplace=True)
        
        df['Date']=pd.to_datetime(df['Date'])
        df.set_index(['Date'],inplace=True)
        
        self.df=df[max(-len(df),-250*years):]
    
    def candle(self):     
        bList,sList=self.bias()
           
        """addPlot=[mpf.make_addplot(self.df[['ma_20','ma_60']]),
                 mpf.make_addplot(bList,scatter=True,markersize=200,marker='^',color='y'),
                 mpf.make_addplot(sList,scatter=True,markersize=200,marker='v',color='r')]"""
        
        """
        make_marketcolors() 设置K线的颜色
        :up 阳线的填充色；
        :down 阴线的填充色；
        :edge 蜡烛线的边沿颜色，'i'表示继承K线的颜色；
        :wick 设置蜡烛图上下影
        :volume 成交量的颜色
        :inherit 是否继承，如果设置了继承inherit=True,那么edge即便设置了颜色也会失效
        """
        
        myColor=mpf.make_marketcolors(#up='red',
                                      down='darkcyan',
                                      edge={'up':'darkcyan','down':'darkcyan'},
                                      wick='i',
                                      volume='silver')
        
       
        """
        设置图标样式 make_mpf_style
        :base_mpf_style 使用mpf系统样式，可以在make_marketcolors和make_mpf_style中使用
        :base_mpl_style 使用matplotlib的系统样式，比如base_mpl_style='seaborn'
        :marketcolors 使用自定义样式
        :facecolor 前景色
        :edgecolor 图像边缘线颜色
        :figcolor 图像外周围填充色
        :gridcolor 网络线颜色
        :gridaxis 设置网络线位置，both双向
        :gridstyle 设置网络线类型 -solid -.dashdot :dotted --dashed None 
        :y_on_right 设置坐标轴是否在右
        """
        myStyle=mpf.make_mpf_style(marketcolors=myColor,gridaxis='both',gridstyle='-.',rc={'font.family': 'SimHei'})
        
        #更新后的版本
        """addPlot=[mpf.make_addplot(self.df[['ma_20','ma_60']],panel=0,linestyle='dashdot'), #linestyle:dashdot、dotted
                 mpf.make_addplot(bList,type='scatter',marker='^',markersize=200,color='y',panel=0),  #type支持scatter、line、bar、ohlc、candle，这样副图可以画任意图像和数据了。
                 mpf.make_addplot(sList,type='scatter',marker='v',markersize=200,color='r',panel=0),
                 mpf.make_addplot(self.df['ma_120'],color='g',secondary_y='auto',panel=1),]"""
        
        addPlot=[mpf.make_addplot(self.df['ema_20'],color='gray',panel=0),
             mpf.make_addplot(self.df['ma_20'],color='gray',linestyle='dotted',panel=0),
             mpf.make_addplot(self.df['ema_60'],color='darkorange',panel=0),
             mpf.make_addplot(self.df['ma_60'],color='darkorange',linestyle='dotted',panel=0),
             mpf.make_addplot(self.df['ema_120'],color='dodgerblue',panel=0),
             mpf.make_addplot(self.df['ma_120'],color='dodgerblue',linestyle='dotted',panel=0),
             mpf.make_addplot(self.df['mav_20'],color='r',panel=1),
             #乖离率
             mpf.make_addplot(self.df['CS'],type='line',color='gray',ylabel='乖离率',panel=2),
             mpf.make_addplot(self.df['SM'],type='line',color='tomato',panel=2,secondary_y=False),
             mpf.make_addplot(self.df['ML'],type='bar',color='lightgray',panel=2,secondary_y=False)
             ]
        
        datesDf=pd.DataFrame(self.df.index)
        buyDate=pd.Timestamp('2020-06-30')
        sellDate=pd.Timestamp('2020-07-15')
        whereValues=pd.notnull(datesDf[(datesDf>=buyDate) & (datesDf<=sellDate)])['Date'].values
        #print(whereValues)
        #print(datesDf)
        
        """
        plot绘制的部分参数
        :type candle、line、ohlc、renko
        :mav 均线
        :show_nontrading=True 显示非交易日，K线之间会有间隔，False，不显示非交易日，K线之间没有间隔
        :title 设置标题
        :ylabel  主图Y轴标题
        :ylabel_lower 成交量Y轴标题
        :figratio 图形纵横比
        :figscale 图像缩小或者放大，1.5就是放大1.5倍
        :style 设置图表样式，内置有“yahoo”等样式，也可以自定义样式
        :savefig 导出图片
        """
        mpf.plot(self.df,type='candle',
                 volume=True,
                 addplot=addPlot,
                 style=myStyle,
                 figscale=1.5,
                 figratio=(15,10),
                 title='上证指数',  #中文显示有问题
                 ylabel='价格',
                 ylabel_lower='成交量',
                 
                 xrotation=0,
                 datetime_format='%Y-%m-%d',
                 tight_layout=True,
                 
                 main_panel=0,
                 volume_panel=1,
                 
                 #fill_between=self.df['Close'].values,
                 #fill_between=dict(y1=self.df['Close'].values,alpha=0.5,color='g'),
                 #fill_between=dict(y1=3200,y2=self.df['Close'].values,alpha=0.5,color='g'),
                 #fill_between=dict(y1=self.df['Close'].values,y2=self.df['ma_60'].values,alpha=0.5,
                 #fill_between=dict(y1=self.df['Close'].values,where=whereValues,alpha=0.5),
                )
    def bias(self):#,data:pd.DataFrame):
        """
        简单的数据分析，并返回数据分析结果列表，分析的逻辑不重要，关键是看如何绘制图形。
        简单逻辑：向下乖离率即（Close-ma_20)/ma_20<-0.1,那么买入；向上乖离率即(Close-ma_20)/ma_20>0.1,则买入。
        """
        #if data.shape[0]==0:
        #    data=self.df
        sList=[]
        bList=[]
        b=-1
        
        for i,v in self.df['Close'].iteritems():
            if (v-self.df['ma_20'][i])/self.df['ma_20'][i]>0.1 and (b==-1 or b==0):
                sList.append(v)
                b=1
            else:
                sList.append(np.nan)
                
            if(v-self.df['ma_20'][i])/self.df['ma_20'][i]<-0.1 and (b==-1 or b==1):
                bList.append(v)
                b=0
            else:
                bList.append(np.nan)
            
        return (bList,sList)
                
    def priceMovement(self):
        df=self.df[-50:]
        
        
        mpf.plot(df,type='candle') 
        mpf.plot(df,type='renko')  
        mpf.plot(df,type='pnf')
        
        
        
    def candleMpfStyle(self):
        print(mpf.available_styles())
        #mpf.plot(self.df,type='candle',style='mike')
        
        #继承系统样式，并做局部修改
        #myColor=mpf.make_marketcolors(up='cyan',down='red',inherit=True)
        #myStyle=mpf.make_mpf_style(base_mpf_style='blueskies',marketcolors=myColor,gridaxis='both',gridstyle='-.',y_on_right=True)
        
        #mpf.plot(self.df,type='candle',style=myStyle)
        kwargs=dict(type='candle',mav=(20,60,120),volume=True,title='报价',ylabel='price',ylabel_lower='volume',figratio=(10,8),figscale=1.5,linecolor='g')
        mpf.plot(self.df,**kwargs,style='checkers')
        

if __name__=="__main__":
    pObj=Paint('../updateData/data/dailyPrice/index/000001.XSHG.csv')
    #pObj=Paint('../updateData/data/dailyPrice/stock/000001.XSHE.csv')
    #print(pObj.candle())
    #pObj.candleMpfStyle()
    #pObj.candle()
    #pObj.priceMovement()
    pObj.candle()
    