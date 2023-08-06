import re
#Dot_ce3 = RegularLanguage("((a+b+c)*b)^x + (-(c*b)*a*a*a)^x")
#Dot_ce2 = RegularLanguage("((b+a)*b)^x+(-(c*b)*a*a)^x")
#Dot_ce =  RegularLanguage("((b+a+c)*(b))^x+((-b)*a*c)^x")
ex7 = { (0,"1"):[1], (0,"2"):[2], (0,"3"):[3],
(1,"1"):[2], (1,"2"):[3], (1,"3"):[4],
(2,"1"):[3], (2,"2"):[4], (2,"3"):[5],
(3,"1"):[4], (3,"2"):[5], (3,"3"):[6],
(4,"1"):[5], (4,"2"):[6], (4,"3"):[0],
(5,"1"):[6], (5,"2"):[0], (5,"3"):[1],
(6,"1"):[0], (6,"2"):[1], (6,"3"):[2]}

ContreExempleOlivierApContinuite = {(0,"a|a"):[1],(0,"b|b"):[2],(1,'a|1'):[0],(1,"b|b"):[2],(2,'a|a'):[0]}
ContreExempleOlivierApContinuite2 = {(0,"a|a"):[1],(1,"b|b"):[5],(2,"b|b"):[5],(1,'a|a'):[2],(5,'a|a'):[4],(3,'a|aa'):[4],(4,'a|a'):[3],(3,'b|b'):[0],(4,'b|b'):[0],(0,'c|c'):[6],(5,'c|c'):[6],(6,'a|a'):[0],(2,'a|1'):[1],}
ContreExempleOlivierApContinuite3 = {(0,"a"):[1],(1,"b"):[5],(2,"b"):[5],(1,'a'):[2],(5,'a'):[4],(3,'a'):[4],(4,'a'):[3],(3,'b'):[0],(4,'b'):[0],(0,'c'):[6],(5,'c'):[6],(6,'a'):[0],(2,'a'):[1]}

def ismael_automata(n,reset=True):
    d = {}
    for i in range(n):
        for j in range(i):
            d[(i,(j,))] = [i]
        for j in range(i+1,n):
            d[(i,(j,))] = [j]
    if reset: 
        d[(i,"c")] = ["r"]
        d[("r",(i,))] = ["r"]
        d[("r","c")] = ["r",0]
        return Automaton(d,["r"],range(n))
    else:
        return Automaton(d,[0],range(n))
    
def colconj_automata(n,k):
    d = {}
    for i in range(n):
        for j in range(i):
            d[(i,(j,))] = [i]
        for j in range(i+1,n):
            d[(i,(j,))] = [j]
        d[(i,"c")] = ["r"]
        d[("r","c")] = ["r","r"+str(0)]
        for j in range(k):
            d[("r"+str(j),(i,))] = ["r"+str(j+1)]
        
    return Automaton(d,["r"],range(n))
            
        
def tupleN(n,p):
    if p == 1:
        return [(i,) for i in range(n)]
    else:
        R = tupleN(n,p-1)
        P = []
        for x in R:
            for i in range(n):
                P.append(x+(i,))    
        return P
    
def TnxTn(n):   
    return n    

def test_stupid_equation(M):
    for x in M:
        for y in M:
            for z in M:
                xyz = M.idempotent_power(x+y+z)
                xy = M.idempotent_power(x+y)
                zxy = M.idempotent_power(z+x+y)
                yx = M.idempotent_power(y+x)
                if not M(xyz+xy+zxy) == M(xyz+yx+zxy): 
                    return (x,y,z)
    return True
def random_automaton_by_connected(k,n,alphabet):
    l = [int(random()*(n-1))+1 for x in range(k)]
    A = random_automaton(l.pop(),alphabet)
    while len(l)>0:
        A = A + random_automaton(l.pop(),alphabet)
    return A
def PreImage(S,u,verbose=False):
    Edges = S.cayley_graph().edges()
    d = {}
    for x in Edges:
        d[(x[0],x[2][0])] = [x[1]]
    if verbose:
        print "Done for transitions"
    A = Automaton(d,[""],[u])
    if verbose:
        print "Done for Automaton loading"
    return A.minimal_automaton()

        

def quotient(semigroup,E,verbose=False):
    Edges = set()
    if verbose:
        print "computing edges"
        size = len(semigroup)
        count = 0
    for x in semigroup:
        Edges.add((x,x))
    for x in semigroup:
        if verbose:
            print str(count)+"/"+str(size)
            sys.stdout.write("\033[F")
            count = count+1
        for y in semigroup:
            for s in E:        
                for r in E:
                    if not (s==r):
                        Edges.add((semigroup(x+r+y),semigroup(x+s+y)))
        
    G = DiGraph(list(Edges))               
    class_gen=[set(x) for x in G.strongly_connected_components()]        
    alphabet = semigroup._automaton._alphabet
    new_alphabet = set()
    for x in class_gen:
        if (len(x.intersection(alphabet))>0):
            new_alphabet.add(x.intersection(alphabet).pop())
    d = {}
    
    for x in class_gen:
       for a in new_alphabet:
            x0 = list(x)[0]
            y = set(G.strongly_connected_component_containing_vertex(semigroup(x0+a)))
            d[(class_gen.index(x),a)] = [class_gen.index(y)]
                        
    return TransitionSemiGroup(Automaton(d,[0],[0],range(len(class_gen)),new_alphabet))

def aperiodic_quotient(semigroup,verbose=False):
    E = set(semigroup)
    while len(E) > 0:
        x = semigroup.pop_J_maximal(E)
        e = semigroup.idempotent_power(x)
        H = semigroup.H_class_of_element(x)
        if len(H)>1:
            return aperiodic_quotient(quotient(semigroup,H,verbose=verbose))
    return semigroup

def reached_set(semigroup,x,y):
    Rs = set()
    for a in x:
        for b in y:
            Rs.add(semigroup(a+b))
    return Rs
    
def compute_cover_once(semigroup,cover,class_dic):
    ncover = list(cover)
    for x in cover:
        for y in cover:
            Rs = reached_set(semigroup,x,y)
            remove = set([class_dic[a] for a in Rs]) 
            if len(remove)>1:
                nH = set()
                for H in remove:
                    nH = nH.union(H)
                    if H in ncover:
                        ncover.remove(H)
                nH = frozenset(nH)             
                ncover.append(nH)
                for a in nH:
                    class_dic[a] = nH
                return ncover    
    return ncover                    
def aperiodic_cover(semigroup,verbose=False):
    E = set(semigroup)
    cover = []
    class_dic = {}
    count = 0
    while len(E) > 0:
        x = E.pop()
        Hx = frozenset(semigroup.H_class_of_element(x))
        E = E.difference(Hx)
        cover.append(Hx)
        for y in Hx:
            class_dic[y] = Hx
        count = count + 1 
    current_len = len(semigroup)                    
    while len(cover)< current_len:
        current_len= len(cover)
        cover = compute_cover_once(semigroup,cover,class_dic)             
    return cover

            
def gene_letter(n):
    d = {}
    F =  FiniteSetMaps(range(n))
    E = set(range(n))
    for x in range(n):
        d[x] = sample(range(n),1)[0]
    return F.from_dict(d)      
