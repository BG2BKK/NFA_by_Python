import os
import pygraphviz as pgv

NonTerminal = 'ABCDEFGHIJKLMNSOPQRTUVWXYZ'
Terminal='abcdefghijklmnopqrstuvwxyz1234567890!'
Operation = '+*|.'
Stackbet = Terminal+NonTerminal+'|!'
StartSymbol = 'S'


class	nfa:
	exp = ''
	lef_bra = []
	rig_bra = []
	RuleSets = {}
	usedVar = ['S']
	unusedVar = list(NonTerminal)
	count = 2
	RuleNFA = {1:[{2:StartSymbol}]}
	RuleDFA = {}
	zero = [1]

	def	setExp(self,exp):
		self.exp = exp

	def	printExp(self):
		print self.exp

	def	getBra(self,exp):
		self.lef_bra = []
		self.rig_bra = []
		for c in range(len(exp)):
			if exp[c] == '(':
				self.lef_bra.append(c)
			elif exp[c] == ')':
				self.rig_bra.append(c)


	def	printBra(self):
		print self.lef_bra
		print self.rig_bra


	def	rmBra(self):
	#	print 'rmBra'
		self.getBra(self.exp)
		exp = self.exp
		if self.rig_bra == []:
			self.RuleSets[StartSymbol] = exp
		while self.rig_bra != []:
			rig_bra = self.rig_bra
			lef_bra = self.lef_bra
			for i in range(len(rig_bra)):
				for j in range(len(lef_bra)):
					if rig_bra[i] > lef_bra[j]:
						if len(rig_bra) == 1 and len(lef_bra) == 1:
							#the brakets have been all eliminated
							#and this the last pair of brakets
							#do as the same as showed below
							var = self.unusedVar[0]
							if var == 'S':
								del self.unusedVar[0]
								var = self.unusedVar[0]
							reg = exp[lef_bra[j-1]+1:rig_bra[i]]
							self.usedVar.append(self.unusedVar[0])
							exp = exp.replace(exp[lef_bra[j-1]:rig_bra[i]+1],var)
							del self.unusedVar[0]
							self.RuleSets[var]=reg
							self.RuleSets[StartSymbol]=exp
						#if it's not the last right braket,just pass and wait for a right braket
						pass
					else:
						#get a unused variable from Nonterminal
						var = self.unusedVar[0]
						if var == 'S':
								del self.unusedVar[0]
								var = self.unusedVar[0]
						#get the set derivated by var
						reg = exp[lef_bra[j-1]+1:rig_bra[i]]
						#add the new var into the usedVar list
						self.usedVar.append(self.unusedVar[0])
						#to change the exp after replace a set by the new Var
						exp = exp.replace(exp[lef_bra[j-1]:rig_bra[i]+1],var)
						#delete the new var from unusedVar list
						del self.unusedVar[0]
						#add the new rule into the RuleSets
						self.RuleSets[var]=reg
						#just deal with one pair of braket,then detect brakets again by getBar(exp)
						break
				#just break to check brakets again
				break
			#check brakets again before enter the while-loop again
			self.getBra(exp)
		#print the result by getBra(exp)
		#print self.RuleSets

	def	rmStar(self):
#		print 'rmStar'
		RuleSets ={} 
		for r in self.RuleSets:
			RuleSets[r] = self.RuleSets[r]
		for r in RuleSets:
			star = '*' in self.RuleSets[r]
			while star == True:
				rule = self.RuleSets[r]
				for c in rule:
					if c == '*':
						#if c == *,then charactor before c will be the form A*,so We can replace 
						#A* with a new var B and change A* to B->BA|!
						t = rule.index('*')
						#get a unused Var B to change A*
						var = self.unusedVar[0]
						if var == 'S':
								del self.unusedVar[0]
								var = self.unusedVar[0]

						#change A* to B-> A*
						self.RuleSets[var]=rule[t-1:t+1]
						#update the changed rule
						rule = rule.replace(rule[t-1:t+1],var)
						#update the RuleSets with the changed rule
						newRule = {r:rule}
						self.RuleSets.update(newRule)
						#add the new Var into the usedVar list
						self.usedVar.append(self.unusedVar[0])
						#delete the new Var from unusedVar list
						del self.unusedVar[0]
						break
				star = '*' in self.RuleSets[r]
		#print the new RuleSets
