/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import java.util.ArrayList;
import java.util.Iterator;

class Pair<A, B extends Comparable<B>>
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

}

class Node {
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
        if (!parents.contains(e)) parents.add(e);
    }

    public void removeParent(Node e) {
        parents.remove(e);
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