def is_idempotent(f):
    n = 1
    
    while not (f^n == f^(2*n)):
        n = n+1
    if f^(n+1) == f^(n):
        return True
    else:
        return False                
def gene_aperiodic_letter(n):
    f = gene_letter(n)
    while not(is_idempotent(f)):
        f = gene_letter(n)    
    return f
def gene_one_automaton(size,alphabet):
    states = range(size)
    transition = {}
    for a in alphabet:
        La = gene_aperiodic_letter(size)
        for x in states:
            transition[(x,a)] = [La(x)]
    return Automaton(transition,sample(states,1),sample(states,1),states,alphabet)

def random_aperiodic_semigroup(size,maxsize=200,alphabet=("a","b","c"),verbose=False):
    complete = False
    count = 0
    while not complete:
        complete = False
        A = gene_one_automaton(size,alphabet)
        S = TransitionSemiGroup(A)
        if S.elements(maxsize=maxsize)== False:
            if verbose:
                print "reject "+str(count)+" Too big         "
                sys.stdout.write("\033[F")
        else:
            if  S.is_equation_satisfied("(x)^wx=(x)^w",["x"]):
                return S
            else:
                if verbose:
                    print "reject "+str(count)+" not aperiodic           "
                    sys.stdout.write("\033[F")
        count = count +1

    
def test_conj_semigroup(S,verbose=False,value=1):
    if verbose:
        print len(S.elements(verbose=verbose))
    E1 = compute_pairs_level1(S,verbose=verbose)
    while (value>0):
        value = value-1                    
        E2 = compute_pairs(S,E1,verbose=verbose)
        contre_ex = set([])
        if verbose:
            print "done computing pairs       "
        for u in S.idempotents():
            for w1 in E2[u]:
                for w2 in E2[u]:
                    for v in S:
                        if u in E1[v]:
                            if not (S(w1+v+w2) in E2[u]):
                                contre_ex.add((u,S(w1+v+w2),w1,w2,v))
                                if verbose:
                                    print "contre-ex"   
                                    print contre_ex
        E1 = E2
    return contre_ex
def fullTransitionSemiGroup(n):
    d = {}
    for x in range(n):
        d[(x,"a")] = [(x+1)%n]
        d[(x,"b")] = [x]
        d[(x,"c")] = [x]
    d[(0,'b')]= [1]
    d[(1,'b')] = [0]
    d[(1,'c')] = [0]
    A = Automaton(d,[0],[0])
    return TransitionSemiGroup(A)

def compute_pairs(semigroup,E,verbose=False, trace=False):
    S = semigroup.elements()
    F = {}
    if trace:
        trace_result = {}

    for x in S:
        F[x] = [x]
        if trace:
            trace_result[(x,x)] = (x,x)

    for x in E:
        for y in E[x]:
            e = semigroup.representent(semigroup.idempotent_power(y))
            t = semigroup.representent(e+x+e)            
            if t not in F[e]:
                F[e].append(t)
                if trace:
                    trace_result[(e,t)] = (y+"^w",y+"^w"+"+"+x+"+"+y+"^w")
    new =[(x,y) for x in F for y in F[x]]

    while len(new)>0:
       old = list(new)
       new = []
       count = 0 
       for x in old:
            if verbose:
                count = count+1
                print str(count)+" / "+str(len(old))+" length new :"+str(len(new))     
                sys.stdout.write("\033[F")
            for y0 in F:
                for y1 in F[y0]:
                       m = semigroup.representent(x[0]+y0)
                       n = semigroup.representent(x[1]+y1)
                       if n not in F[m]:
                           F[m].append(n)
                           new.append((m,n)) 
                           if trace:
                               trace_result[(m,n)] = (trace_result[x][0]+"+"+trace_result[(y0,y1)][0],trace_result[x][1]+"+"+trace_result[(y0,y1)][1]) 
    if trace:
        return [F,trace_result]
    else :
        return F

def compute_pairs_level1(semigroup,verbose=False,trace=False):

    S = semigroup.elements()
    F = {}
    for x in S:
        F[x] = [x]
    F[""] = list(S)
    new =[(x,y) for x in F for y in F[x]]
    if trace:
        trace_result = {}
        for x in new:
            trace_result[x] = x
    
    while len(new)>0:
       old = list(new)
       new = []
       count = 0 
       for x in old:
            if verbose:
                count = count+1
                print str(count)+" / "+str(len(old))+" length new :"+str(len(new))     
                sys.stdout.write("\033[F")
            for y0 in F:
                for y1 in F[y0]:
                       m = semigroup.representent(x[0]+y0)
                       n = semigroup.representent(x[1]+y1)
                       if n not in F[m]:
                           F[m].append(n)
                           new.append((m,n))
                           if trace:
                               trace_result[(m,n)] = (trace_result[x][0]+"+"+trace_result[(y0,y1)][0],trace_result[x][1]+"+"+trace_result[(y0,y1)][1]) 
    if trace:
        return [F,trace_result]
    else :
        return F

def process_test(n,alphabet,verbose=False):
    S = random_aperiodic_semigroup(n,alphabet,verbose=verbose)
 
    count = 0
    while (test_conj_semigroup(S,verbose=verbose)):
        if verbose:
            print count
        count = count+1
        f = open("status", 'a')
        f.write(str(S._automaton._transitions)+"\n")
        f.write("Taille du monoide:"+str(len(S))+"\n")
        f.write(" test n° "+str(count)+"\n")
        f.write("######################\n")
        f.close()
        S = random_aperiodic_semigroup(n,alphabet,verbose=verbose)
    f = open("status", 'a')
    f.write("Contre-exemple\n")
    f.write(str(L)+"\n")
    f.write(str(count)+"\n")
    f.close()
    
def view_chain(semigroup,depth,verbose=False,mindepth=0,node_sep=1):
    s = 'digraph {\n node [shape= record]\nranksep= 0.1;\n nodesep= 0.1;\n splines=False '
    s = graphviz_string_exp(semigroup,header=s,verbose=verbose)
    box = semigroup.box_representation()
    rep = list(box)
    dic_rep = {"1":"1"}
    for x in rep:    
        for y in semigroup.J_class_of_element(x):
            if y == "":   
                dic_rep[1] = x
            else:        
                dic_rep[y] = x

    s = s[0:len(s)-1]
    L = []     
    L.append(compute_pairs_level1(S,verbose=verbose))
    for i in range(depth-1):
        L.append(compute_pairs(S,L[i],verbose=verbose))
    L.reverse()
    edge_done = []
    s = s +   'edge [constraint=False];\n'

    for i in range(depth):
        for x in semigroup:
            for y in L[i][x]:
                if not (x==y) and not ((x,y) in edge_done) and ((depth-i) >= mindepth):
                    edge_done.append((x,y))
                    if x == "":
                        ux = "1"
                    else:
                        ux = x
                    if y == "":
                        uy = "1"
                    else:
                        uy = y

                    s = s+dic_rep[ux]+':'+ux+'->'+dic_rep[uy]+':'+uy+'[constraint=False colorscheme = "orrd9" color = '+str(2*(depth-i)+2)+'];\n'
    s= s +"}"
    display_graphviz(s)
