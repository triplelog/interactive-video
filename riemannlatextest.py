import sympy
from sympy import *
from sympy.abc import x

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
\LARGE'''

def makegraph(a,b,n,fn,framen,rtype):
	ymin = min(0,fn.evalf(subs={x: a}))
	ymax = max(0,fn.evalf(subs={x: a}))
	allValues = []
	for i in range(0,2*n+1):
		fntemp = fn.evalf(subs={x: a+i*.5*(b-a)/n})
		if rtype == 'LRAM':
			if i % 2 == 0 and i < 2*n:
				allValues.append(fntemp)
		elif rtype == 'RRAM':
			if i % 2 == 0 and i > 0:
				allValues.append(fntemp)
		elif rtype == 'MRAM':
			if i % 2 == 1:
				allValues.append(fntemp)
		if fntemp < ymin:
			ymin = fntemp
		elif fntemp > ymax:
			ymax = fntemp
			
	rectstr = ''
	for i in range(0,n):
		fillcolor = 'white'
		if i == framen - 2:
			fillcolor = 'red'
		elif i <= framen - 2:
			fillcolor = 'blue'
		if i <= framen - 2:
			yvalmin = str(0)
			yvalmax = str(allValues[i])
		elif framen == 0:
			yvalmin = str(0)
			yvalmax = str(0)
		else:
			yvalmin = str(ymin-(ymax-ymin)*.1)
			yvalmax = str(ymax+(ymax-ymin)*.1)
		rectstr += '\draw[fill='+fillcolor+', draw=black, fill opacity=0.25] ('+str(a+i*1.0*(b-a)/n)+','+yvalmin+') rectangle ('+str(a+(i+1)*1.0*(b-a)/n)+','+yvalmax+');\n'
	graphstr = r'''\begin{minipage}{.475\linewidth}
	\begin{tikzpicture}[xscale='''+str(12.0/(b-a+2.0))+r''',yscale='''+str(9.0/(1.2*ymax-1.2*ymin))+r''']
	  \draw[->] ('''+str(a-1)+r''',0) -- ('''+str(b+1)+r''',0) node[right] {$x$};
	  \draw[->] (0,'''+str(ymin-(ymax-ymin)*.1)+r''') -- (0,'''+str(ymax+(ymax-ymin)*.1)+r''') node[above] {$y$};
  
	  \draw[domain='''+str(a-1)+r''':'''+str(b+1)+r''',smooth,variable=\x,blue] plot ({\x},{'''+trigradian(str(fn).replace('x','(\\x)').replace('**','^'))+r'''});
	  '''+rectstr+r'''
	\end{tikzpicture}
	\end{minipage}\hfill'''
	return graphstr

def makeequation(a,b,n,fn,framen,rtype):
	allValues = []
	allX = []
	if rtype == 'LRAM':
		modifier = 0
	elif rtype == 'RRAM':
		modifier = 1
	elif rtype == 'MRAM':
		modifier = .5
	for i in range(0,n):
		fntemp = fn.evalf(subs={x: a+(i+modifier)*1.0*(b-a)/n})
		allValues.append(fntemp)
		allX.append(a+(i+modifier)*1.0*(b-a)/n)
	w = (float(b)-float(a))/float(n)
	if framen ==0:
		line1str = r''
	elif framen ==1:
		line1str = '\n'+r'\displaystyle\int f(x) dx & \approx\\'
	elif framen ==2:
		line1str = '\n'+r'\displaystyle\int_{'+str(a)+r'}^{'+str(b)+r'} f(x) dx & \approx\\'
	else:
		if n > 4:
			line1str = '\n'+r'\displaystyle\int_{'+str(a)+r'}^{'+str(b)+r'} f(x) dx & \approx A(r_1)+A(r_2)+\dots+A(r_{'+str(n)+r'})\\'
		elif n > 3:
			line1str = '\n'+r'\displaystyle\int_{'+str(a)+r'}^{'+str(b)+r'} f(x) dx & \approx A(r_1)+A(r_2)+A(r_3)+A(r_4)\\'
		elif n > 2:
			line1str = '\n'+r'\displaystyle\int_{'+str(a)+r'}^{'+str(b)+r'} f(x) dx & \approx A(r_1)+A(r_2)+A(r_3)\\'
		else:
			line1str = '\n'+r'\displaystyle\int_{'+str(a)+r'}^{'+str(b)+r'} f(x) dx & \approx A(r_1)+A(r_2)\\'
			
	if framen < 4:
		line2str = r''
	else:
		if n > 4:
			line2str = '\n'+r'& \approx w\cdot h(r_1)+w\cdot h(r_2)+\dots+w\cdot h(r_{'+str(n)+r'})\\'
		elif n > 3:
			line2str = '\n'+r'& \approx w\cdot h(r_1)+w\cdot h(r_2)+w\cdot h(r_3)+w\cdot h(r_4)\\'
		elif n > 2:
			line2str = '\n'+r'& \approx w\cdot h(r_1)+w\cdot h(r_2)+w\cdot h(r_3)\\'
		else:
			line2str = '\n'+r'& \approx w\cdot h(r_1)+w\cdot h(r_2)\\'
	if framen < 5:
		line3str = r''
	else:
		if n > 4:
			line3str = '\n'+r'& \approx w\cdot (h(r_1)+h(r_2)+\dots+h(r_{'+str(n)+r'}))\\'
		elif n > 3:
			line3str = '\n'+r'& \approx w\cdot (h(r_1)+h(r_2)+h(r_3)+h(r_4))\\'
		elif n > 2:
			line3str = '\n'+r'& \approx w\cdot (h(r_1)+h(r_2)+h(r_3))\\'
		else:
			line3str = '\n'+r'& \approx w\cdot (h(r_1)+h(r_2))\\'
	if framen < 6:
		line4str = r''
	elif framen <7:
		if n > 4:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(h(r_1)+h(r_2)+\dots+h(r_{'+str(n)+r'}))\\'
		elif n > 3:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(h(r_1)+h(r_2)+h(r_3)+h(r_4))\\'
		elif n > 2:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(h(r_1)+h(r_2)+h(r_3))\\'
		else:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(h(r_1)+h(r_2))\\'
	else:
		if n > 4:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(f(x_1)+f(x_2)+\dots+f(x_{'+str(n)+r'}))\\'
		elif n > 3:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(f(x_1)+f(x_2)+f(x_3)+f(x_4))\\'
		elif n > 2:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(f(x_1)+f(x_2)+f(x_3))\\'
		else:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(f(x_1)+f(x_2))\\'
	if n == 2:
		if framen < 8:
			line5str = r''
		elif framen < 9:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+f(x_2))\\'
		else:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r')\\'
		if framen < 10:
			line6str = r''
		elif framen < 11:
			line6str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0]+allValues[1],2)+r')\\'
		else:
			line6str = '\n'+r'& \approx '+cleandecimal(w*(allValues[0]+allValues[1]),3)+r'\\'
	elif n == 3:
		if framen < 8:
			line5str = r''
		elif framen < 9:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+f(x_2)+f(x_3))\\'
		elif framen < 10:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+f(x_3))\\'
		else:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+'+cleandecimal(allValues[2],2)+r')\\'
		if framen < 11:
			line6str = r''
		elif framen < 12:
			line6str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0]+allValues[1]+allValues[2],2)+r')\\'
		else:
			line6str = '\n'+r'& \approx '+cleandecimal(w*(allValues[0]+allValues[1]+allValues[2]),3)+r'\\'
	elif n == 4:
		if framen < 8:
			line5str = r''
		elif framen < 9:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+f(x_2)+f(x_3)+f(x_4))\\'
		elif framen < 10:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+f(x_3)+f(x_4))\\'
		elif framen < 11:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+'+cleandecimal(allValues[2],2)+r'+f(x_4))\\'
		else:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+'+cleandecimal(allValues[2],2)+'+'+cleandecimal(allValues[3],2)+r')\\'
		if framen < 12:
			line6str = r''
		elif framen < 13:
			line6str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0]+allValues[1]+allValues[2]+allValues[3],2)+r')\\'
		else:
			line6str = '\n'+r'& \approx '+cleandecimal(w*(allValues[0]+allValues[1]+allValues[2]+allValues[3]),2)+r'\\'
	elif n > 4:
		if framen < 8:
			line5str = r''
		elif framen < 9:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+f(x_2)+\dots+f(x_{'+str(n)+r'}))\\'
		elif framen < 10:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+\dots+f(x_{'+str(n)+r'}))\\'
		else:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+\dots+'+cleandecimal(allValues[-1],2)+r')\\'
		if framen < 11:
			line6str = r''
		elif framen < 12:
			line6str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(sum(allValues),2)+r')\\'
		else:
			line6str = '\n'+r'& \approx '+cleandecimal(w*sum(allValues),2)+r'\\'
	equationstr = r'''\begin{minipage}{.5\linewidth}
	\scalebox{1.45}{\parbox{.5\linewidth}{%
	\large
	\begin{align*}'''+line1str+line2str+line3str+line4str+line5str+line6str+r'''
	\end{align*}
	}}
	\end{minipage}'''
	return equationstr.replace('+-','-')

def maketext(a,b,n,fn,framen,rtype):
	if framen > 0:
		texta = str(a)
	else:
		texta = '??'
	if framen > 1:
		textb = str(b)
	else:
		textb = '??'
	if framen > 2:
		textn = str(n)
	else:
		textn = '??'
	if framen > 3:
		textw = str(cleandecimal((float(b)-float(a))/float(n),4))
	else:
		textw = '??'
	textstr = r'''\begin{minipage}{.475\linewidth}
	\huge
	\vspace{5pt}
	\noindent
	Approximate the area under the curve $f(x)='''+sympy.latex(fn)+r'''$ on the interval $['''+str(a)+r''','''+str(b)+r''']$ with $'''+str(n)+r'''$ rectangles of equal width using the '''+str(rtype)+r''' method.
	\begin{center}
	\begin{tabular}{ |c|c|c|c| } 
		\hline
		$a='''+texta+r'''$ & $b='''+textb+r'''$ & $n='''+textn+r'''$ & $w=\frac{b-a}{n}='''+textw+r'''$\\ 
		\hline
		\end{tabular}
	\end{center}
	\end{minipage}\hfill'''
	return textstr

def maketable(a,b,n,fn,framen,rtype):
	allValues = []
	allX = []
	if rtype == 'LRAM':
		modifier = 0
	elif rtype == 'RRAM':
		modifier = 1
	elif rtype == 'MRAM':
		modifier = .5
	for i in range(0,n):
		fntemp = fn.evalf(subs={x: a+(i+modifier)*1.0*(b-a)/n})
		allValues.append(fntemp)
		allX.append(a+(i+modifier)*1.0*(b-a)/n)
	if n > 8:
		tablesize = r'\Large'
	else:
		tablesize = ''
	colstr = '|'
	for i in range(0,n+1):
		colstr += 'c|'
	row1str = 'i'
	row2str = '$x_i$'
	row3str = '$f(x_i)$'
	row4str = '$A(r_i)$'
	for i in range(0,n):
		row1str += ' & '+str(i+1)
	for i in range(0,n):
		if i > framen - 1:
			row2str += ' & '
		else:
			row2str += ' & '+cleandecimal(allX[i],2)
	for i in range(0,n):
		if i > framen - 1 - n:
			row3str += ' & '
		else:
			row3str += ' & '+cleandecimal(allValues[i],2)
	for i in range(0,n):
		if i > framen - 1 - 2 * n:
			row4str += ' & '
		else:
			row4str += ' & '+cleandecimal(allValues[i]*(b-a)/n,2)
	tablestr = r'''\begin{minipage}{.5\linewidth}
	\huge
	\vspace{5pt}
	\begin{center}
	'''+tablesize+r'''
	\begin{tabular}{ '''+colstr+r''' } 
	 \hline
	 '''+row1str+r'''\\ 
	 \hline
	'''+row2str+r'''\\ 
	\hline
	'''+row3str+r'''\\ 
	\hline
	'''+row4str+r'''\\ 
	 \hline
	\end{tabular}
	\end{center}
	\end{minipage}
	\end{document}'''
	return tablestr
	
a = 0
b = 3.14
n = 10
fn = sympy.sympify('sin(x)*cos(x)')
rtype = 'LRAM'
if n == 2:
	maxframes = 5+4*n+1+12
elif n == 3:
	maxframes = 5+4*n+1+13
elif n == 4:
	maxframes = 5+4*n+1+14
elif n > 4:
	maxframes = 5+4*n+1+13
framen = maxframes-1
thestr = startstr

if framen < 5:
	thestr += '\n'+makegraph(a,b,n,fn,0,rtype)
elif framen < 5+n+2:
	thestr += '\n'+makegraph(a,b,n,fn,framen-4,rtype)
else:
	thestr += '\n'+makegraph(a,b,n,fn,5+n+1-4,rtype)
	
if framen < 5+4*n+2:
	thestr += '\n'+makeequation(a,b,n,fn,0,rtype)
else:
	thestr += '\n'+makeequation(a,b,n,fn,framen-5-4*n-1,rtype)
	
if framen > 4:
	thestr += '\n'+maketext(a,b,n,fn,4,rtype)
else:
	thestr += '\n'+maketext(a,b,n,fn,framen,rtype)
	
if framen < 5+n+2:
	thestr += '\n'+maketable(a,b,n,fn,0,rtype)
elif framen < 5+4*n+2:
	thestr += '\n'+maketable(a,b,n,fn,framen-5-n-1,rtype)
else:
	thestr += '\n'+maketable(a,b,n,fn,5+4*n+1,rtype)
print(thestr)