class node: #Node class defined
    def __init__(self,element):
        self.element=element
        self.parent=None
        self.lchild=None
        self.rchild=None
        self.y_info=None
def merge_y(l1,l2): #This function merges two lists sorted on their y coordinates, into a new sorted list 
    x1=len(l1)
    x2=len(l2)
    i,j=0,0
    L=[]
    while i<x1 and j<x2:
        if l1[i][1]<=l2[j][1]:
            L.append(l1[i])
            i+=1
        else:
            L.append(l2[j])
            j+=1
    while i<x1:
        L.append(l1[i])
        i+=1
    while j<x2:
        L.append(l2[j])
        j+=1
    return L
def segmenttree(pointlist,low,high): 
    #Pre condition: pointlist is sorted on x
    #This function creates a segment tree with ranges of indices as elements of each node, these ranges split into 2 equal halves at every node until we reach singleton elements
    if len(pointlist)==0:
        return None
    else:
        if low<high:
            w=(low+high-1)//2
            v=node((low,high))
            v.lchild=segmenttree(pointlist,low,w)
            v.rchild=segmenttree(pointlist,w+1,high)
            return v
        if low==high:
            v=node(low)
            return v
        if low>high:
            return None
def orderofy(pointlist,Segmenttree): #This function creates a list of elements of pointlist in the range that is stored in the element of that node,
    #List is sorted on y
    if len(pointlist)==0:
        return []
    if type(Segmenttree.element)==int:
        Segmenttree.y_info=pointlist[Segmenttree.element] #Segmenttree.y_info stores this list sorted on y 
        return [pointlist[Segmenttree.element]]
    elif (type(Segmenttree.lchild.element)==int and type(Segmenttree.rchild.element)==int):
        a=Segmenttree.lchild.element
        b=Segmenttree.rchild.element
        if pointlist[a][1]<pointlist[b][1]:
            Segmenttree.y_info=[pointlist[a],pointlist[b]]
            return([pointlist[a],pointlist[b]])
        else:
            Segmenttree.y_info=[pointlist[b],pointlist[a]]
            return([pointlist[b],pointlist[a]])
    else:
        a=orderofy(pointlist,Segmenttree.lchild)
        b=orderofy(pointlist,Segmenttree.rchild)
        Segmenttree.y_info=merge_y(a,b)
        return(merge_y(a,b))
def checkinrange(point,range):  #This function checks if a point is present in a range
    (a,b)=point
    (a1,b1),(a2,b2)=range
    if (a>=a1 and a<=a2 and b>=b1 and b<=b2):
        return True
    else:
        False
class PointDatabase:
    def __init__(self,pointlist):  #This method initialises a data structure which stores the elements of pointlist 
        #Creation time O(nlogn) Reccurence=> T(n)=2T(n/2)+O(n)
        pointlist.sort()
        self.pointlist=pointlist
        x=segmenttree(pointlist,0,len(pointlist)-1)
        orderofy(pointlist,x)
        self.a=x
    def searchNearby(self,q,d): #Given a q,d we will first find the nodes that lie in l(inf) distance d from q based on x coordinates which will take O(log(n)) time and is computed in function searchxinTree
        #Now for these chosen nodes the binary search function checks that y lies in the range as well in O(log(n)) time 
        #maximum m append operations, where m is no. of elements in the desired range
        #So total runtime of function is O(log^2(n)+m)
        low_bound=(q[0]-d,q[1]-d)
        high_bound=(q[0]+d,q[1]+d)
        range=(low_bound,high_bound)
        l8=[]
        if len(self.pointlist)==0:
            return []
        def binarysearch(sorted_list,range,small,large):
            (a,low)=range[0]
            (b,high)=range[1]
            if small<large:
                n=(small+large-1)//2
                if sorted_list[n][1]>high:
                    binarysearch(sorted_list,range,small,n)
                elif sorted_list[n][1]<low:
                    binarysearch(sorted_list,range,n+1,large)
                else:
                    if checkinrange(sorted_list[n],range)==True:
                        l8.append(sorted_list[n])
                    binarysearch(sorted_list,range,small,n-1)
                    binarysearch(sorted_list,range,n+1,large)
            elif small==large:
                if checkinrange(sorted_list[small],range)==True:
                    l8.append(sorted_list[small])
            elif small>large:
                return []
        def searchxinTree(pointer):
            if pointer==None:
                return False
            elif type(pointer.element)==int:
                x=pointer.element
                if checkinrange(self.pointlist[x],range)==True:
                    l8.append(self.pointlist[x])
            else:
                (a,b)=(self.pointlist[pointer.element[0]][0],self.pointlist[pointer.element[1]][0])
                if a>=low_bound[0] and b<=high_bound[0]:
                    binarysearch(pointer.y_info,range,0,len(pointer.y_info)-1)
                elif a<=low_bound[0] and low_bound[0]<=b:
                    if a<=high_bound[0] and high_bound[0]<=b:
                        searchxinTree(pointer.lchild)
                        searchxinTree(pointer.rchild)
                    else:
                        if low_bound[0]>(a+b-1)//2:
                            searchxinTree(pointer.rchild) 
                        else:
                            searchxinTree(pointer.lchild)
                            searchxinTree(pointer.rchild)
                elif a<=high_bound[0]<=b:
                    if high_bound[0]<((a+b-1)//2)+1:
                        searchxinTree(pointer.lchild) 
                    else:
                        searchxinTree(pointer.lchild)
                        searchxinTree(pointer.rchild)     
                else:
                    return False    
        searchxinTree(self.a)
        return l8