def graphviz_string_exp(semigroup,header=False, arrow=True,verbose=False,unfold=True):
    r"""  
    Return graphviz eggbox representation of self. Set arrow to False to delete the arrow.
    INPUT :
    -  ``self`` -  Automaton        
    -  ``arrow`` -  boolean
    -  ``verbose`` -  boolean

    OUTPUT:

    string 

    EXAMPLES::
              
    """

    if verbose:
        print "computing box diagramm ..."
    box = semigroup.box_representation(verbose=verbose) 
    if verbose:
        print "done."
    repre = set(box) 
    Gcal =  DiGraph(semigroup.cayley_graph(idempotent=False, loop=False, orientation="left_right"))  
    if verbose:
        edge_nb = str(len(Gcal.edges()))
        print "computing global structure ..."
        count = 0 
    for x in repre:
        if verbose:
            count = count+1
            print str(count)+"/"+str(edge_nb)
            sys.stdout.write("\033[F")
        Jx = set(semigroup.J_class_of_element(x))
        Jx.remove(x)    
        Lx = [x]
        Lx.extend(Jx)            
        Gcal.merge_vertices(Lx)
    if verbose:
        print "done."

    Edge = []
    if header==False:
        graph_viz = 'digraph {\n node [shape= record]\nranksep= 0.1;\n nodesep= 0.1;\n '
    else:   
        graph_viz = header

    for x in repre:
        if x == '':
            rx = '1'
        else:
            rx = x
        if unfold:
           graph_viz = graph_viz + rx + ' [label='+draw_box_dot(box[x])+'];\n'
        else:
           graph_viz = graph_viz + rx + ' [label='+rx+'];\n'

    if not arrow:         
        graph_viz = graph_viz + 'edge [style="invis"]\n'            
    if verbose:
        print "computing successor edges ..."
        count = 0
        loop_ln = len(repre)^2
    for x in repre:        
        for y in repre:                
            if (x,y)  in Gcal.edges(labels=False):      
                if x == '':
                    rx = '1'
                else:
                    rx = x
                if y == '':
                    ry = '1'
                else:
                    ry = y
                graph_viz = graph_viz+rx+'->'+ry+'[style="invis"];\n'
    return graph_viz + '}'  
def display_graphviz(s):
    from sage.misc.viewer import browser
    #file_dot = sage.misc.temporary_file.tmp_filename(".",".dot")
    #file_gif = sage.misc.temporary_file.tmp_filename(".",".gif")
    file_dot = "debug.dot"
    file_gif = "debug.gif"
    print s
    f = file(file_dot,'w')
    f.write(s)
    f.close()
    os.system('dot %s -o %s; %s %s  2>/dev/null 1>/dev/null '%(file_dot,file_gif,browser(),file_gif))


def core_js_cola_dclass(data):
    return """

     <html lang="en">
<head>
    <meta charset="utf-8" />
 <style>  
.node {
   
}
.Dselected {
   fill: red;
    stroke: darkred;
  stroke-width: 1.5px;
    cursor: move;
}
.Hselected {
   fill: red;
    stroke: darkred;
  stroke-width: 1.5px;
    cursor: move;
}

.trivialHclass {
   fill: CadetBlue ;
    stroke: darkblue;
  stroke-width: 1.5px;
    cursor: move;
}
.regHclass {
   fill: blue;
   stroke: darkblue;
  stroke-width: 1.5px;
    cursor: move;
}

.dclass {
    fill: CadetBlue ;
    stroke: darkblue;
  stroke-width: 1.5px;
    cursor: move;
}
.regdclass{
    fill: blue;
    stroke: darkgreen;
  stroke-width: 1.5px;
    cursor: move;
}

.group {
  stroke: #fff;
  stroke-width: 1.5px;
  cursor: move;
  opacity: 0.7;
}
.boxed {
      border: 2px solid black ;
    } 
.link {
  stroke: #7a4e4e;
  opacity: 0.5;
  stroke-width: 3px;
  stroke-opacity: 1;
}

.label {
    stroke: white;
    fill: white;
    font-family: Verdana;
    font-size: 25px;
    text-anchor: middle;
    cursor: move;

}

</style>
</head>
<body>

    <script src="http://marvl.infotech.monash.edu/webcola/extern/d3.v3.js"></script>
    <script src="http://marvl.infotech.monash.edu/webcola/cola.v3.min.js"></script>
<script> """+data+"""
    var width =600,
        height = 400; 
    var color = d3.scale.category20();
    function draw_Jbox(repr){
    
    }
    var cola = cola.d3adaptor()
        .linkDistance(200)
        .avoidOverlaps(True)
        .handleDisconnected(False)
        .size([width, height]);
   var scale = 0.5;
   var zoomWidth = (width-scale*width)/2;
   var zoomHeight = (height-scale*height)/2;
    var zoom = d3.behavior.zoom()
         .scaleExtent([0.1, 10])
        .on("zoom", zoomed);
    var zoom2 = d3.behavior.zoom()
         .scaleExtent([0.1, 10])
        .on("zoom", zoomed2);
    var zoom3= d3.behavior.zoom()
         .scaleExtent([0.1, 10])
        .on("zoom", zoomed3);

    var drag = d3.behavior.drag()
        .origin(function(d) { return d; })
        .on("dragstart", dragstarted)
        .on("drag", dragged)
        .on("dragend", dragended);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("class","boxed")
        .call(zoom);
   var container = svg.append("g")
    .attr("transform", "translate("+zoomWidth+","+zoomHeight+") scale("+scale+")");
    d3.behavior.zoom().translate([zoomWidth,zoomHeight]).scale(scale);

    function restart() 
    {
        cola.stop();
        cola
            .nodes(nodes)
            .links(links)
            .constraints(constraints)
            .avoidOverlaps(True)
            .start();
        var link = container.selectAll(".link")
            .data(links)
              .enter().append("line")
            .attr("class", "link");
//       var  node2 = container3.selectAll(".node")
//            .data(cola.nodes())
//            .enter()//.filter(function(d){ if (d.type == "group") return True;}).append("g")
//            .attr("class","node");
//       node2.append("circle").attr("r",5);
       var  node1 = container.selectAll(".node")
            .data(cola.nodes())
            .enter().append("g")
            .attr("class","node");
        node1.append("rect")
            .attr("width", function (d) { return d.width ; })
            .attr("height", function (d) { return d.height;})
            .attr("class",function(d){if (d.type=="regdclass") {return "regdclass";}else {return "dclass";}})
            .attr("rx", 5).attr("ry", 5)
            .on("click",function(d){
                d3.selectAll(".Dselected").attr("class",function(d){if (d.type=="regdclass") {return "regdclass";}else {return "dclass";}});
                d3.select(this).attr("class","Dselected");                              
                var bwidth = d.boxwidth;
                var bheight = d.height;    
                container2.selectAll("g").remove();
                var box = container2.append("g");
                var line = box.selectAll("g").data(d.box).enter().append("g");
                line.attr("transform",function(d,i){ 
                    var inode = i;
                    rows = box.append("g");
                    var noderaw = rows.selectAll(".node").data(d.row).enter().append("g").attr("class","node");
                    noderaw.append("rect").attr("width",bwidth)
                    .attr("height",bheight)
                    .attr("rx", 5).attr("ry", 5)
                    .attr("width", function (d) {return bwidth ; })
                    .attr("height", function (d) { return bheight;})
                    .attr("class",function(d){
                    if (d.group.type == "trivial"){
                        return "trivialHclass";
                     }
                    else{
                        return "regHclass";
                    }
                    });
                    noderaw.attr("transform",function(d,i){ 
                     return "translate("+(5+(5+bwidth)*inode)+","+(10+(5+bheight)*i)+")";

                        
                        });
                     noderaw.append("text")
                        .attr("class", "label")
                        .text(function (d) { if (d.idempotent=="False") {return d.name; } else { return d.name+" *" ;}  })
                        .attr("transform",function(d){ 
                         return "translate("+bwidth/2+","+bheight/2+")";                        
                        });
                     noderaw.select("rect").on("click",function(d){
                        
                            d3.selectAll(".Hselected").attr("class",function(d){if (d.group.type =="trivial") {return "trivialHclass";}else {return "regHclass";}});
                            d3.select(this).attr("class","Hselected");   
                            for (x in d.group.nodes){
                               nodes.push(d.group.nodes[x]);
                            }
                            for (x in d.group.link){
                               links.push(d.group.link[x]);
                            }

                            restart();

                        });
                     return "translate("+(5+(5+bwidth)*inode)+","+10+")";});           
                                     
            });  
             node1.append("text")
            .attr("class", "label")
            .attr("transform", function(d){ return "translate("+d.width/2+","+(d.height/2+4)+")";}) 
            .text(function (d) { return d.name; });
            node1.append("title")
            .text(function (d) { return d.name; });
        cola.on("tick", function () {
            link.attr("x1", function (d) { return d.source.x; })
                .attr("y1", function (d) { return d.source.y; })
                .attr("x2", function (d) { return d.target.x; })
                .attr("y2", function (d) { return d.target.y; });

         node1.attr("transform", function(d) { 
  	        return "translate(" + (d.x-d.width/2) + "," + (d.y-d.height/2) + ")"; });                 
         node2.attr("transform", function(d) { 
  	        return "translate(" + (d.x-d.width/2) + "," + (d.y-d.height/2) + ")"; });                 
        });
    }  
    


        var svg2 = d3.select("body").append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("class","boxed")
            .call(zoom2);

        var svg3 = d3.select("body").append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("class","boxed")
            .call(zoom3);

        var container2 = svg2.append("g");
        var container3 = svg3.append("g");

        var pad = 3;
    restart();
    function zoomed() {
          container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }
    function zoomed2() {
          container2.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }
    function zoomed3() {
          container3.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }

        function dragstarted(d) {
          d3.event.sourceEvent.stopPropagation();
          
          d3.select(this).classed("dragging", True);
          cola.start();
        }

        function dragged(d) {
          
          d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
          
        }

        function dragended(d) {
          
          d3.select(this).classed("dragging", False);
        }
</script>
</body>
</html> 
"""

