import csv

with open('enjoySport.csv') as cfile:
    examples = [ tuple(row) for row in csv.reader(cfile) ]

# To obtain the domain of attribute values defined in the instances X
def getdomains(examples):
    # set function returns the unordered collection of items with no duplicates
    
    d = [ set() for i in examples[0] ] 
    
    for r in examples:
          for c, v in enumerate(r): 
              #print(list(enumerate(r)))
              d[c].add(v)
              
          
    return [ list(sorted(x)) for x in d ]


def g0(n):
    print('?'*n)
    return ('?',)*n 
def s0(n):
    return ('0',)*n


def more_general(h, e):
    mgparts = []
    for x, y in zip(h, e):
         mg = x == '?' or (x != '0' and (x == y or y == "0")) 
         mgparts.append(mg)
        # print(mgparts)
    
    return all(mgparts)


def consistent(hypothesis, example):
    return more_general(hypothesis, example)
 
def min_generalizations(s, e):
     s_new = list(s)
     
    # print(s_new)
     for i in range(len(s)):
           if not consistent(s[i:i+1],e[i:i+1]): 
               if s[i] != '0':
                   s_new[i] = '?'
 
               else: 
                   s_new[i] = e[i]
     return [tuple(s_new)]
 
def generalize_S(e, G, S): 
    S_prev = list(S) 
    
    for s in S_prev:
        if s not in S:
           continue
        if not consistent(s,e):
           S.remove(s)
           Splus = min_generalizations(s, e)
          
           S.update( [ h for h in Splus    if any( [ more_general(g, h)    for g in G ] ) ] )
           S.difference_update( [ h for h in S
                if any( [ more_general(h, h1) for h1 in S if h != h1 ] ) ] )
   
   
    return S


def min_specializations(h, domains, e): 
      results = []
      for i in range(len(h)):
        if h[i] == '?':
          for val in domains[i]:
              if e[i] != val:
                 h_new = h[:i] + (val, ) + h[i+1:] 
                 results.append(h_new)
              elif h[i] != '0':
                 h_new = h[: i] + ('0', ) + h[i+1:] 
                 results.append(h_new)
      return results
 
def specialize_G(e, domains, G, S): 
    G_prev = list(G)
    for g in G_prev:
       if g not in G:
           continue
       if consistent(g, e):
           G.remove(g)
           Gminus = min_specializations(g, domains, e)
           G.update( [ h for h in Gminus    if any( [ more_general(h, s)    for s in S] ) ] )
           G.difference_update( [ h for h in G
                  if  any( [ more_general(g1, h)    for g1 in G if h != g1 ] ) ] )
    return G


def candidate_elimination(examples): 
      
       domains = getdomains(examples)[:-1] 
       
       G = set( [ g0(len(domains) ) ] )
       S = set( [ s0(len(domains) ) ] ) 
       i = 0
       print("\nInitially")
       print("G[{0}]:".format(i), G)
       print("S[{0}]:".format(i), S) 
       for r in examples:
            i = i+1
            e, t = r[:-1], r[-1] # Splitting data into attributes and decisions
            #print(e)
            #print(t)
            if t == 'Yes':    # positive example
                  G = {g for g in G if consistent(g, e)} 
                  S = generalize_S(e, G, S)
            else:    # negative example
                  S = {s for s in S if not consistent(s, e)}
                  G = specialize_G(e, domains, G, S)
            print("For Training example {0}".format(i)) 
            print("G[{0}]:".format(i), G)
            print("S[{0}]:".format(i), S)
       return
candidate_elimination(examples)