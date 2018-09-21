import sympy
from sympy import *
from sympy.abc import x
import sys

    
def cleandecimal(inputval,maxd):
	rval = str(round(inputval,maxd))
	while rval.find('.') > -1 and (rval[-1] == '0' or rval[-1] == '.'):
		rval=rval[:-1]
	return rval

def trigradian(rawfn):
	index = rawfn.find('(')
	if index == -1:
		return rawfn
	elif index < 3:
		return rawfn[:index+1]+trigradian(rawfn[index+1:])
	else:
		if rawfn[index-3:index] in ['sin','cos','tan','cot','sec','csc']:
			indexf = index
			npars = 1
			indexr = -1
			while npars > 0 and index < len(rawfn) - 1:
				index += 1
				if rawfn[index] == '(':
					npars += 1
				elif rawfn[index] == ')':
					npars -= 1
				if npars == 0:
					indexr = index
			if indexr > -1:
				rawfn = rawfn[:indexr]+' r'+rawfn[indexr:]
			return rawfn[:indexf+1]+trigradian(rawfn[indexf+1:])
		else:
			return rawfn[:index+1]+trigradian(rawfn[index+1:])		
					
startstr = r'''\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

\usetikzlibrary{shapes.geometric, arrows}


\begin{document}
\huge'''

def makegraph(fn,x0,framen):
	y0 = fn.evalf(subs={x: x0})
	ymin = fn.evalf(subs={x: x0-2.5})
	ymax = ymin
	for i in range(0,21):
		fntemp = fn.evalf(subs={x: x0-1+i*5.0/20})
		if fntemp < ymin:
			ymin = fntemp
		elif fntemp > ymax:
			ymax = fntemp
	xaxisstr = r'''\draw[->] ('''+str(x0-2.5)+r''',0) -- ('''+str(x0+2.5)+r''',0) node[right] {$x$};'''
	yaxisstr = r'''\draw[->] (0,'''+str(ymin-(ymax-ymin)*.1)+r''') -- (0,'''+str(ymax+(ymax-ymin)*.1)+r''') node[above] {$y$};'''
	if x0 < -2.5 or x0 > 2.5:
		yaxisstr = ''
	if ymin-(ymax-ymin)*.1 >0 or ymax+(ymax-ymin)*.1 < 0:
		xaxisstr = ''
	graphstr = r'''\begin{center}
		\begin{tikzpicture}[xscale=1,yscale='''+str(5.0/(1.2*ymax-1.2*ymin))+r''']
		  '''+xaxisstr+r'''
		  '''+yaxisstr+r'''
		  
		  \draw[domain='''+str(x0-2.5)+r''':'''+str(x0+2.5)+r''',smooth,variable=\x,blue] plot ({\x},{'''+trigradian(str(fn).replace('x','(\\x)'))+r'''});
		  \draw[fill,red] ('''+str(x0)+r''','''+str(y0)+r''') circle (.05);
		\end{tikzpicture}
		\end{center}
	\end{minipage}

	\end{document}'''
	return graphstr

def maketext(fn,x0,framen,dfn,dfnx0,y0):
	
	derivativestr = r''
	if framen > 0:
		derivativestr = sympy.latex(dfn)+r'''\\'''
		
	plugstr = r''
	if framen == 2:
		plugstr = r'''f'(x_0) & ='''+r'''\\'''
	elif framen > 2:
		plugstr = r'''f'(x_0) & ='''+sympy.latex(dfn.subs(x,x0))+r'''\\'''
		
	evalstr = r''
	if framen == 4:
		evalstr = r'''f'(x_0) & ='''+r'''\\'''
	elif framen > 4:
		evalstr = r'''f'(x_0) & ='''+cleandecimal(dfnx0,5)+r'''\\'''
		
	yplugstr = r''
	if framen == 6:
		yplugstr = r'''y_0 & ='''+r'''\\'''
	elif framen > 6:
		yplugstr = r'''y_0 & ='''+sympy.latex(fn.subs(x,x0))+r'''\\'''
		
	yevalstr = r''
	if framen == 8:
		yevalstr = r'''y_0 & ='''+r'''\\'''
	elif framen > 8:
		yevalstr = r'''y_0 & ='''+cleandecimal(y0,5)+r'''\\'''
	textstr = r'''\begin{minipage}{.575\linewidth}
		\begin{center}
			Find the equation of the tangent line to the curve $f(x)='''+sympy.latex(fn)+r'''$ at $x='''+str(x0)+r'''$.
		\end{center}
		\scalebox{1.95}{\parbox{.575\linewidth}{%
			\large
			\begin{align*}
		f'(x) & = '''+derivativestr+plugstr+evalstr+yplugstr+yevalstr+r'''
			\end{align*}
			}}
			\end{minipage}\hfill'''
	return textstr

def makelist(fn,x0,framen,dfn,dfnx0,y0):
	y0str = r'f(x_0)'
	if framen > 3:
		y0str = cleandecimal(y0,5)
		
	x0str = r'f(x_0)'
	if framen > 0:
		x0str = str(x0)
	
	dfnstr = r''
	if framen > 1:
		dfnstr = sympy.latex(dfn)
	
	mstr = r'''f'(x_0)'''
	if framen > 2:
		mstr = cleandecimal(dfnx0,5)
	liststr = r'''\begin{minipage}{.4\linewidth}
			\scalebox{1.95}{\parbox{.4\linewidth}{%
			\large
			\begin{align*}
		x_0 & = '''+x0str+r'''\\
		y_0 & = '''+y0str+r'''\\
		f'(x) & = '''+dfnstr+r'''\\
		m & = '''+mstr+r'''\\
		y & = m(x-x_0)+y_0\\
			\end{align*}
			}}'''
	return liststr
	
fn = sympy.sympify('sin(x)')
x0 = 2
framen = int(sys.argv[1])
thestr = startstr

dfn = sympy.diff(fn)
dfnx0 = dfn.evalf(subs={x:x0})
y0 = fn.evalf(subs={x:x0})
thestr += '\n'+maketext(fn,x0,framen,dfn,dfnx0,y0)
thestr += '\n'+makelist(fn,x0,framen,dfn,dfnx0,y0)
thestr += '\n'+makegraph(fn,x0,framen)

print(thestr)