def cayley_group(S,u):
    u = S(u)
    H_class = S.H_class_of_element(u)
    if len(H_class.intersection(S.idempotents()))>0:
        neutral = H_class.intersection(S.idempotents()).pop()
        alphabet = S._automaton._alphabet
        generators = set([S(neutral+a) for a in alphabet])
        vertex = []
        for x in H_class:
            for a in generators:
                if S(x+a) in H_class:
                    vertex.append((x,S(x+a),a))
        return DiGraph(vertex)
    else:
        return DiGraph()
def js_d_class_struct(semigroup,verbose=False):
    from sage.misc.viewer import browser

    S = semigroup
    box = S.box_representation(verbose=verbose,idempotent=False) 
    repre = set(box) 
    Gcal =  DiGraph(S.cayley_graph(idempotent=False, loop=False, orientation="left_right"))  
    J = {}
    if verbose:
        count = 0
    for x in repre:
        if verbose:
            count = count+1
            print str(count)
            sys.stdout.write("\033[F")
        J[x] = list(S.J_class_of_element(x))
        Jx = set(J[x])
        Jx.remove(x)    
        Lx = [x]
        Lx.extend(Jx)            
        Gcal.merge_vertices(Lx)
    if verbose:
        print "done."
    
    A = S._automaton._alphabet
    file_html = sage.misc.temporary_file.tmp_filename(".",".html")
    #file_jsop = sage.misc.temporary_file.tmp_filename(".",".jsop")
    Ls = list(Gcal.vertices())
    data2 = ""
    s = "var nodes = [\n"    
    for x in Ls:
        maxlen = 0
        if  len(set(J[x]).intersection(S.idempotents()))>0:
            s = s+'{"name":"'+x+'","type":"regdclass","width":'+str(int(60*(1+len(x)/4)))+',"height":40,"box":['
        else:
            s = s+'{"name":"'+x+'","type":"dclass","width":'+str(int(60*(1+len(x)/4)))+',"height":40,"box":['
        for L in box[x]:
            s = s + '{"row" : ['
            for y in L:
                if len(set(y).intersection(S.idempotents())):
                    y0 = set(y).intersection(S.idempotents()).pop()
                else:   
                    y0 = y[0]
                if len(y)>maxlen:
                    maxlen = len(y)
                s = s+'{"name":"'+y0+'","idempotent":"'+str(y0 in S.idempotents())+'", "group":{'
                Ggroup = cayley_group(S,y0)
                if len(Ggroup)>0:
                    s = s + '"type":"nontrivial",'
                    s = s+ 'nodes:[  '
                    for x in Ggroup.vertices():
                        s = s+'{"type":"group","name":"'+x+'"},'
                    s = s[0:len(s)-1]+'],'
                    s = s+ 'link:[  '
                    for e in Ggroup.edges():
                        s = s+'{"source":"'+e[0]+'","target":"'+e[1]+'"},'
                    s =  s[0:len(s)-1]+']'        
                else:
                    s = s + '"type":"trivial"'
                s = s+'}},'
            s = s[0:len(s)-1] + ']},\n'
        s = s[0:len(s)-2]+'],"boxwidth":'+str(int(60*(3+(maxlen)/4)))+'},\n'
    s = s[0:len(s)-2]+'\n];\n var links = [\n'    
    for e in Gcal.edges():
        s = s + '{"source":'+str(Ls.index(e[0]))+',"target":'+str(Ls.index(e[1]))+'},\n'
    s = s[0:len(s)-2] +'\n];\n  var constraints = [ \n'
    
    Gcal.allow_loops(False)
    neighbors = set(Gcal.neighbors_out(""))
    layer = {"":0}
    i = 0   
    while len(neighbors)>0:
        newN = set()
        i = i+1
        for x in neighbors:
            layer[x] = i
            newN = newN.union(Gcal.neighbors_out(x))  
        neighbors = newN        
    s = s + '{"type":"alignment","axis":"y","offsets":[  '
    for x in repre:
       s = s + '{"node":"'+str(Ls.index(x))+'","offset":"'+str(layer[x]*150)+'"},'       
    s = s[0:len(s)-1]+ ']},\n'
             

    s = s[0:len(s)-2] + "\n ];\n"   

    f = file(file_html,'w')
    f.write(core_js_cola_dclass(s))
    f.close()
    os.system('%s %s  2>/dev/null 1>/dev/null '%(browser(),file_html))


