/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import java.util.ArrayList;
import java.util.Iterator;
import java.io.*;

class Pair<A, B extends Comparable<B>> implements Comparable<Pair<A,B>>
{
    public A e1;
    public B e2;
    public Pair(A e1, B e2)
    {
        this.e1 = e1;
        this.e2 = e2;
    }

    public int compareTo(Pair<A,B> o) {

        return e2.compareTo(o.e2);
    }

    public boolean equals(Pair<A,B> o)
    {
        return e1.equals(o.e1) && e2.equals(o.e2);
    }

}

class Node implements Serializable{
    private String name;
    private ArrayList<Node> parents;
    private ArrayList<Node> children;
    private Boolean learned;

    public Node(String name) {
        this.name = name;
        this.parents = new ArrayList<>();
        this.children = new ArrayList<>();
        learned = false;
    }

    public void addParent(Node e) {
        if (e == null) return;
        if (!parents.contains(e))
        {
            parents.add(e);
            e.addChild(this);
        }

    }

    public void addParent(Node[] e) {
        for (Node n : e)
        {
            addParent(n);
        }
    }

    public void addChild(Node e) {
        if (e == null) return;
        if (!children.contains(e))
        {
            children.add(e);
            e.addParent(this);
        }

    }

    public void addChild(Node[] e) {
        for (Node n : e)
        {
            addChild(n);
        }
    }

    public void removeParent(Node e) {
        parents.remove(e);
    }

    public void removeChild(Node e) {
        children.remove(e);
    }

    public Integer parentCount()
    {
        return parents.size();
    }

    public Integer childCount()
    {
        return children.size();
    }

    public double complexity()
    {
        return parents.size() - children.size();
    }

    public Iterator<Node> parentsIterator() {
        return new Iterator<Node>() {
            int index = 0;

            @Override
            public boolean hasNext() {
                return (index < parents.size());
            }

            @Override
            public Node next() {
                return parents.get(index++);
            }
        };
    }

    public Iterator<Node> childrenIterator() {
        return new Iterator<Node>() {
            int index = 0;

            @Override
            public boolean hasNext() {
                return (index < children.size());
            }

            @Override
            public Node next() {
                return children.get(index++);
            }
        };
    }

    public  Boolean isEndNode()
    {
        if (parents == null) return true;
        for (Node d: parents)
        {
            if (!d.learned) return false;
        }
        return true;
    }


    @Override
    public String toString()
    {
        return name;
    }
}

class UnionFind {
    int[] ids;
    int[] sz;

    public UnionFind(int n) {
        if (n < 1) {
            throw new IllegalArgumentException();
        } else {
            this.ids = new int[n];
            this.sz = new int[n];

            for(int i = 0; i < n; ++i) {
                this.ids[i] = i;
                this.sz[i] = 1;
            }

        }
    }

    public void union(int p, int q) {
        if (!this.connected(p, q)) {
            if (this.sz[q] > this.sz[p]) {
                int temp = p;
                p = q;
                q = temp;
            }

            this.ids[this.root(q)] = this.root(p);
            int[] var10000 = this.sz;
            var10000[p] += this.sz[q];
        }
    }

    public Integer root(int p) {
        while(p != this.ids[p]) {
            this.ids[p] = this.ids[this.ids[p]];
            p = this.ids[p];
        }

        return p;
    }

    public Boolean connected(int p, int q) {
        int root_p = this.root(p);
        int root_q = this.root(q);
        return root_p == root_q;
    }

    public Boolean allConnected()
    {
        for (int i = 1; i < ids.length; i++)
        {
            if (!connected(0, i)) return false;
        }
        return true;
    }

    public void clear()
    {
        for(int i = 0; i < ids.length; ++i) {
            ids[i] = i;
            sz[i] = 1;
        }
    }
}

class Stack<Base>
{
    private class StackNode<Base>
    {
        Base value;
        StackNode<Base> next;

        public StackNode(Base val, StackNode<Base> next)
        {
            this.value = val;
            this.next = next;
        }
    }

    private StackNode<Base> head;

    public Stack()
    {
        head = null;
    }

    public void push (Base val)
    {
        head = new StackNode<>(val, head);
    }

    public Base pop()
    {
        if (head == null) return null;
        Base ret = head.value;
        head = head.next;
        return ret;
    }

    public Base peek()
    {
        if (head == null) return null;
        return head.value;
    }

    public boolean contains (Base val)
    {
        StackNode<Base> iterator = head;
        while (iterator != null)
        {
            if (iterator.value == val) return true;
            iterator = iterator.next;
        }
        return false;
    }
}