#		print self.RuleSets

	def	rmAdd(self):
		#print 'rmAdd'
		RuleSets ={} 
		for r in self.RuleSets:
			RuleSets[r] = self.RuleSets[r]
		for r in RuleSets:
			add = '+'in self.RuleSets[r]
			while add == True:
				rule = self.RuleSets[r]
				for c in rule:
					if c == '+':
						#if c == +,then charactor before c will be the form A+,so We can replace 
						#A* with a new var B and change A+ to B->BA|A
						t = rule.index('+')
						#get a unused Var B to change A+
						var = self.unusedVar[0]
						if var == 'S':
								del self.unusedVar[0]
								var = self.unusedVar[0]

						#change A+ to B-> A+
						self.RuleSets[var]=rule[t-1:t+1]
						#update the changed rule
						rule = rule.replace(rule[t-1:t+1],var)
						#update the RuleSets with the changed rule
						newRule = {r:rule}
						self.RuleSets.update(newRule)
						#add the new Var into the usedVar list
						self.usedVar.append(self.unusedVar[0])
						#delete the new Var from unusedVar list
						del self.unusedVar[0]
						break
				add = '+' in self.RuleSets[r]
		#print the new RuleSets
		#print self.RuleSets

	def	rmBeg(self):
		#print 'rmBeg'
		rule = self.RuleSets[StartSymbol]
		if '^' in rule:
			if rule[-1] == '^':
				var = self.unusedVar[0]
				if var == 'S':
					del	self.unusedVar[0]
					var = self.unusedVar[0]
				del	self.unusedVar[0]
				newvar = self.unusedVar[0]
				if newvar == 'S':
					del	self.unusedVar[0]
					newvar = self.unusedVar[0]
				del	self.unusedVar[0]
				rule = rule.replace('^',var)
				x = {StartSymbol:rule}
				self.RuleSets.update(x)
				
				self.RuleSets[var]=var+newvar+'|!'
				self.RuleSets[newvar]='.'
				#print 'armBeg',self.RuleSets[var],self.RuleSets[newvar]
				#print var,newvar

			else:
				rule = rule.replace('^','')
				newRule = {StartSymbol:rule}
				self.RuleSets.update(newRule)
		#print self.RuleSets

	def	rmTai(self):
		#print 'rmTai'
		rule = self.RuleSets[StartSymbol]
		if '$' in rule:
			if rule[-1] == '$':
				var = self.unusedVar[0]
				if var == 'S':
					del	self.unusedVar[0]
					var = self.unusedVar[0]
				del	self.unusedVar[0]
				newvar = self.unusedVar[0]
				if newvar == 'S':
					del	self.unusedVar[0]
					newvar = self.unusedVar[0]
				del	self.unusedVar[0]
				rule = rule.replace('$','')
				rule = var+rule
				x = {StartSymbol:rule}
				self.RuleSets.update(x)
				
				self.RuleSets[var]=var+newvar+'|!'
				self.RuleSets[newvar]='.'
				#print 'armBeg',self.RuleSets[var],self.RuleSets[newvar]
				#print var,newvar

			else:
				rule = rule.replace('$','')
				newRule = {StartSymbol:rule}
				self.RuleSets.update(newRule)
		#print self.RuleSets

	def	genRule(self):
		self.rmBra()
		self.rmBeg()
		self.rmTai()
		self.rmStar()
		self.rmAdd()


	def	checkTerm(self):
		#print 'checkTerm'
		for i in self.RuleNFA:
			dt = self.RuleNFA[i]
			for r in dt:
				#print dt
				#print r
				for c in r:
					#print c
					for rule in r[c]:
						if rule in NonTerminal:
							return True
		return False

	def	checkExp(self,exp):
		#print 'checkExp'
		for r in exp:
			if r in NonTerminal:
				return True
		return False

	def	copyRule(self,rule):
		#print 'copyRule'
		Rule = {}
		for r in rule:
			subNFA = rule[r]
			subRule = []
			#print 'copyRule',r
			for e in subNFA:
				#print e
				#print subNFA
				subsubRule = {}
				for t in e:
					#print t
					#print e[t]
					subsubRule[t]=e[t]
				subRule.append(subsubRule)
			Rule[r] = subRule
		#print 'end Copy'
		return Rule

	def	genNFA(self):
		RuleSets = self.RuleSets
		s_count  = 0
		e_count  = 0
		while self.checkTerm():
			RuleNFA=self.copyRule(self.RuleNFA)
			#print RuleNFA
			for r in RuleNFA:
				for sub in RuleNFA[r]:
					#print sub
					for e in sub:
						rule = sub[e]
						if self.checkExp(rule):
							exp = RuleSets[rule[0]]
							if '+' in exp:
								self.count += 1
								s_count = self.count
								self.count += 1
								e_count = self.count
								self.RuleNFA[s_count]=[{e_count:exp[0]}]
								tmp = [{e:'!'},{s_count:'!'}]
								self.RuleNFA[e_count]=tmp
								tmp = [{s_count:'!'}]
								self.RuleNFA[r]=tmp
								#print 'New Rules ',self.RuleNFA

				
							elif '*' in exp:
								self.count += 1
								s_count = self.count
								self.count += 1
								e_count = self.count
								self.RuleNFA[s_count]=[{e_count:exp[0]}]
								tmp = [{e:'!'},{s_count:'!'}]
								self.RuleNFA[e_count]=tmp
								tmp = [{e:'!'},{s_count:'!'}]
								self.RuleNFA[r]=tmp
								#print 'New Rules ',self.RuleNFA
							elif '|' in exp:
								#print '|||||'
								self.count +=1
								s1=self.count
								self.count +=1
								e1=self.count
								self.count +=1
								s2=self.count
								self.count +=1
								e2=self.count
								index = exp.find('|')
								self.RuleNFA[r].remove({e:rule[0]})
								self.RuleNFA[s1]=[{e1:exp[index-1]}]
								self.RuleNFA[s2]=[{e2:exp[index+1]}]
								self.RuleNFA[r].append({s1:'!'})
								self.RuleNFA[r].append({s2:'!'})
								self.RuleNFA[e1]=[{e:'!'}]
								self.RuleNFA[e2]=[{e:'!'}]
								#print self.RuleNFA
						#	elif '.' in exp:
						#		print '|'
							else:
								self.count += 1
								s_count = self.count
								self.RuleNFA[r]=[]
								self.RuleNFA[r].append({s_count:'!'})
								for t in exp:
									self.count += 1
									e_count = self.count
									#print 's_count ',t,e_count
									if self.RuleNFA.has_key(s_count):
										x = self.RuleNFA[s_count]
										x = x.append({e_count:t})
										self.RuleNFA[s_count].append(x)
									else:
										self.RuleNFA[s_count]=[{e_count:t}]
									s_count = e_count
								if self.RuleNFA.has_key(e_count):
									x=self.RuleNFA[e_count]
									x=x.append({e:'!'})
									self.RuleNFA[e_count].append(x)
								else:
									self.RuleNFA[e_count]=[{e:'!'}]
			#print 'self.RuleNFA'
			#print self.RuleNFA

	def	genDFA(self):
		self.genZero()

	def	genZero(self):
		RuleNFA = self.RuleNFA
		for i in RuleNFA:
			for ruleset in RuleNFA[i]:
				for j in ruleset:
					rule = ruleset[j]
					if '!' in rule:
						if i in self.zero:
							self.zero.append(j)
		#print 'genZero'
		#print self.zero


#	def	gen
	
	def	drawNFA(self):
		NFA = pgv.AGraph(directed=True,strict=True)
		for r in self.RuleNFA:
			for t in self.RuleNFA[r]:
				for e in t:
					if t[e]!='.':
						NFA.add_edge(r,e,label=t[e])
					else:
						NFA.add_edge(r,e,label='[a-z1-9]')
		NFA.graph_attr['epsilon']='0.001'
		NFA.write('NFA.dot');
		NFA.layout('dot')
		NFA.draw('NFA.pdf')
		os.system('"evince" NFA.pdf')