def core_js_cola_cayley(data):
    return """ <html lang="en">
<head>
    <meta charset="utf-8" />
    
<style>
.node {
    stroke: darkblue;
  stroke-width: 1.5px;
    cursor: move;
}

.group {
  stroke: #fff;
  stroke-width: 1.5px;
  cursor: move;
  opacity: 0.7;
}

.link {
  stroke: #7a4e4e;
  opacity: 0.5;
  stroke-width: 3px;
  stroke-opacity: 1;
}

.label {
    stroke: white;
    fill: white;
    font-family: Verdana;
    font-size: 25px;
    text-anchor: middle;
    cursor: move;

}

</style>
</head>
<body>

    <script src="http://marvl.infotech.monash.edu/webcola/extern/d3.v3.js"></script>
    <script src="http://marvl.infotech.monash.edu/webcola/cola.v3.min.js"></script>
<script>
    var width = 1560,
        height = 1000;
    """+data+"""
    

    var color = d3.scale.category20();
    function draw_Jbox(repr){
    
    }
    var cola = cola.d3adaptor()
        .linkDistance(function(l){return l.length;})
        .size([width, height]);
    var cont = 1;
    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)
        .on("dblclick",function(){  cont = 0;});
    cola
            .nodes(nodes)
            .links(links)
            .constraints(constraints)
        .start();

        var link = svg.selectAll(".link")
            .data(links)
              .enter().append("line")
                .attr("class", "link")
            .style("stroke",function(d){return d.colorlink;})
            .style("opacity",function(d){ return d.opacity;});
        link.append("title").text(function(d){ return d.type;});
        var pad = 3;
        var node = svg.selectAll(".node")
            .data(cola.nodes())
            .enter().append("g")
            .attr("class", "node")   
            .call(cola.drag);
            node.append("circle")   
            .attr("r", 5)
            .style("fill", function (d) { return color(2); });  

        node.append("title")
            .text(function (d) { return d.name; });

        cola.on("tick", function () {
            if (cont == 1){
            cola.start();
            }
            link.attr("x1", function (d) { return d.source.x; })
                .attr("y1", function (d) { return d.source.y; })
                .attr("x2", function (d) { return d.target.x; })
                .attr("y2", function (d) { return d.target.y; });

             node.attr("transform", function(d) { 
  	        return "translate(" + (d.x) + "," + (d.y) + ")"; });
         
            

        });

</script>
</body>
</html>"""

def js_cayley(semigroup,verbose=False,orientation="left_right"):
    from sage.misc.viewer import browser
    S = semigroup
    Gcal =  DiGraph(S.cayley_graph(idempotent=False, loop=False, orientation="left_right"))  
    Gd = DiGraph(Gcal)
    J = {}
    J_rev = {}
    Sp = set(S)
    while len(Sp)>0:
        x = Sp.pop()
        Jx = list(S.J_class_of_element(x))
        x = Jx[0]
        J[x] = Jx
        for y in J[x]:
            J_rev[y] = x
        
        Sp = Sp.difference(J[x])
        Gd.merge_vertices(J[x])
    Gd.allow_loops(False)
    neighbors = set(Gd.neighbors_out(""))
    layer = {"":0}
    i = 0   
    while len(neighbors)>0:
        newN = set()
        i = i+1
        for x in neighbors:
            layer[x] = i
            newN = newN.union(Gd.neighbors_out(x))  
        neighbors = newN        

    if verbose:
        print "done."
    
    A = S._automaton._alphabet
    file_html = sage.misc.temporary_file.tmp_filename(".",".html")
    #file_jsop = sage.misc.temporary_file.tmp_filename(".",".jsop")
    Ls = list(Gcal.vertices())
    data2 = ""
    s = "var nodes = [\n"    
    for x in Ls:
        s = s+'{"name":"'+x+'"},\n'
    s = s[0:len(s)-2]+'\n];\n var links = [\n'   
    for e in Gcal.edges():
        diff = layer[J_rev[e[1]]]-layer[J_rev[e[0]]]
        if (diff > 0):
            s = s + '{"source":'+str(Ls.index(e[0]))+',"target":'+str(Ls.index(e[1]))+',length:'+str(70*diff)+',"colorlink":"blue","opacity":0.1, "type":"'+e[2]+'"},\n'
        else:
            s = s + '{"source":'+str(Ls.index(e[0]))+',"target":'+str(Ls.index(e[1]))+',length:'+str(40)+',"colorlink":"red","opacity":0.2, "type":"'+e[2]+'"},\n'

    s = s[0:len(s)-2] +'\n];\n  var constraints = [ \n'
    s = s + '{"type":"alignment","axis":"y","offsets":[  '
    for x in layer:
       s = s + '{"node":"'+str(Ls.index(x))+'","offset":"'+str(layer[x]*90)+'"},'       
    s = s[0:len(s)-1]+ ']},\n'
      
    s = s[0:len(s)-2] + "\n ];\n"   

    f = file(file_html,'w')
    f.write(core_js_cola_cayley(s))
    f.close()
    os.system('%s %s  2>/dev/null 1>/dev/null '%(browser(),file_html))

def QJ(M):
    S = M.stable_semigroup()[1]
    for x in S:
        for y in S:
            xy = M.idempotent_power(x+y)
            if not (M(xy+x) == M(xy)):
                return (x,y)
            if not (M(y+xy) == M(xy)):
                return (x,y)
    return True 
def JstarLI(M):
    for e in M.idempotents():
        for f in M.idempotents():
            ef = set()
            fe = set()
            for x in M:
                ef.add(M(e+x+f))
                fe.add(M(f+x+e))
            for x in ef:
                for y in ef:
                    for u in fe:
                        for v in fe:
                            xu = M.idempotent_power(x+u)
                            vy = M.idempotent_power(v+y)
                            if not (M(xu+x+vy) == M(xu+y+vy)):
                                return (e,f,x,y,v,u)
    return True
   
def QJstarLI(M):
    S = M.stable_semigroup()[1]
    for e in M.idempotents():
        print e
        for f in M.idempotents():
            ef = set()
            fe = set()
            for x in S:
                ef.add(M(e+x+f))
                fe.add(M(f+x+f))
            for x in ef:
                for y in ef:
                    for u in fe:
                        for v in fe:
                            xu = M.idempotent_power(x+u)
                            vy = M.idempotent_power(v+y)
                            if not (M(xu+x+vy) == M(xu+y+vy)):
                                return (e,f,x,y,v,u)
    return True
    
def JstarLIstarMod(L):
    A = L.automaton_minimal_deterministic()
    s = M.stable_semigroup()[0]
    final = []
    d = {}
    for x in range(s):
        for y in range(s):
            if (y == (x+1) % s):
                d[(str(x),str(y))] = [str(((x+1)%s))]
            else :
                d[(str(x),str(y))] = ["p"]
        d[("p",str(x))] = ["p"]
        final.append(str(x))
    A = A.intersection(Automaton(d,[str(0)],final))
    return A
def LJ(M):
    for e in M.idempotents():
        Le = set()
        for x in M:
            Le.add(M(e+x+e))
        print Le
        for x in Le:
            for y in Le:
                xy = M.idempotent_power(x+y)
                if not (M(xy) == M(xy+x)):
                    return (e,x,y)
                if not (M(xy) == M(y+xy)):
                    return (e,x,y)

    return True
