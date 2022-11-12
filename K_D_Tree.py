class node:
    def __init__(self,element):
        self.element=element
        self.parent=None
        self.lchild=None
        self.rchild=None
        self.newtree=None
def K_DTree(pointlist,var):
    if len(pointlist)==0:
        return None
    if len(pointlist)==1:
        return (node(pointlist[0]))
    else:
        n=len(pointlist)
        def merge_y(l1,l2):
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
        def sort_y(l,low,high):
            if low<high:
                m=(low+high-1)//2
                x=sort_y(l,low,m)
                y=sort_y(l,m+1,high)
                return(merge_y(x,y))
            elif low==high:
                return[l[low]]
            else:
                return []
        if var==1:
            pointlist.sort()
            sl=pointlist[0:(n//2)]
            sr=pointlist[(n//2)+1:n]
            v=node(pointlist[n//2])
        else:
            l=sort_y(pointlist,0,n-1)
            sl=l[0:(n//2)]
            sr=l[(n//2)+1:]
            v=node(l[n//2])
        vl=K_DTree(sl,not(var))
        vr=K_DTree(sr,not(var))
        v.lchild=vl
        v.rchild=vr
        #f vl!=None and vr!=None:
            #print(v.element,vl.element,vr.element)
        return v
def checkinrange(point,range):
    (a,b)=point
    (a1,b1),(a2,b2)=range
    if (a>=a1 and a<=a2 and b>=b1 and b<=b2):
        return True
    else:
        False
class PointDatabase:
    def __init__(self,pointlist):
        self.a=(K_DTree(pointlist,1))
    def searchNearby(self,q,d):
        low=(q[0]-d,q[1]-d)
        high=(q[0]+d,q[1]+d)
        range=(low,high)
        final_list=[]
        def what_to_check(variable):
            if variable==True:
                return 0
            else:
                return 1
        def searchinTree(pointer,variable):
            if pointer==None:
                return False
            if (pointer.element[what_to_check(variable)]>high[what_to_check(variable)]):
                searchinTree(pointer.lchild,not(variable))
            elif (pointer.element[what_to_check(variable)]<low[what_to_check(variable)]):
                searchinTree(pointer.rchild,not(variable))
            else:
                if checkinrange(pointer.element,range):
                    final_list.append(pointer.element)
                searchinTree(pointer.lchild,not(variable))
                searchinTree(pointer.rchild,not(variable))
        searchinTree(self.a,True)
        return(final_list)
