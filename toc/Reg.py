NonTerminal = 'ABCDEFGHIJKLMNSOPQRTUVWXYZ'
Terminal='abcdefghijklmnopqrstuvwxyz1234567890'
Stackbet = Terminal+NonTerminal+'|!'
StartSymbol = 'S'

class	Reg:
	exp = ''
	lef_bra = []
	rig_bra = []
	RuleSets = {}
	usedVar = ['S']
	unusedVar = list(NonTerminal)

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
#		print 'rmBra'
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
#		print self.RuleSets
	def	rmBeg(self):
#		print 'rmBeg'
		s = self.RuleSets[StartSymbol]
		if '^' in s:
			if s[-1] == '^':
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
				s = s.replace('^',var)
				x = {StartSymbol:s}
				self.RuleSets.update(x)
				
				self.RuleSets[var]=newvar+var+'|!'
				self.RuleSets[newvar]='.'
#				print 'armBeg',self.RuleSets[var],self.RuleSets[newvar]
#				print var,newvar
			else:
				s = s.replace('^','')
				x= {StartSymbol:s}
				self.RuleSets.update(x)

#		print self.RuleSets

	def	rmTai(self):
#		print 'rmTai'
		s = self.RuleSets[StartSymbol]
		if '$' in s:
			if s[-2] == s[0]:
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
				s = s.replace('$','')
				s = var+s
				x = {StartSymbol:s}
				self.RuleSets.update(x)
				self.RuleSets[newvar]='.'
				self.RuleSets[var]=newvar+var+'|!'
#				print 'armTai',var,newvar

			else:
				s = s.replace('$','')
				x= {StartSymbol:s}
				self.RuleSets.update(x)

#		print self.RuleSets

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

						#change A* to B-> BA|!
						self.RuleSets[var]=rule[t-1]+var+'|!'
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
#		print 'rmAdd'
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

						#change A+ to B-> BA|A
						self.RuleSets[var]=rule[t-1]+'|'+rule[t-1]+var
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
#		print self.RuleSets

	def	rmVer(self):
#		print 'rmVer'
		RuleSets = {}
		for r in self.RuleSets:
			RuleSets[r] = self.RuleSets[r]
		for r in RuleSets:
			if '|' in RuleSets[r]:
				rule = RuleSets[r]
				rules = rule.split('|')
				x = {r:rules}
				self.RuleSets.update(x)
#		print self.RuleSets

	def	rmDot(self):
#		print 'rmDot'
		RuleSets = {}
		for r in self.RuleSets:
			RuleSets[r] = self.RuleSets[r]
		for r in RuleSets:
			dot = ('.' in RuleSets[r])
			rule = RuleSets[r]
			while dot == True:
				var = self.unusedVar[0]
				if var == 'S':
					del self.unusedVar[0]
					var = self.unusedVar[0]

				rule = rule.replace('.',var,1)
				x = {r:rule}
				self.RuleSets.update(x)
				self.RuleSets[var]=list(Terminal)
				self.usedVar.append(var)
				del self.unusedVar[0]
				dot = ('.' in rule)
#		print self.RuleSets



	def	genRule(self):
		self.rmBra()
		self.rmBeg()
		self.rmTai()
		self.rmStar()
		self.rmAdd()
		self.rmDot()
		self.rmVer()

	def	countTerminal(self,s):
		count = 0
		for i in range(len(s)):
			if s[i] in Terminal:
				count += 1
		return count