def aut_bridge(Alph):
    d = {}
    F = power_set(list(Alph))
    for a in Alph:
        d[(1,a)] = [(frozenset([a]),a)]
        d[(0,a)] = [0]
    for f in F:
        for a in Alph:
            if a in f:
                d[((f,a),a)] = [(f,a,"s")]
                for b in Alph:
                    if not (a==b):
                        d[((f,a),b)] = [(f,a)]
                    if b in f:
                        d[((f,a,"s"),b)] = [0]
                    else:
                        sf = set(f)
                        sf.add(b)
                        d[((f,a,"s"),b)] = [(frozenset(sf),a)]
    return Automaton(d,[1],[0])
def depth_DAG(G):
    Top = G.topological_sort()
    Top.reverse()
    Depth = {}
    for x in G:
        Depth[x] = 0
    while len(Top) > 0:
        x = Top.pop()
        for y in G.depth_first_search(x):
            Depth[y] = Depth[y]+1          
    val = list(set(Depth.values()))
    val.sort()
    result = {}
    for k in range(len(val)):
        result[k] = []    
    for x in G:
        result[val.index(Depth[x])].append(x)  
    return result
def depth_DAG_JSON(G):
    Top = G.topological_sort()
    Top.reverse()
    Depth = {}
    for x in G:
        Depth[x] = 0
    while len(Top) > 0:
        x = Top.pop()
        for y in G.depth_first_search(x):
            Depth[y] = Depth[y]+1          
    val = list(set(Depth.values()))
    val.sort()
    result = {}
    for k in range(len(val)):
        result[str(k)] = []    
    for x in G:
        result[str(val.index(Depth[x]))].append(x)  
    result.replace("'",'"')
    return result

def J_class_graph_JSON(S,representant):
    Gcal =  DiGraph(S.cayley_graph(idempotent=False, loop=False, orientation="left_right"))  
    J = {}
    if verbose:
        count = 0
    for x in representant:
        J[x] = list(S.J_class_of_element(x))
        Jx = set(J[x])
        Jx.remove(x)    
        Lx = [x]
        Lx.extend(Jx)            
        Gcal.merge_vertices(Lx)
    
    return depth_DAG_JSON(G)
def sg_reverse(S,u,v):
    G = S.cayley_graph(orientation="left_right",idempotent=False)
    su = S(u)
    sv = S(v)
    l = G.shortest_path(u,v)
    if len(l) == 0:
        raise TypeError("no inverse")
    l.reverse()
    x = l.pop()
    w1 = ""
    w2 = ""
    while len(l)>0:
        y = l.pop()
        a = G.edge_label(x,y)
        a = a.split(",")[0]        
        if a[0] == ".":
            w1 = w1 + a[1]
        else:
            w2 = a[0] + w2 
   
        x = y
    return (w2,w1)                
    
def new_box(S,x):
    if (x not in S):
        raise TypeError("unboxable element")
    else:
        shiftR = [""]
        shiftL = [""]
        box = {}       
        Jx = S.J_class_of_element(x)
        Lx = S.L_class_of_element(x)
        Rx = S.R_class_of_element(x)
        Idempotents = Jx.intersection(S.idempotents())
        cx = 0
        cy = 0
        if len(Idempotents) > 0:        
            x = Idempotents.pop()
            Lx = S.L_class_of_element(x)
            Rx = S.R_class_of_element(x)
            Idempotents = Idempotents.difference(S.R_class_of_element(x))
            Idempotents = Idempotents.difference(S.L_class_of_element(x))
            while len(Idempotents) > 0:
                y = Idempotents.pop()
                cx = cx + 1
                cy = cy + 1
                Idempotents = Idempotents.difference(S.R_class_of_element(y))
                Idempotents = Idempotents.difference(S.L_class_of_element(y))
                z = sg_reverse(S,x,y)
                Lx = Lx.difference(S.H_class_of_element(S(z[0]+x)))
                Rx = Rx.difference(S.H_class_of_element(S(x+z[1])))                
                shiftR.append(z[1])
                shiftL.append(z[0])
        while len(Lx) > 0:
            l = Lx.pop()
            cy = cy + 1
            Hl = S.H_class_of_element(l)
            Lx = Lx.difference(Hl)
            shiftL.append(sg_reverse(S,x,l)[0])
        while len(Rx) > 0:
            r = Rx.pop()
            cx = cx + 1
            Hr = S.H_class_of_element(r)
            Rx = Rx.difference(Hr)
            shiftR.append(sg_reverse(S,x,r)[1])
    for i in range(0,cx):
        for j in range(0,cy):
            sr = shiftR[i]
            sl = shiftL[j]
            y = S(sl+x+sr)
            box[(i,j)] = (y,S.H_class_of_element(y))
    box["width"] = cx
    box["height"] = cy
    return box

def newbox_oldbox(S,x,idempotent=True):
    nbox = new_box(S,x)
    obox = []
    for x in nbox["width"]:
        L = []
        for y in nbox["height"]:
            H = list(nbox[(i,j)][1])
            if idempotent:
                I = H.intersection(S.idempotents())
                for i in I:
                    H.remove(i)
                    H.add(i+"*")
            L.append(H)
        obox.append(L)
    return obox               
                
def box_representation(S):
    E = set(S.elements())
    dic = {}
    box = {}
    if verbose:
        print "computing Jclass ..."
    while len(E)>0:
        x = S.pop_J_maximal(E)
        Jclass = S.J_class_of_element(x)            
        box[x] = []
        E = E.difference(Jclass)
    for x in box:
        box[x] = new_box(S,x)
    return box

def is_extractable(l):
    n = len(l)
    for k in range(n/2):
        for x in range(n-2*k):
            if ((l[x]<l[k+x]) and (l[k+x] < l[2*k+x])):
                return True
            if ((l[x]>l[k+x]) and (l[k+x] > l[2*k+x])):
                return True
    return False                
def next_one(l):
    sort_l = list(l)
    sort_l.append(0)
    sort_l.append(1)
    sort_l.sort()
    for x in range(len(sort_l)-1):
        new_l = list(l)
        new_l.append((sort_l[x]+sort_l[x+1])/2)
        if not(is_extractable(new_l)):
            return new_l
    return False                    
def random_next_one(l):
    sort_l = list(l)
    sort_l.append(0)
    sort_l.append(1)
    sort_l.sort()
    E = set(range(len(sort_l)-1))
    while len(E) > 0:
        x = sample(E,1)[0]
        E.remove(x)
        new_l = list(l)
        new_l.append((sort_l[x]+sort_l[x+1])/2)
        if not(is_extractable(new_l)):
            return new_l
    return False          

def fly_time_random(start=[1/2]):
    k = start
    count = 0
    while not (k==False):
        k = random_next_one(k)
        count = count + 1
    return count                 
     
def extraction(N,lazy=False,starting=[1/2],verbose=0):
    if N == 1:
        return [starting]
    L = extraction(N-1,lazy=False,starting=starting,verbose=verbose-1) 
    if verbose > 0:
        print "starting "+str(N)
        
    new_L = []
    for l in L:
        sort_l = list(l)
        sort_l.append(0)
        sort_l.append(1)
        sort_l.sort()
        for x in range(len(sort_l)-1):
            new_l = list(l)
            new_l.append((sort_l[x]+sort_l[x+1])/2)
            if not (new_l in new_L):
                if not(is_extractable(new_l)):
                    if lazy:
                        return new_l
                    else:    
                        new_L.append(new_l)
    return new_L                
    
