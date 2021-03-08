import sys
import argparse
import random
import ast
import time, datetime

class Show(object):
    def __init__(self, message):
        sys.stdout.write('\r')
        sys.stdout.write(str(message))
        sys.stdout.flush()

class CNF(object):
    def __init__(self, cnf_file):
        self.cnf_file = cnf_file
        self.cnf_data = self._ReadCNFfile()

    # Reads the .cnf file and returns the content
    def _ReadCNFfile(self):
        try:
            with open(cnf_file) as f:
                Show('[*] Reading "{}" file...'.format(self.cnf_file))
                cnf_data = f.read().strip()
            Show("\t\t\t\t\t\t\t[Done]\n")
            return cnf_data.split("\n")
        except IOError as e:
            if "[Errno 2] No such file or directory" in str(e):
                print '\n[-] You must specify "{0}" path'.format(self.cnf_file)
            else:
                print e
            sys.exit()
    
    # Returns the number of variables from cnf data
    def VariablesNumber(self):
        for data in self.cnf_data:
            data = data.split(" ")
            if data[0] == "p":
                cnf_variable_number = data[2]
                return int(cnf_variable_number)
    
    # Returns the number of clauses from cnf data
    def ClausesNumber(self):
        for data in self.cnf_data:
            data = data.split(" ")
            if data[0] == "p":
                cnf_variable_number = data[3]
                return int(cnf_variable_number)

    # Sets into a list all clauses
    def GetCNFClauses(self):
        cnf_clauses = []
        for data in self.cnf_data:
            data = data.split(" ")[:-1]
            if data[0] != "c" and data[0] != "p":
                clause = []
                for literal in data:
                    clause.append(int(literal))
                cnf_clauses.append(clause)
        return cnf_clauses
    


class WalkSAT(CNF):
    def __init__(self, cnf_file, max_tries, max_flips, p):
        super(WalkSAT, self).__init__(cnf_file)
        self.max_tries = max_tries
        self.max_flips = max_flips
        self.p = p
        self.clauses = self.GetCNFClauses()
        self.literals = self._CreateLiterals()      
    
    def WalkStart(self):
        output = False, 0
        for tries in range(1, self.max_tries+1):
            T = self._SetRandomAssignment()
            self.false_clauses = self._GetFalseClauses(T)

            if self._ProblemSatisfied() == True:
                return True, T
            else: 
                for flip in range(1, self.max_flips+1):
                    C = self._GetRandomUnsatisfiedClause(self.false_clauses)
                    if random.random() > self.p:
                        variable = self._ChooseVariableToFlip(C)
                    else:
                        variable = random.randint(1,self.VariablesNumber()) - 1
                    self._Flip(T, variable)
                    percentage = float(tries)/float(self.max_tries) * 100
                    
                    Show('[*] Completed: {0}%   Tries: {1}/{2}   Flips: {3} /{4}'.format(percentage, tries, self.max_tries, flip, self.max_flips))
                    if self._ProblemSatisfied() == True:
                        return True, T
        return output

                

    # Sets random integer values into a list
    def _SetRandomAssignment(self):
        random_assign = []
        for i in range(1, self.VariablesNumber()+1):
            if random.random() < self.p:
                i *= -1
            random_assign.append(i)
        return random_assign
    
    # Each literal is located by clause
    def _CreateLiterals(self):
        literals = {}
        for i in range(1, self.VariablesNumber()+1):
            literals[i] = []
            literals[i*-1] = []
            for instance in self.clauses:
                if i in instance:
                    literals[i].append(instance)
                if i*-1 in instance:
                    literals[i*-1].append(instance)
        return literals
    
    # Returns all unsatisfied clauses
    def _GetFalseClauses(self, T):
        unsatisfied_clauses = []
        self.numSatisfiedLitsPerClause = {}
        for clause in self.clauses:
            satisfied_literal = 0
            for literal in T:
                if literal in clause:
                   satisfied_literal += 1 
            if satisfied_literal == 0:
                unsatisfied_clauses.append(clause)
            self.numSatisfiedLitsPerClause[str(clause)] = satisfied_literal 
        return unsatisfied_clauses
    
    # Returns a random clause from the unsatisfied clause list
    def _GetRandomUnsatisfiedClause(self, false_clauses):
        return random.choice(false_clauses)
    
    # Returns a variable to Flip
    def _ChooseVariableToFlip(self, C):
        max_v = -1000
        for literal in C:
            b = 0
            broken = 0
            for y in self.literals[literal]:
                if self.numSatisfiedLitsPerClause[str(y)] == 0:
                    b += 1
            for y in self.literals[literal*-1]:
                if self.numSatisfiedLitsPerClause[str(y)] == 1:
                    broken +=1
            v = b - broken
            if max_v < v:
                max_v = v
                variable = abs(literal) - 1
        return variable
    
    # Flips a choosen variable and updates false clauses list
    def _Flip(self,T, variable):
        T[variable] = T[variable] * (-1)
        for clause in self.numSatisfiedLitsPerClause.keys():
            data = ast.literal_eval(clause)
            if variable in data:
                if (self.numSatisfiedLitsPerClause[clause] > 0):
                    self.numSatisfiedLitsPerClause[clause] -= 1
                if(self.numSatisfiedLitsPerClause[clause] == 0):
                    self.false_clauses.append(data)
            if str(variable * -1) in clause:
                self.numSatisfiedLitsPerClause[clause] += 1
                if(self.numSatisfiedLitsPerClause[clause] - 1 == 0):
                    self.false_clauses.remove(data)
    
    # Returns True if the problem is satisfiable
    def _ProblemSatisfied(self):
        satisfied = False
        z = 0
        for instance in self.numSatisfiedLitsPerClause.keys():
            if (self.numSatisfiedLitsPerClause[instance] ==0):
                z+=1
        if z == 0:
            satisfied = True
        return satisfied
        


def main(cnf_file, max_tries, max_flips, p):
    walk_sat = WalkSAT(cnf_file, max_tries, max_flips, p)
    start_time = time.time()
    out = walk_sat.WalkStart()
    print ''
    if out[0] == True:
        print "[+] Problem is Satisfiable"
        print "[+] Solution: {0}".format(out[1])
    else:
        print "[-] Problem is not Satisfiable"
    script_time = time.time()-start_time
    print "[*] Script Completed in {0}".format(str(datetime.timedelta(seconds=script_time)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-cnf", dest="cnf_file", help="[*] Import your cnf file")
    parser.add_argument("-tries", dest="max_tries", type=int, default=1000, help="[*] Max Tries")
    parser.add_argument("-flips", dest="max_flips", type=int, default=1000, help="[*] Max Flips")
    parser.add_argument("-p", dest="p", type=float, default=0.5, help="[*] Possibility")
    args  = parser.parse_args()
    cnf_file = args.cnf_file
    max_tries = args.max_tries
    max_flips = args.max_flips
    p = args.p

    if p < 0 and p > 1.0:
        print "[-] p must be between 0 and 1"
        sys.exit()

    if cnf_file != None:
        try:
            main(cnf_file, max_tries, max_flips, p)
        except KeyboardInterrupt:
            sys.exit()
    else:
        print "[-] cnf file was not specified"