def random_extraction(N,verbose=True):
    if N == 1:
        return [1/2]
    find_one = False
    count = 0
    while not(find_one):
        if verbose:
            count = count + 1
            print count                
        l = random_extraction(N-1,verbose=False)
        sort_l = list(l)
        sort_l.append(0)
        sort_l.append(1)
        sort_l.sort()
        x = sample(range(len(sort_l)-1),1)[0]
        new_l = list(l)
        new_l.append((sort_l[x]+sort_l[x+1])/2)
        if not(is_extractable(new_l)):
            find_one = True

    return new_l

def H_class_to_group(S,x):
    H = S.H_class_of_element(x)
    if (len(H.intersection(S.idempotents())) > 0 ): 
        H = list(H)
        s = "GroupByMultiplicationTable([ "
        for i in range(len(H)):
            s = s + "["
            for j in range(len(H)):
                s = s + str(1+H.index(S(H[i]+H[j]))) + ", "    
            s = s[0:len(s)-2] + "], "
        s = s[0:len(s)-2] + " ]);"
        gap.set("g",s)
        return gap.StructureDescription("g")
    else:
        return False                
def shortlex(u,v):
    if len(u)<len(v):
        return True
    if len(u) > len(v):
        return False
    return u<v      
def execute_aut(d,u):
    state = ""
    for i in range(len(u)):
        if (state,u[i]) in d:
            state = d[(state,u[i])][0]
        else:
            return u   
    return state
    
def reduce_word(u,R,d,maxlen=None):
    result = set([u])
    for e in R:           
        p = re.compile(e[0])
        for m in p.finditer(u):
            v = u[0:m.start()]+e[1]+u[m.end():len(u)]
            result.add(execute_aut(d,v))  
    if (maxlen > 0):
        v = pop_shortlex(set(result))
        if (len(v) > maxlen):
            u = pop_shortlex_max(set(flatten(list(d))))
            result.add(u)  
    return result                
def pop_shortlex(E):
    if len(E) > 0:
        v = list(E)[0]
        for u in E:
            if shortlex(u,v):
                v = u
        E.remove(v)
        return v

def pop_shortlex_max(E):
    if len(E) > 0:
        v = list(E)[0]
        for u in E:
            if shortlex(v,u):
                v = u
        E.remove(v)
        return v
             
def merge_states(d,E):
    v = pop_shortlex(E)
    newd = {}
    for t in d:
        if not t[0] in E:
            if len(E.intersection(d[t])) > 0:
                S = set(d[t]).difference(E)
                S.add(v)
                newd[t] = list(S)
            else:
                newd[t] = d[t]
    return newd                                
def simplify_automaton(d):
    for t in d:
        if len(d[t]) > 1:
            dp = merge_states(d,set(d[t]))
            dp = simplify_automaton(dp)
            return dp
    return d                                                       
def simplify_automaton_final(d,R):
    states = set(flatten(list(d)))
    dp = d
    for u in states:
        for e in R:
            v0 = execute_aut(d,u+e[0])
            v1 = execute_aut(d,u+e[1])
            if not (v0 == v1):
                dp = merge_states(dp,set([v0,v1]))    
                return simplify_automaton_final(dp,R)                   
    return d                                                       
                
def semigroup_by_presentation(E,maxlen=None,verbose=False):
    R = []
    alphabet = set()
    for e in E:
        alphabet = alphabet.union(set(e[0]))
        alphabet = alphabet.union(set(e[1]))
        if not (shortlex(e[0],e[1])):
            R.append(e)
        else:
            R.append((e[1],e[0]))
    alphabet = list(alphabet)
    alphabet.sort()        
    d = {}
    current = set([""])
  
    while len(current) > 0:      
        u = pop_shortlex(current)
        if verbose:
            print len(current)
            print u

        if (execute_aut(d,u) == u):
            for a in alphabet:
                v = u+a
                red = reduce_word(v,R,d,maxlen=maxlen)
                if verbose:
                    print v
                    print red

                if len(red) == 1 :
                    current.add(v)    
                d[(u,a)] = list(red)
        d = simplify_automaton(d)
    d = simplify_automaton_final(d,R)           
    return TransitionSemiGroup(Automaton(d,[],[]))                    
                                   
def Aut2reg(d,alphabet,i,f,states_list):
    A = alphabet
    states = list(states_list)
    d_reg = {}
    if i in states:
        states.remove(i)
    if f in states:
        states.remove(f)
    for t in d:
        for x in d[t]:
            if (t[0],x) in d_reg:
                d_reg[(t[0],x)] =  d_reg[(t[0],x)] + RegularLanguage(t[1],letters=A) 
            else:
                d_reg[(t[0],x)] =  RegularLanguage(t[1],letters=A)
                   
    while len(states) > 0:
        s = states.pop()
        d_reg_buff = dict(d_reg)
        to_remove = set() 
        for t1 in d_reg_buff:
            for t2 in d_reg_buff:
                if (t1[1] == s) and (t2[0] == s):
                    to_remove.add(t1)
                    to_remove.add(t2)
                    if not (s,s) in d_reg: 
                        if (t1[0],t2[1]) in d_reg:
                            d_reg[(t1[0],t2[1])] =  d_reg[(t1[0],t2[1])] +  d_reg[t1]*d_reg[t2]
                        else:
                            d_reg[(t1[0],t2[1])] =   d_reg[t1]*d_reg[t2]
                    if  (s,s) in d_reg: 
                        if (t1[0],t2[1]) in d_reg:
                            d_reg[(t1[0],t2[1])] =  d_reg[(t1[0],t2[1])] +  d_reg[t1]*(d_reg[(s,s)].kleene_star())*d_reg[t2]
                        else:
                            d_reg[(t1[0],t2[1])] = d_reg[t1]*(d_reg[(s,s)].kleene_star())*d_reg[t2]
        [d_reg.pop(t) for t in to_remove]
    
    if not (i,f) in d_reg:
        raise TypeError("Empty language")
    if (i == f):
        return d_reg[(i,i)].kleene_star()
    if (f,f) in d_reg:
        d_reg[(i,f)] = d_reg[(i,f)]*(d_reg[(f,f)].kleene_star())    
    if (i,i) in d_reg:
        d_reg[(i,f)] = (d_reg[(i,i)].kleene_star())*d_reg[(i,f)]    
    
    if ((f,i) in d_reg):
        return (d_reg[(i,f)]*d_reg[(f,i)]).kleene_star()*d_reg[(i,f)]
    else:
        return d_reg[(i,f)]     

def random_certification(state_size,nb,alphabet=["a","b"]):
    count = 0
    while count < nb:
        count = count +1
        print count
        A = random_automaton(state_size,alphabet).minimal_automaton()        
        while not (len(A._states) > 2):
            A = random_automaton(state_size,alphabet).minimal_automaton()
        print "automaton found"            
        try :
            L = Aut2reg(A._transitions,alphabet,A._initial_states[0],A._final_states[0],list(A._states))
        except:
            print "error"
            return A    
        print "regexp computed size:"+str(len(str(L)))
        B = L.automaton_minimal_deterministic()
        print "automaton computed"
        if ((A-B)+(B-A)).is_finite_state_reachable():
            return A
        print "certification satisfied, next"    
    return True             

def find_regexp_random(aut,nb_iter=10):
    result = None
    for i in aut._initial_states:
        for f in aut._final_states:
            buff = None
            try:
                for k in range(nb_iter):
                    L = Aut2reg(aut._transitions,aut._alphabet,i,f,Permutations(list(aut._states)).random_element())                    
                    if not (buff):
                        buff = L
                    if (buff) and (len(str(L)) < len(str(buff))):
                        buff = L
            except:
                print "error in Aut2reg"
                buff = None            
            if result:
                result = result + buff
            else:
                result = buff
    return result               
   
def is_JstarLI(S):
    for e in S.idempotents():
        for f in S.idempotents():
            eSf = set()
            fSe = set()
            for x in S:
                eSf.add(S(e+x+f))
                fSe.add(S(f+x+e))                            
        for x in eSf:
            for y in eSf:
                for s in fSe:
                    for t in fSe:
                        id1 = S.idempotent_power(x+s)
                        id2 = S.idempotent_power(y+t)
                        if not( S(id1+id2) == S(id1+x+t+id2)):
                            return False                        
    return True
        
def is_QJstarLI(L):
    S = L.syntactic_monoid()
    St = S.stable_semigroup()[1]
    for e in S.idempotents():
        for f in S.idempotents():
            eSf = set()
            fSe = set()
            for x in St:
                eSf.add(S(e+x+f))
                fSe.add(S(f+x+e))                            
        for x in eSf:
            for y in eSf:
                for s in fSe:
                    for t in fSe:
                        id1 = S.idempotent_power(x+s)
                        id2 = S.idempotent_power(y+t)
                        if not( S(id1+id2) == S(id1+x+t+id2)):
                            return False                        
    return True
import string    
def enriched_aut(aut,d):
    A = aut._alphabet
    newl = set(string.ascii_lowercase)
    if len(A)*d > len(newl):
        raise TypeError("Enrichment too big")
    label = {}
    for a in A:
        for i in range(d):
            label[(a,i)] = newl.pop()
    wf = {}
    for i in range(d):
        for a in A:
            wf[(i,label[(a,i)])] = [(i+1)%d]
    wf_aut = Automaton(wf,[0],range(d))    
    transitions_enr = {}
    for t in aut._transitions:
        for i in range(d):
            transitions_enr[(t[0],label[(t[1],i)])] = aut._transitions[t]     
    enr_aut = Automaton(transitions_enr,aut._initial_states, aut._final_states)
    return enr_aut.intersection(wf_aut).minimal_automaton()                      
def is_JstarLIstarMOD(L):
    alphabet = set(string.ascii_lowercase)
    S = L.syntactic_monoid()
    x = S.stable_semigroup()
    St = x[1]   
    d = x[0]
    S = TransitionSemiGroup(enriched_aut(L.automaton_minimal_deterministic(),d),monoid=False)
                    
    return is_JstarLI(S)    

def is_QJ(L):
    S = L.syntactic_monoid()
    St = S.stable_semigroup()[1]
    for x in St:
        for y in St:
            xyw = S.idempotent_power(x+y)
            if not (S(xyw+x) == S(xyw)):
                return (x,y)
            if not (S(y+xyw) == S(xyw)):
                return (x,y)
    return True                

def reverse(A):
    d = A._transitions
    d_rev = {}
    for t in d:
        a = (d[t][0],t[1])
        if a not in d_rev:
            d_rev[a] = [t[0]]
        else:
            d_rev[a].append(t[0])
    return Automaton(d_rev,list(A._final_states),list(A._initial_states)).minimal_automaton()
                             
                    
def test_cfc_conj(size=10,alphabet=['a','b','c']):
    A = random_automaton(size,alphabet=alphabet)
    A = A.minimal_automaton()
    print "first minimization"
    B = reverse(A)
    print "second minimization"
    CFCA = len(A.to_graph().strongly_connected_components())
    print "first cfc"
    CFCB = len(B.to_graph().strongly_connected_components())
    print "second cfc"
    nA = len(A._states)

    nB = len(B._states)
    if max(CFCA,CFCB)> min(nA,nB):
        return A
    else:
        print "one more "+str( max(CFCA,CFCB))+" < "+str(min(nA,nB))+" worst state: "+str(max(nA,nB)) 
        test_cfc_conj(size=size,alphabet=alphabet)
        
def random_DAG_automaton(Dagsize=10,Cfcsize=10,alphabet=["a","b","c"]):
    DAG = random_DAG(Dagsize)
    Aut_list = [random_automaton(Cfcsize,alphabet=alphabet)]
        
    
def size_max_L_chain(S):
    G = S.cayley_graph(orientation="left")
    H = G.strongly_connected_components_digraph()
    L = H.topological_sort()
    root = L[0] 
    c = 0
    distance = {}
    distance[root] = 0
    To_deal = set([root])
    while len(To_deal) > 0:
        Dealt = set(To_deal)
        To_deal = set()
        c = c + 1
        for x in Dealt:
            To_deal = To_deal.union(H.neighbors_out(x))
        for x in To_deal:
            distance[x] = c
    return max(distance.values())                                    	    

@parallel
def size_max_R_chain(S, verbose=False):
    G = S.cayley_graph(orientation="right")
    H = G.strongly_connected_components_digraph()
    L = H.topological_sort()
    root = L[0] 
    c = 0
    distance = {}
    distance[root] = 0
    To_deal = set([root])
    distance = {}
    while len(To_deal) > 0:
        Dealt = set(To_deal)
        To_deal = set()
        c = c + 1
        for x in Dealt:
            To_deal = To_deal.union(H.neighbors_out(x))
        for x in To_deal:
            distance[x] = c
    if verbose:
        print "Done"        
    return max(distance.values())                                    	    

def full_transformation(size):
    d = {}
    a = "a"
    b = "b"
    c = "c"
    for i in range(size):
        d[(i,a)] = [(i+1)%size]
        d[(i,b)] = [i]
        d[(i,c)] = [i]
    d[(1,b)] = [0]
    d[(1,c)] = [0]
    d[(0,b)] = [1]
    return TransitionSemiGroup(Automaton(d,[0],[0]))

def to_delete(n):
    a = []
    E = S.elements()
    for i in range(n):
        x = sample(E,1)[0]
        Jx = S.J_class_of_element(x)
        a.append(len(S.sub_semigroup_generated(sample(Jx,3))))
        print "i:"+str(i)+" nb:"+str(a[i])
    return a    

def group_of_J_class_of_element(S,x):
    J = set(S.J_class_of_element(x))
    E = J.intersection(S.idempotents())
    if (len(E) > 0):
        e = E.pop()
        H = S.H_class_of_element(e)
        A = [(h,) for h in H]
        d = {}
        for h in H:
            for a in A:
                d[(h,a)] = [S(h+a[0])]
        return TransitionSemiGroup(Automaton(d,[e],[e]))             
    else:
        raise ValueError("J class should be regular")
        
def random_one_letter_aut(size):
    G = random_digraph(size)
    d = {}
    E = G.edges()
    c = 0
    for e in G.edges():
        c = c + 1
        for x in G.vertices():            
            d[(x,c)] = [size+1]
        d[(size+1,c)] = [size+1]
        d[(e[0],c)] = [e[1]]
    return Automaton(d,[0],G.vertices()) 
    


